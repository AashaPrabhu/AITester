"""Skill registry: scans the skills/ folder (the source of truth) and parses every SKILL.md."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

DEFAULT_SKILLS_DIR = Path(__file__).resolve().parents[2] / "skills"

# Display order for categories: STLC phases first, then extensions, then framework packs.
CATEGORY_ORDER = [
    "01-requirement-analysis",
    "02-test-planning",
    "03-test-design",
    "04-test-case-development",
    "05-test-execution",
    "06-defect-management",
    "07-test-closure",
    "08-non-functional-testing",
    "09-ai-quality",
    "framework-packs",
]

STLC_PHASES = CATEGORY_ORDER[:7]

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def category_label(category: str) -> str:
    """'05-test-execution' -> 'Test Execution'."""
    return re.sub(r"^\d+-", "", category).replace("-", " ").title()


@dataclass
class Skill:
    name: str
    title: str
    description: str
    category: str
    group: str  # category for STLC skills, "<pack>-pack" for framework packs
    pack: str | None
    stlc_phase: str | None
    author: str | None
    version: str | None
    license: str | None
    path: Path
    relpath: str
    raw: str
    body: str
    sections: dict[str, str] = field(default_factory=dict)
    supporting_files: list[str] = field(default_factory=list)

    @property
    def uri(self) -> str:
        return f"skill://{self.name}"

    def summary(self) -> dict:
        return {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "group": self.group,
            "pack": self.pack,
            "stlc_phase": self.stlc_phase,
            "uri": self.uri,
        }

    def metadata(self) -> dict:
        return {
            **self.summary(),
            "author": self.author,
            "version": self.version,
            "license": self.license,
            "path": self.relpath,
            "sections": list(self.sections),
            "supporting_files": self.supporting_files,
        }


class SkillLoadError(Exception):
    pass


def parse_skill(skill_md: Path, root: Path) -> Skill:
    raw = skill_md.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(raw.lstrip("﻿"))
    if not m:
        raise SkillLoadError("missing YAML frontmatter")
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        raise SkillLoadError(f"invalid YAML frontmatter: {e}") from e
    body = m.group(2)

    skill_dir = skill_md.parent
    name = str(fm.get("name") or skill_dir.name).strip()
    description = " ".join(str(fm.get("description") or "").split())
    if not description:
        raise SkillLoadError("frontmatter has no description")
    meta = fm.get("metadata") or {}

    rel_parts = skill_dir.relative_to(root).parts
    category = rel_parts[0]
    pack = meta.get("pack")
    if category == "framework-packs" and len(rel_parts) > 2:
        group = rel_parts[1]
        pack = pack or group.removesuffix("-pack")
    else:
        group = category

    title_m = TITLE_RE.search(body)
    sections: dict[str, str] = {}
    heads = list(SECTION_RE.finditer(body))
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        sections[h.group(1)] = body[h.end():end].strip()

    supporting = sorted(
        p.relative_to(skill_dir).as_posix()
        for p in skill_dir.rglob("*")
        if p.is_file() and p.name != "SKILL.md"
    )

    return Skill(
        name=name,
        title=title_m.group(1) if title_m else name,
        description=description,
        category=category,
        group=group,
        pack=pack,
        stlc_phase=meta.get("stlc-phase"),
        author=meta.get("author"),
        version=str(meta["version"]) if meta.get("version") is not None else None,
        license=fm.get("license"),
        path=skill_dir,
        relpath=skill_dir.relative_to(root).as_posix(),
        raw=raw,
        body=body,
        sections=sections,
        supporting_files=supporting,
    )


class SkillRegistry:
    def __init__(self, skills_dir: str | Path | None = None):
        self.root = Path(
            skills_dir or os.environ.get("TESTSKILL_SKILLS_DIR") or DEFAULT_SKILLS_DIR
        ).resolve()
        self.skills: dict[str, Skill] = {}
        self.errors: dict[str, str] = {}
        self.load()

    def load(self) -> None:
        skills: dict[str, Skill] = {}
        errors: dict[str, str] = {}
        if not self.root.is_dir():
            raise FileNotFoundError(f"skills folder not found: {self.root}")
        for skill_md in sorted(self.root.rglob("SKILL.md")):
            rel = skill_md.relative_to(self.root).as_posix()
            try:
                skill = parse_skill(skill_md, self.root)
            except (SkillLoadError, OSError, UnicodeDecodeError) as e:
                errors[rel] = str(e)
                continue
            if skill.name in skills:
                errors[rel] = f"duplicate skill name '{skill.name}'"
                continue
            skills[skill.name] = skill
        self.skills = dict(sorted(skills.items(), key=lambda kv: self._sort_key(kv[1])))
        self.errors = errors

    @staticmethod
    def _sort_key(skill: Skill) -> tuple:
        cat = CATEGORY_ORDER.index(skill.category) if skill.category in CATEGORY_ORDER else 99
        return (cat, skill.group, skill.name)

    def get(self, name: str) -> Skill | None:
        return self.skills.get(name.strip().lower())

    def groups(self) -> dict[str, list[Skill]]:
        out: dict[str, list[Skill]] = {}
        for s in self.skills.values():
            out.setdefault(s.group, []).append(s)
        return out

    def filter(self, category: str | None = None, pack: str | None = None) -> list[Skill]:
        result = list(self.skills.values())
        if category:
            c = category.strip().lower()
            result = [
                s for s in result
                if c in (s.category, s.group) or c == category_label(s.group).lower()
                or c in s.category or c in s.group
            ]
        if pack:
            p = pack.strip().lower().removesuffix("-pack")
            result = [s for s in result if (s.pack or "").lower() == p]
        return result
