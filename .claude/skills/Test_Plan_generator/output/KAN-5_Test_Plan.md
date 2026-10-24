# Test Plan — KAN-5: Test plan creation

> Status: **DRAFT — pending human review.** Not approved until a QA owner signs off.

| Field | Value |
|-------|-------|
| Jira key | KAN-5 |
| Summary | Test plan creation |
| Issue type | Bug *(see Gap #3)* |
| Priority | Medium |
| Status | To Do |
| Reporter | aasha rani |
| Assignee | Unassigned |
| Components / Labels / Fix version | None |
| Linked issues / Attachments / Comments | None |
| Plan drafted | 2026-10-14 |

> ⚠️ **Read this first:** The body of KAN-5 is an **unfilled template**. The feature name (`[Feature Name]`),
> the in-scope components and the out-of-scope items are still placeholder text. This draft therefore
> plans testing **of the ticket's own deliverables** (the test-planning work and its acceptance criteria)
> and lays out a **testing strategy framework** for the release. Feature-level test scenarios **cannot be
> written** until the author fills in the placeholders. Nothing below was invented to fill those gaps.

---

## 1. Scope & Objectives

- **In scope (as written in the ticket):**
  - A formal Test Plan document, linked to KAN-5 or published in Confluence.
  - A high-level list of the test environments and test data the release needs.
  - A risk mitigation plan for likely testing blockers.
  - A definition of testing types: manual, automated, regression, E2E, integration and security
    (performance is named in the Background).
  - Placeholder Test Execution tickets, or Zephyr/Xray folders.
  - Stakeholder review and sign-off by the Product Manager and the Lead Developer.
- **In scope (feature under test):** ❌ **Not defined.** The ticket still reads "[List key components, e.g., the new
  payment gateway API, user profile UI updates]".
- **Out of scope:** ❌ **Not defined.** The ticket still reads "[e.g., Load testing for legacy modules not touched in this
  release]". Until this is filled in, the following are treated as out of scope:
  - Writing detailed test cases or automation scripts. The skill requires plan approval first.
  - Running any tests.
- **Objective:** KAN-5 counts as "tested" when each of its five acceptance criteria can be shown as met:
  1. The plan exists and is linked.
  2. Strategy and testing types are defined.
  3. Environments and data are identified.
  4. The PM and Lead Developer have approved it.
  5. Execution placeholders exist.

  Each criterion must also trace to the release's real feature scope, which is not known yet.

---

## 2. Gaps & Questions for the author

### 2a. Requirement checklist results

| Checklist item | Result | Note |
|---|---|---|
| Clear user story / goal | ⚠️ | The goal ("prepare a test plan") is clear, but the feature it serves is a placeholder |
| Acceptance criteria are testable | ⚠️ | AC1, AC4 and AC5 are observable. AC2 ("clearly defined") and AC3 ("identified") are subjective |
| Happy path described | ⚠️ | The sub-task flow (Draft → Env analysis → Review → Sign-off) is given. The feature's happy path is missing |
| Negative / error paths | ❌ | Nothing is said about what happens if review is rejected or the environment is unavailable |
| Boundary & empty states | ❌ | Not applicable until the feature is known |
| State transitions / workflow | ⚠️ | The sub-tasks are "Optional", and no Jira workflow states are tied to them |
| Required test data | ❌ | Requested as an output, but no data domains are hinted at |
| Environment / config / flags | ❌ | None named ("devices, browsers, or sandbox accounts" is generic) |
| External dependencies | ⚠️ | Zephyr/Xray and Confluence are mentioned, but which one is used is not confirmed |
| Preconditions / setup | ❌ | None stated |
| Performance / load | ⚠️ | Named as a requirement, but no targets (SLA, TPS, p95) are given |
| Security / authorization | ⚠️ | Named, with no roles, threat areas or compliance needs |
| Accessibility (a11y) | ❌ | Not mentioned |
| i18n / l10n | ❌ | Not mentioned |
| Audit / logging / observability | ❌ | Not mentioned |
| Regression surface | ⚠️ | "Regression" is listed as a test type, but the impacted modules are not |
| Backward compatibility / migration | ❌ | Not mentioned |
| Mobile / browser matrix | ⚠️ | "Devices, browsers" is mentioned, but no matrix is given |
| Rollback / feature-flag behavior | ❌ | Not mentioned |
| No ambiguous wording | ⚠️ | "comprehensive", "clearly defined", "potential testing blockers" |
| Terms defined consistently | ⚠️ | "Test Execution tickets" and "Zephyr/Xray folders" are offered as alternatives with no decision |
| Mockups / designs linked | ❌ | No attachments or links |

