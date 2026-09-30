# SUAP Traceability — TerapIA

Não foi encontrado no repositório um plano SUAP formal com números próprios de objetivo/meta. Para não inventar evidência, esta matriz relaciona somente critérios P0 documentados em `context/09_DEFINITION_OF_DONE.md` e entregas comprovadas. A associação a códigos institucionais SUAP deve ser feita posteriormente pelo responsável do projeto.

| Objetivo/Meta suportado | Entrega implementada | Teste | Screenshot | Documento | Situação |
|---|---|---|---|---|---|
| Execução local reproduzível | Compose com PostgreSQL, Redis, API, worker e web | INFRA-001 / healthchecks | D01, D02 | README.md; QA_REPORT.md | Comprovado |
| Seed e jornada DEMO | Quatro perfis fictícios e disclosure sintético | PILOT-001 / A11Y-001 | D01, D02 | README.md; DEMO_SCRIPT.md | Comprovado |
| Check-in persistente | Escala 1–5, histórico e tendência | MOOD-001 / MOOD-002 | D04, D05, M02 | API.md; DATA_DICTIONARY.md | Comprovado |
| Diário privado e isolado | CRUD, tags, filtros e imagem owner-scoped | JOURNAL-001/003/004; JOURNAL-ISOLATION-002 | D09–D12, M04 | PRIVACY.md; SECURITY.md | Comprovado |
| Autocuidado versionado | Biblioteca, respiração, grounding e conclusão | CARE-001/002/003 | D06–D08, M03 | AI_SAFETY.md; DEMO_SCRIPT.md | Comprovado |
| RAG e source refs | Respostas grounded sobre KB publicada | CHAT-001/002; golden 100/100 | D14, D16–D18 | AI_SAFETY.md; API.md | Comprovado |
| Recusa clínica | Diagnóstico e prescrição bloqueados antes do provider | DIAGNOSIS-001; PRESCRIPTION-001 | D19, D20 | AI_SAFETY.md | Comprovado |
| Safety e anti-dependência | Escalonamento de crise e redirecionamento humano | SAFE-001; DEPENDENCY-001; regressão Sprint 3 | D21, D22, D28, M07 | AI_SAFETY.md | Comprovado |
| Limite de escopo | Geração livre bloqueada para assunto alheio | golden 100/100 | D23 | AI_SAFETY.md | Comprovado |
| Agenda DEMO | Mês/semana, reserva e remarcação | APPT-001; test_appt_002 | D24–D27, M06 | API.md; DEMO_SCRIPT.md | Comprovado |
| Consentimento e controle de dados | Histórico, exportação e preferências | CONS-001; PRIV-001 | D29, D30, M08 | PRIVACY.md | Comprovado |
| Dashboard agregado | KPIs derivados do banco e supressão n<5 | ADMIN-002; DASH-003 | D31 | PRIVACY.md; ARCHITECTURE.md | Comprovado |
| Governança de KB/policies | Publicação versionada e revisão identificada | ADMIN-001 | D32, D34 | ARCHITECTURE.md; AI_SAFETY.md | Comprovado |
| Research Lab não clínico | Model card isolado e dataset sintético | RES-001; RES-002 | D33 | MODEL_CARD.md | Comprovado |
| Transparência do provider | Provider/modelo/RAG/safety exibidos sem mascarar Ollama | test_ai_001_transparency_status; Ollama 001–005 | D03, D14, D34 | OLLAMA_LOCAL_AI.md; QA_REPORT.md | Comprovado |
| Responsividade | Fluxos principais em viewport 390×844 | PILOT-001 + captura Playwright | M01–M08 | SCREENSHOT_GUIDE.md | Comprovado visualmente |
| Qualidade técnica | Testes, lint, typecheck e build | QA final | EVIDENCE_INDEX completo | QA_REPORT.md | Comprovado |
| Eficácia clínica ou piloto real | Não implementado nem alegado | não aplicável | nenhuma | PILOT_READINESS.md | Fora de escopo |

