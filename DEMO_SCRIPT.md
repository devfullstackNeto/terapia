# Roteiro de demonstração

1. Entrar como `jovem@demo.local` e, se exibido, aceitar o consentimento versionado.
2. Registrar humor 4, observar data/hora e próximos passos; iniciar, pausar e concluir a respiração guiada.
3. Criar e editar uma entrada fictícia no diário, adicionar tags e uma imagem sintética; apontar o isolamento e excluir a entrada.
4. No chat, clicar “Estou ansioso com uma prova”, mostrar typing, horário, provider/modelo, RAG, cartão de fonte e feedback útil/não útil.
5. Usar os botões de diagnóstico, dose, dependência, crise e clima para demonstrar desvios seguros anteriores ao provider.
6. Abrir Safety Center, destacar a hierarquia humana e o selo de contato DEMO.
7. Alternar agenda mensal/semanal, reservar/remarcar/cancelar um horário DEMO e abrir a Central de Privacidade.
8. Entrar como `admin@demo.local`, mostrar transparência de IA, dashboard derivado do banco, supressão n < 5, KB e políticas publicadas.
9. Abrir Research Lab e reforçar: NON-CLINICAL, dataset sintético, chat desconectado e usos proibidos.
10. Encerrar reiterando que texto/imagens do diário não aparecem em chat/dashboard/research, que Ollama é opcional com fallback visível e que não houve piloto real.

## Evidência automatizada final

O roteiro `apps/web/e2e/evidence.capture.mjs` percorre a mesma jornada com a persona sintética, registra nove cenários do chatbot, alterna para o perfil admin e salva screenshots/vídeo em `docs/evidence/`. O relatório oficial deve sempre informar o provider realmente observado em `/health` e `/ai/status`.

Na captura de 2026-09-30, o provider efetivo foi `mock-offline`; Ollama/Mistral estava indisponível e não foi instalado. A frase de crise “Não quero mais viver” acionou `safety_escalation` sem chamada ao provider após a correção mínima de regressão documentada no relatório de captura.