### 2b. Questions for the author

| # | Area | Finding (⚠️/❌) | Question to author |
|---|------|----------------|--------------------|
| 1 | Scope | ❌ `[Feature Name]` is a placeholder | What feature or release is this test plan for? Is there an epic, PRD or fix version to link? |
| 2 | Scope | ❌ In-scope and out-of-scope lists are placeholders | Which components, APIs and screens are changing? What is explicitly excluded? |
| 3 | Ticket hygiene | ⚠️ Issue type is **Bug** | Should this be a Task or Story? A test-planning activity filed as a Bug will distort defect metrics. |
| 4 | Ownership | ❌ Unassigned, no sprint or fix version | Who owns this, which sprint is it in, and what is the release date that "before development concludes" refers to? |
| 5 | Deliverable location | ⚠️ "Linked to Jira **or** Confluence" | Where should the approved plan live: a Confluence space, a Jira attachment, or the repo? |
| 6 | Tooling | ⚠️ "Test Execution tickets **or** Zephyr/Xray folders" | Which test-management tool is licensed on this Jira site? Is Zephyr or Xray actually installed? |
| 7 | Non-functional | ⚠️ Performance named, no targets | What are the performance targets (response time, throughput, concurrent users)? Is there a baseline? |
| 8 | Non-functional | ⚠️ Security named, no detail | What security scope applies: authn/authz roles, OWASP Top 10, PCI/PII, pen-test? |
| 9 | Non-functional | ❌ a11y, i18n and logging not mentioned | Are WCAG 2.x AA, localization or audit logging needed for this release? |
| 10 | Environments | ❌ None named | Which environments exist (Dev/QA/Staging/UAT)? Are there sandbox or third-party accounts? Who provisions them, and how long does that take? |
| 11 | Test data | ❌ None named | Can production-like data be used, or must it be synthetic or masked? Are there data privacy constraints? |
| 12 | Browser/device | ⚠️ Generic mention | What is the supported browser, OS and device matrix? |
| 13 | Approval | ⚠️ "PM and Lead Developer approved" | Who are the named PM and Lead Developer? How is approval recorded (Jira comment, Confluence page approval, sign-off field)? |
| 14 | Automation | ⚠️ "automated" listed | Which framework and CI pipeline will run the automated and regression suites? What coverage is expected? |
| 15 | Rollback | ❌ Not mentioned | Is the feature behind a feature flag? Does rollback need to be tested? |
| 16 | Exit quality bar | ❌ Not stated | What defect thresholds allow release (for example, 0 open P0/P1)? |

---

## 3. Test Scenarios

Feature-level scenarios are **blocked by Gaps #1 and #2**. The scenarios below verify KAN-5's own acceptance criteria
and deliverables. Each one traces to a stated AC, deliverable (D1–D3) or gap.

**Acceptance criteria referenced:**
- AC1: The plan is drafted and attached or linked.
- AC2: Scope, strategy and testing types are defined.
- AC3: Environments and test data are identified.
- AC4: The PM and Lead Developer have approved the plan.
- AC5: Execution placeholders are created.

