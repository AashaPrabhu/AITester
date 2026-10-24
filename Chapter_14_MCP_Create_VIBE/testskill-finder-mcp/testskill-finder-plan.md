# Test Skill Finder MCP — Plan

## 1. Goal

Build a **FastMCP** server that lets any MCP-capable LLM client (Claude, Copilot, Cursor,
MCP Inspector, …) **discover, search, read and apply QA/testing Agent Skills** by keyword.

- "playwright" → all `pw-*` skills
- "playwright api" → `pw-api-tester` first, then `api-test-designer`
- "test case creator" → `test-case-writer`
- "test plan creator" → `test-plan-generator`
- "bug strategy" / "test strategy" → `bug-reporter`, `bug-triage-assistant`, `test-strategy-builder`, …

**Source of truth:** the local `skills/` folder. Every tool, resource and prompt is
derived from the `SKILL.md` files on disk — no hard-coded skill list in the server.
Drop a new skill folder in, call `reload_skills` (or restart), and it is searchable.

## 2. Skill source

| Source | Count | Notes |
|---|---|---|
| github.com/PramodDutta/skillmasterclass → `skillmasterclass/skills` | 36 | 14 STLC-phase skills + Playwright pack (11) + Selenium pack (11). Copied as-is, folder layout preserved. |
| New skills written for this MCP (same format) | 17 | Fill gaps: test strategy, non-functional, BDD, contract, mobile, API/perf/Cypress packs, AI-quality, test-code review. |
| **Total** | **53** | Requirement: ≥ 50 |

### 2.1 Skill format (kept identical to upstream)

```
skills/<category>/<skill-name>/SKILL.md      # YAML frontmatter + markdown body
skills/<category>/<skill-name>/references/*  # optional supporting files
skills/<category>/<skill-name>/scripts/*     # optional
```

Frontmatter: `name`, `description` (with "Use when …" trigger phrases), `license`,
`metadata.{author, stlc-phase | pack, version}`.
Body sections: `# Title`, `## When to use`, `## Workflow` (ending in a HUMAN REVIEW GATE),
`## Output shape`, `## Guardrails`.

### 2.2 New skills (17)

| Folder | Skill | Purpose |
|---|---|---|
| `02-test-planning/` | `test-strategy-builder` | Org/project-level test strategy (levels, types, tools, environments, risks) |
| `02-test-planning/` | `risk-based-test-prioritizer` | Likelihood × impact risk matrix → test priority |
| `02-test-planning/` | `test-estimation-helper` | Effort estimation (WBS / 3-point) for a test scope |
| `03-test-design/` | `bdd-scenario-writer` | Gherkin Given/When/Then feature files from stories |
| `03-test-design/` | `exploratory-test-charter` | Session-based exploratory charters + heuristics |
| `03-test-design/` | `boundary-equivalence-designer` | BVA / equivalence partitioning / decision tables |
| `08-non-functional-testing/` | `performance-test-planner` | Load/stress/soak plan, SLOs, workload model |
| `08-non-functional-testing/` | `security-test-designer` | OWASP Top 10 / ASVS-based security test cases |
| `08-non-functional-testing/` | `mobile-test-designer` | Device matrix, gestures, interruptions, offline |
| `08-non-functional-testing/` | `contract-test-designer` | Consumer-driven contracts (Pact) |
| `08-non-functional-testing/` | `database-test-designer` | Schema, integrity, migration and ETL checks |
| `framework-packs/api-pack/` | `restassured-api-tester` | Java REST Assured API tests |
| `framework-packs/api-pack/` | `postman-collection-builder` | Postman/Newman collections with test scripts |
| `framework-packs/api-pack/` | `k6-load-script-generator` | k6 load scripts with thresholds |
| `framework-packs/cypress-pack/` | `cypress-test-generator` | Cypress E2E specs |
| `09-ai-quality/` | `llm-output-evaluator` | Test LLM/AI features: rubric, golden set, hallucination checks |
| `09-ai-quality/` | `test-automation-code-reviewer` | Review automation code for flakiness, weak assertions, design smells |

## 3. Architecture

```
testskill-finder-mcp/
├── testskill-finder-plan.md      ← this file
├── pyproject.toml                ← uv project (fastmcp, pyyaml, pytest)
├── README.md                     ← how to run + connect
├── skills/                       ← SOURCE OF TRUTH (53 skills)
├── src/testskill_finder/
│   ├── registry.py               ← scan + parse SKILL.md, build search index
│   ├── search.py                 ← keyword scoring, synonyms, fuzzy matching
│   └── server.py                 ← FastMCP tools / resources / prompts + CLI
├── scripts/sync_skills.py        ← re-download upstream skills from GitHub
└── tests/test_server.py          ← in-memory FastMCP Client tests
```

