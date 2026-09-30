\# TERAPIA — EXECUÇÃO FINAL EM UMA ÚNICA RODADA



Você está trabalhando no produto final do projeto de pesquisa TerapIA.



Seu objetivo é transformar o baseline demonstrativo existente em:



UMA APLICAÇÃO FUNCIONAL, INTEGRADA, PERSISTENTE, TESTADA E EXECUTÁVEL LOCALMENTE.



\## Antes de escrever qualquer código



1\. Leia integralmente:



context/00\_MASTER\_CONTEXT.md

context/01\_PRODUCT\_SPEC.md

context/02\_ARCHITECTURE.md

context/03\_DATABASE\_API.md

context/04\_SECURITY\_THREAT\_MODEL.md

context/05\_AI\_SAFETY.md

context/06\_PRIVACY.md

context/07\_TEST\_PLAN.md

context/08\_UI\_UX.md

context/09\_DEFINITION\_OF\_DONE.md

context/10\_EXECUTION\_ORDER.md



2\. Analise:



baseline/



3\. Analise:



data/terapia\_synthetic\_v3.json



4\. Gere:



IMPLEMENTATION\_PLAN.md



MAS NÃO PARE PARA PEDIR APROVAÇÃO.



Após gerar o plano, continue imediatamente para implementação.



\---



\# REGRA PRINCIPAL



Não entregue apenas planejamento, mockups, documentação ou scaffolding.



IMPLEMENTE O SISTEMA.



Você deve continuar trabalhando até:



\- backend funcionar;

\- frontend funcionar;

\- persistência funcionar;

\- autenticação funcionar;

\- testes P0 passarem;

\- Docker Compose subir;

\- README permitir execução;

\- QA\_REPORT.md não possuir falhas P0 conhecidas.



\---



\# BASELINE



O diretório:



baseline/



é a referência visual e conceitual.



Preserve:

\- identidade visual;

\- fluxo;

\- páginas;

\- linguagem;

\- conceito mobile-first.



Você pode refatorar completamente a implementação.



Não precisa manter HTML/JS estático se isso atrapalhar.



\---



\# STACK DESEJADA



Monorepo.



Frontend web:

React

TypeScript

Vite



Mobile:

Expo React Native



Backend:

FastAPI

Python



Persistência:

PostgreSQL



Cache/jobs:

Redis



Infraestrutura:

Docker Compose



IA:

Provider abstraction



Obrigatório:

MockProvider funcional offline.



Opcional:

provider compatível com OpenAI via variáveis de ambiente.



Não exija chave externa para rodar a demo.



\---



\# PRIORIDADE



Implemente primeiro todos os requisitos P0.



Depois P1.



Não desperdice tempo criando funcionalidades além da especificação enquanto houver P0 incompleto.



\---



\# FUNCIONALIDADES OBRIGATÓRIAS



\## Autenticação



Login real de demonstração.



RBAC no backend.



Perfis:



young\_user

psychologist

admin

researcher\_aggregated



Criar usuários demo via seed.



\---



\## Onboarding



Exibir:



\- que o sistema utiliza IA;

\- que não substitui psicólogo;

\- limitações;

\- privacidade;

\- consentimento versionado.



Persistir aceite.



\---



\## Check-in



Escala de humor 1–5.



Contexto opcional.



Histórico pessoal.



Persistência em PostgreSQL.



Não gerar diagnóstico.



\---



\## Diário



CRUD privado.



Somente proprietário pode acessar.



NÃO incluir conteúdo do diário no:



\- chatbot;

\- dashboard;

\- analytics;

\- modelo experimental.



Criar testes que comprovem isso.



\---



\## Autocuidado



Biblioteca versionada.



Seed inicial:



\- respiração;

\- grounding;

\- sono;

\- organização;

\- busca de apoio.



Itens devem conter:



\- título;

\- conteúdo;

\- fonte;

\- versão;

\- status;

\- reviewed\_by opcional.



\---



\# CHATBOT



Este é um dos módulos mais importantes.



Pipeline obrigatório:



input

→ PII minimization

→ safety classifier/rules

→ dependency detector

→ scope classifier

→ retrieval KB

→ provider

→ output safety

→ source validator

→ response



Resposta da API deve retornar:



text

source\_refs

policy\_events

response\_type



\---



\## O chatbot NÃO pode:



diagnosticar;

prescrever;

recomendar dose;

orientar suspensão de tratamento;

alegar ser psicólogo;

prometer cura;

estimular segredo;

reforçar dependência emocional;

fornecer instruções perigosas.



\---



\## Safety



Não use apenas o LLM para detecção.



Implemente camada determinística e/ou classificador separado.



Para cenário crítico:



\- interromper geração livre;

\- exibir resposta curta e segura;

\- orientar contato humano;

\- mostrar contatos configurados no banco;

\- criar SafetyEvent.



Não inventar números ou contatos reais.



Use contatos DEMO claramente marcados na seed.



\---



\## Anti-dependency



Exemplos como:



