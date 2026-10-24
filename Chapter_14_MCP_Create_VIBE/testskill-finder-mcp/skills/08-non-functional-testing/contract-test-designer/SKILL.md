---
name: contract-test-designer
description: >-
  Design consumer-driven contract tests between services (Pact or similar). Use when an
  SDET says "add contract tests between these services", "write a Pact test", "stop
  breaking the API for the mobile app", or "provider verification is failing". Produces
  consumer expectations, provider states, Pact consumer test skeletons, and broker/CI
  verification steps, then stops for review by both consumer and provider teams.
license: MIT
metadata:
  author: AITesterBlueprint4X
  stlc-phase: Non-Functional Testing
  version: 1.0.0
---

# Contract Test Designer

You make **API compatibility a test, not a meeting** — each consumer states exactly what
it relies on, and the provider proves it still delivers before deploying.

## When to use
- Microservices or front-end/back-end teams break each other with API changes.
- Someone asks for Pact / Spring Cloud Contract / consumer-driven contracts.
- E2E tests are too slow to catch integration breakage.

## Workflow
1. **Identify the pair.** Consumer, provider, and the interactions the consumer actually
   uses. Ask for real request/response examples — do not invent fields.
2. **Write consumer expectations.** Only the fields the consumer reads; use matchers
   (type, regex, eachLike) instead of exact values.
3. **Define provider states.** e.g. "order 42 exists", "user has no orders" — named,
   reusable, and set up by the provider's state handlers.
4. **Generate consumer test skeleton** that runs against the Pact mock server and
   publishes the pact.
5. **Provider verification & CI.** Broker publishing, `can-i-deploy` gate, versioning/tags
   or branches, and webhook to trigger provider builds.
6. **HUMAN REVIEW GATE (mandatory).** Present the contract draft; confirm with both teams
   before it becomes a deployment gate.

## Output shape
```typescript
const provider = new PactV3({ consumer: 'web-app', provider: 'orders-api' });
provider
  .given('order 42 exists')
  .uponReceiving('a request for order 42')
  .withRequest({ method: 'GET', path: '/orders/42' })
  .willRespondWith({ status: 200, body: { id: like('42'), status: regex('open|closed', 'open') } });
```
CI: publish pact → provider verifies → `can-i-deploy` gate
`--- HUMAN REVIEW GATE ---` "Confirm with consumer and provider teams"

## Guardrails
- Contracts capture what the consumer uses, not the provider's whole schema.
- Never invent fields or status codes; derive them from real traffic or the consumer code.
- Contract tests do not replace functional tests of the provider's business logic.
- The contract is a draft until both teams agree.
