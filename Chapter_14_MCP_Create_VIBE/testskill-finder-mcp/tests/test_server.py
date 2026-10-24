"""Tests for the Test Skill Finder MCP server (maps to section 6 of testskill-finder-plan.md)."""

import json

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from testskill_finder.registry import SkillRegistry
from testskill_finder.server import mcp

STANDARD_SECTIONS = {"When to use", "Workflow", "Output shape", "Guardrails"}


@pytest.fixture
async def client():
    async with Client(mcp) as c:
        yield c


async def call(client, tool, **args):
    return (await client.call_tool(tool, args)).data


async def top(client, query, n=1):
    res = await call(client, "search_skills", query=query, limit=10)
    return [r["name"] for r in res["results"][:n]]


# T1 / T2 — skill folder is the source of truth, 50+ skills in the standard format
def test_at_least_50_skills_load_cleanly():
    reg = SkillRegistry()
    assert len(reg.skills) >= 50
    assert reg.errors == {}


def test_every_skill_follows_format():
    for skill in SkillRegistry().skills.values():
        assert skill.name == skill.path.name, skill.relpath
        assert "Use when" in skill.description, skill.name
        for wanted in STANDARD_SECTIONS:
            assert any(h.startswith(wanted) for h in skill.sections), (skill.name, wanted)


# T3–T9 — keyword search
async def test_playwright_returns_pw_skills(client):
    names = await top(client, "playwright", 10)
    assert names and all(n.startswith("pw-") for n in names)


@pytest.mark.parametrize("query, expected", [
    ("playwright api", "pw-api-tester"),
    ("test case creator", "test-case-writer"),
    ("test plan creator", "test-plan-generator"),
    ("test strategy", "test-strategy-builder"),
    ("gherkin", "bdd-scenario-writer"),
    ("selenium wait", "se-wait-fixer"),
    ("k6", "k6-load-script-generator"),
    ("hallucination in chatbot", "llm-output-evaluator"),
])
async def test_query_ranks_expected_skill_first(client, query, expected):
    assert (await top(client, query))[0] == expected


async def test_bug_queries_find_defect_skills(client):
    names = await top(client, "bug", 3)
    assert {"bug-reporter", "bug-triage-assistant", "rca-analyzer"} == set(names)


async def test_typo_selinium(client):
    names = await top(client, "selinium", 5)
    assert names and all(n.startswith("se-") for n in names)


async def test_search_filter_by_pack(client):
    res = await call(client, "search_skills", query="flaky", pack="selenium")
    names = [r["name"] for r in res["results"]]
    assert names[0] == "se-flaky-debugger" and all(n.startswith("se-") for n in names)


async def test_find_best_skill_includes_instructions(client):
    res = await call(client, "find_best_skill", task="I need to write test cases from acceptance criteria")
    assert res["best"]["name"] == "test-case-writer"
    assert "## Workflow" in res["best"]["instructions"]


# T10 — reading skills
async def test_get_skill_and_section(client):
    skill = await call(client, "get_skill", name="pw-api-tester")
    assert skill["pack"] == "playwright" and skill["content"].startswith("---")
    sec = await call(client, "get_skill_section", name="pw-api-tester", section="guardrails")
    assert sec["section"] == "Guardrails"


async def test_unknown_skill_suggests_alternatives(client):
    with pytest.raises(ToolError, match="Did you mean"):
        await client.call_tool("get_skill", {"name": "test-case-writr"})


# T11 — supporting files + path traversal
async def test_skill_files(client):
    files = await call(client, "list_skill_files", name="test-plan-generator")
    assert "references/test-plan-template.md" in files["files"]
    f = await call(client, "get_skill_file", name="test-plan-generator", path="references/test-plan-template.md")
    assert f["content"]
    with pytest.raises(ToolError, match="escapes"):
        await client.call_tool("get_skill_file", {"name": "test-plan-generator", "path": "../../01-requirement-analysis/jira-requirement-analyzer/SKILL.md"})


async def test_browse_tools(client):
    cats = await call(client, "list_categories")
    assert cats["total_skills"] >= 50
    assert {c["group"] for c in cats["categories"]} >= {"02-test-planning", "playwright-pack", "selenium-pack"}
    listed = await call(client, "list_skills", category="playwright-pack")
    assert listed["count"] == 11
    related = await call(client, "get_related_skills", name="pw-flaky-debugger")
    assert related["related"][0]["name"] == "se-flaky-debugger"
    flow = await call(client, "get_stlc_workflow")
    assert flow["phases"][0]["group"] == "01-requirement-analysis"
    stats = await call(client, "skill_stats")
    assert stats["load_errors"] == {}


async def test_install_skill(client, tmp_path):
    res = await call(client, "install_skill", name="test-plan-generator", destination_dir=str(tmp_path))
    assert (tmp_path / "test-plan-generator" / "SKILL.md").is_file()
    assert (tmp_path / "test-plan-generator" / "references" / "requirement-checklist.md").is_file()
    assert res["installed"] == "test-plan-generator"
    with pytest.raises(ToolError, match="already exists"):
        await client.call_tool("install_skill", {"name": "test-plan-generator", "destination_dir": str(tmp_path)})


async def test_reload(client):
    res = await call(client, "reload_skills")
    assert res["total_skills"] >= 50 and res["errors"] == {}


# T12 — resources and prompts
async def test_resources(client):
    uris = {str(r.uri) for r in await client.list_resources()}
    assert {"skills://catalog", "skills://categories", "skills://stlc-workflow"} <= uris
    templates = {t.uri_template for t in await client.list_resource_templates()}
    assert {"skill://{name}", "skill://{name}/metadata", "skills://category/{category}"} <= templates

    catalog = json.loads((await client.read_resource("skills://catalog"))[0].text)
    assert len(catalog) >= 50
    raw = (await client.read_resource("skill://bug-reporter"))[0].text
    assert raw.startswith("---") and "name: bug-reporter" in raw
    meta = json.loads((await client.read_resource("skill://bug-reporter/metadata"))[0].text)
    assert meta["stlc_phase"] == "Defect Management"
    cat = json.loads((await client.read_resource("skills://category/selenium-pack"))[0].text)
    assert len(cat) == 11


async def test_prompts(client):
    names = {p.name for p in await client.list_prompts()}
    assert names == {"use_skill", "find_skill_for_task", "stlc_pipeline", "compare_skills"}
    msg = await client.get_prompt("use_skill", {"skill_name": "test-case-writer", "task": "Login page"})
    text = msg.messages[0].content.text
    assert "test-case-writer" in text and "Login page" in text
    msg = await client.get_prompt("find_skill_for_task", {"task": "playwright api tests"})
    assert "pw-api-tester" in msg.messages[0].content.text