"você é a única pessoa que me entende"

"só preciso de você"

"não quero falar com ninguém além de você"



devem produzir resposta que:



\- não reforça exclusividade;

\- identifica-se como ferramenta;

\- incentiva rede humana.



\---



\# KNOWLEDGE BASE



Admin deve poder:



\- criar;

\- editar;

\- versionar;

\- publicar;

\- despublicar.



Chatbot só usa versões publicadas.



Guardar fonte.



Guardar reviewed\_by.



Guardar versão.



\---



\# PROFISSIONAIS E AGENDA



CRUD básico de profissionais DEMO.



Não inventar CRP real.



Slots de agenda.



Criar/cancelar agendamento.



Evitar dupla reserva.



Persistir tudo.



\---



\# PRIVACIDADE



Criar Central de Privacidade.



Usuário deve conseguir:



\- exportar dados;

\- excluir dados opcionais;

\- revogar consentimento quando aplicável;

\- controlar notificações.



Implementar:



group suppression n < 5 no dashboard.



Researcher não pode acessar:



\- diário;

\- texto das conversas;

\- dados identificáveis.



\---



\# DASHBOARD



Somente agregado.



Mostrar:



\- usuários demo;

\- check-ins;

\- recursos de autocuidado;

\- appointments;

\- fallback;

\- safety events;

\- cobertura da knowledge base.



Nunca mostrar conteúdo individual.



\---



\# RESEARCH LAB



Separado do cuidado.



Usar somente dados sintéticos.



Modelo-alvo:



engagement prediction



NÃO:



depressão;

suicídio;

diagnóstico;

risco clínico.



Implementar pelo menos:



\- baseline;

\- Logistic Regression;

\- Random Forest ou Gradient Boosting;

\- train/test ou CV;

\- métricas;

\- feature importance;

\- model card.



Endpoint:



/research/\*



Nunca chamado pelo chatbot.



\---



\# MOBILE



Criar Expo React Native.



Fluxos mínimos:



login

onboarding

home

check-in

self-care

chat

help

appointments

privacy



Pode compartilhar tipos/API client com web.



\---



\# DADOS



Use:



data/terapia\_synthetic\_v3.json



para seed/demonstração.



Mantenha banner:



DADOS SINTÉTICOS



Não apresentar números sintéticos como pesquisa real.



\---



\# TESTES



Implemente e EXECUTE:



pytest

Vitest

Playwright

lint

typecheck

build



Preserve IDs do plano de QA.



Criar golden set com no mínimo 100 cenários.



Obrigatórios:



CHAT

SAFE

DEPENDENCY

DIAGNOSIS

PRESCRIPTION

PRIVACY

RBAC

JOURNAL ISOLATION



\---



\# INFRA



Criar:



docker-compose.yml



Subir:



postgres

redis

api

web

worker



MinIO apenas se necessário.



Com:



healthchecks

seed

.env.example



\---



\# DOCUMENTAÇÃO FINAL



Gerar:



README.md

ARCHITECTURE.md

API.md

DATA\_DICTIONARY.md

SECURITY.md

PRIVACY.md

AI\_SAFETY.md

MODEL\_CARD.md

CHANGELOG.md

QA\_REPORT.md

SCREENSHOT\_GUIDE.md

DEMO\_SCRIPT.md



\---



\# QA REPORT



No fim, executar todos os testes.



QA\_REPORT.md deve listar:



Test ID

Status

Evidence

Notes



Nenhum P0 pode ficar FAIL.



Se houver FAIL:



CORRIJA.



Rode novamente.



Continue até não haver falha P0 conhecida.



\---



\# VERIFICAÇÃO FINAL



Antes de finalizar:



1\. docker compose up --build

2\. verificar healthchecks

3\. executar backend tests

4\. executar frontend tests

5\. executar E2E

6\. executar golden set

7\. executar lint

8\. executar typecheck

9\. executar build

10\. buscar TODO

11\. buscar FIXME

12\. verificar placeholders

13\. verificar imports quebrados

14\. verificar páginas mobile

15\. verificar dados sintéticos

16\. verificar que diário não aparece no chatbot/dashboard

17\. verificar que Research Lab está isolado

18\. verificar source\_refs

19\. verificar safety flow

20\. verificar anti-dependency



\---



\# NÃO FAÇA



Não pare depois de gerar estrutura.



Não me entregue apenas instruções.



Não peça confirmação entre etapas.



Não diga apenas o que ainda falta.



Implemente o máximo possível nesta execução.



Não invente:

\- usuários reais;

\- psicólogos reais;

\- CRPs reais;

\- contato de emergência real;

\- estudo clínico;

\- resultado de piloto;

\- consentimento real.



\---



\# RESULTADO ESPERADO



Ao final desta rodada deve existir um MVP FULL STACK funcional do TerapIA, apto para:



\- executar localmente;

\- demonstrar;

\- fotografar;

\- tirar screenshots;

\- produzir evidências;

\- realizar nova auditoria técnica;

\- servir como baseline para piloto futuro.

