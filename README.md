# TerapIA V3 — IA local + UX imersiva

MVP full stack de apoio emocional complementar para demonstração e pesquisa técnica. Não é atendimento psicológico, não diagnostica, não prescreve e não usa evidência clínica ou contatos reais. Todos os indicadores de demonstração são **DADOS SINTÉTICOS**.

## Execução recomendada

1. Copie `.env.example` para `.env` e troque `JWT_SECRET` fora de demonstração.
2. Execute `docker compose up --build`.
3. Abra `http://localhost:8088`; API/OpenAPI em `http://localhost:8000/docs`.

O compose sobe PostgreSQL, Redis, API, worker e web com healthchecks. O seed é idempotente e roda ao iniciar a API.

O padrão é `AI_PROVIDER=mock`, totalmente offline. A Sprint 3 também aceita `AI_PROVIDER=ollama` com `OLLAMA_BASE_URL` e `OLLAMA_MODEL`, além do endpoint `openai-style` da Sprint 2. Falha técnica produz fallback controlado para `AI_FALLBACK_PROVIDER=mock`; fluxos de safety são interrompidos antes de qualquer provider. O estado real fica visível na interface e em `GET /ai/status`. Consulte [OLLAMA_LOCAL_AI.md](OLLAMA_LOCAL_AI.md).

## Contas DEMO

Senha de todas: `Demo123!`.

| E-mail | Perfil |
|---|---|
| `jovem@demo.local` | young_user |
| `psicologa@demo.local` | psychologist |
| `admin@demo.local` | admin |
| `pesquisa@demo.local` | researcher_aggregated |

Todos os nomes, profissionais, contatos e dados são fictícios. Não há CRP ou número de emergência real.

## Desenvolvimento e testes

```powershell
cd services/api
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python -m app.seed
.venv\Scripts\pytest -q
.venv\Scripts\ruff check .

cd ../../apps/web
npm install
npm run test
npm run typecheck
npm run lint
npm run build
npx playwright install chromium
npm run e2e
```

Mobile: `cd apps/mobile; npm install; $env:EXPO_PUBLIC_API_URL='http://SEU-IP:8000'; npm start`. O app Expo contém login, onboarding, home, check-in, autocuidado, chat, ajuda, agenda e privacidade.

Research Lab: `pip install -r services/research/requirements.txt; python services/research/train.py`. O alvo é somente engajamento, com baseline, regressão logística, random forest, CV, métricas e importância de features.

## Jornada recomendada da demo

Entre como `jovem@demo.local`, registre um check-in, execute uma prática interativa, use o chat com fontes e feedback, anexe uma imagem fictícia ao diário e navegue pela agenda mensal/semanal. A home e as áreas de chat/admin exibem provider, modelo, fallback, RAG e safety. Depois entre como `admin@demo.local` para mostrar KPIs agregados, versões publicadas e o Research Lab não clínico. Consulte [DEMO_SCRIPT.md](DEMO_SCRIPT.md), [SPRINT3_VALIDATION.md](SPRINT3_VALIDATION.md) e [PILOT_READINESS.md](PILOT_READINESS.md).

## Limites de segurança e privacidade

- O diário e suas imagens protegidas só são acessíveis ao proprietário; não entram no chat, dashboard ou pesquisa.
- O pipeline determinístico precede o provider e bloqueia crise, diagnóstico, prescrição, dependência, prompt injection e temas fora do escopo.
- `MockProvider`, `OllamaProvider` e provider OpenAI-style compartilham o mesmo contrato. A demo não exige chave externa nem Ollama instalado.
- Dashboard e pesquisador recebem somente agregados; grupos com `n < 5` são suprimidos.
- Conteúdo bruto do usuário não é incluído em logs de auditoria.
