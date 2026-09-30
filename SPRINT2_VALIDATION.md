# Sprint 2 — Validation

Data: 2026-09-30. Resultado: **PASS para todos os requisitos P0 da Sprint 2**.

## Incrementos validados

- Provider abstraction com `MockProvider` offline e provider OpenAI-style opcional via ambiente; timeout, duas tentativas, fallback controlado e mensagens técnicas sem conteúdo sensível.
- Classificação determinística anterior ao provider para crise, prescrição, diagnóstico, dependência, prompt injection e assuntos fora do escopo.
- Retrieval ranqueado somente sobre conhecimento publicado; `source_refs` ricos e validação explícita de fonte.
- Cinco temas iniciais de conhecimento e cinco práticas de autocuidado enriquecidas, com seeds idempotentes.
- Filtros/exclusão no check-in; busca/edição/exclusão no diário; conclusão/feedback de autocuidado; agenda enriquecida; histórico de consentimento; dashboard derivado do banco.
- Interface pilot-ready responsiva com cenários prontos de demonstração e sem JSON bruto nas telas de dashboard, pesquisa ou administração.
- Migração Alembic `0002_pilot_ready` e testes de regressão Sprint 2.

## Matriz de validação

| Área | Evidência | Resultado |
|---|---|---|
| Backend/P0 | `pytest -q`: 125 passed | PASS |
| Golden safety | `test_golden.py`: 100 cenários | PASS |
| Sprint 2 API | `test_sprint2.py`: contrato HTTP mockado, retry, fallback, short-circuit, fontes, CRUD, métricas | PASS |
| Provider offline | `scripts/verify_provider.py`: `provider=mock-offline status=ok` | PASS |
| Web unit | Vitest: 2 passed | PASS |
| Jornada | Playwright: 2 passed | PASS |
| Qualidade | Ruff, ESLint, web/mobile typecheck | PASS |
| Entrega | Vite build e Docker Compose build | PASS |
| Pesquisa | `services/research/train.py` reproduz baseline, LR e RF | PASS |

Warnings conhecidos são de depreciação em dependências (`datetime.utcnow`, alias AnyIO e opção de solver scikit-learn); não afetam os requisitos P0. Não há falha P0 conhecida.

