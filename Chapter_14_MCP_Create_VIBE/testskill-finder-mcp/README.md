# Test Skill Finder MCP

A [FastMCP](https://gofastmcp.com) server that lets any LLM client **find, read and apply
53 QA/testing Agent Skills** by keyword. The `skills/` folder is the source of truth.

- 36 skills from [PramodDutta/skillmasterclass](https://github.com/PramodDutta/skillmasterclass/tree/main/skillmasterclass/skills)
- 17 additional skills in the same format (strategy, risk, estimation, BDD, exploratory, BVA,
  performance, security, mobile, contract, database, REST Assured, Postman, k6, Cypress, LLM eval, test-code review)

See [testskill-finder-plan.md](testskill-finder-plan.md) for the design and test plan.

## Run

```bash
uv sync
uv run testskill-finder                      # stdio (default) — for clients that launch the server
uv run testskill-finder --transport http     # Streamable HTTP on http://127.0.0.1:8000/mcp
uv run testskill-finder --transport http --port 9000 --skills-dir D:/my/skills
```

## Connect with MCP Inspector

Let Inspector launch it over stdio. The `--` is required: without it Inspector
swallows `--transport` as its own option.
```bash
npx @modelcontextprotocol/inspector -- uv --directory "<path-to>/testskill-finder-mcp" run testskill-finder --transport stdio
```

Or start `uv run testskill-finder --transport http` yourself, then in Inspector choose
Transport **Streamable HTTP**, URL **`http://127.0.0.1:8000/mcp`** → Connect.

## Client config (Claude Desktop / Claude Code / VS Code)

```json
{
  "mcpServers": {
    "testskill-finder": { "type": "http", "url": "http://127.0.0.1:8000/mcp" }
  }
}
```
stdio variant: `"command": "uv", "args": ["--directory", "<path-to>/testskill-finder-mcp", "run", "testskill-finder", "--transport", "stdio"]`.
Claude Code: `claude mcp add --transport http testskill-finder http://127.0.0.1:8000/mcp`.

## What it exposes

| Tools | Resources | Prompts |
|---|---|---|
| `search_skills`, `find_best_skill`, `get_skill`, `get_skill_section`, `list_skills`, `list_categories`, `get_related_skills`, `get_stlc_workflow`, `list_skill_files`, `get_skill_file`, `install_skill`, `reload_skills`, `skill_stats` | `skills://catalog`, `skills://categories`, `skills://stlc-workflow`, `skill://{name}`, `skill://{name}/metadata`, `skills://category/{category}` | `use_skill`, `find_skill_for_task`, `stlc_pipeline`, `compare_skills` |

Example searches: `playwright`, `playwright api`, `test case creator`, `test plan creator`,
`test strategy`, `bug triage`, `selinium` (typos are handled).

## Add a skill

Create `skills/<category>/<skill-name>/SKILL.md` with the same frontmatter
(`name`, `description` with "Use when …", `license`, `metadata`) and the sections
`When to use` / `Workflow` / `Output shape` / `Guardrails`, then call the `reload_skills` tool.
Refresh upstream skills with `uv run python scripts/sync_skills.py`.

## Test

```bash
uv run pytest
```
