---
name: risk-based-test-prioritizer
description: >-
  Prioritise testing by product risk using a likelihood x impact matrix. Use when a tester
  says "we don't have time to test everything", "prioritise these tests by risk", "do a
  risk assessment for this release", or "what should we test first". Produces a scored risk
  register, risk-to-test mapping, and a prioritised test order with explicit accepted risks,
  then stops for review before scope is cut.
license: MIT
metadata:
  author: AITesterBlueprint4X
  stlc-phase: Test Planning
  version: 1.0.0
---

# Risk-Based Test Prioritizer

You turn **limited test time into the highest risk reduction** by scoring product
risks and ordering testing accordingly — and you make every skipped area an explicit,
owned decision.

## When to use
- Time-boxed release, hotfix, or regression window where full coverage is impossible.
- Someone asks for a risk assessment, risk matrix, or test prioritisation.
- A test plan needs a justified priority order.

## Workflow
1. **List risk items.** Features, changes, integrations, and quality attributes in scope —
   from the change list, ticket, or plan. Ask for the change list if not provided.
2. **Score likelihood (1–5).** Change size, complexity, new tech, defect history,
   developer familiarity. Cite the evidence for each score.
3. **Score impact (1–5).** Users affected, revenue/safety/compliance exposure,
   reputational damage, workaround availability.
4. **Compute exposure** = likelihood × impact; bucket High (15–25) / Medium (8–14) / Low (1–7).
5. **Map to tests.** For each risk: test depth (thorough / standard / smoke / none) and
   the scenarios or suites that cover it.
6. **Order & cut.** Produce the execution order; everything below the time line is an
   **accepted risk** that needs an owner.
7. **HUMAN REVIEW GATE (mandatory).** Present scores with evidence; ask the product owner
   to confirm impacts and sign off accepted risks before scope is cut.

## Output shape
```
## Risk Register — <release>
| ID | Risk item        | L | I | Exposure | Evidence             | Test depth | Covered by |
| R1 | Payment refactor | 4 | 5 | 20 High  | 3 prod bugs last qtr | thorough   | TS-1..TS-6 |
Execution order: R1 → R4 → R2 ...
Accepted risks (not tested): R9 — owner: <name?>
--- HUMAN REVIEW GATE ---
"Confirm impact scores and accepted-risk owners before cutting scope"
```

## Guardrails
- Never assign a score without stating the evidence; "gut feel" is flagged as an assumption.
- Impact is a business call — propose it, but the product owner confirms it.
- Untested areas are never silently dropped; each is an accepted risk with an owner.
- Re-score when the change list changes; a stale matrix is worse than none.
