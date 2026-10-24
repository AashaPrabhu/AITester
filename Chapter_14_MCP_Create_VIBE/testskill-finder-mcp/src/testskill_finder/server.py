"""Test Skill Finder MCP server (FastMCP): find, read, and apply QA/testing Agent Skills."""

from __future__ import annotations

import argparse
import difflib
import json
import shutil
from pathlib import Path
from typing import Annotated

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field

from .registry import CATEGORY_ORDER, STLC_PHASES, Skill, SkillRegistry, category_label
from .search import SkillSearchIndex

INSTRUCTIONS = """\
Test Skill Finder: a catalog of 50+ QA / software-testing Agent Skills (SKILL.md files)
covering the full STLC (requirements → planning → design → cases → execution → defects →
closure), non-functional testing, AI quality, and framework packs (Playwright, Selenium,
Cypress, API/REST Assured/Postman/k6).

Typical flow: `search_skills` (or `find_best_skill` for a task description) → `get_skill`
to read the instructions → follow them. Use the `use_skill` prompt to load a skill with a task.
"""

mcp = FastMCP("Test Skill Finder", instructions=INSTRUCTIONS, version="1.0.0")


class _State:
    registry: SkillRegistry | None = None
    index: SkillSearchIndex | None = None


state = _State()


def configure(skills_dir: str | Path | None = None) -> SkillRegistry:
    state.registry = SkillRegistry(skills_dir)
    state.index = SkillSearchIndex(list(state.registry.skills.values()))
    return state.registry


def _reg() -> SkillRegistry:
    if state.registry is None:
        configure()
    return state.registry


def _idx() -> SkillSearchIndex:
    if state.index is None:
        configure()
    return state.index


def _require(name: str) -> Skill:
    skill = _reg().get(name)
    if skill:
        return skill
    names = list(_reg().skills)
    close = difflib.get_close_matches(name.strip().lower(), names, n=3, cutoff=0.5)
    if not close:
        close = [h.skill.name for h in _idx().search(name, 3)]
    hint = f" Did you mean: {', '.join(close)}?" if close else ""
    raise ToolError(f"Skill '{name}' not found.{hint} Use search_skills or list_skills to browse.")


def _related(skill: Skill, limit: int) -> list[dict]:
    reg = _reg()
    out: dict[str, str] = {}
    # Counterpart in the other framework pack (pw-flaky-debugger <-> se-flaky-debugger).
    for prefix, other in (("pw-", "se-"), ("se-", "pw-")):
        if skill.name.startswith(prefix):
            twin = other + skill.name[len(prefix):]
            if twin in reg.skills:
                out[twin] = "same task in the other framework pack"
    # STLC hand-offs: previous / next phase.
    if skill.category in STLC_PHASES:
        i = STLC_PHASES.index(skill.category)
        for j, why in ((i - 1, "upstream STLC phase (feeds this skill)"), (i + 1, "downstream STLC phase (consumes this output)")):
            if 0 <= j < len(STLC_PHASES):
                for s in reg.filter(category=STLC_PHASES[j]):
                    out.setdefault(s.name, why)
    for s in reg.skills.values():
        if s.group == skill.group and s.name != skill.name:
            out.setdefault(s.name, f"same group ({s.group})")
    for h in _idx().search(skill.description, limit + 1):
        if h.skill.name != skill.name:
            out.setdefault(h.skill.name, "similar description")
    return [{**reg.skills[n].summary(), "reason": why} for n, why in list(out.items())[:limit]]


def _stlc_markdown() -> str:
    lines = ["# QA Skill Catalog — STLC order", ""]
    for group, skills in _reg().groups().items():
        lines.append(f"## {category_label(group)} (`{group}`)")
        lines += [f"- **{s.name}** — {s.description.split('. Use when')[0]}" for s in skills]
        lines.append("")
    return "\n".join(lines)


# ----------------------------------------------------------------------------- tools

READ_ONLY = {"readOnlyHint": True, "openWorldHint": False}


