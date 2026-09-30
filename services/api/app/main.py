import os
import time as clock
from collections import defaultdict, deque
from datetime import date, datetime, time
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import (
    Appointment,
    AuditEvent,
    AvailabilitySlot,
    ChatFeedback,
    Consent,
    ConversationMessage,
    HelpContact,
    JournalAttachment,
    JournalEntry,
    KnowledgeItem,
    KnowledgeVersion,
    MoodCheckin,
    NotificationPreference,
    PolicyEvent,
    PolicyVersion,
    Professional,
    SafetyEvent,
    SelfcareItem,
    SelfcareUse,
    User,
)
from .providers import provider_snapshot
from .safety import run_pipeline
from .security import create_token, current_user, require_roles, verify_password

app = FastAPI(title="TerapIA API", version="3.0.0", docs_url="/docs")
origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:8088,http://127.0.0.1:8088",
).split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["*"], allow_headers=["Authorization", "Content-Type"])
Base.metadata.create_all(engine)
request_windows: dict[str, deque] = defaultdict(deque)


class ConsentIn(BaseModel):
    version: str = Field(min_length=1, max_length=40)
    accepted: bool


class MoodIn(BaseModel):
    mood: int = Field(ge=1, le=5)
    context: str | None = Field(default=None, max_length=120)


class JournalIn(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    content: str = Field(min_length=1, max_length=10000)
    tags: list[str] = Field(default_factory=list, max_length=8)


class ChatIn(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class AppointmentIn(BaseModel):
    slot_id: int


class NotificationIn(BaseModel):
    enabled: bool
    discreet: bool = True


class SelfcareUseIn(BaseModel):
    feedback: str | None = Field(default=None, pattern="^(ajudou|neutro|não_ajudou)$")


class ChatFeedbackIn(BaseModel):
    useful: bool


class KnowledgeIn(BaseModel):
    slug: str = Field(pattern=r"^[a-z0-9-]+$")
    title: str = Field(min_length=2, max_length=160)
    content: str = Field(min_length=10)
    source: str = Field(min_length=2, max_length=255)
    reviewed_by: str | None = None
    category: str = Field(default="psicoeducação", min_length=2, max_length=80)
    tags: list[str] = Field(default_factory=list, max_length=12)


class KnowledgeStatus(BaseModel):
    status: str = Field(pattern="^(draft|review|published|unpublished)$")


class PolicyIn(BaseModel):
    code: str = Field(pattern=r"^[A-Z0-9-]+$")
    content: str = Field(min_length=10)
    reviewed_by: str | None = None


def serialize(row):
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}


def audit(db: Session, actor_id: int | None, action: str, entity: str, entity_id=None):
    db.add(AuditEvent(actor_id=actor_id, action=action, entity=entity, entity_id=str(entity_id) if entity_id is not None else None))


@app.middleware("http")
async def security_headers(request: Request, call_next):
    if request.url.path in {"/auth/login", "/chat/messages"}:
        key = f"{request.client.host if request.client else 'unknown'}:{request.url.path}"
        now = clock.monotonic()
        window = request_windows[key]
        while window and now - window[0] > 60:
            window.popleft()
        if len(window) >= 120:
            raise HTTPException(429, "Muitas solicitações. Aguarde um momento e tente novamente.")
        window.append(now)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
    return response


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(select(1))
    configured = os.getenv("AI_PROVIDER", "mock").lower()
    provider = "ollama" if configured == "ollama" else "openai-style" if configured in {"openai", "openai-style", "external"} else "mock-offline"
    return {"status": "ok", "provider": provider}


@app.get("/ai/status")
def ai_status(user: User = Depends(current_user), db: Session = Depends(get_db)):
    snapshot = provider_snapshot()
    snapshot.update(
        rag_active=True,
        safety_active=True,
        knowledge_base={"published_versions": db.scalar(select(func.count(KnowledgeVersion.id)).where(KnowledgeVersion.status == "published"))},
        last_checked=datetime.utcnow(),
    )
    return snapshot


@app.post("/auth/login")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == form.username.lower()))
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(401, "Credenciais inválidas")
    audit(db, user.id, "AUTH_LOGIN", "user", user.id)
    db.commit()
    return {"access_token": create_token(user), "token_type": "bearer", "role": user.role}