### 3.1 Registry
- Recursively find every `SKILL.md` under `skills/`.
- Parse YAML frontmatter (PyYAML) + split body into `##` sections.
- Derive `category` (top-level folder, e.g. `05-test-execution`), `pack` (`playwright`, `selenium`, …),
  `stlc_phase`, `supporting_files` (references/scripts/copilot).
- Skip & report malformed skills instead of crashing.

### 3.2 Search
- Tokenise query; lowercase; strip stop-words.
- **Synonym expansion** (QA vocabulary): `playwright→pw`, `selenium→se`, `bug→defect`,
  `creator/create/write→writer/generator`, `plan→planning`, `strategy`, `api→endpoint/rest`,
  `flaky→flake`, `perf→performance/load`, `a11y→accessibility`, `gherkin→bdd`, …
- Weighted field scoring: name (×6), pack/category (×4), description (×3), headings (×2), body (×1).
- Phrase bonus when the whole query appears in name/description; all-terms-matched bonus.
- Fuzzy fallback with `difflib` for typos ("playwrite", "selinium").
- Returns ranked results with score + matched terms (explainable).

## 4. MCP surface

### 4.1 Tools
| Tool | Purpose |
|---|---|
| `search_skills(query, limit, category?, pack?)` | Ranked keyword search — the main entry point |
| `find_best_skill(task)` | Single best skill for a natural-language task + runners-up |
| `get_skill(name)` | Full SKILL.md content + metadata |
| `get_skill_section(name, section)` | Just "Workflow", "Guardrails", "Output shape", … |
| `list_skills(category?, pack?)` | Browse catalog |
| `list_categories()` | Categories / packs with counts |
| `get_related_skills(name)` | Same category/pack + STLC upstream/downstream hand-offs |
| `get_stlc_workflow()` | Skills grouped in STLC order (requirement → closure) |
| `list_skill_files(name)` / `get_skill_file(name, path)` | Supporting references/scripts (path-traversal safe) |
| `install_skill(name, destination_dir, overwrite=False)` | Copy a skill folder into e.g. `~/.claude/skills` |
| `reload_skills()` | Rescan the `skills/` folder (source of truth) |
| `skill_stats()` | Totals per category/pack, load errors |

### 4.2 Resources
| URI | Content |
|---|---|
| `skills://catalog` | JSON catalog of all skills |
| `skills://categories` | JSON categories + counts |
| `skills://stlc-workflow` | Markdown STLC map |
| `skill://{name}` (template) | Raw SKILL.md |
| `skill://{name}/metadata` (template) | JSON metadata |
| `skills://category/{category}` (template) | JSON list for a category |

### 4.3 Prompts
| Prompt | Use |
|---|---|
| `use_skill(skill_name, task)` | Injects the skill's instructions + the user's task |
| `find_skill_for_task(task)` | Guides the LLM to search → pick → apply |
| `stlc_pipeline(feature)` | Walks a feature through all STLC phase skills |
| `compare_skills(skill_a, skill_b)` | Side-by-side to choose between two skills |

## 5. Transports
- **Streamable HTTP** (default for Inspector): `http://127.0.0.1:8000/mcp`
- **stdio** for desktop clients: `uv run testskill-finder --transport stdio`

## 6. Test plan (verification)

| # | Check | Expected |
|---|---|---|
| T1 | Skill count | ≥ 50 skills load, 0 load errors |
| T2 | Format | Every skill has name == folder name, description, the 4 standard sections |
| T3 | `search_skills("playwright")` | Top results all `pw-*` |
| T4 | `search_skills("playwright api")` | `pw-api-tester` ranked #1 |
| T5 | `search_skills("test case creator")` | `test-case-writer` #1 |
| T6 | `search_skills("test plan creator")` | `test-plan-generator` #1 |
| T7 | `search_skills("test strategy")` | `test-strategy-builder` #1 |
| T8 | `search_skills("bug")` | bug-reporter / bug-triage / rca in top results |
| T9 | Typo `"selinium"` | Selenium skills returned |
| T10 | `get_skill` unknown name | Clear error with suggestions |
| T11 | `get_skill_file` with `../` | Rejected |
| T12 | Resources + prompts | Listed and readable via Client |
| T13 | HTTP transport | Server starts, `/mcp` reachable from MCP Inspector |

Automated via `uv run pytest` using FastMCP's in-memory `Client`.

## 7. Out of scope / risks
- Upstream skills are copied, not auto-synced; `scripts/sync_skills.py` refreshes on demand.
- Keyword search (no embeddings) keeps it dependency-light and deterministic; synonyms cover QA jargon.
- `install_skill` writes to disk — only to the explicit destination given, never overwrites by default.

## 8. Status

- [x] Plan written
- [x] 36 upstream skills downloaded + 17 new skills authored → **53 skills**, 0 load errors
- [x] FastMCP 4.1 server: 13 tools, 3 resources + 3 resource templates, 4 prompts
- [x] `uv run pytest` → 23 passed (T1–T12)
- [x] T13: server reachable over Streamable HTTP at `http://127.0.0.1:8000/mcp`
