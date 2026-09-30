from datetime import datetime, timedelta

import httpx
import pytest
from sqlalchemy import select

import app.providers as provider_module
from app.db import SessionLocal
from app.models import AvailabilitySlot, Professional
from app.providers import OllamaProvider, ProviderError, configured_provider
from app.safety import run_pipeline
from tests.conftest import auth


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def client_factory(get_payload=None, post_payload=None, error=None, captures=None):
    class FakeClient:
        def __init__(self, timeout):
            if captures is not None:
                captures.setdefault("timeouts", []).append(timeout)

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def get(self, url):
            if error:
                raise error
            if captures is not None:
                captures["get_url"] = url
            return FakeResponse(get_payload)

        def post(self, url, json):
            if captures is not None:
                captures.setdefault("posts", []).append((url, json))
            if error:
                raise error
            return FakeResponse(post_payload)

    return FakeClient


def test_ollama_001_configuration_and_health(monkeypatch):
    captures = {}
    monkeypatch.setenv("AI_PROVIDER", "ollama")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://ollama.test:11434")
    monkeypatch.setenv("OLLAMA_MODEL", "mistral")
    monkeypatch.setattr(provider_module.httpx, "Client", client_factory(get_payload={"models": [{"name": "mistral:latest"}]}, captures=captures))
    provider = configured_provider()
    assert isinstance(provider, OllamaProvider)
    assert provider.health() == (True, "ready")
    assert captures["get_url"].endswith("/api/tags")


def test_ollama_002_missing_model_and_unavailable(monkeypatch):
    monkeypatch.setattr(provider_module.httpx, "Client", client_factory(get_payload={"models": [{"name": "llama3"}]}))
    provider = OllamaProvider("http://ollama.test", "mistral")
    assert provider.health() == (False, "model_not_installed")
    monkeypatch.setattr(provider_module.httpx, "Client", client_factory(error=httpx.ConnectError("offline")))
    assert provider.health() == (False, "unavailable")


def test_ollama_003_grounded_contract(monkeypatch):
    captures = {}
    monkeypatch.setattr(provider_module.httpx, "Client", client_factory(post_payload={"response": "resposta grounded"}, captures=captures))
    provider = OllamaProvider("http://ollama.test", "mistral", timeout=4)
    assert provider.generate("pergunta minimizada", "fonte publicada") == "resposta grounded"
    payload = captures["posts"][0][1]
    assert payload["stream"] is False and payload["model"] == "mistral"
    assert "fonte publicada" in payload["prompt"]


def test_ollama_004_timeout_retry_and_fallback(monkeypatch):
    captures = {}
    monkeypatch.setenv("AI_FALLBACK_PROVIDER", "mock")
    monkeypatch.setattr(provider_module.httpx, "Client", client_factory(error=httpx.ReadTimeout("timeout"), captures=captures))
    monkeypatch.setattr(provider_module.time, "sleep", lambda _seconds: None)
    with pytest.raises(ProviderError, match="ollama pull mistral"):
        OllamaProvider("http://ollama.test", "mistral").generate("q", "c")
    assert len(captures["posts"]) == 2
    with SessionLocal() as db:
        result = run_pipeline(db, "estou ansioso com a prova", OllamaProvider("http://ollama.test", "mistral"))
    assert result.provider == "mock-offline" and "PROVIDER_FALLBACK" in result.policy_events


def test_ollama_005_safety_never_calls_provider():
    class ForbiddenProvider:
        name = "ollama:mistral"
        model = "mistral"

        def generate(self, question, context):
            raise AssertionError("provider não deveria ser chamado")

    with SessionLocal() as db:
        for prompt in ["acho que tenho depressão", "qual dose de remédio?", "você é a única pessoa que me entende", "não quero mais viver"]:
            result = run_pipeline(db, prompt, ForbiddenProvider())
            assert "FREE_GENERATION_BLOCKED" in result.policy_events


def test_ai_001_transparency_status(client, tokens, monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "mock")
    result = client.get("/ai/status", headers=auth(tokens["young"]))
    assert result.status_code == 200
    body = result.json()
    assert body["label"] == "Modo demonstrativo offline"
    assert body["rag_active"] and body["safety_active"] and body["knowledge_base"]["published_versions"] >= 1


