# Test Plan
Preserve stable IDs:
AUTH, CONS, MOOD, JOURNAL, CARE, CHAT, SAFE, APPT, PRIV, ADMIN, RES, A11Y, SEC.

Automate P0 tests with pytest/Vitest/Playwright.
Include:
- RBAC/ownership
- journal isolation
- chat grounded refs
- diagnosis/prescription refusal
- safety flow
- dependency
- provider disabled fallback
- appointment conflict
- export/delete
- suppression threshold
- admin KB versioning
- audit
- research isolation
- a11y smoke
- rate limit / XSS / secret scan

Generate QA_REPORT.md mapping test IDs -> PASS/FAIL/evidence.
