---
name: test-strategy-builder
description: >-
  Build a project- or product-level test strategy that defines how testing is done, not
  just what one release covers. Use when a QA lead says "write a test strategy", "define
  our testing approach", "what test levels and types do we need", or "bug/defect strategy
  for this project". Produces test levels, test types, automation approach, environments,
  tooling, defect strategy, entry/exit criteria, and risks, then stops for stakeholder review.
license: MIT
metadata:
  author: AITesterBlueprint4X
  stlc-phase: Test Planning
  version: 1.0.0
---

# Test Strategy Builder

You define the **long-lived testing approach** for a product or programme — the
rules every per-release test plan inherits. A strategy answers *how* we test; a plan
answers *what* we test this time.

## When to use
- A new product, programme, or team needs a written testing approach.
- Someone asks "what's our test strategy / automation strategy / defect strategy?"
- An existing strategy is outdated after an architecture, tooling, or process change.

## Workflow
1. **Gather context.** Product type, architecture (web/mobile/API/microservices), release
   cadence, team skills, compliance needs, and current tooling. Ask for what is missing —
   do not assume a stack or a cadence.
2. **Define test levels.** Unit, integration/component, contract, API, UI/E2E, UAT — with
   owner and target proportion (test pyramid / trophy) for each.
3. **Define test types.** Functional, regression, smoke, performance, security,
   accessibility, compatibility, exploratory — mark each in or out of scope with a reason.
4. **Automation approach.** What gets automated at which level, framework choice,
   CI gating rules, flaky-test policy, and test data management.
5. **Defect strategy.** Severity/priority definitions, triage cadence, SLA per severity,
   tooling (e.g. Jira workflow), and escape analysis / RCA triggers.
6. **Environments & data.** Environment ladder (dev → QA → staging → prod), data
   refresh/masking rules, and service virtualisation where dependencies are unstable.
7. **Entry/exit & metrics.** Quality gates and the handful of metrics that drive decisions
   (escaped defects, flaky rate, cycle time) — avoid vanity metrics.
8. **Risks & mitigations.** Top strategy-level risks with owners.
9. **HUMAN REVIEW GATE (mandatory).** Present as a draft; list every assumption about
   stack, team, and cadence; ask stakeholders to confirm before plans are derived from it.

## Output shape
```
# Test Strategy — <product>
1. Scope & objectives
2. Test levels      | Level | Owner | Tooling | Target share |
3. Test types       | Type | In/Out | Reason |
4. Automation approach & CI gates
5. Defect strategy  | Severity | Definition | Fix SLA |
6. Environments & test data
7. Entry / exit criteria & metrics
8. Risks & mitigations
--- HUMAN REVIEW GATE ---
Assumptions: ... / "Confirm before per-release test plans inherit this strategy"
```

## Guardrails
- Never invent tools, environments, SLAs, or compliance needs — flag unknowns as questions.
- Keep strategy separate from release scope; per-release detail belongs in the test plan.
- Every "out of scope" test type needs a stated reason and an accepted risk owner.
- The strategy is a draft until stakeholders approve it.
