# Arquitetura

Monorepo: `apps/web` (React/Vite), `apps/mobile` (Expo), `services/api` (FastAPI/SQLAlchemy), `services/worker` (Redis), `services/research` (scikit-learn) e `packages/shared`.

Bounded contexts: identidade/consentimento, bem-estar, suporte conversacional, safety, cuidado profissional, governança e pesquisa. PostgreSQL é a persistência oficial; SQLite existe apenas para testes locais. Redis mantém heartbeat e está preparado para jobs.

Fluxo do chat: minimização de PII → regras de safety → detector de dependência → classificador de escopo → retrieval ranqueado de KB publicada → provider configurado → safety de saída → validação de fonte → resposta estruturada. O provider pode ser Mock offline, Ollama local (`/api/generate`) ou endpoint OpenAI-style, todos com fallback explícito. `GET /ai/status` consolida provider/modelo, disponibilidade, fallback, RAG e safety sem expor segredo. Diário e Research Lab não possuem dependência no pipeline.

As migrations Alembic são a fonte de evolução do schema. A migração `0003_local_ai_immersive` adiciona anexos privados de diário, feedback do chat, estado de início/conclusão de autocuidado e remarcação concorrente da agenda. Imagens ficam como binário protegido no PostgreSQL e são servidas apenas ao dono, com `no-store`. Dashboard consulta contagens operacionais diretamente no PostgreSQL, com supressão de coortes n < 5 e sem queries de diário, anexos ou conteúdo de conversa.
