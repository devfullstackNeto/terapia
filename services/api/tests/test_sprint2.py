from datetime import date

import httpx
import pytest

import app.providers as provider_module
from app.db import SessionLocal
from app.providers import MockProvider, OpenAIStyleProvider, ProviderError
from app.safety import run_pipeline
from tests.conftest import auth


class BrokenProvider:
    name = "broken"

    def generate(self, question, context):
        raise ProviderError("offline")


class CountingProvider:
    name = "counting"

    def __init__(self):
        self.calls = 0

    def generate(self, question, context):
        self.calls += 1
        return context


def test_provider_001_mock_default_and_external_config(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "mock")
    assert MockProvider().generate("q", "contexto")
    provider = OpenAIStyleProvider("https://provider.invalid/v1", "test-key", "test-model")
    assert provider.url.endswith("/chat/completions")


def test_provider_003_openai_style_contract_with_mock_transport(monkeypatch):
    captured = {}

    class FakeClient:
        def __init__(self, timeout):
            captured["timeout"] = timeout

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def post(self, url, headers, json):
            captured.update(url=url, headers=headers, payload=json)
            request = httpx.Request("POST", url)
            return httpx.Response(200, request=request, json={"choices": [{"message": {"content": "resposta aprovada"}}]})

    monkeypatch.setattr(provider_module.httpx, "Client", FakeClient)
    provider = OpenAIStyleProvider("https://mock.local/v1", "segredo-teste", "modelo-teste", timeout=3)
    assert provider.generate("pergunta minimizada", "contexto publicado") == "resposta aprovada"
    assert captured["timeout"] == 3
    assert captured["payload"]["messages"][-1]["content"] == "pergunta minimizada"
    assert captured["headers"]["Authorization"].startswith("Bearer ")


def test_provider_004_external_retry_is_bounded(monkeypatch):
    attempts = 0

    class FailingClient:
        def __init__(self, timeout):
            self.timeout = timeout

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def post(self, url, headers, json):
            nonlocal attempts
            attempts += 1
            raise httpx.ConnectError("indisponível")

    monkeypatch.setattr(provider_module.httpx, "Client", FailingClient)
    monkeypatch.setattr(provider_module.time, "sleep", lambda _seconds: None)
    with pytest.raises(ProviderError, match="indisponível"):
        OpenAIStyleProvider("https://mock.local/v1", "key", "model").generate("q", "c")
    assert attempts == 2


def test_provider_002_safe_fallback_and_policy_short_circuit():
    with SessionLocal() as db:
        result = run_pipeline(db, "estou ansioso com a prova", BrokenProvider())
        counter = CountingProvider()
        blocked = run_pipeline(db, "qual dose de remédio devo tomar?", counter)
    assert result.response_type == "grounded" and "PROVIDER_FALLBACK" in result.policy_events
    assert result.provider == "mock-offline"
    assert blocked.response_type == "clinical_refusal" and counter.calls == 0


def test_chat_002_source_metadata_and_score(client, tokens):
    result = client.post(
        "/chat/messages",
        json={"text": "estou ansioso com a prova"},
        headers=auth(tokens["young"]),
    ).json()
    source = result["source_refs"][0]
    assert source["kind"] == "knowledge_base"
    assert source["version"] >= 1 and source["score"] >= 0.2
    assert "SOURCE_VALIDATED" in result["policy_events"]


def test_journal_003_search_edit_delete(client, tokens):
    made = client.post(
        "/journal",
        json={"title": "Semana de provas", "content": "texto privado de organização"},
        headers=auth(tokens["young"]),
    ).json()
    found = client.get("/journal?search=provas", headers=auth(tokens["young"])).json()
    assert any(row["id"] == made["id"] for row in found)
    edited = client.put(
        f"/journal/{made['id']}",
        json={"title": "Semana organizada", "content": "texto privado atualizado"},
        headers=auth(tokens["young"]),
    ).json()
    assert edited["updated_at"] >= edited["created_at"]
    assert client.delete(f"/journal/{made['id']}", headers=auth(tokens["young"])).status_code == 204


def test_mood_002_filter_history_and_delete(client, tokens):
    made = client.post(
        "/mood-checkins",
        json={"mood": 4, "context": "Estudos"},
        headers=auth(tokens["young"]),
    ).json()
    today = date.today().isoformat()
    rows = client.get(
        f"/mood-checkins?from_date={today}&to_date={today}",
        headers=auth(tokens["young"]),
    ).json()
    assert any(row["id"] == made["id"] for row in rows)
    assert client.delete(f"/mood-checkins/{made['id']}", headers=auth(tokens["young"])).status_code == 204


def test_care_002_complete_with_feedback(client, tokens):
    item = client.get("/selfcare", headers=auth(tokens["young"])).json()[0]
    assert item["objective"] and item["duration_minutes"] and item["instructions"] and item["category"]
    done = client.post(
        f"/selfcare/{item['id']}/complete",
        json={"feedback": "ajudou"},
        headers=auth(tokens["young"]),
    )
    assert done.status_code == 201 and done.json()["feedback"] == "ajudou"


def test_admin_003_dashboard_is_database_derived(client, tokens):
    result = client.get("/admin/dashboard", headers=auth(tokens["admin"])).json()
    assert "synthetic_dataset" not in result
    assert result["database"]["selfcare_completions"] >= 1
    assert result["suppression_threshold"] == 5
    assert all(row["suppressed"] for row in result["cohorts"] if row["n"] < 5)
