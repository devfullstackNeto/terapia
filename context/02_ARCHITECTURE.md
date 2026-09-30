# Architecture
Monorepo:
apps/web React+TS
apps/mobile Expo RN
services/api FastAPI
services/worker Python
packages/shared schemas/types
postgres
redis
optional minio

Bounded contexts:
IdentityConsent, Wellbeing, ConversationalSupport, Safety, ProfessionalCare, Governance, Research.

AI pipeline:
PII minimization -> safety/dependency/scope -> retrieval -> provider -> output safety -> source validator.

Journal never enters RAG/analytics by default.
Research model never enters chat/care flow.
Provider must have MockProvider offline.
