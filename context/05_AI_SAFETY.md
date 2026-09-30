# AI Safety - Non-negotiable
Prohibited:
diagnosis, prescription/dose, stopping treatment, clinical assessment, exclusive/dependent relationship,
unsafe self-harm guidance, claiming human/professional identity, invented emergency contacts.

Dedicated safety mechanism MUST run before LLM/provider.
LLM alone cannot decide crisis.

Implement:
- ScopeClassifier
- SafetyClassifier/rules
- DependencyDetector
- Retriever over APPROVED KB only
- Provider interface (Mock required)
- OutputSafety
- SourceValidator

Return:
text, source_refs, policy_events, response_type.

Golden set >=100 cases:
25 normal/psychoeducation
15 OOS
15 diagnosis/prescription
20 safety
15 dependency/manipulation
10 jailbreak/privacy

Release blocks on any critical unsafe completion.
