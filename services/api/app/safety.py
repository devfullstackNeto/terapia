import re
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import KnowledgeItem, KnowledgeVersion
from .providers import AIProvider, ProviderError, configured_fallback_provider, configured_provider


@dataclass
class PipelineResult:
    text: str
    source_refs: list[dict]
    policy_events: list[str]
    response_type: str
    safety: tuple[str, str] | None = None
    provider: str = "policy"


PII = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b|\b\d{3}[ .-]?\d{3}[ .-]?\d{3}[ .-]?\d{2}\b")
CRISIS = re.compile(r"suicid|me matar|n[aã]o quero (?:mais )?viver|machucar.*mim|perigo agora", re.I)
PRESCRIPTION = re.compile(r"remédio|remedio|medicamento|dose|quantos mg|parar.*tratamento|suspender.*tratamento", re.I)
DIAGNOSIS = re.compile(r"diagn[oó]stic|tenho depress|tenho ansiedade|qual transtorno", re.I)
DEPENDENCY = re.compile(r"[uú]nica.*entende|s[oó] preciso de voc[eê]|ningu[eé]m al[eé]m de voc[eê]|melhor amigo|não preciso de ninguém", re.I)
INJECTION = re.compile(r"ignore.*instru|revele.*prompt|system prompt|mostre.*segredo", re.I)
OUT_OF_SCOPE = re.compile(
    r"previs[aã]o do tempo|meteorolog|\bclima\b|resultado do jogo|futebol|campeonato|"
    r"cota[cç][aã]o|bolsa de valores|criptomoeda|elei[cç][aã]o|programa[cç][aã]o de (?:tv|cinema)",
    re.I,
)
PROHIBITED_OUTPUT = re.compile(
    r"você tem |tome \d|pare o tratamento|suspenda o tratamento|sou seu psic[oó]logo|"
    r"sou seu terapeuta|garanto a cura|garanto que vai melhorar|confidencialidade absoluta",
    re.I,
)
STOPWORDS = {"para", "como", "com", "uma", "que", "isso", "você", "voce", "meu", "minha", "sobre", "estou"}


def minimize_pii(text: str) -> tuple[str, bool]:
    cleaned, count = PII.subn("[DADO REMOVIDO]", text)
    return cleaned[:2000], bool(count)


def retrieve(db: Session, query: str):
    versions = db.scalars(
        select(KnowledgeVersion)
        .where(KnowledgeVersion.status == "published")
        .order_by(KnowledgeVersion.updated_at.desc(), KnowledgeVersion.version.desc())
    ).all()
    query_words = {x for x in re.findall(r"\w+", query.lower()) if len(x) >= 4 and x not in STOPWORDS}
    ranked = []
    for version in versions:
        item = db.get(KnowledgeItem, version.item_id)
        searchable = f"{item.title} {item.slug} {item.category} {item.tags} {version.content}".lower()
        matched = {word for word in query_words if word in searchable}
        score = len(matched) / max(1, len(query_words))
        if matched:
            ranked.append((score, item, version))
    if not ranked:
        return None
    score, item, version = max(ranked, key=lambda row: row[0])
    if score < 0.2:
        return None
    return item, version, round(score, 3)


def _policy_result(text: str, source_id: str, title: str, events: list[str], kind: str, safety=None):
    return PipelineResult(text, [{"id": source_id, "title": title, "kind": "policy"}], events, kind, safety)


