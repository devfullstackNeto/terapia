# AI Safety

Regras determinísticas rodam antes do provider. Crise interrompe geração livre, cria evento e orienta rede humana/contatos configurados DEMO. Diagnóstico, prescrição/dose/suspensão, dependência, prompt injection e assuntos explicitamente fora do escopo recebem respostas de política sem chamada ao provider.

Retrieval ranqueia termos somente em versões `published` e exige relevância mínima. Saída é revalidada e toda resposta contém fonte ou política; referências de KB incluem versão, categoria, tags e score. O golden set cobre 100 cenários.

O padrão é `MockProvider` offline. Providers OpenAI-style e Ollama são opcionais, recebem apenas texto já minimizado e contexto aprovado, usam timeout e retry limitados e nunca incluem segredo, prompt ou resposta em erro/log técnico. Falha aciona fallback configurável com evento `PROVIDER_FALLBACK`; ela não relaxa nenhum bloqueio de safety. Se o fallback estiver desativado, a resposta é uma política de indisponibilidade — nunca geração improvisada.

A transparência operacional expõe provider/modelo, estado, fallback, RAG e safety ao usuário sem prometer disponibilidade. O script `services/api/scripts/test_ollama_provider.py` faz um probe seguro e, quando necessário, orienta explicitamente `ollama pull <modelo>`.