@mcp.tool(annotations=READ_ONLY, tags={"search"})
def search_skills(
    query: Annotated[str, Field(description="Keywords, e.g. 'playwright api', 'test case creator', 'bug triage'")],
    limit: Annotated[int, Field(ge=1, le=60, description="Max results")] = 10,
    category: Annotated[str | None, Field(description="Optional category/group filter, e.g. '03-test-design', 'playwright-pack', 'test planning'")] = None,
    pack: Annotated[str | None, Field(description="Optional framework pack filter: playwright, selenium, cypress, api")] = None,
) -> dict:
    """Search the QA skill catalog by keyword. Handles QA synonyms (playwright→pw, bug→defect,
    creator→writer/generator) and typos. Returns ranked skills with score and matched terms."""
    candidates = _reg().filter(category, pack) if (category or pack) else None
    hits = _idx().search(query, limit, candidates)
    return {
        "query": query,
        "count": len(hits),
        "results": [h.to_dict() for h in hits],
        "tip": "Call get_skill(name) to read full instructions." if hits else
               "No match. Try broader keywords or list_categories / list_skills.",
    }


@mcp.tool(annotations=READ_ONLY, tags={"search"})
def find_best_skill(
    task: Annotated[str, Field(description="What you want to do, in plain language")],
) -> dict:
    """Pick the single best skill for a natural-language task, with its instructions and runners-up."""
    hits = _idx().search(task, 4)
    if not hits:
        raise ToolError("No skill matches that task. Try search_skills with different keywords.")
    best = hits[0].skill
    return {
        "best": {**hits[0].to_dict(), "instructions": best.body},
        "alternatives": [h.to_dict() for h in hits[1:]],
    }


@mcp.tool(annotations=READ_ONLY, tags={"read"})
def get_skill(
    name: Annotated[str, Field(description="Skill name, e.g. 'pw-api-tester'")],
) -> dict:
    """Get a skill's full SKILL.md content and metadata."""
    skill = _require(name)
    return {**skill.metadata(), "content": skill.raw}


@mcp.tool(annotations=READ_ONLY, tags={"read"})
def get_skill_section(
    name: Annotated[str, Field(description="Skill name")],
    section: Annotated[str, Field(description="Section heading, e.g. 'Workflow', 'Guardrails', 'Output shape', 'When to use'")],
) -> dict:
    """Get one section of a skill (case-insensitive, partial heading match allowed)."""
    skill = _require(name)
    want = section.strip().lower()
    for heading, text in skill.sections.items():
        if heading.lower() == want or want in heading.lower():
            return {"name": skill.name, "section": heading, "content": text}
    raise ToolError(f"Section '{section}' not in {skill.name}. Available: {', '.join(skill.sections)}")


@mcp.tool(annotations=READ_ONLY, tags={"browse"})
def list_skills(
    category: Annotated[str | None, Field(description="Optional category/group filter")] = None,
    pack: Annotated[str | None, Field(description="Optional pack filter: playwright, selenium, cypress, api")] = None,
) -> dict:
    """List skills in the catalog (STLC order), optionally filtered by category or pack."""
    skills = _reg().filter(category, pack)
    return {"count": len(skills), "skills": [s.summary() for s in skills]}


@mcp.tool(annotations=READ_ONLY, tags={"browse"})
def list_categories() -> dict:
    """List skill categories / framework packs with skill counts."""
    groups = _reg().groups()
    return {
        "total_skills": len(_reg().skills),
        "categories": [
            {"group": g, "label": category_label(g), "category": ss[0].category,
             "count": len(ss), "skills": [s.name for s in ss]}
            for g, ss in groups.items()
        ],
    }


@mcp.tool(annotations=READ_ONLY, tags={"browse"})
def get_related_skills(
    name: Annotated[str, Field(description="Skill name")],
    limit: Annotated[int, Field(ge=1, le=20)] = 8,
) -> dict:
    """Find skills related to a given skill: framework counterpart, STLC hand-offs, same group, similar purpose."""
    skill = _require(name)
    return {"name": skill.name, "related": _related(skill, limit)}


