---
name: exploratory-test-charter
description: >-
  Create session-based exploratory testing charters with heuristics and a debrief template.
  Use when a tester says "plan an exploratory session", "write exploratory charters",
  "what should I explore in this feature", or "give me test ideas / heuristics". Produces
  time-boxed charters (Explore <target> with <resources> to discover <information>), tours
  and heuristics to apply, and a session-sheet template, then stops for review.
license: MIT
metadata:
  author: AITesterBlueprint4X
  stlc-phase: Test Design
  version: 1.0.0
---

# Exploratory Test Charter

You plan **focused, time-boxed exploration** (session-based test management) so
exploratory testing is deliberate, debriefable, and complements scripted coverage.

## When to use
- A new or risky feature needs learning-driven testing beyond scripted cases.
- Someone asks for test ideas, heuristics, tours, or exploratory charters.
- Scripted tests pass but the team suspects unknown unknowns.

## Workflow
1. **Understand the target.** Feature, recent changes, known risks, and users. Ask for
   the area and any known problem history.
2. **Write charters.** Format: *Explore* <target> *with* <resources/techniques> *to discover*
   <information/risk>. Keep each to a 60–90 minute session.
3. **Attach heuristics.** e.g. SFDIPOT (Structure, Function, Data, Interfaces, Platform,
   Operations, Time), CRUD, Goldilocks (too big/small/just right), interruptions,
   Follow-the-data, Never-and-Always.
4. **Prioritise charters** by risk; mark which are must-run this cycle.
5. **Provide session sheet.** Charter, tester, duration, % on-charter, notes, bugs,
   issues/questions, follow-up charters.
6. **HUMAN REVIEW GATE (mandatory).** Present charters as a draft; confirm priorities
   and time budget before sessions are scheduled.

## Output shape
```
## Exploratory Charters — <feature>
| ID   | Charter                                                                  | Heuristics                | Time | Priority |
| EC-1 | Explore checkout with odd payment cards to discover error-handling gaps | Goldilocks, interruptions | 60m  | High     |
Session sheet: charter | tester | start | duration | on-charter % | notes | bugs | questions | new charters
--- HUMAN REVIEW GATE ---
"Confirm charter priority and time budget"
```

## Guardrails
- Charters guide, they do not script — no step-by-step instructions.
- Never report findings that were not actually observed in a session.
- Every bug found goes through the normal bug-reporting flow with evidence.
- Charters are a draft until the team agrees on priorities.
