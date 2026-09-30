# Changelog

## 3.2.0 — 2026-09-30

- `OllamaProvider` local opcional com healthcheck, modelo configurável, timeout/retry, instrução de pull e fallback seguro.
- Transparência de IA na home, chat e admin: provider/modelo, disponibilidade, fallback, RAG e safety.
- Chat imersivo com sugestões, typing state, horários, cartões de fonte e feedback útil/não útil.
- Diário com tags, filtros e imagens privadas; autocuidado interativo; calendário mensal/semanal com remarcação.
- Migração `0003_local_ai_immersive`; 136 testes backend, golden 100/100, Vitest 4/4 e Playwright 2/2.

## 3.1.0 — 2026-09-30

- Sprint 2 pilot-ready: jornada web completa, estados em português, cenários prontos e visualizações agregadas.
- Provider OpenAI-style opcional com timeout, retry, fallback e script de conectividade sem segredo.
- RAG ranqueado sobre KB publicada, `source_refs` enriquecidos e cinco temas iniciais.
- Check-in filtrável, diário pesquisável/editável, conclusão de autocuidado, agenda e privacidade ampliadas.
- Dashboard derivado do banco, migração `0002`, 125 testes backend e E2E da persona simulada.

## 3.0.0 — 2026-09-29

- Baseline estático transformado em monorepo persistente e containerizado.
- Auth/RBAC, consentimento, bem-estar, diário isolado, IA segura, agenda, privacidade, governança, pesquisa e mobile Expo.
- Suite P0, golden set, documentação e healthchecks.
