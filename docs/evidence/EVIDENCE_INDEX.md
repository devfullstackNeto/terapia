# Evidence Index — TerapIA Sprint 3 final

Gerado em 2026-09-30 com Playwright contra o ambiente local real. Todas as pessoas, mensagens, imagens, contatos e registros são sintéticos.

| ID | Arquivo | Tela/Fluxo | Funcionalidade comprovada | Teste relacionado | Documento relacionado | Resultado |
|---|---|---|---|---|---|---|
| D01 | [D01-login.png](screenshots/desktop/D01-login.png) | Login DEMO | Credenciais sintéticas e disclosure inicial | A11Y-001 | [README.md](../../README.md) | PASS |
| D02 | [D02-home.png](screenshots/desktop/D02-home.png) | Home | Jornada contextual e atalhos | PILOT-001 | [DEMO_SCRIPT.md](../../DEMO_SCRIPT.md) | PASS |
| D03 | [D03-transparencia-ia-provider.png](screenshots/desktop/D03-transparencia-ia-provider.png) | Transparência da IA | Provider/modelo/RAG/safety visíveis | test_ai_001_transparency_status | [OLLAMA_LOCAL_AI.md](../../OLLAMA_LOCAL_AI.md) | PASS |
| D04 | [D04-checkin-inicial.png](screenshots/desktop/D04-checkin-inicial.png) | Check-in inicial | Escala 1–5 e contexto opcional | test_mood_001_validation_and_history | [API.md](../../API.md) | PASS |
| D05 | [D05-checkin-historico-tendencia.png](screenshots/desktop/D05-checkin-historico-tendencia.png) | Histórico de check-in | Persistência, data/hora e tendência | test_mood_002_filter_and_delete | [DATA_DICTIONARY.md](../../DATA_DICTIONARY.md) | PASS |
| D06 | [D06-autocuidado.png](screenshots/desktop/D06-autocuidado.png) | Biblioteca de autocuidado | Itens publicados/versionados | test_care_001_versioned_published_library | [AI_SAFETY.md](../../AI_SAFETY.md) | PASS |
| D07 | [D07-atividade-respiracao.png](screenshots/desktop/D07-atividade-respiracao.png) | Respiração interativa | Início, temporizador e conclusão | test_care_003_start_and_complete | [DEMO_SCRIPT.md](../../DEMO_SCRIPT.md) | PASS |
| D08 | [D08-grounding.png](screenshots/desktop/D08-grounding.png) | Grounding 5-4-3-2-1 | Experiência progressiva não clínica | test_care_003_start_and_complete | [DEMO_SCRIPT.md](../../DEMO_SCRIPT.md) | PASS |
| D09 | [D09-diario.png](screenshots/desktop/D09-diario.png) | Diário privado | Isolamento arquitetural e timeline | test_journal_001_crud_and_owner_scope | [PRIVACY.md](../../PRIVACY.md) | PASS |
| D10 | [D10-novo-registro-diario.png](screenshots/desktop/D10-novo-registro-diario.png) | Novo registro | Texto, tags e upload sintético | test_journal_004_private_image_lifecycle | [SECURITY.md](../../SECURITY.md) | PASS |
| D11 | [D11-diario-tags-data-hora.png](screenshots/desktop/D11-diario-tags-data-hora.png) | Diário com tags/data | Persistência e metadados | test_journal_003_search_edit_delete | [DATA_DICTIONARY.md](../../DATA_DICTIONARY.md) | PASS |
| D12 | [D12-diario-imagem-privada.png](screenshots/desktop/D12-diario-imagem-privada.png) | Imagem privada | Renderização autenticada owner-scoped | test_journal_004_private_image_lifecycle | [PRIVACY.md](../../PRIVACY.md) | PASS |
| D13 | [D13-chat-inicial.png](screenshots/desktop/D13-chat-inicial.png) | Chat inicial | Disclosure, prompts e pipeline | PILOT-001 | [AI_SAFETY.md](../../AI_SAFETY.md) | PASS |
| D14 | [D14-chat-grounded-fonte.png](screenshots/desktop/D14-chat-grounded-fonte.png) | Resposta grounded | RAG, source ref e provider real da captura | test_chat_001_grounded_and_sources | [AI_SAFETY.md](../../AI_SAFETY.md) | PASS |
| D15 | [D15-feedback-resposta.png](screenshots/desktop/D15-feedback-resposta.png) | Feedback do chat | Persistência útil/não útil | test_chat_003_feedback_is_owner_scoped | [API.md](../../API.md) | PASS |
| D16 | [D16-chat-organizar-rotina.png](screenshots/desktop/D16-chat-organizar-rotina.png) | Chat: rotina | Grounding com KB publicada | CHAT-GOLD-001..100 | [AI_SAFETY.md](../../AI_SAFETY.md) | PASS |
| D17 | [D17-chat-dormir-melhor.png](screenshots/desktop/D17-chat-dormir-melhor.png) | Chat: sono | Grounding com fonte de sono | CHAT-GOLD-001..100 | [AI_SAFETY.md](../../AI_SAFETY.md) | PASS |
| D18 | [D18-chat-pedir-apoio.png](screenshots/desktop/D18-chat-pedir-apoio.png) | Chat: pedir apoio | Grounding e rede humana | CHAT-GOLD-001..100 | [AI_SAFETY.md](../../AI_SAFETY.md) | PASS |
| D19 | [D19-chat-diagnostico.png](screenshots/desktop/D19-chat-diagnostico.png) | Recusa de diagnóstico | Policy anterior ao provider | DIAGNOSIS-001 | [AI_SAFETY.md](../../AI_SAFETY.md) | PASS |
| D20 | [D20-chat-medicamento.png](screenshots/desktop/D20-chat-medicamento.png) | Recusa de medicamento | Sem indicação de dose | PRESCRIPTION-001 | [AI_SAFETY.md](../../AI_SAFETY.md) | PASS |
| D21 | [D21-chat-anti-dependencia.png](screenshots/desktop/D21-chat-anti-dependencia.png) | Anti-dependência | Redirecionamento à rede humana | DEPENDENCY-001 | [AI_SAFETY.md](../../AI_SAFETY.md) | PASS |
| D22 | [D22-chat-safety.png](screenshots/desktop/D22-chat-safety.png) | Crise/safety | Escalonamento determinístico sem provider | SAFE-001 + regressão Sprint 3 | [AI_SAFETY.md](../../AI_SAFETY.md) | PASS |
| D23 | [D23-chat-fora-de-escopo.png](screenshots/desktop/D23-chat-fora-de-escopo.png) | Fora de escopo | Bloqueio de geração livre | CHAT-GOLD-001..100 | [AI_SAFETY.md](../../AI_SAFETY.md) | PASS |
| D24 | [D24-agenda-mensal.png](screenshots/desktop/D24-agenda-mensal.png) | Agenda mensal | Calendário e slots DEMO | APPT-001 | [DEMO_SCRIPT.md](../../DEMO_SCRIPT.md) | PASS |
| D25 | [D25-agenda-semanal.png](screenshots/desktop/D25-agenda-semanal.png) | Agenda semanal | Alternância de visualização | PILOT-001 | [DEMO_SCRIPT.md](../../DEMO_SCRIPT.md) | PASS |
| D26 | [D26-criacao-agendamento.png](screenshots/desktop/D26-criacao-agendamento.png) | Criação de agendamento | Reserva persistente | APPT-001 | [API.md](../../API.md) | PASS |
| D27 | [D27-reagendamento.png](screenshots/desktop/D27-reagendamento.png) | Reagendamento | Troca de slot e prevenção de conflito | test_appt_002_reschedule_and_double_booking | [API.md](../../API.md) | PASS |
| D28 | [D28-safety-center.png](screenshots/desktop/D28-safety-center.png) | Safety Center | Hierarquia humana e contatos DEMO | SAFE-001 | [AI_SAFETY.md](../../AI_SAFETY.md) | PASS |
| D29 | [D29-central-privacidade.png](screenshots/desktop/D29-central-privacidade.png) | Central de Privacidade | Controles e consentimento | PRIV-001 | [PRIVACY.md](../../PRIVACY.md) | PASS |
| D30 | [D30-exportacao-preferencias.png](screenshots/desktop/D30-exportacao-preferencias.png) | Exportação/preferências | Export local e notificação discreta | PRIV-001 | [PRIVACY.md](../../PRIVACY.md) | PASS |
| D31 | [D31-dashboard.png](screenshots/desktop/D31-dashboard.png) | Dashboard agregado | KPIs e supressão n<5 | ADMIN-002 / DASH-003 | [PRIVACY.md](../../PRIVACY.md) | PASS |
| D32 | [D32-admin-knowledge-base.png](screenshots/desktop/D32-admin-knowledge-base.png) | Admin Knowledge Base | Versões publicadas e revisão | ADMIN-001 | [ARCHITECTURE.md](../../ARCHITECTURE.md) | PASS |
| D33 | [D33-research-lab.png](screenshots/desktop/D33-research-lab.png) | Research Lab | Modelo não clínico e isolamento | RES-001 / RES-002 | [MODEL_CARD.md](../../MODEL_CARD.md) | PASS |
| D34 | [D34-admin-provider-safety.png](screenshots/desktop/D34-admin-provider-safety.png) | Admin provider/policies | Transparência e governança safety | test_ai_001_transparency_status / ADMIN-001 | [AI_SAFETY.md](../../AI_SAFETY.md) | PASS |
| M01 | [M01-home.png](screenshots/mobile/M01-home.png) | Home mobile | Responsividade da jornada | PILOT-001 | [SCREENSHOT_GUIDE.md](../../SCREENSHOT_GUIDE.md) | PASS |
| M02 | [M02-checkin.png](screenshots/mobile/M02-checkin.png) | Check-in mobile | Fluxo principal em smartphone | MOOD-001 | [SCREENSHOT_GUIDE.md](../../SCREENSHOT_GUIDE.md) | PASS |
| M03 | [M03-autocuidado.png](screenshots/mobile/M03-autocuidado.png) | Autocuidado mobile | Cards responsivos | CARE-001 | [SCREENSHOT_GUIDE.md](../../SCREENSHOT_GUIDE.md) | PASS |
| M04 | [M04-diario.png](screenshots/mobile/M04-diario.png) | Diário mobile | Privacidade e composição responsiva | JOURNAL-001 | [SCREENSHOT_GUIDE.md](../../SCREENSHOT_GUIDE.md) | PASS |
| M05 | [M05-chat.png](screenshots/mobile/M05-chat.png) | Chat mobile | Chat e transparência em smartphone | CHAT-001 | [SCREENSHOT_GUIDE.md](../../SCREENSHOT_GUIDE.md) | PASS |
| M06 | [M06-agenda.png](screenshots/mobile/M06-agenda.png) | Agenda mobile | Calendário responsivo | APPT-001 | [SCREENSHOT_GUIDE.md](../../SCREENSHOT_GUIDE.md) | PASS |
| M07 | [M07-safety-center.png](screenshots/mobile/M07-safety-center.png) | Safety Center mobile | Acesso móvel a ajuda humana | SAFE-001 | [SCREENSHOT_GUIDE.md](../../SCREENSHOT_GUIDE.md) | PASS |
| M08 | [M08-privacidade.png](screenshots/mobile/M08-privacidade.png) | Privacidade mobile | Controles pessoais responsivos | PRIV-001 | [SCREENSHOT_GUIDE.md](../../SCREENSHOT_GUIDE.md) | PASS |
| V01 | [V01-jornada-principal.webm](videos/V01-jornada-principal.webm) | Jornada principal completa | Login → home → check-in → autocuidado → chat → safety → agenda → diário → privacidade → admin/Research Lab | PILOT-001 | [DEMO_SCRIPT.md](../../DEMO_SCRIPT.md) | VÁLIDO |
| R01 | [capture-data.json](reports/capture-data.json) | Metadados brutos da captura | Nove respostas, classificações, policies, provider e source refs | CHAT-GOLD-001..100 | [AI_SAFETY.md](../../AI_SAFETY.md) | PASS |
| R02 | [terapia-export-demo.json](reports/terapia-export-demo.json) | Exportação DEMO | Arquivo produzido pela Central de Privacidade | PRIV-001 | [PRIVACY.md](../../PRIVACY.md) | PASS |
| R03 | [EVIDENCE_CAPTURE_REPORT.md](reports/EVIDENCE_CAPTURE_REPORT.md) | Relatório técnico | Ambiente, resultados, chat e limitações | QA final | [QA_REPORT.md](../../QA_REPORT.md) | PASS |

## Totais

- Desktop: **34 screenshots**.
- Mobile: **8 screenshots**.
- Vídeos oficiais: **1 válido**.
- Cenários de chatbot: **9 executados**.
- Telas solicitadas não capturadas: **nenhuma**.

