# API

OpenAPI interativo: `/docs`. Autenticação usa Bearer JWT obtido em `POST /auth/login` (form fields `username`, `password`). Rotas pessoais impõem owner/role no servidor.

Principais grupos: `/auth/*`, `/me`, `/consents`, `/mood-checkins`, `/journal`, `/selfcare`, `/chat/messages`, `/help-contacts`, `/professionals`, `/appointments`, `/privacy/*`, `/admin/*` e `/research/model-card`.

`POST /chat/messages` retorna sempre `text`, `source_refs`, `policy_events`, `response_type` e `provider`. Fontes de KB incluem título, origem, versão, categoria, tags, score e `kind`; respostas de política apontam a política aplicada.

Incrementos Sprint 3: `GET /ai/status`; tags no diário; `GET/POST /journal/{id}/attachments`, `GET/DELETE /journal/attachments/{id}`; `POST /selfcare/{id}/start`; `POST /chat/messages/{id}/feedback`; e `POST /appointments/{id}/reschedule`. Upload usa multipart, imagens permitidas e limite de 5 MB. Leitura e remoção de anexos são owner-scoped.

Providers opcionais: `AI_PROVIDER=openai-style` usa `/chat/completions`; `AI_PROVIDER=ollama` usa `OLLAMA_BASE_URL`, `OLLAMA_MODEL` e `/api/generate`. Respostas inválidas/timeout são tratadas como `ProviderError` e acionam `AI_FALLBACK_PROVIDER`. O conteúdo do diário e seus anexos nunca compõem requisições ao provider.
