# Plano de implementação — TerapIA

1. Criar monorepo com API FastAPI, web React/Vite, mobile Expo, worker e tipos compartilhados.
2. Modelar persistência relacional e migração inicial para identidade/consentimento, bem-estar, chat seguro, agenda, governança e pesquisa.
3. Implementar autenticação JWT com Argon2id, RBAC e ownership em todos os recursos pessoais.
4. Implementar consentimento versionado, check-in, diário isolado, autocuidado versionado, profissionais/agenda e central de privacidade.
5. Implementar pipeline de IA determinístico antes do provider, MockProvider offline, retrieval apenas publicado, safety, anti-dependência, validação de fontes e eventos de política.
6. Implementar administração de KB/políticas/auditoria e dashboard estritamente agregado com supressão n < 5.
7. Implementar Research Lab isolado, apenas sintético, para predição não clínica de engajamento e model card.
8. Recriar no web a identidade calma, roxa, mobile-first e os fluxos do baseline; preparar os mesmos fluxos essenciais no Expo.
9. Automatizar testes P0 (pytest, Vitest, Playwright e golden set >= 100), lint, typecheck e builds.
10. Entregar Docker Compose com PostgreSQL, Redis, API, web e worker, healthchecks e seed; completar documentação e QA report com evidências.

Decisões: dados de cuidado e pesquisa permanecem fisicamente separados por tabelas/rotas; diário nunca é consultado por chat, dashboard ou pesquisa; contatos e profissionais são marcados DEMO; nenhuma chave externa é necessária.

## Sprint 3 — IA local + UX imersiva

Baseline congelado: 125 Pytest, golden 100/100, 2 Vitest, 2 Playwright e cinco containers saudáveis.

1. Adicionar `OllamaProvider` à abstração existente, status/transparência, timeout, retry, fallback configurável, smoke script e testes, sem adicionar um sexto container obrigatório.
2. Evoluir o schema via Alembic `0003`: tags/anexos privados de diário, estado de uso de autocuidado e feedback de mensagens.
3. Implementar anexos de imagem owner-scoped com validação de tipo/tamanho, leitura autorizada e remoção; nunca consultar esses dados no pipeline, dashboard ou Research Lab.
4. Implementar início/conclusão de autocuidado, feedback de chat e reagendamento atômico com prevenção de double booking.
5. Evoluir web: home contextual, chat com timestamps/feedback/transparência, experiências guiadas, calendário mensal/semanal, diário multimídia e microinterações acessíveis.
6. Ampliar testes API/E2E sem alterar IDs ou expectativas P0 existentes; executar suíte completa e comparar explicitamente com o baseline.
7. Atualizar documentação, criar `OLLAMA_LOCAL_AI.md`, reconstruir Compose e manter zero falhas P0 conhecidas.
