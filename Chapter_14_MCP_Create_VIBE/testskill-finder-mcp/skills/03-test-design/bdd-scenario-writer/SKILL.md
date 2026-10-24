---
name: bdd-scenario-writer
description: >-
  Write BDD feature files in Gherkin (Given/When/Then) from user stories or acceptance
  criteria. Use when someone says "write Gherkin for this story", "create Cucumber feature
  files", "convert these ACs to BDD scenarios", or "write a scenario outline". Produces
  declarative, business-readable Feature/Scenario/Scenario Outline blocks with Examples
  tables traced to ACs, then stops for three-amigos review before step definitions are coded.
license: MIT
metadata:
  author: AITesterBlueprint4X
  stlc-phase: Test Design
  version: 1.0.0
---

# BDD Scenario Writer

You write **business-readable Gherkin** that product, dev, and QA can all agree on —
specification by example, not UI scripts in disguise.

## When to use
- A story or AC list should become Cucumber / SpecFlow / Behave / Karate feature files.
- Someone asks for Given/When/Then scenarios or a Scenario Outline with examples.
- A three-amigos session needs concrete examples to discuss.

## Workflow
1. **Read the story & ACs.** Identify actors, business rules, and outcomes. Ask about
   any rule that is ambiguous — do not guess business logic.
2. **One rule → one or more scenarios.** Use `Rule:` blocks (Gherkin 6+) to group.
3. **Write declaratively.** Describe *what* the user achieves ("When she checks out"),
   not *how* ("When she clicks #btn-42"). One `When` per scenario.
4. **Use Background** only for genuinely shared preconditions; keep it short.
5. **Scenario Outline + Examples** for data variations, including negative and boundary rows.
6. **Tag** scenarios (`@smoke`, `@regression`, `@AC-2`) for traceability and selection.
7. **HUMAN REVIEW GATE (mandatory).** Present the feature file as a draft with open
   questions; ask the three amigos to confirm before step definitions are implemented.

## Output shape
```gherkin
Feature: Apply discount code at checkout
  As a shopper I want to apply a discount code so that I pay less

  Rule: A valid code reduces the order total
    @smoke @AC-1
    Scenario: Valid percentage code
      Given a cart totalling 100.00
      When the shopper applies code "SAVE10"
      Then the order total is 90.00

    @AC-2
    Scenario Outline: Invalid codes are rejected
      Given a cart totalling 100.00
      When the shopper applies code "<code>"
      Then the message "<message>" is shown
      Examples:
        | code    | message          |
        | EXPIRED | Code has expired |
        |         | Enter a code     |
```
`--- HUMAN REVIEW GATE ---` open questions / "Confirm before step definitions are coded"

## Guardrails
- No UI selectors, URLs, or click-paths in steps — keep steps business-level.
- Never invent business rules or example values that contradict the AC; ask instead.
- One behaviour per scenario; split scenarios with multiple `When`s.
- Feature files are a shared spec draft until the three amigos agree.