@mcp.tool(annotations=READ_ONLY, tags={"browse"})
def get_stlc_workflow() -> dict:
    """Return skills grouped in Software Testing Life Cycle order, plus extensions and framework packs."""
    groups = _reg().groups()
    ordered = sorted(groups, key=lambda g: (CATEGORY_ORDER.index(groups[g][0].category)
                                            if groups[g][0].category in CATEGORY_ORDER else 99, g))
    return {
        "flow": "requirement → plan → design → cases → execute → defects → closure",
        "phases": [
            {"step": i + 1, "group": g, "label": category_label(g),
             "is_stlc_phase": groups[g][0].category in STLC_PHASES,
             "skills": [{"name": s.name, "title": s.title} for s in groups[g]]}
            for i, g in enumerate(ordered)
        ],
    }


@mcp.tool(annotations=READ_ONLY, tags={"read"})
def list_skill_files(name: Annotated[str, Field(description="Skill name")]) -> dict:
    """List supporting files (references, scripts, templates) shipped with a skill."""
    skill = _require(name)
    return {"name": skill.name, "files": ["SKILL.md", *skill.supporting_files]}


@mcp.tool(annotations=READ_ONLY, tags={"read"})
def get_skill_file(
    name: Annotated[str, Field(description="Skill name")],
    path: Annotated[str, Field(description="Relative path from list_skill_files, e.g. 'references/test-plan-template.md'")],
) -> dict:
    """Read a supporting file of a skill (path must stay inside the skill folder)."""
    skill = _require(name)
    base = skill.path.resolve()
    target = (base / path).resolve()
    if not target.is_relative_to(base):
        raise ToolError("Path escapes the skill folder.")
    if not target.is_file():
        raise ToolError(f"File '{path}' not found. Available: {', '.join(['SKILL.md', *skill.supporting_files])}")
    try:
        content = target.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ToolError("File is not UTF-8 text.")
    return {"name": skill.name, "path": target.relative_to(base).as_posix(), "content": content}


@mcp.tool(annotations={"readOnlyHint": False, "destructiveHint": False, "openWorldHint": False}, tags={"manage"})
def install_skill(
    name: Annotated[str, Field(description="Skill name")],
    destination_dir: Annotated[str, Field(description="Folder to copy the skill into, e.g. '~/.claude/skills' or '.github/skills'")],
    overwrite: Annotated[bool, Field(description="Replace an existing copy")] = False,
) -> dict:
    """Copy a skill folder (SKILL.md + supporting files) into a destination folder, e.g. ~/.claude/skills."""
    skill = _require(name)
    dest_root = Path(destination_dir).expanduser().resolve()
    target = dest_root / skill.name
    if target.exists():
        if not overwrite:
            raise ToolError(f"{target} already exists. Pass overwrite=true to replace it.")
        shutil.rmtree(target)
    dest_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(skill.path, target)
    return {"installed": skill.name, "path": str(target), "files": ["SKILL.md", *skill.supporting_files]}


@mcp.tool(annotations={"readOnlyHint": False, "idempotentHint": True, "openWorldHint": False}, tags={"manage"})
def reload_skills() -> dict:
    """Rescan the skills folder (the source of truth) after adding or editing SKILL.md files."""
    reg = configure(_reg().root)
    return {"skills_dir": str(reg.root), "total_skills": len(reg.skills), "errors": reg.errors}


@mcp.tool(annotations=READ_ONLY, tags={"manage"})
def skill_stats() -> dict:
    """Catalog statistics: totals per category and pack, skills with supporting files, load errors."""
    reg = _reg()
    packs: dict[str, int] = {}
    for s in reg.skills.values():
        if s.pack:
            packs[s.pack] = packs.get(s.pack, 0) + 1
    return {
        "skills_dir": str(reg.root),
        "total_skills": len(reg.skills),
        "per_group": {g: len(ss) for g, ss in reg.groups().items()},
        "per_pack": packs,
        "with_supporting_files": [s.name for s in reg.skills.values() if s.supporting_files],
        "load_errors": reg.errors,
    }


# ------------------------------------------------------------------------- resources

@mcp.resource("skills://catalog", mime_type="application/json", description="All skills with summary metadata")
def catalog_resource() -> str:
    return json.dumps([s.summary() for s in _reg().skills.values()], indent=2)


@mcp.resource("skills://categories", mime_type="application/json", description="Categories / packs with counts")
def categories_resource() -> str:
    return json.dumps(list_categories_data(), indent=2)


