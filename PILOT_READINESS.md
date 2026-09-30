# Pilot Readiness — TerapIA Sprint 3

Data da avaliação: 2026-09-30. Escopo: **piloto simulado**, sem participantes reais e sem alegação de validade clínica.

## Estado atual

O produto está pronto para demonstração local controlada. A jornada web cobre login, consentimento, home contextual, check-in, diário privado com imagens, autocuidado interativo, chat fundamentado, Safety Center, calendário mensal/semanal e privacidade. Admin vê governança e estado da IA; Research Lab permanece agregado, desconectado do chat e exclusivamente sintético.

| Critério | Estado | Evidência |
|---|---|---|
| Execução sem chave externa | Pronto | MockProvider padrão; Compose 5/5 healthy |
| IA local opcional | Pronto | Ollama health/generate, timeout, retry e fallback; guia dedicado |
| Safety antes do provider | Pronto | bloqueios determinísticos e testes de não chamada |
| Transparência | Pronto | provider/modelo/estado/fallback/RAG/safety na UI e API |
| Privacidade multimídia | Pronto | imagens owner-scoped e isoladas de analytics/chat |
| Jornada imersiva | Pronto | PILOT-001 ampliado e executado contra Compose |
| Qualidade técnica | Pronto | Pytest 136/136; golden 100/100; Vitest 4/4; Playwright 2/2; lint/typecheck/build verdes |

## Go / no-go

**GO apenas para piloto simulado e auditoria técnica local.** Antes de qualquer estudo com pessoas reais: aprovação ética e jurídica, controlador/operador definidos, contatos regionais validados, revisão profissional dos conteúdos/protocolos, observabilidade sem conteúdo sensível, resposta a incidentes, retenção no ambiente-alvo, acessibilidade participativa e hardening da infraestrutura e do storage de imagens.

## Limites explícitos

- Não é dispositivo médico, atendimento psicológico ou serviço de emergência.
- Não há psicólogos, CRPs, contatos, usuários ou resultados clínicos reais.
- Ollama é opcional; ausência do daemon/modelo aciona fallback e não é mascarada na interface.
- Métricas do Research Lab são demonstrações sobre dados sintéticos e não generalizam para pessoas reais.