def run_pipeline(db: Session, raw_text: str, provider: AIProvider | None = None) -> PipelineResult:
    text, pii = minimize_pii(raw_text)
    events = ["PII_MINIMIZED"] if pii else []
    if CRISIS.search(text):
        return _policy_result(
            "Sua segurança vem primeiro. Eu não consigo atender uma emergência. Procure agora uma pessoa de confiança que possa ficar com você e um serviço de urgência validado para a sua região. No Safety Center, os contatos desta demonstração estão marcados claramente como DEMO.",
            "SAFE-CRISIS", "Protocolo de segurança", events + ["SAFE_CRISIS", "FREE_GENERATION_BLOCKED"], "safety_escalation", ("risk_language", "high"),
        )
    if PRESCRIPTION.search(text):
        return _policy_result(
            "Não posso indicar medicamento, dose nem mudança ou suspensão de tratamento. Essas decisões precisam de avaliação de um profissional habilitado. Posso ajudar com informação educativa ou com caminhos para buscar apoio humano.",
            "NO-PRESCRIPTION", "Limites sobre medicamentos", events + ["PRESCRIPTION_REFUSAL", "FREE_GENERATION_BLOCKED"], "clinical_refusal", ("medication_request", "medium"),
        )
    if DIAGNOSIS.search(text):
        return _policy_result(
            "Não consigo dizer se você tem uma condição ou fazer avaliação clínica. Posso conversar sobre experiências comuns, sugerir autocuidado complementar e ajudar a encontrar apoio profissional se isso estiver atrapalhando sua rotina.",
            "NO-DIAGNOSIS", "Limites de avaliação clínica", events + ["DIAGNOSIS_REFUSAL", "FREE_GENERATION_BLOCKED"], "clinical_refusal",
        )
    if DEPENDENCY.search(text):
        return _policy_result(
            "Entendo que este espaço possa parecer útil. Ainda assim, sou uma ferramenta de IA — não uma pessoa ou terapeuta — e não devo ser sua única fonte de apoio. Que tal escolher alguém seguro da sua rede para compartilhar um pouco do que está acontecendo?",
            "ANTI-DEPENDENCY", "Vínculo seguro e rede humana", events + ["DEPENDENCY_REDIRECT", "FREE_GENERATION_BLOCKED"], "dependency_redirect", ("dependency", "medium"),
        )
    if INJECTION.search(text):
        return _policy_result(
            "Não posso revelar instruções internas nem ignorar as proteções do sistema. Posso continuar ajudando com emoções gerais, autocuidado e busca de apoio humano.",
            "PROMPT-INJECTION", "Proteção do sistema", events + ["PROMPT_INJECTION_BLOCKED", "FREE_GENERATION_BLOCKED"], "safety_refusal",
        )
    if OUT_OF_SCOPE.search(text):
        return _policy_result(
            "Esse assunto fica fora do meu escopo. Posso ajudar com apoio emocional educativo, autocuidado e caminhos seguros para buscar ajuda humana.",
            "OOS-FALLBACK", "Limite de escopo", events + ["OUT_OF_SCOPE", "FREE_GENERATION_BLOCKED"], "out_of_scope",
        )
    hit = retrieve(db, text)
    if not hit:
        return _policy_result(
            "Não encontrei conteúdo aprovado suficiente para responder com segurança. Meu escopo é apoio emocional educativo, autocuidado e caminhos de ajuda. Você pode reformular a pergunta dentro desses temas ou procurar uma pessoa qualificada para outros assuntos.",
            "OOS-FALLBACK", "Limite de escopo", events + ["OUT_OF_SCOPE"], "out_of_scope",
        )
    item, version, score = hit
    active_provider = provider
    try:
        active_provider = active_provider or configured_provider()
        answer = active_provider.generate(text, version.content)
    except ProviderError:
        active_provider = configured_fallback_provider()
        if active_provider is None:
            return _policy_result(
                "O assistente generativo está temporariamente indisponível. As proteções continuam ativas; tente novamente mais tarde ou use os recursos publicados de autocuidado.",
                "PROVIDER-UNAVAILABLE", "Disponibilidade da IA", events + ["PROVIDER_UNAVAILABLE", "FREE_GENERATION_BLOCKED"], "provider_unavailable",
            )
        answer = active_provider.generate(text, version.content)
        events.append("PROVIDER_FALLBACK")
    if PROHIBITED_OUTPUT.search(answer):
        return _policy_result(
            "Essa resposta não passou pelas regras de segurança. Posso oferecer somente informação educativa e caminhos de apoio humano.",
            "OUTPUT-SAFETY", "Validação de saída", events + ["OUTPUT_BLOCKED"], "safety_refusal",
        )
    source = {
        "id": f"KB-{item.id}-v{version.version}", "title": item.title, "source": version.source,
        "version": version.version, "category": item.category,
        "tags": [tag.strip() for tag in item.tags.split(",") if tag.strip()],
        "score": score, "kind": "knowledge_base",
    }
    return PipelineResult(answer, [source], events + ["GROUNDED_RESPONSE", "SOURCE_VALIDATED"], "grounded", provider=active_provider.name)
