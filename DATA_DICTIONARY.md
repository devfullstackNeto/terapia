# Dicionário de dados

| Tabela | Finalidade | Sensibilidade/isolamento |
|---|---|---|
| users | conta, role e hash Argon2id | identificável; RBAC |
| consent_records | aceite/revogação versionados | owner |
| mood_checkins | humor 1–5 e contexto opcional | owner; agregado sem texto |
| journal_entries | diário privado | owner; excluído de chat/dashboard/research |
| journal_attachments | imagens binárias privadas, MIME, nome e tamanho | owner; `no-store`; excluído de chat/dashboard/research |
| selfcare_items | biblioteca versionada | publicada |
| knowledge_items / knowledge_versions | KB, fonte, revisão e status | somente publicada no chat |
| conversation_messages | registro minimizado | owner operacional; sem analytics textual |
| chat_feedback | útil/não útil por mensagem | owner da conversa; agregado operacionalmente |
| policy_events / safety_events | códigos de controle | agregado |
| professionals / availability_slots / appointments | agenda DEMO | owner no agendamento |
| notification_preferences | opt-in e discrição | owner |
| help_contacts | contatos DEMO configuráveis | nunca inventados pelo provider |
| audit_events | ação, entidade e ator | sem conteúdo sensível |