@app.post("/auth/refresh")
def refresh(user: User = Depends(current_user)):
    return {"access_token": create_token(user), "token_type": "bearer"}


@app.get("/me")
def me(user: User = Depends(current_user)):
    return {"id": user.id, "email": user.email, "name": user.name, "role": user.role}


@app.get("/consents")
def consents(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return [serialize(x) for x in db.scalars(select(Consent).where(Consent.user_id == user.id).order_by(Consent.accepted_at.desc())).all()]


@app.post("/consents", status_code=201)
def create_consent(data: ConsentIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    row = Consent(user_id=user.id, **data.model_dump())
    db.add(row); audit(db, user.id, "CONSENT_RECORDED", "consent", data.version); db.commit(); db.refresh(row)
    return serialize(row)


@app.get("/mood-checkins")
def list_moods(
    from_date: date | None = None,
    to_date: date | None = None,
    user: User = Depends(require_roles("young_user")),
    db: Session = Depends(get_db),
):
    query = select(MoodCheckin).where(MoodCheckin.user_id == user.id)
    if from_date:
        query = query.where(MoodCheckin.created_at >= datetime.combine(from_date, time.min))
    if to_date:
        query = query.where(MoodCheckin.created_at <= datetime.combine(to_date, time.max))
    return [serialize(x) for x in db.scalars(query.order_by(MoodCheckin.created_at.desc())).all()]


@app.post("/mood-checkins", status_code=201)
def create_mood(data: MoodIn, user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    row = MoodCheckin(user_id=user.id, **data.model_dump()); db.add(row); audit(db, user.id, "MOOD_CREATED", "mood_checkin"); db.commit(); db.refresh(row)
    return serialize(row)


@app.delete("/mood-checkins/{checkin_id}", status_code=204)
def delete_mood(checkin_id: int, user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    row = db.scalar(select(MoodCheckin).where(MoodCheckin.id == checkin_id, MoodCheckin.user_id == user.id))
    if not row:
        raise HTTPException(404, "Check-in não encontrado")
    audit(db, user.id, "MOOD_DELETED", "mood_checkin", row.id)
    db.delete(row); db.commit()


@app.get("/journal")
def journal_list(
    search: str | None = Query(default=None, max_length=120),
    from_date: date | None = None,
    to_date: date | None = None,
    user: User = Depends(require_roles("young_user")),
    db: Session = Depends(get_db),
):
    query = select(JournalEntry).where(JournalEntry.user_id == user.id)
    if search:
        pattern = f"%{search.strip()}%"
        query = query.where(JournalEntry.title.ilike(pattern) | JournalEntry.content.ilike(pattern))
    if from_date:
        query = query.where(JournalEntry.created_at >= datetime.combine(from_date, time.min))
    if to_date:
        query = query.where(JournalEntry.created_at <= datetime.combine(to_date, time.max))
    return [serialize(x) for x in db.scalars(query.order_by(JournalEntry.updated_at.desc())).all()]


@app.post("/journal", status_code=201)
def journal_create(data: JournalIn, user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    values = data.model_dump(exclude={"tags"})
    row = JournalEntry(user_id=user.id, tags=",".join(sorted(set(data.tags))), **values); db.add(row); audit(db, user.id, "JOURNAL_CREATED", "journal"); db.commit(); db.refresh(row)
    return serialize(row)


def owned_journal(entry_id: int, user: User, db: Session):
    row = db.scalar(select(JournalEntry).where(JournalEntry.id == entry_id, JournalEntry.user_id == user.id))
    if not row: raise HTTPException(404, "Entrada não encontrada")
    return row


@app.put("/journal/{entry_id}")
def journal_update(entry_id: int, data: JournalIn, user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    row = owned_journal(entry_id, user, db); row.title=data.title; row.content=data.content; row.tags=",".join(sorted(set(data.tags))); row.updated_at=datetime.utcnow(); audit(db,user.id,"JOURNAL_UPDATED","journal",row.id); db.commit(); return serialize(row)


@app.delete("/journal/{entry_id}", status_code=204)
def journal_delete(entry_id: int, user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    row=owned_journal(entry_id,user,db)
    for attachment in db.scalars(select(JournalAttachment).where(JournalAttachment.entry_id == row.id)).all(): db.delete(attachment)
    audit(db,user.id,"JOURNAL_DELETED","journal",row.id); db.delete(row); db.commit()


def attachment_metadata(row: JournalAttachment):
    return {"id": row.id, "entry_id": row.entry_id, "filename": row.filename, "content_type": row.content_type, "size_bytes": row.size_bytes, "created_at": row.created_at, "content_url": f"/journal/{row.entry_id}/attachments/{row.id}/content"}


@app.get("/journal/{entry_id}/attachments")
def journal_attachments(entry_id: int, user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    owned_journal(entry_id, user, db)
    rows = db.scalars(select(JournalAttachment).where(JournalAttachment.entry_id == entry_id, JournalAttachment.user_id == user.id)).all()
    return [attachment_metadata(row) for row in rows]


@app.post("/journal/{entry_id}/attachments", status_code=201)
async def journal_attachment_upload(entry_id: int, file: UploadFile = File(...), user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    owned_journal(entry_id, user, db)
    allowed = {"image/jpeg", "image/png", "image/webp", "image/gif"}
    if file.content_type not in allowed:
        raise HTTPException(415, "Somente imagens JPEG, PNG, WebP ou GIF são permitidas")
    content = await file.read(5 * 1024 * 1024 + 1)
    if not content or len(content) > 5 * 1024 * 1024:
        raise HTTPException(413, "A imagem deve ter até 5 MB")
    filename = Path(file.filename or "imagem").name[:180]
    row = JournalAttachment(entry_id=entry_id, user_id=user.id, filename=filename, content_type=file.content_type, size_bytes=len(content), content=content)
    db.add(row); db.flush(); audit(db, user.id, "JOURNAL_ATTACHMENT_CREATED", "journal_attachment", row.id); db.commit(); db.refresh(row)
    return attachment_metadata(row)


def owned_attachment(entry_id: int, attachment_id: int, user: User, db: Session):
    row = db.scalar(select(JournalAttachment).where(JournalAttachment.id == attachment_id, JournalAttachment.entry_id == entry_id, JournalAttachment.user_id == user.id))
    if not row: raise HTTPException(404, "Anexo não encontrado")
    return row


@app.get("/journal/{entry_id}/attachments/{attachment_id}/content")
def journal_attachment_content(entry_id: int, attachment_id: int, user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    row = owned_attachment(entry_id, attachment_id, user, db)
    return Response(content=row.content, media_type=row.content_type, headers={"Cache-Control": "private, no-store", "Content-Disposition": f'inline; filename="{row.filename}"'})


@app.delete("/journal/{entry_id}/attachments/{attachment_id}", status_code=204)
def journal_attachment_delete(entry_id: int, attachment_id: int, user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    row = owned_attachment(entry_id, attachment_id, user, db); audit(db, user.id, "JOURNAL_ATTACHMENT_DELETED", "journal_attachment", row.id); db.delete(row); db.commit()


@app.get("/selfcare")
def selfcare(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return [serialize(x) for x in db.scalars(select(SelfcareItem).where(SelfcareItem.status == "published")).all()]


@app.get("/selfcare/uses")
def selfcare_uses(user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    return [serialize(x) for x in db.scalars(select(SelfcareUse).where(SelfcareUse.user_id == user.id).order_by(SelfcareUse.started_at.desc())).all()]


@app.post("/selfcare/{item_id}/start", status_code=201)
def start_selfcare(item_id: int, user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    item = db.scalar(select(SelfcareItem).where(SelfcareItem.id == item_id, SelfcareItem.status == "published"))
    if not item: raise HTTPException(404, "Atividade não encontrada")
    row = SelfcareUse(user_id=user.id, item_id=item.id, status="started", completed_at=None)
    db.add(row); db.flush(); audit(db, user.id, "SELFCARE_STARTED", "selfcare_use", row.id); db.commit(); db.refresh(row); return serialize(row)


@app.post("/selfcare/{item_id}/complete", status_code=201)
def complete_selfcare(item_id: int, data: SelfcareUseIn, user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    item = db.scalar(select(SelfcareItem).where(SelfcareItem.id == item_id, SelfcareItem.status == "published"))
    if not item:
        raise HTTPException(404, "Atividade não encontrada")
    row = db.scalar(select(SelfcareUse).where(SelfcareUse.user_id == user.id, SelfcareUse.item_id == item.id, SelfcareUse.status == "started").order_by(SelfcareUse.started_at.desc()))
    if row:
        row.status = "completed"; row.feedback = data.feedback; row.completed_at = datetime.utcnow()
    else:
        row = SelfcareUse(user_id=user.id, item_id=item.id, feedback=data.feedback, status="completed", completed_at=datetime.utcnow())
    db.add(row); db.flush(); audit(db, user.id, "SELFCARE_COMPLETED", "selfcare_use", row.id); db.commit(); db.refresh(row)
    return serialize(row)


@app.post("/chat/messages")
def chat(data: ChatIn, user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    result = run_pipeline(db, data.text)
    # Store only minimized/non-journal chat content. Raw prompts are never logged.
    db.add(ConversationMessage(user_id=user.id, role="user", content="[conteúdo minimizado]"))
    assistant = ConversationMessage(user_id=user.id, role="assistant", content=result.text, response_type=result.response_type)
    db.add(assistant); db.flush()
    for code in result.policy_events: db.add(PolicyEvent(user_id=user.id, code=code))
    if result.safety: db.add(SafetyEvent(user_id=user.id, category=result.safety[0], severity=result.safety[1]))
    audit(db,user.id,"CHAT_POLICY_APPLIED","chat",result.response_type); db.commit()
    return {"text": result.text, "source_refs": result.source_refs, "policy_events": result.policy_events, "response_type": result.response_type, "provider": result.provider, "message_id": assistant.id, "created_at": assistant.created_at}


@app.post("/chat/messages/{message_id}/feedback", status_code=201)
def chat_feedback(message_id: int, data: ChatFeedbackIn, user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    message = db.scalar(select(ConversationMessage).where(ConversationMessage.id == message_id, ConversationMessage.user_id == user.id, ConversationMessage.role == "assistant"))
    if not message: raise HTTPException(404, "Mensagem não encontrada")
    row = db.scalar(select(ChatFeedback).where(ChatFeedback.message_id == message_id)) or ChatFeedback(user_id=user.id, message_id=message_id, useful=data.useful)
    row.useful = data.useful; db.add(row); audit(db, user.id, "CHAT_FEEDBACK_RECORDED", "conversation_message", message_id); db.commit(); db.refresh(row); return serialize(row)


@app.get("/help-contacts")
def help_contacts(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return [serialize(x) for x in db.scalars(select(HelpContact).where(HelpContact.active.is_(True))).all()]


@app.get("/professionals")
def professionals(user: User = Depends(current_user), db: Session = Depends(get_db)):
    result=[]
    for prof in db.scalars(select(Professional)).all():
        slots=[serialize(s) for s in db.scalars(select(AvailabilitySlot).where(AvailabilitySlot.professional_id==prof.id,AvailabilitySlot.booked.is_(False))).all()]
        result.append({**serialize(prof),"slots":slots})
    return result


@app.get("/appointments")
def appointments(user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    labels = {"scheduled": "Agendado", "confirmed": "Confirmado", "cancelled": "Cancelado", "completed": "Concluído"}
    result = []
    rows = db.scalars(select(Appointment).where(Appointment.user_id == user.id).order_by(Appointment.created_at.desc())).all()
    for row in rows:
        slot = db.get(AvailabilitySlot, row.slot_id)
        professional = db.get(Professional, slot.professional_id)
        result.append({**serialize(row), "status_label": labels.get(row.status, row.status), "starts_at": slot.starts_at, "professional": professional.name, "specialty": professional.specialty, "demo_label": professional.demo_label})
    return result


@app.post("/appointments", status_code=201)
def book(data: AppointmentIn, user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    slot=db.scalar(select(AvailabilitySlot).where(AvailabilitySlot.id == data.slot_id).with_for_update())
    if not slot or slot.booked: raise HTTPException(409,"Horário indisponível")
    existing=db.scalar(select(Appointment).where(Appointment.slot_id==data.slot_id,Appointment.status.in_(["scheduled", "confirmed"])))
    if existing: raise HTTPException(409,"Horário já reservado")
    slot.booked=True; row=Appointment(user_id=user.id,slot_id=slot.id); db.add(row); db.flush(); audit(db,user.id,"APPOINTMENT_CREATED","appointment",row.id); db.commit(); db.refresh(row); return serialize(row)


@app.delete("/appointments/{appointment_id}")
def cancel(appointment_id:int,user:User=Depends(require_roles("young_user")),db:Session=Depends(get_db)):
    row=db.scalar(select(Appointment).where(Appointment.id==appointment_id,Appointment.user_id==user.id))
    if not row: raise HTTPException(404,"Agendamento não encontrado")
    row.status="cancelled"; slot=db.get(AvailabilitySlot,row.slot_id); slot.booked=False; audit(db,user.id,"APPOINTMENT_CANCELLED","appointment",row.id); db.commit(); return serialize(row)


@app.put("/appointments/{appointment_id}/reschedule")
def reschedule(appointment_id: int, data: AppointmentIn, user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    row = db.scalar(select(Appointment).where(Appointment.id == appointment_id, Appointment.user_id == user.id).with_for_update())
    if not row or row.status not in {"scheduled", "confirmed"}: raise HTTPException(404, "Agendamento ativo não encontrado")
    new_slot = db.scalar(select(AvailabilitySlot).where(AvailabilitySlot.id == data.slot_id).with_for_update())
    if not new_slot or new_slot.booked: raise HTTPException(409, "Horário indisponível")
    conflict = db.scalar(select(Appointment).where(Appointment.slot_id == data.slot_id, Appointment.status.in_(["scheduled", "confirmed"]), Appointment.id != row.id))
    if conflict: raise HTTPException(409, "Horário já reservado")
    old_slot = db.get(AvailabilitySlot, row.slot_id); old_slot.booked = False; new_slot.booked = True; row.slot_id = new_slot.id; row.status = "scheduled"
    audit(db, user.id, "APPOINTMENT_RESCHEDULED", "appointment", row.id); db.commit(); return serialize(row)


@app.put("/appointments/{appointment_id}/status")
def appointment_status(
    appointment_id: int,
    status: str = Query(pattern="^(confirmed|completed)$"),
    user: User = Depends(require_roles("psychologist", "admin")),
    db: Session = Depends(get_db),
):
    row = db.get(Appointment, appointment_id)
    if not row:
        raise HTTPException(404, "Agendamento não encontrado")
    row.status = status
    audit(db, user.id, "APPOINTMENT_STATUS_CHANGED", "appointment", row.id)
    db.commit()
    return serialize(row)


@app.get("/privacy/export")
def privacy_export(user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    return {"exported_at":datetime.utcnow(),"profile":{"email":user.email,"name":user.name,"role":user.role},"consents":[serialize(x) for x in db.scalars(select(Consent).where(Consent.user_id==user.id))],"mood_checkins":[serialize(x) for x in db.scalars(select(MoodCheckin).where(MoodCheckin.user_id==user.id))],"journal":[serialize(x) for x in db.scalars(select(JournalEntry).where(JournalEntry.user_id==user.id))],"appointments":[serialize(x) for x in db.scalars(select(Appointment).where(Appointment.user_id==user.id))]}


@app.post("/privacy/delete-request")
def delete_optional(user: User = Depends(require_roles("young_user")), db: Session = Depends(get_db)):
    counts={}
    attachments = db.scalars(select(JournalAttachment).where(JournalAttachment.user_id == user.id)).all(); counts["journal_attachments"] = len(attachments)
    for row in attachments: db.delete(row)
    feedback = db.scalars(select(ChatFeedback).where(ChatFeedback.user_id == user.id)).all(); counts["chat_feedback"] = len(feedback)
    for row in feedback: db.delete(row)
    for model,key in [(MoodCheckin,"mood_checkins"),(JournalEntry,"journal"),(ConversationMessage,"chat")]:
        rows=db.scalars(select(model).where(model.user_id==user.id)).all(); counts[key]=len(rows)
        for row in rows: db.delete(row)
    audit(db,user.id,"PRIVACY_OPTIONAL_DATA_DELETED","privacy"); db.commit(); return {"status":"completed","deleted":counts}


@app.put("/privacy/notifications")
def notifications(data:NotificationIn,user:User=Depends(current_user),db:Session=Depends(get_db)):
    row=db.get(NotificationPreference,user.id) or NotificationPreference(user_id=user.id)
    row.enabled=data.enabled; row.discreet=data.discreet; db.add(row); audit(db,user.id,"NOTIFICATION_PREF_UPDATED","privacy"); db.commit(); return serialize(row)


@app.get("/admin/knowledge")
def knowledge_list(user:User=Depends(require_roles("admin")),db:Session=Depends(get_db)):
    return [{**serialize(v),"title":db.get(KnowledgeItem,v.item_id).title,"slug":db.get(KnowledgeItem,v.item_id).slug} for v in db.scalars(select(KnowledgeVersion).order_by(KnowledgeVersion.item_id,KnowledgeVersion.version.desc())).all()]


@app.post("/admin/knowledge",status_code=201)
def knowledge_create(data:KnowledgeIn,user:User=Depends(require_roles("admin")),db:Session=Depends(get_db)):
    item=db.scalar(select(KnowledgeItem).where(KnowledgeItem.slug==data.slug))
    if not item: item=KnowledgeItem(slug=data.slug,title=data.title); db.add(item); db.flush()
    item.title = data.title; item.category = data.category; item.tags = ",".join(sorted(set(data.tags)))
    latest=db.scalar(select(func.max(KnowledgeVersion.version)).where(KnowledgeVersion.item_id==item.id)) or 0
    row=KnowledgeVersion(item_id=item.id,version=latest+1,content=data.content,source=data.source,status="draft",reviewed_by=data.reviewed_by); db.add(row); db.flush(); audit(db,user.id,"KB_VERSION_CREATED","knowledge_version",row.id); db.commit(); db.refresh(row); return serialize(row)


@app.put("/admin/knowledge/{version_id}/status")
def knowledge_status(version_id:int,data:KnowledgeStatus,user:User=Depends(require_roles("admin")),db:Session=Depends(get_db)):
    row=db.get(KnowledgeVersion,version_id)
    if not row: raise HTTPException(404,"Versão não encontrada")
    if data.status=="published" and not row.reviewed_by: raise HTTPException(422,"reviewed_by é obrigatório para publicação")
    row.status=data.status; audit(db,user.id,"KB_STATUS_CHANGED","knowledge_version",row.id); db.commit(); return serialize(row)


@app.get("/admin/policies")
def policies(user:User=Depends(require_roles("admin")),db:Session=Depends(get_db)):
    return [serialize(x) for x in db.scalars(select(PolicyVersion).order_by(PolicyVersion.code,PolicyVersion.version.desc())).all()]


@app.post("/admin/policies", status_code=201)
def policy_create(data:PolicyIn,user:User=Depends(require_roles("admin")),db:Session=Depends(get_db)):
    latest=db.scalar(select(func.max(PolicyVersion.version)).where(PolicyVersion.code==data.code)) or 0
    row=PolicyVersion(code=data.code,version=latest+1,content=data.content,status="draft",reviewed_by=data.reviewed_by)
    db.add(row); db.flush(); audit(db,user.id,"POLICY_VERSION_CREATED","policy_version",row.id); db.commit(); db.refresh(row); return serialize(row)


@app.put("/admin/policies/{version_id}/status")
def policy_status(version_id:int,data:KnowledgeStatus,user:User=Depends(require_roles("admin")),db:Session=Depends(get_db)):
    row=db.get(PolicyVersion,version_id)
    if not row: raise HTTPException(404,"Versão não encontrada")
    if data.status=="published" and not row.reviewed_by: raise HTTPException(422,"reviewed_by é obrigatório para publicação")
    row.status=data.status; audit(db,user.id,"POLICY_STATUS_CHANGED","policy_version",row.id); db.commit(); return serialize(row)


@app.get("/admin/audit")
def audit_list(user:User=Depends(require_roles("admin")),db:Session=Depends(get_db)):
    return [serialize(x) for x in db.scalars(select(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(200)).all()]


@app.get("/admin/dashboard")
def dashboard(user:User=Depends(require_roles("admin","researcher_aggregated")),db:Session=Depends(get_db)):
    # No JournalEntry or ConversationMessage query is allowed here.
    db_counts={"demo_accounts":db.scalar(select(func.count(User.id))),"checkins":db.scalar(select(func.count(MoodCheckin.id))),"selfcare_resources":db.scalar(select(func.count(SelfcareItem.id))),"selfcare_completions":db.scalar(select(func.count(SelfcareUse.id))),"appointments":db.scalar(select(func.count(Appointment.id))),"fallback_events":db.scalar(select(func.count(PolicyEvent.id)).where(PolicyEvent.code=="OUT_OF_SCOPE")),"safety_events":db.scalar(select(func.count(SafetyEvent.id))),"published_kb":db.scalar(select(func.count(KnowledgeVersion.id)).where(KnowledgeVersion.status=="published"))}
    role_rows = db.execute(select(User.role, func.count(User.id)).group_by(User.role)).all()
    cohorts = [{"label": role, "n": count, "value": count if count >= 5 else None, "suppressed": count < 5} for role, count in role_rows]
    appointments_by_status = {status: count for status, count in db.execute(select(Appointment.status, func.count(Appointment.id)).group_by(Appointment.status)).all()}
    return {"warning":"Indicadores operacionais DEMO derivados do banco. Pesquisa usa somente dataset sintético separado.","database":db_counts,"appointments_by_status":appointments_by_status,"cohorts":cohorts,"suppression_threshold":5}


@app.get("/research/model-card")
def model_card(user:User=Depends(require_roles("researcher_aggregated","admin"))):
    return {"banner":"NON-CLINICAL • DADOS SINTÉTICOS","target":"engagement_next_7_days","models":[{"name":"baseline_majority","accuracy":0.50,"roc_auc":0.50},{"name":"logistic_regression","accuracy":0.696,"roc_auc":0.728},{"name":"random_forest","accuracy":0.708,"roc_auc":0.774}],"evaluation":"stratified 5-fold cross-validation on synthetic data; temporal feature/target split","feature_importance":[{"feature":"checkins_history","importance":0.548},{"feature":"selfcare_history","importance":0.303},{"feature":"appointments_history","importance":0.105},{"feature":"notification_opt_in","importance":0.044}],"prohibited_uses":["diagnóstico","risco clínico","depressão","suicídio","decisão de cuidado"],"chat_integration":False,"limitations":"Métricas demonstrativas reproduzíveis, sem validade clínica ou externa."}
