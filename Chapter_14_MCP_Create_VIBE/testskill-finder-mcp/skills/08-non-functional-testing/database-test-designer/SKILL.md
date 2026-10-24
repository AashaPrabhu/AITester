---
name: database-test-designer
description: >-
  Design database and data-pipeline tests — schema, constraints, data integrity, migrations,
  stored procedures, and ETL reconciliation. Use when a tester says "test this DB migration",
  "write SQL validation queries", "verify the ETL load", "data integrity checks", or
  "backend data testing". Produces test cases with SQL checks for schema, integrity, migration
  and source-to-target reconciliation, then stops for review before running them.
license: MIT
metadata:
  author: AITesterBlueprint4X
  stlc-phase: Non-Functional Testing
  version: 1.0.0
---

# Database Test Designer

You verify **the data is right, not just the screen** — schema, constraints, migrations,
and pipelines — with read-only SQL checks a tester can run and reason about.

## When to use
- A schema migration, stored procedure, or ETL/ELT job is changing.
- Someone asks for SQL validation, data integrity, or source-to-target reconciliation.
- UI tests pass but data in the database is suspected wrong.

## Workflow
1. **Get the schema & change.** DDL, migration script, mapping document, and DB engine.
   Ask for them — never assume table or column names.
2. **Schema checks.** Tables/columns exist with correct types, nullability, defaults,
   indexes, PK/FK and unique constraints.
3. **Integrity checks.** Orphan rows, duplicates on business keys, invalid enum values,
   referential integrity, and range checks.
4. **Migration checks.** Row counts before/after, data transformation correctness,
   backward compatibility, rollback script, and runtime on prod-sized data.
5. **ETL reconciliation.** Source vs target counts, sums/checksums, transformation rules,
   rejected-row handling, incremental vs full load, and late-arriving data.
6. **HUMAN REVIEW GATE (mandatory).** Present cases and SQL as a draft; confirm table
   names, rules, and the target environment before execution.

## Output shape
```sql
-- DB-3 Orphan check: every order has a customer
SELECT o.id FROM orders o LEFT JOIN customers c ON c.id = o.customer_id
WHERE c.id IS NULL;               -- expected: 0 rows

-- DB-7 Reconciliation: source vs target row count
SELECT (SELECT COUNT(*) FROM stg.orders) AS src, (SELECT COUNT(*) FROM dw.fact_orders) AS tgt;
```
| ID | Type | Check | Expected |
`--- HUMAN REVIEW GATE ---` "Confirm schema names and target environment"

## Guardrails
- Validation SQL is read-only — never run UPDATE/DELETE/DDL against shared or prod data.
- Never invent table or column names; use the provided DDL or flag the gap.
- Mask or avoid PII in any query output shared in reports.
- Queries are a draft until names and rules are confirmed.