def list_categories_data() -> list[dict]:
    return [{"group": g, "label": category_label(g), "count": len(ss), "skills": [s.name for s in ss]}
            for g, ss in _reg().groups().items()]


@mcp.resource("skills://stlc-workflow", mime_type="text/markdown", description="Skills mapped onto the STLC, as markdown")
def stlc_resource() -> str:
    return _stlc_markdown()


@mcp.resource("skill://{name}", mime_type="text/markdown", description="Raw SKILL.md for a skill")
def skill_resource(name: str) -> str:
    return _require(name).raw


@mcp.resource("skill://{name}/metadata", mime_type="application/json", description="Metadata for a skill")
def skill_metadata_resource(name: str) -> str:
    return json.dumps(_require(name).metadata(), indent=2)


@mcp.resource("skills://category/{category}", mime_type="application/json", description="Skills in one category or pack group")
def category_resource(category: str) -> str:
    skills = _reg().filter(category=category)
    if not skills:
        raise ToolError(f"No skills in category '{category}'. See skills://categories.")
    return json.dumps([s.summary() for s in skills], indent=2)


# --------------------------------------------------------------------------- prompts

@mcp.prompt(description="Load a skill's instructions and apply them to a task")
def use_skill(skill_name: str, task: str) -> str:
    skill = _require(skill_name)
    return (
        f"You are applying the QA skill **{skill.name}** ({skill.title}).\n\n"
        f"Follow these skill instructions exactly, including the human review gate and guardrails:\n\n"
        f"<skill>\n{skill.body.strip()}\n</skill>\n\n"
        f"Task:\n{task}"
    )


@mcp.prompt(description="Find the right QA skill for a task, then apply it")
def find_skill_for_task(task: str) -> str:
    hits = _idx().search(task, 5)
    shortlist = "\n".join(f"- {h.skill.name}: {h.skill.description}" for h in hits) or "- (no direct match)"
    return (
        "You have access to the Test Skill Finder MCP server.\n\n"
        f"Task: {task}\n\n"
        f"Candidate skills from a keyword search:\n{shortlist}\n\n"
        "1. Pick the best-fitting skill (call search_skills again with other keywords if none fit).\n"
        "2. Call get_skill with its name and read the instructions.\n"
        "3. Apply the skill's workflow to the task, honouring its guardrails and human review gate.\n"
        "4. State which skill you used and why."
    )


@mcp.prompt(description="Walk a feature through every STLC phase using the phase skills")
def stlc_pipeline(feature: str) -> str:
    steps = []
    for phase in STLC_PHASES:
        names = ", ".join(s.name for s in _reg().filter(category=phase))
        steps.append(f"{len(steps) + 1}. {category_label(phase)} — skills: {names}")
    return (
        f"Plan testing for this feature end-to-end across the Software Testing Life Cycle:\n\n{feature}\n\n"
        + "\n".join(steps)
        + "\n\nFor each phase, call get_skill on the most relevant skill, produce that phase's output, "
          "and pause at each skill's human review gate before handing off to the next phase."
    )


@mcp.prompt(description="Compare two skills to choose the right one")
def compare_skills(skill_a: str, skill_b: str) -> str:
    a, b = _require(skill_a), _require(skill_b)
    return (
        "Compare these two QA skills and recommend when to use each. Cover purpose, inputs, "
        "outputs, and where they overlap.\n\n"
        f"<skill name=\"{a.name}\">\n{a.raw.strip()}\n</skill>\n\n"
        f"<skill name=\"{b.name}\">\n{b.raw.strip()}\n</skill>"
    )


# ------------------------------------------------------------------------------- CLI

def main() -> None:
    parser = argparse.ArgumentParser(description="Test Skill Finder MCP server")
    parser.add_argument("--transport", choices=["stdio", "http", "sse"], default="stdio",
                        help="stdio (default) when launched by a client/Inspector; http = Streamable HTTP")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--path", default="/mcp", help="HTTP endpoint path")
    parser.add_argument("--skills-dir", default=None, help="Override skills folder (or set TESTSKILL_SKILLS_DIR)")
    args = parser.parse_args()

    configure(args.skills_dir)
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=args.transport, host=args.host, port=args.port, path=args.path)


if __name__ == "__main__":
    main()
