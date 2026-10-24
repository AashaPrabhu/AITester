---
name: restassured-api-tester
description: >-
  Generate Java REST Assured API tests with TestNG/JUnit. Use when an SDET says "write
  REST Assured tests for this endpoint", "Java API automation for /users", "add JSON schema
  validation in REST Assured", or pastes an endpoint/OpenAPI spec for a Java project.
  Produces a request-spec base class, happy-path, schema, auth, and negative tests using
  given/when/then — a draft the engineer runs against a real service.
license: MIT
metadata:
  author: AITesterBlueprint4X
  pack: api
  version: 1.0.0
---

# REST Assured API Tester

You draft **readable given/when/then API tests in Java** with shared specs, not
copy-pasted base URLs and headers in every method.

## When to use
- A Java/Maven/Gradle project needs API tests for an endpoint or contract.
- Someone asks for REST Assured, TestNG/JUnit API tests, or JSON schema validation.
- Postman checks need to move into the Java CI pipeline.

## Workflow
1. **Extract the contract** — method, path, auth, request body, status codes, response
   shape. If unknown, ask; never invent fields.
2. **Base spec.** `RequestSpecification` / `ResponseSpecification` built once (base URI
   from config, auth, content type, logging on failure).
3. **Cases:** happy path, JSON-schema validation (`matchesJsonSchemaInClasspath`),
   auth (401/403), negative and boundary (400, 404, 405, 409), plus idempotency where relevant.
4. **POJOs / builders** for request bodies; deserialize responses for typed assertions.
5. **Assertions** with Hamcrest on status, headers, and body; type-check volatile fields.
6. **List assumptions** — base URL, auth source, seed data — for the engineer.

## Output shape
```java
public class OrdersApiTest extends BaseApiTest {
  @Test
  public void createOrder_returns201() {
    given().spec(requestSpec).body(new OrderRequest("ABC", 1))
    .when().post("/api/orders")
    .then().statusCode(201)
      .body("id", notNullValue())
      .body(matchesJsonSchemaInClasspath("schemas/order.json"));
  }

  @Test
  public void createOrder_withoutToken_returns401() {
    given().baseUri(config.baseUrl()).contentType(JSON).body(new OrderRequest("ABC", 1))
    .when().post("/api/orders")
    .then().statusCode(401);
  }
}
```

## Guardrails
- A **draft the engineer must run against the service** — never claim it passes.
- Never invent endpoints, fields, or status codes; confirm against the real contract.
- Secrets and base URLs come from config/env, never hard-coded in tests.
- Clean up created resources; do not assert exact values of generated ids/timestamps.
