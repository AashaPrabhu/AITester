---
name: cypress-test-generator
description: >-
  Generate Cypress end-to-end and component tests in JavaScript/TypeScript. Use when an
  SDET says "write a Cypress test for login", "convert these cases to Cypress", "add
  cy.intercept for this API", or "create custom Cypress commands". Produces specs using
  data-cy selectors, cy.intercept for network control, cy.session for auth, and custom
  commands — a draft the engineer runs against the app.
license: MIT
metadata:
  author: AITesterBlueprint4X
  pack: cypress
  version: 1.0.0
---

# Cypress Test Generator

You draft **Cypress specs that respect Cypress's model** — chained commands, retry-able
assertions, no manual waits — instead of Selenium habits ported over.

## When to use
- Manual test cases or a user flow need Cypress automation.
- Someone asks for Cypress specs, cy.intercept stubs, cy.session login, or custom commands.
- An existing Cypress suite needs a new feature covered.

## Workflow
1. **Read the flow & app.** Steps, expected results, and available `data-cy` /
   `data-testid` attributes. If selectors are unknown, ask or propose attributes —
   do not invent CSS paths.
2. **Auth once** with `cy.session()` (UI or API login) instead of logging in per test.
3. **Control the network** with `cy.intercept()` — alias and `cy.wait('@alias')` on
   real calls; stub only for edge states (500s, empty lists).
4. **Assert with retry-ability** (`should`) — never `cy.wait(5000)`.
5. **Custom commands** for repeated domain actions in `cypress/support/commands`.
6. **Data & isolation.** Seed via API (`cy.request`) and clean up; tests independent.
7. **List assumptions** — baseUrl, selectors, seed data — for the engineer.

## Output shape
```javascript
describe('Checkout', () => {
  beforeEach(() => {
    cy.session('shopper', () => cy.loginByApi('shopper@test.dev'));
    cy.intercept('POST', '/api/orders').as('createOrder');
    cy.visit('/cart');
  });

  it('places an order', () => {
    cy.get('[data-cy=checkout]').click();
    cy.wait('@createOrder').its('response.statusCode').should('eq', 201);
    cy.get('[data-cy=order-confirmation]').should('be.visible');
  });
});
```

## Guardrails
- A draft the engineer must run — never claim it passes.
- No hard waits (`cy.wait(ms)`), no brittle CSS/XPath chains; prefer `data-cy`.
- Never invent selectors or endpoints; ask or propose test attributes.
- Keep secrets in `cypress.env.json`/CI env, not in specs.
