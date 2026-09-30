# IA local com Ollama

O Ollama é opcional. A configuração padrão continua sendo `AI_PROVIDER=mock`, sem chave, internet ou daemon local.

## Preparação no host

1. Instale o Ollama pelo canal oficial do seu sistema.
2. Inicie o serviço: `ollama serve`.
3. Baixe o modelo configurado: `ollama pull mistral`.
4. Copie `.env.example` para `.env` e defina:

```env
AI_PROVIDER=ollama
AI_FALLBACK_PROVIDER=mock
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=mistral
AI_TIMEOUT_SECONDS=8
OLLAMA_HEALTH_TIMEOUT=2
```

Fora do Docker, use normalmente `OLLAMA_BASE_URL=http://localhost:11434`. O Compose usa `host.docker.internal` para alcançar o daemon do Windows/macOS. Em Linux pode ser necessário mapear o host gateway conforme a instalação Docker.

## Verificação segura

No host:

```powershell
cd services/api
.venv\Scripts\python scripts\test_ollama_provider.py
```

O script consulta `/api/tags` e executa uma geração curta em `/api/generate`. Ele imprime somente provider, modelo, disponibilidade e orientação técnica — nunca prompt completo, resposta, token ou segredo. Se o modelo não existir, execute `ollama pull mistral` ou altere `OLLAMA_MODEL`.

Após reiniciar o Compose, confira `GET /health`, `GET /ai/status` autenticado e o cartão “Transparência da IA” na aplicação.

## Contrato e fallback

O backend envia ao Ollama somente a mensagem com PII minimizada e o contexto RAG de versões publicadas. Safety determinístico roda antes. Timeout, erro HTTP, JSON inválido ou modelo ausente geram `ProviderError` e acionam `AI_FALLBACK_PROVIDER=mock`. O usuário vê que houve fallback; os logs guardam apenas códigos técnicos.

Para testar indisponibilidade de forma controlada, pare o Ollama ou configure uma porta inexistente. Chat normal continua pelo fallback; crise, diagnóstico, prescrição, dependência e prompt injection continuam bloqueados antes de qualquer tentativa.

## Limitações

- A qualidade e latência dependem do modelo, hardware e memória do host.
- Modelo local não torna o sistema clinicamente validado.
- O Ollama não faz parte dos cinco containers obrigatórios e não é iniciado pelo Compose.
- Antes de uso real, fixe versão/hash de modelo, revise licenças, faça red teaming e defina observabilidade e política de atualização.

