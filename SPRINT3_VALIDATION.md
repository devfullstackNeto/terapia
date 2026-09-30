# Validação da Sprint 3

Data: 2026-09-30. Baseline congelado: estado final validado da Sprint 2.

## Resultado

Sprint 3 concluída sem regressão P0. O sistema preserva os cinco containers e todos os 125 testes anteriores, adiciona 11 testes backend e dois testes unitários web, e mantém golden set e E2E integralmente verdes.

| Dimensão | Sprint 2 | Sprint 3 | Mudança |
|---|---|---|---|
| Pytest | 125 | **136** | +11 |
| Golden | 100/100 | **100/100** | nenhuma |
| Vitest | 2 | **4** | +2 |
| Playwright | 2 | **2** | contagem igual, jornada ampliada |
| Containers | 5 healthy | **5 healthy** | nenhuma |
| Providers | Mock, OpenAI-style | **Mock, OpenAI-style, Ollama** | + Ollama local |
| Diário | texto pesquisável | **texto, tags, filtros e imagens privadas** | ampliado |
| Autocuidado | conclusão | **atividades interativas com start/complete** | ampliado |
| Agenda | lista/reserva/cancelamento | **mês/semana, filtros e remarcação** | ampliado |
| Chat | RAG/fontes/políticas | **transparência, sugestões, typing e feedback** | ampliado |
| Home/check-in | funcional | **contextual e orientado a próximos passos** | ampliado |

## Observação do ambiente

O Compose validado usa MockProvider e está disponível em `http://localhost:8088`; API em `http://localhost:8000/docs`. O Ollama não estava ativo/com o modelo `mistral` disponível no host de QA. O probe falhou de forma esperada, exibiu `ollama pull mistral` e confirmou o caminho de fallback sem afetar os critérios P0.

Detalhes e limites estão em [QA_REPORT.md](QA_REPORT.md), [OLLAMA_LOCAL_AI.md](OLLAMA_LOCAL_AI.md) e [PILOT_READINESS.md](PILOT_READINESS.md).