def test_journal_004_private_image_lifecycle(client, tokens):
    entry = client.post("/journal", json={"title": "Foto privada", "content": "registro privado", "tags": ["prova", "rotina"]}, headers=auth(tokens["young"])).json()
    upload = client.post(
        f"/journal/{entry['id']}/attachments",
        files={"file": ("momento.png", b"\x89PNG\r\nconteudo-privado", "image/png")},
        headers=auth(tokens["young"]),
    )
    assert upload.status_code == 201
    attachment = upload.json()
    assert "content" not in attachment and attachment["filename"] == "momento.png"
    assert client.get(f"/journal/{entry['id']}/attachments", headers=auth(tokens["admin"])).status_code == 403
    content = client.get(attachment["content_url"], headers=auth(tokens["young"]), follow_redirects=True)
    assert content.status_code == 200 and content.content.startswith(b"\x89PNG")
    assert content.headers["cache-control"] == "private, no-store"
    assert client.delete(f"/journal/{entry['id']}/attachments/{attachment['id']}", headers=auth(tokens["young"])).status_code == 204
    assert client.delete(f"/journal/{entry['id']}", headers=auth(tokens["young"])).status_code == 204


def test_journal_005_rejects_non_image_and_oversize(client, tokens):
    entry = client.post("/journal", json={"title": "Validação", "content": "arquivo"}, headers=auth(tokens["young"])).json()
    bad = client.post(
        f"/journal/{entry['id']}/attachments",
        files={"file": ("x.txt", b"texto", "text/plain")},
        headers=auth(tokens["young"]),
    )
    huge = client.post(
        f"/journal/{entry['id']}/attachments",
        files={"file": ("x.png", b"x" * (5 * 1024 * 1024 + 1), "image/png")},
        headers=auth(tokens["young"]),
    )
    assert bad.status_code == 415 and huge.status_code == 413


def test_care_003_start_and_complete(client, tokens):
    item = client.get("/selfcare", headers=auth(tokens["young"])).json()[0]
    started = client.post(f"/selfcare/{item['id']}/start", headers=auth(tokens["young"])).json()
    assert started["status"] == "started" and started["completed_at"] is None
    completed = client.post(f"/selfcare/{item['id']}/complete", json={"feedback": "ajudou"}, headers=auth(tokens["young"])).json()
    assert completed["id"] == started["id"] and completed["status"] == "completed"


def test_chat_003_feedback_is_owner_scoped(client, tokens):
    message = client.post("/chat/messages", json={"text": "estou ansioso com a prova"}, headers=auth(tokens["young"])).json()
    saved = client.post(
        f"/chat/messages/{message['message_id']}/feedback",
        json={"useful": True},
        headers=auth(tokens["young"]),
    )
    assert saved.status_code == 201 and saved.json()["useful"] is True
    assert client.post(f"/chat/messages/{message['message_id']}/feedback", json={"useful": False}, headers=auth(tokens["admin"])).status_code == 403


def test_appt_002_reschedule_and_double_booking(client, tokens):
    with SessionLocal() as db:
        professional = db.scalar(select(Professional).limit(1))
        first = AvailabilitySlot(professional_id=professional.id, starts_at=datetime.utcnow() + timedelta(days=20), booked=False)
        second = AvailabilitySlot(professional_id=professional.id, starts_at=datetime.utcnow() + timedelta(days=21), booked=False)
        db.add_all([first, second]); db.commit(); db.refresh(first); db.refresh(second)
        first_id, second_id = first.id, second.id
    appointment = client.post("/appointments", json={"slot_id": first_id}, headers=auth(tokens["young"])).json()
    moved = client.put(
        f"/appointments/{appointment['id']}/reschedule",
        json={"slot_id": second_id},
        headers=auth(tokens["young"]),
    )
    assert moved.status_code == 200 and moved.json()["slot_id"] == second_id
    assert client.post("/appointments", json={"slot_id": second_id}, headers=auth(tokens["young"])).status_code == 409
