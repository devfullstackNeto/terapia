# Validação com persona simulada — Sprint 3

Data: 2026-09-30. Método: percurso automatizado com `jovem@demo.local`. **Nenhum adolescente ou participante real foi envolvido; não é validação clínica.**

## Persona

**Júlia Demo**, adolescente inteiramente fictícia, quer organizar como se sente antes de uma prova, praticar autocuidado e entender quando procurar apoio humano. Dados, imagem anexada, profissional e horário usados no teste são sintéticos.

## Percurso validado

1. Login e disclosure de IA/dados sintéticos.
2. Check-in 4/5 com data/hora e próximos passos.
3. Início e conclusão de respiração interativa.
4. Chat grounded com cartão de fonte/RAG e cenário anti-dependência.
5. Agenda com disponibilidade e reserva quando há slot; calendário e ações permanecem funcionais.
6. Diário privado com texto, tags, imagem sintética, edição e exclusão.
7. Safety Center e Central de Privacidade.

Resultado: **PASS**, Playwright `PILOT-001`; smoke A11Y também passou. O teste não captura tela ou vídeo e não envia dados a participantes.

## Safety e isolamento complementares

Diagnóstico, dose/medicamento, dependência, crise, assunto fora do escopo e prompt injection continuam cobertos pelo golden set 100/100. A imagem do diário exige autenticação/ownership, usa resposta `no-store` e nunca entra no chat, dashboard ou Research Lab.

## Interpretação

A evidência demonstra funcionamento técnico e usabilidade automatizável da jornada. Não mede eficácia, satisfação de adolescentes, acessibilidade participativa, desfecho clínico ou adequação a implantação real.

