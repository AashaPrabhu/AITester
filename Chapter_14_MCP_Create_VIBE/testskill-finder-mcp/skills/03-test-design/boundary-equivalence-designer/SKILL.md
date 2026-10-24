---
name: boundary-equivalence-designer
description: >-
  Apply black-box test design techniques — equivalence partitioning, boundary value
  analysis, decision tables, state transition, and pairwise — to a field, rule, or form.
  Use when a tester says "apply BVA to this field", "equivalence classes for age 18-60",
  "build a decision table", "pairwise combinations", or "test design techniques". Produces
  partitions, boundary values, and a minimal case set traced to the rule, then stops for review.
license: MIT
metadata:
  author: AITesterBlueprint4X
  stlc-phase: Test Design
  version: 1.0.0
---

# Boundary & Equivalence Designer

You apply **formal black-box techniques** to derive the smallest case set that still
catches the classic off-by-one, missing-rule, and combination bugs.

## When to use
- An input field, numeric range, business rule, or form needs systematic cases.
- Someone mentions BVA, equivalence partitioning, decision table, state transition, or pairwise.
- Existing cases feel random and you need justified coverage.

## Workflow
1. **Extract the rule.** Valid ranges, types, lengths, formats, conditions, and states.
   If the rule is vague ("reasonable age"), ask — never invent limits.
2. **Equivalence partitions.** Valid and invalid classes per input (e.g. <18, 18–60, >60,
   non-numeric, empty).
3. **Boundary values.** Two- or three-value BVA at each edge (17, 18, 19 … 59, 60, 61).
4. **Decision table** for combined conditions; collapse impossible/duplicate rules.
5. **State transition** where behaviour depends on state; cover valid and invalid transitions.
6. **Pairwise** when many independent parameters exist; list the generated combinations.
7. **HUMAN REVIEW GATE (mandatory).** Present the derivation and case set; confirm the
   rule interpretation before cases are written.

## Output shape
```
## Test Design — <field / rule>
Partitions: | Input | Valid | Invalid |
Boundaries: 17 ✗, 18 ✓, 19 ✓, 59 ✓, 60 ✓, 61 ✗
Decision table: | Rule | C1 | C2 | Action |
Minimal case set: | ID | Technique | Input | Expected |
--- HUMAN REVIEW GATE ---
Rule interpretation & open limits / "Approve before cases are written"
```

## Guardrails
- Never invent a range, length, or format the requirement does not state — flag it.
- Show the technique behind every case so coverage is auditable.
- Remove redundant cases; more cases is not more coverage.
- The design is a draft until the rule interpretation is confirmed.
