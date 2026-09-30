from datetime import datetime, timedelta

from sqlalchemy import select

from .db import Base, SessionLocal, engine
from .models import (
    AvailabilitySlot,
    HelpContact,
    KnowledgeItem,
    KnowledgeVersion,
    PolicyVersion,
    Professional,
    SelfcareItem,
    User,
)
from .security import hash_password

DEMO_USERS = [
    ("jovem@demo.local", "Jovem Demo", "young_user"),
    ("psicologa@demo.local", "Psicóloga Demo", "psychologist"),
    ("admin@demo.local", "Admin Demo", "admin"),
    ("pesquisa@demo.local", "Pesquisa Agregada Demo", "researcher_aggregated"),
]


def seed():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if not db.scalar(select(User).limit(1)):
            for email, name, role in DEMO_USERS:
                db.add(User(email=email, name=name, role=role, password_hash=hash_password("Demo123!")))
        selfcare = [
            ("breathing", "Respiração lenta", "Reduzir a aceleração por alguns minutos", 3, "Respire sem forçar. Inspire suavemente e deixe a expiração durar um pouco mais.", "regulação"),
            ("grounding", "Grounding 5-4-3-2-1", "Trazer a atenção para o momento presente", 5, "Observe 5 coisas que vê, 4 que toca, 3 que ouve, 2 que cheira e 1 sabor.", "atenção"),
            ("sleep", "Preparar o sono", "Organizar uma transição mais tranquila para o descanso", 10, "Reduza estímulos, anote o que ficou pendente e prepare o ambiente sem buscar perfeição.", "sono"),
            ("planning", "Próximo passo pequeno", "Diminuir a sobrecarga de uma tarefa", 7, "Escolha uma tarefa, divida em partes e faça apenas o menor próximo passo possível.", "organização"),
            ("seek_support", "Mapa de apoio", "Identificar uma pessoa segura ou serviço humano", 5, "Liste duas pessoas ou serviços confiáveis e uma forma simples de iniciar a conversa.", "apoio humano"),
        ]
        for slug, title, objective, duration, instructions, category in selfcare:
            row = db.scalar(select(SelfcareItem).where(SelfcareItem.slug == slug))
            if not row:
                row = SelfcareItem(slug=slug, title=title, content=instructions, source="Biblioteca TerapIA DEMO — conteúdo educativo", version="2.0", status="published", reviewed_by="Revisão DEMO")
                db.add(row)
            row.objective, row.duration_minutes, row.instructions, row.category = objective, duration, instructions, category
        knowledge = [
            ("ansiedade", "Ansiedade situacional", "emoções", "ansiedade,preocupação,tensão", "Ansiedade situacional pode envolver preocupação, tensão e sinais físicos. Uma pausa breve, respiração confortável e um próximo passo pequeno podem ajudar a reduzir a sobrecarga do momento."),
            ("sono", "Sono e rotina", "sono", "sono,dormir,descanso,insônia", "Uma rotina de desaceleração, horários consistentes e menos estímulos antes de dormir podem favorecer o descanso. Dificuldades persistentes merecem conversa com um profissional."),
            ("prova", "Organização para provas", "estudos", "prova,estudo,escola,ansiedade", "Antes de uma prova, faça uma pausa curta, escolha o conteúdo mais importante e divida o estudo em blocos pequenos com intervalos."),
            ("rotina", "Organização da rotina", "organização", "rotina,organização,tarefa,tempo", "Quando tudo parece urgente, registre as tarefas, escolha uma prioridade possível e transforme-a em um próximo passo de até dez minutos."),
            ("apoio", "Buscar apoio humano", "apoio humano", "apoio,conversa,ajuda,pessoa", "Buscar uma pessoa segura pode aliviar a sensação de enfrentar tudo sozinho. Você pode começar dizendo que não precisa de soluções, apenas de escuta."),
        ]
        for slug, title, category, tags, content in knowledge:
            item = db.scalar(select(KnowledgeItem).where(KnowledgeItem.slug == slug))
            if not item:
                item = KnowledgeItem(slug=slug, title=title)
                db.add(item)
                db.flush()
            item.title, item.category, item.tags = title, category, tags
            if not db.scalar(select(KnowledgeVersion).where(KnowledgeVersion.item_id == item.id)):
                db.add(KnowledgeVersion(item_id=item.id, version=1, content=content, source="Biblioteca TerapIA DEMO — fonte interna revisada", status="published", reviewed_by="Revisão DEMO"))
        if not db.scalar(select(Professional).limit(1)):
            for name, specialty in [("Psicóloga Demo A", "Adolescentes"), ("Psicólogo Demo B", "Orientação breve")]:
                prof = Professional(name=name, specialty=specialty)
                db.add(prof)
                db.flush()
                for days in (2, 4, 7):
                    db.add(AvailabilitySlot(professional_id=prof.id, starts_at=datetime.utcnow() + timedelta(days=days), booked=False))
        if not db.scalar(select(HelpContact).limit(1)):
            db.add(HelpContact(label="Serviço de urgência DEMO — validar localmente", value="CONTATO-DEMO-NÃO-REAL", region="DEMO"))
        if not db.scalar(select(PolicyVersion).limit(1)):
            db.add(PolicyVersion(code="SAFE-CORE", version=1, content="No diagnosis; no prescription; crisis escalation; anti-dependency; PII minimization.", status="published", reviewed_by="Revisão DEMO"))
        db.commit()


if __name__ == "__main__":
    seed()