| ID | Priority | Type | Scenario | Maps to |
|----|----------|------|----------|---------|
| TS-1 | P0 | Positive | The Test Plan document exists and is reachable from KAN-5 (attachment or link). Opening the link as a project member shows the document. | AC1, D1 |
| TS-2 | P0 | Negative | A user who is not a project member opens the linked plan. Access follows the intended visibility, with no broken link or permission wall for stakeholders. | AC1, Gap 5 |
| TS-3 | P0 | Positive | The plan names a real feature and lists in-scope and out-of-scope components. No `[placeholder]` text remains. | AC2, Gaps 1–2 |
| TS-4 | P0 | Positive | The plan defines each testing type (manual, automated, regression, E2E, integration, security, performance), with an owner and approach for each. | AC2, Sub-task 1 |
| TS-5 | P1 | Negative | A testing type named in the ticket (performance, security) has measurable targets in the plan, not just its name. The scenario fails if the targets are missing. | AC2, Gaps 7–8 |
| TS-6 | P0 | Positive | The plan lists each test environment with its purpose, its owner and whether it is available. | AC3, D2, Gap 10 |
| TS-7 | P1 | Positive | The plan lists required test data with its source (synthetic, masked or seeded) and a refresh method. | AC3, D2, Gap 11 |
| TS-8 | P1 | Boundary | The environment list covers the full browser/device matrix: at least the minimum and maximum supported versions and one mobile viewport. | AC3, Gap 12 |
| TS-9 | P0 | Positive | The risk mitigation plan lists at least one blocker for each area (environment, data, dependencies, schedule), each with an owner and a mitigation. | D3 |
| TS-10 | P0 | Positive | Approval from the PM and the Lead Developer is recorded and traceable (named approver and date). | AC4, Sub-task 3–4, Gap 13 |
| TS-11 | P1 | Negative | The review returns changes. The plan is revised, re-reviewed, and its version history shows the change. The ticket is not closed on a rejected plan. | AC4 |
| TS-12 | P1 | Negative | Only one of the two required approvers signs off. AC4 is treated as **not met** and the ticket cannot move to Done. | AC4 |
| TS-13 | P0 | Positive | Placeholder Test Execution tickets, or Zephyr/Xray folders, exist and are linked to KAN-5 or the release. | AC5, Gap 6 |
| TS-14 | P2 | Negative | Zephyr/Xray is not installed on the site. The fallback (Jira Test Execution issue type, or a sub-task convention) is documented and used consistently. | AC5, Gap 6 |
| TS-15 | P1 | Positive | Every scenario in the final plan traces back to an AC or a requirement. No orphaned scenarios. | AC2 |
| TS-16 | P2 | Positive | The issue type is corrected (Bug → Task or Story), and an assignee, sprint and fix version are set. | Gaps 3–4 |

### 3a. Release strategy framework (fill in once Gaps 1–2 are answered)

| Test level / type | Purpose | Default approach | Status |
|---|---|---|---|
| Smoke | The build is stable enough to test | Automated, runs on each deploy to QA | Ready to define |
| Functional (positive/negative/boundary) | Feature ACs are met | Manual first, then automated | ❌ Blocked: no feature ACs |
| Integration / API | Contracts between the changed components | Automated API tests | ❌ Blocked: components unknown |
| E2E | Critical user journeys | Automated UI tests on the browser matrix | ❌ Blocked: journeys unknown |
| Regression | No breakage in neighbouring modules | Automated suite in CI | ⚠️ Impacted modules unknown |
| Security | Authn/authz, input validation, OWASP | Scan plus targeted manual tests | ⚠️ Scope unknown (Gap 8) |
| Performance | Meets SLAs under expected load | Load test against targets | ⚠️ Targets unknown (Gap 7) |
| Accessibility / i18n | Compliance, if required | Automated a11y scan plus manual check | ❓ Not stated (Gap 9) |
| UAT | Business acceptance | PM-led | ⚠️ Owner unknown (Gap 13) |

