import logging
import os
import time
from typing import Protocol

import httpx

logger = logging.getLogger("terapia.provider")


class ProviderError(RuntimeError):
    pass


class AIProvider(Protocol):
    name: str
    model: str

    def generate(self, question: str, context: str) -> str: ...


class MockProvider:
    """Offline provider that composes only approved retrieved context."""

    name = "mock-offline"
    model = "deterministic-grounded-v1"

    def generate(self, question: str, context: str) -> str:
        return (
            f"{context}\n\n"
            "Se fizer sentido para você, escolha um passo pequeno e observe como se sente. "
            "Esta é uma orientação educativa e complementar, não uma avaliação profissional."
        )


class OpenAIStyleProvider:
    name = "openai-style"

    def __init__(self, base_url: str, api_key: str, model: str, timeout: float = 8.0):
        if not base_url or not api_key or not model:
            raise ProviderError("Configuração incompleta do provider externo")
        self.url = f"{base_url.rstrip('/')}/chat/completions"
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def generate(self, question: str, context: str) -> str:
        payload = {
            "model": self.model,
            "temperature": 0.2,
            "max_tokens": 280,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Você é uma ferramenta de apoio emocional educativo, não um profissional. "
                        "Responda somente com base no contexto aprovado. Não diagnostique, não "
                        "prescreva, não prometa sigilo absoluto ou cura e não estimule exclusividade."
                    ),
                },
                {"role": "system", "content": f"CONTEXTO APROVADO:\n{context}"},
                {"role": "user", "content": question},
            ],
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        last_error: Exception | None = None
        for attempt in range(2):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.post(self.url, headers=headers, json=payload)
                    response.raise_for_status()
                    text = response.json()["choices"][0]["message"]["content"].strip()
                    if not text:
                        raise ProviderError("Provider retornou resposta vazia")
                    return text
            except (httpx.HTTPError, KeyError, IndexError, TypeError, ProviderError) as exc:
                last_error = exc
                logger.warning("external_provider_failure attempt=%s type=%s", attempt + 1, type(exc).__name__)
                if attempt == 0:
                    time.sleep(0.1)
        raise ProviderError("Provider externo indisponível") from last_error


class OllamaProvider:
    """Local Ollama provider. Safety and retrieval always happen before this class."""

    def __init__(self, base_url: str, model: str, timeout: float = 12.0):
        if not base_url or not model:
            raise ProviderError("Configuração incompleta do Ollama")
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.name = f"ollama:{model}"

    def health(self, timeout: float = 1.5) -> tuple[bool, str]:
        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                models = [row.get("name", "") for row in response.json().get("models", [])]
            installed = any(name == self.model or name.startswith(f"{self.model}:") for name in models)
            return installed, "ready" if installed else "model_not_installed"
        except (httpx.HTTPError, KeyError, TypeError, ValueError):
            return False, "unavailable"

    def generate(self, question: str, context: str) -> str:
        payload = {
            "model": self.model,
            "stream": False,
            "options": {"temperature": 0.2, "num_predict": 280},
            "system": (
                "Você é uma ferramenta de apoio emocional educativo, não terapeuta. "
                "Use exclusivamente o contexto aprovado. Não diagnostique, prescreva, "
                "prometa cura/sigilo ou estimule vínculo exclusivo."
            ),
            "prompt": f"CONTEXTO APROVADO:\n{context}\n\nPERGUNTA MINIMIZADA:\n{question}",
        }
        last_error: Exception | None = None
        for attempt in range(2):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.post(f"{self.base_url}/api/generate", json=payload)
                    response.raise_for_status()
                    text = response.json()["response"].strip()
                    if not text:
                        raise ProviderError("Ollama retornou resposta vazia")
                    return text
            except (httpx.HTTPError, KeyError, TypeError, ProviderError) as exc:
                last_error = exc
                logger.warning("ollama_failure attempt=%s type=%s", attempt + 1, type(exc).__name__)
                if attempt == 0:
                    time.sleep(0.1)
        raise ProviderError("Ollama indisponível. Inicie o serviço e execute: ollama pull %s" % self.model) from last_error


def configured_provider() -> AIProvider:
    provider = os.getenv("AI_PROVIDER", "mock").lower()
    if provider == "ollama":
        return OllamaProvider(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434"),
            model=os.getenv("OLLAMA_MODEL", "mistral"),
            timeout=float(os.getenv("AI_TIMEOUT_SECONDS", "12")),
        )
    if provider in {"openai", "openai-style", "external"}:
        return OpenAIStyleProvider(
            base_url=os.getenv("AI_BASE_URL", ""),
            api_key=os.getenv("AI_API_KEY", ""),
            model=os.getenv("AI_MODEL", ""),
            timeout=float(os.getenv("AI_TIMEOUT_SECONDS", "8")),
        )
    return MockProvider()


def configured_fallback_provider() -> AIProvider | None:
    fallback = os.getenv("AI_FALLBACK_PROVIDER", "mock").lower()
    return MockProvider() if fallback in {"mock", "mock-offline"} else None


def provider_snapshot() -> dict:
    configured = configured_provider()
    if isinstance(configured, OllamaProvider):
        available, state = configured.health(float(os.getenv("OLLAMA_HEALTH_TIMEOUT", "1.5")))
        return {
            "provider": "ollama",
            "label": f"IA local — Ollama / {configured.model.title()}",
            "model": configured.model,
            "available": available,
            "state": state,
            "mode": "local",
            "fallback": os.getenv("AI_FALLBACK_PROVIDER", "mock"),
        }
    if isinstance(configured, OpenAIStyleProvider):
        return {"provider": "openai-style", "label": "Provider externo compatível", "model": configured.model, "available": True, "state": "configured", "mode": "external", "fallback": os.getenv("AI_FALLBACK_PROVIDER", "mock")}
    return {"provider": "mock", "label": "Modo demonstrativo offline", "model": configured.model, "available": True, "state": "ready", "mode": "offline", "fallback": None}
