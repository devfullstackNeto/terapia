"""Safe Ollama connectivity check. It never prints prompts, responses or secrets."""

__test__ = False

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.providers import OllamaProvider, ProviderError


def main():
    model = os.getenv("OLLAMA_MODEL", "mistral")
    provider = OllamaProvider(
        os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        model,
        float(os.getenv("AI_TIMEOUT_SECONDS", "12")),
    )
    available, state = provider.health()
    print(f"provider=ollama model={model} available={str(available).lower()} state={state}")
    if not available:
        print("Inicie o Ollama e execute: ollama pull %s" % model)
        raise SystemExit(2)
    try:
        result = provider.generate("pergunta técnica sem dados pessoais", "contexto educativo aprovado")
        print(f"generation=ok chars={len(result)}")
    except ProviderError as exc:
        print(f"generation=failed reason={type(exc).__name__}")
        raise SystemExit(3) from exc


if __name__ == "__main__":
    main()