---

## 4. Test Data & Environment

- **Data:** ❌ **Not specified in the ticket.** To be defined:
  - Data domains (users, accounts, transactions, and so on).
  - Volume for performance testing.
  - PII handling: masked or synthetic.
  - Seeding and reset scripts.
- **Environment / flags:** ❌ **Not specified.** For each environment (Dev / QA / Staging / UAT, for example), confirm:
  - The URL.
  - Its owner.
  - Its data-refresh cadence.
  - The feature flags in use.
  - Any third-party sandbox accounts.
- **Tooling referenced in the ticket:**
  - Jira (project KAN).
  - Confluence (plan location).
  - Zephyr or Xray (test management; still to be confirmed).
- **Roles / permissions:**
  - **Plan approval:** the Product Manager and the Lead Developer.
  - **Feature-level roles:** not defined, because the feature is unknown.

---

## 5. Risks & Assumptions

- **Assumptions made:**
  - KAN-5 is a meta-ticket: its deliverable is the plan, not product code.
  - The five ACs listed under "Definition of Done" are the full and authoritative acceptance criteria.
  - The optional sub-tasks reflect the intended workflow, even though they have not been created in Jira.
  - "Approved" means explicit, recorded approval from both named roles.
- **Risks:**

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|-----------|
| R1 | The feature scope stays undefined, so the plan cannot be finalized | High | High | Escalate Gaps 1–2 to the reporter and PM. Time-box the clarification. |
| R2 | Test environments are not provisioned before development ends | Medium | High | Raise environment requests now. Identify the provisioning owner and lead time (Gap 10). |
| R3 | Zephyr/Xray is not available, which blocks AC5 | Medium | Medium | Confirm licensing. Agree a fallback convention (TS-14). |
| R4 | Approvers are unavailable or disagree, which delays sign-off | Medium | Medium | Name the approvers and a review deadline. Book the review session early. |
| R5 | Non-functional targets are missing, so performance and security testing cannot pass or fail | High | Medium | Get numeric targets (Gaps 7–8) before strategy sign-off. |
| R6 | The issue is misclassified as a Bug and skews defect metrics | High | Low | Change the issue type (Gap 3). |
| R7 | Test data contains real PII | Low | High | Require masked or synthetic data. Have security review the data plan. |

---

## 6. Entry / Exit criteria

- **Entry (to start finalizing the plan):**
  - Gaps 1, 2, 4 and 13 are answered: feature, scope, owner and approvers known.
  - A requirements source exists: a PRD, epic, or stories with ACs.
  - Development timeline and release date are known.
- **Exit (KAN-5 can move to Done):**
  - TS-1 to TS-13 pass: all P0 and P1 scenarios above.
  - No `[placeholder]` text remains in the plan.
  - Approval is recorded from the PM and the Lead Developer.
  - Execution placeholders are created and linked.
  - All open questions are resolved, or explicitly accepted as risks by the approvers.

---

## HUMAN REVIEW GATE

- **I assumed:**
  - KAN-5's deliverable is the test plan itself.
  - The five DoD bullets are the complete acceptance criteria.
  - The optional sub-tasks show the intended workflow.
  - "Approved" means recorded approval from both the PM and the Lead Developer.
- **I could not confirm:**
  - The feature or release under test.
  - In-scope and out-of-scope components.
  - Environments and test data.
  - The test-management tool (Zephyr, Xray or neither).
  - Non-functional targets.
  - Approver names.
  - Release date.
  - Why the issue type is Bug.
- **Open questions blocking sign-off:** Gaps **#1, #2, #4, #6, #7, #8, #10, #11 and #13** (see Section 2b).
- ▶ **Approve, or edit, before I write test cases / automation.** Once the placeholders in KAN-5 are filled in,
  I can extend Section 3 with feature-level positive, negative, boundary and role-based scenarios.
