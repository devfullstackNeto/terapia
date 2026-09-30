# Guia de screenshots

Use viewport desktop 1440×900 e mobile 390×844. Capture manualmente: login com aviso sintético; home com transparência da IA; check-in e próximos passos; diário com imagem estritamente fictícia; respiração/grounding; chat com provider, RAG e source card; recusas/crise/anti-dependência; Safety Center; calendário mensal e semanal; privacidade; dashboard/admin; Research Lab NON-CLINICAL. Nunca insira dados reais, nomes reais, contatos reais ou imagens de participantes. A validação funcional original da Sprint 3 não gerou screenshots nem vídeo; o pacote abaixo pertence à etapa final específica de evidências.

## Pacote final automatizado

A etapa final de evidências foi executada com Playwright, sem dados reais:

```powershell
cd apps/web
$env:E2E_BASE_URL='http://localhost:8088'
node e2e/evidence.capture.mjs
```

Saída oficial: `docs/evidence/`, com 34 screenshots desktop, 8 mobile, nove cenários de chat, exportação DEMO e um vídeo WebM validado. Consulte `docs/evidence/EVIDENCE_INDEX.md` antes de reutilizar qualquer arquivo.

O roteiro identifica o provider efetivo nos metadados. Se Ollama estiver indisponível, a evidência deve declarar `mock-offline`; nunca rotular uma resposta Mock como Mistral. Vídeos parciais, corrompidos ou sem metadados de reprodução devem ser removidos e marcados como inválidos no relatório.
