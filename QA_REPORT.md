# QA Report — TerapIA V3 / Sprint 3

Data: 2026-09-30. Escopo: requisitos P0 da Sprint 3, regressão da Sprint 2 e execução containerizada. Resultado: **PASS — zero falhas P0 conhecidas**.

## Comparação obrigatória com o baseline da Sprint 2

| Evidência | Baseline Sprint 2 | Sprint 3 | Diferença |
|---|---:|---:|---:|
| Pytest | 125 passed | **136 passed** | **+11**, sem regressão |
| Golden set | 100/100 | **100/100** | 0 |
| Vitest | 2 passed | **4 passed** | **+2** |
| Playwright | 2 passed | **2 passed** | 0; jornada PILOT-001 ampliada |
| Containers saudáveis | 5 | **5** | 0 |
| Providers implementados | 2: Mock + OpenAI-style | **3: Mock + OpenAI-style + Ollama** | **+1** |

O provider ativo no Compose validado é `mock-offline`. O probe do Ollama encontrou o serviço/modelo indisponível nesta máquina e retornou a instrução segura `ollama pull mistral`; o fallback permaneceu operacional. Indisponibilidade opcional do Ollama não altera safety, RAG nem os cinco containers obrigatórios.

## Matriz P0 e regressão

| Área | Status | Evidência |
|---|---|---|
| Auth, RBAC, consentimento e ownership | PASS | testes Sprint 2 preservados; anexos/feedback owner-scoped |
| Safety antes do provider | PASS | crise, diagnóstico, prescrição, dependência, injection e OOS não chamam provider |
| RAG publicado e fontes | PASS | golden 100/100; metadados e relevância preservados |
| Ollama local opcional | PASS | configuração, health, geração grounded, timeout, retry, modelo ausente e fallback testados |
| Transparência de IA | PASS | `GET /ai/status` e cartões na home/chat/admin |
| Chat imersivo | PASS | sugestões, typing, timestamps, source cards e feedback persistido |
| Diário multimídia privado | PASS | upload/list/read/delete, MIME/tamanho, `no-store`, IDOR e remoção em cascata |
| Autocuidado interativo | PASS | respiração, grounding e checklists com start/complete persistidos |
| Agenda | PASS | mês/semana, filtros, reserva, cancelamento, remarcação e dupla reserva bloqueada |
| Check-in e home dinâmica | PASS | data/hora, próximos passos e cards derivados da API |
| Privacidade e pesquisa | PASS | anexos fora de chat/dashboard/research; coortes n < 5 suprimidas |
| Responsividade e movimento | PASS | layouts desktop/mobile e `prefers-reduced-motion` |
| Jornada da persona | PASS | Playwright PILOT-001 percorre check-in, autocuidado, chat, agenda, diário com foto, Safety e privacidade |

## Execuções finais

- Backend: `pytest -q` → **136 passed**, 0 failed; golden → **100/100**.
- Qualidade Python: `ruff check .` → **PASS**.
- Web unitária: `vitest run` → **4 passed**, 0 failed.
- E2E contra `http://localhost:8088`: Playwright → **2 passed**, 0 failed.
- ESLint, typecheck web e mobile, build Vite → **PASS**.
- Compose: PostgreSQL, Redis, API, worker e web → **5/5 healthy**.
- Endpoints: API `http://localhost:8000`; web `http://localhost:8088`.
- Provider padrão: `provider=mock-offline status=ok`.
- Ollama opcional: indisponível no host de QA; falha tratada, instrução de instalação/pull exibida, sem vazamento de prompt/segredo.

Warnings não bloqueantes: depreciações já conhecidas de `datetime.utcnow()`, alias AnyIO e opção de solver scikit-learn. Não há falha P0 conhecida.

## Diferenças funcionais da Sprint 3

Além dos fluxos da Sprint 2, a jornada agora inclui IA local Ollama opcional, transparência operacional, feedback no chat, diário com imagem privada/tags/filtros, autocuidado realmente interativo, home contextual e calendário mensal/semanal com remarcação. O número de cenários E2E permanece dois porque a jornada principal existente foi aprofundada, não fragmentada.

## Limite de aprovação

**Aprovado somente para piloto simulado, demonstração e auditoria técnica local.** Uso com pessoas reais ainda exige aprovação ética/jurídica, contatos regionais validados, revisão profissional formal, TLS/secret manager, storage de imagens endurecido, MFA administrativo, rate limiting distribuído e avaliação de acessibilidade com participantes.

