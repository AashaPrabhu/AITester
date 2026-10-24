---
name: test-estimation-helper
description: >-
  Estimate testing effort for a feature, release, or project. Use when a QA lead says
  "how long will testing take", "estimate test effort for this sprint", "give me a QA
  estimate", or needs numbers for a test plan. Produces a work-breakdown estimate using
  three-point (PERT) ranges per activity, with assumptions and contingency stated, then
  stops for review before the estimate is committed.
license: MIT
metadata:
  author: AITesterBlueprint4X
  stlc-phase: Test Planning
  version: 1.0.0
---

# Test Estimation Helper

You produce a **defensible range, not a single magic number**, for test effort —
built bottom-up from activities, with every assumption visible.

## When to use
- A test plan, sprint, or release needs QA effort numbers.
- Someone asks "how many days of testing" or "how many testers do we need".
- An estimate must be re-baselined after scope change.

## Workflow
1. **Confirm scope.** Features/stories in scope, platforms, test types, and team size.
   Ask — do not assume velocity or headcount.
2. **Break down work (WBS).** Analysis, design, test-case writing, data/env setup,
   automation, execution cycles (incl. regression), defect retest, reporting.
3. **Three-point estimate each item.** Optimistic (O), most likely (M), pessimistic (P);
   expected = (O + 4M + P) / 6; standard deviation = (P − O) / 6.
4. **Add cycles & overhead.** Number of test cycles, expected defect re-test load,
   meetings, environment downtime.
5. **Contingency.** Add a stated buffer (e.g. +1 σ total) tied to named risks.
6. **HUMAN REVIEW GATE (mandatory).** Present as a range with assumptions; ask for
   confirmation before it is communicated as a commitment.

## Output shape
```
## Test Estimate — <scope>
| Activity    | O | M | P | Expected (d) | σ   |
| Test design | 1 | 2 | 4 | 2.2          | 0.5 |
...
Total expected: X d | Range (±1σ): A–B d | Contingency: +Y d (reasons)
Assumptions: team of N, env ready by <date?>, 2 regression cycles
--- HUMAN REVIEW GATE ---
"Confirm assumptions before this becomes a commitment"
```

## Guardrails
- Never present a single-point estimate without the range and assumptions.
- Do not invent team velocity or historical data; use the user's numbers or flag the gap.
- Re-estimate when scope changes instead of stretching the old number.
- The estimate is a draft until the team agrees.
