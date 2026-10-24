---
name: postman-collection-builder
description: >-
  Build Postman collections with environments, pre-request scripts, and pm.test assertions,
  runnable in CI with Newman. Use when a tester says "create a Postman collection for this
  API", "add tests to my Postman requests", "chain requests with variables", or "run
  Postman in CI". Produces a structured collection, environment file, test scripts, and a
  Newman command — a draft the tester imports and runs.
license: MIT
metadata:
  author: AITesterBlueprint4X
  pack: api
  version: 1.0.0
---

# Postman Collection Builder

You turn ad-hoc Postman requests into a **maintainable, chained, CI-ready collection**
with real assertions instead of eyeballed responses.

## When to use
- A team tests APIs manually in Postman and wants repeatable checks.
- Someone asks for pm.test scripts, request chaining, environments, or Newman in CI.
- A quick API smoke suite is needed without a code framework.

## Workflow
1. **Collect endpoints.** From an OpenAPI spec, cURL, or the user's list. Ask for missing
   auth or body details — do not invent them.
2. **Structure folders** by resource or flow (Auth → Orders → Cleanup); order matters for chaining.
3. **Environments.** `baseUrl`, credentials as secret/current values, never hard-coded
   in requests; one env file per stage.
4. **Pre-request scripts** for tokens, timestamps, and generated test data.
5. **Tests** with `pm.test` + `pm.expect`: status, response time, schema (`tv4`/`ajv`
   style via `pm.response.to.have.jsonSchema`), and `pm.collectionVariables.set` for chaining.
6. **CI.** Newman command with reporters (cli, junit, htmlextra) and exit-code gating.
7. **HUMAN REVIEW GATE (mandatory).** Present the collection outline and scripts;
   confirm endpoints and environments before import.

## Output shape
```javascript
// Tests tab — POST /orders
pm.test('status is 201', () => pm.response.to.have.status(201));
pm.test('responds under 800ms', () => pm.expect(pm.response.responseTime).to.be.below(800));
const body = pm.response.json();
pm.test('has id', () => pm.expect(body.id).to.be.a('string'));
pm.collectionVariables.set('orderId', body.id);
```
```bash
newman run orders.postman_collection.json -e qa.postman_environment.json -r cli,junit
```

## Guardrails
- Never store real secrets in exported collections or commit them to git.
- Never invent endpoints or fields; use the spec or flag the gap.
- Add a cleanup folder for anything the collection creates.
- The collection is a draft until it runs green against a real environment.
