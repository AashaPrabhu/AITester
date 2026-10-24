"""Keyword search over skills: tokenising, QA-synonym expansion, IDF-weighted field scoring, fuzzy fallback."""

from __future__ import annotations

import difflib
import math
import re
from collections import Counter
from dataclasses import dataclass

from .registry import Skill, category_label

STOPWORDS = {
    "a", "an", "the", "for", "to", "of", "and", "or", "in", "on", "with", "i", "we", "want",
    "need", "skill", "skills", "find", "me", "my", "how", "do", "help", "related", "about",
    "that", "which", "using", "use", "something", "can", "is", "are", "it", "this", "some",
    "please", "show", "get", "give", "any", "be", "by", "from", "our",
}

# QA vocabulary: query term -> extra terms to look for. Keys/values are normalised tokens.
SYNONYMS: dict[str, list[str]] = {
    "playwright": ["pw"], "pw": ["playwright"],
    "selenium": ["se", "webdriver"], "webdriver": ["selenium", "se"],
    "bug": ["defect", "issue"], "defect": ["bug"], "issue": ["bug", "defect"],
    "creator": ["writer", "generator", "builder", "designer"],
    "create": ["writer", "generator", "builder", "designer"],
    "generate": ["generator", "writer"], "generator": ["writer", "builder"],
    "write": ["writer", "generator"], "writer": ["generator"],
    "make": ["generator", "builder"], "build": ["builder", "generator"],
    "builder": ["generator"], "design": ["designer"], "designer": ["design"],
    "plan": ["planning", "planner"], "planning": ["plan", "planner"], "planner": ["plan"],
    "strategy": ["approach", "strategist"], "approach": ["strategy"],
    "api": ["endpoint", "rest"], "rest": ["api", "restassured"], "endpoint": ["api"],
    "restassured": ["rest", "api"],
    "perf": ["performance", "load"], "performance": ["load", "k6"], "load": ["performance", "k6"],
    "stress": ["performance", "load"], "jmeter": ["performance", "load"],
    "a11y": ["accessibility"], "wcag": ["accessibility"], "accessibility": ["a11y", "axe"],
    "gherkin": ["bdd"], "cucumber": ["bdd", "gherkin"], "bdd": ["gherkin", "cucumber"],
    "flake": ["flaky"], "flakiness": ["flaky"], "flaky": ["flake", "unstable"],
    "selector": ["locator"], "xpath": ["locator"], "css": ["locator"], "locator": ["selector"],
    "testcase": ["case"], "report": ["reporter", "reporting"], "reporter": ["report"],
    "triage": ["severity", "priority"], "severity": ["triage"],
    "rca": ["root", "cause"], "root": ["rca"],
    "coverage": ["traceability", "gap"], "traceability": ["coverage"],
    "mock": ["mocker", "stub", "intercept", "network"], "stub": ["mock", "mocker"],
    "intercept": ["mock", "network"], "screenshot": ["visual"], "snapshot": ["visual"],
    "visual": ["screenshot", "snapshot"],
    "ci": ["pipeline", "configurator"], "pipeline": ["ci"], "jenkins": ["ci"], "github": ["ci"],
    "requirement": ["jira", "analyzer", "story"], "jira": ["requirement", "ticket"],
    "story": ["requirement", "jira"], "ticket": ["jira"],
    "closure": ["summary", "closing"], "summary": ["closure"],
    "security": ["owasp", "vulnerability"], "owasp": ["security"], "pentest": ["security"],
    "vulnerability": ["security"], "xss": ["security"], "injection": ["security"],
    "mobile": ["android", "ios", "appium"], "android": ["mobile"], "ios": ["mobile"],
    "appium": ["mobile"], "pact": ["contract"], "contract": ["pact"],
    "database": ["db", "sql"], "db": ["database", "sql"], "sql": ["database"],
    "etl": ["database", "reconciliation"],
    "llm": ["ai", "genai"], "ai": ["llm"], "genai": ["llm"], "chatbot": ["llm"], "rag": ["llm"],
    "hallucination": ["llm"], "estimate": ["estimation"], "estimation": ["estimate", "effort"],
    "effort": ["estimation"], "exploratory": ["charter", "exploration"],
    "bva": ["boundary"], "equivalence": ["boundary", "partition"], "partition": ["equivalence"],
    "review": ["reviewer"], "reviewer": ["review"], "pom": ["page", "object"],
    "wait": ["waits", "synchronization"], "sync": ["wait"], "grid": ["remote"],
    "crossbrowser": ["cross", "browser"], "newman": ["postman"], "postman": ["newman"],
    "k6": ["load", "performance"], "data": ["dataset"], "fixture": ["fixtures"],
    "priority": ["prioritizer", "risk"], "prioritize": ["prioritizer", "risk"],
    "prioritise": ["prioritizer", "risk"], "risk": ["prioritizer"],
    "execution": ["execute", "run"], "run": ["execution", "runner"],
}

FIELD_WEIGHTS = {"name": 6.0, "group": 4.0, "description": 3.0, "headings": 2.0, "body": 1.0}
EXPANSION_FACTOR = 0.6
FUZZY_FACTOR = 0.8


def normalise(token: str) -> str:
    t = token.lower()
    if len(t) > 6 and t.endswith("ing"):
        t = t[:-3]
        if len(t) > 2 and t[-1] == t[-2]:
            t = t[:-1]
    elif len(t) > 3 and t.endswith("s") and not t.endswith("ss"):
        t = t[:-1]
    return t


def tokenize(text: str, drop_stopwords: bool = False) -> list[str]:
    toks = [normalise(t) for t in re.findall(r"[a-z0-9]+", text.lower())]
    if drop_stopwords:
        toks = [t for t in toks if t not in STOPWORDS]
    return toks


@dataclass
class _Doc:
    skill: Skill
    fields: dict[str, Counter]
    all_terms: set[str]
    name_text: str
    desc_text: str


@dataclass
class SearchHit:
    skill: Skill
    score: float
    matched_terms: list[str]

    def to_dict(self) -> dict:
        return {
            **self.skill.summary(),
            "score": round(self.score, 2),
            "matched_terms": self.matched_terms,
        }


class SkillSearchIndex:
    def __init__(self, skills: list[Skill]):
        self.docs: list[_Doc] = []
        df: Counter = Counter()
        for s in skills:
            fields = {
                "name": Counter(tokenize(s.name)),
                "group": Counter(tokenize(f"{s.group} {s.pack or ''} {category_label(s.category)} {s.stlc_phase or ''}")),
                "description": Counter(tokenize(s.description)),
                "headings": Counter(tokenize(f"{s.title} {' '.join(s.sections)}")),
                "body": Counter(tokenize(s.body)),
            }
            terms = set().union(*fields.values())
            df.update(terms)
            self.docs.append(_Doc(s, fields, terms, s.name.lower(), s.description.lower()))
        n = max(len(self.docs), 1)
        self.idf = {t: math.log(1 + n / c) for t, c in df.items()}
        self.vocab = sorted(df)

    def _expand(self, term: str) -> dict[str, float]:
        exp = {term: 1.0}
        for syn in SYNONYMS.get(term, []):
            exp.setdefault(normalise(syn), EXPANSION_FACTOR)
        if term not in self.idf:
            for close in difflib.get_close_matches(term, self.vocab, n=2, cutoff=0.8):
                exp.setdefault(close, FUZZY_FACTOR)
        return exp

    def _term_score(self, doc: _Doc, term: str) -> float:
        idf = self.idf.get(term, 0.0)
        if not idf:
            return 0.0
        score = 0.0
        for fname, weight in FIELD_WEIGHTS.items():
            tf = doc.fields[fname].get(term, 0)
            if tf:
                score += weight * (1 + math.log(tf))
        return score * idf

    def search(self, query: str, limit: int = 10, candidates: list[Skill] | None = None) -> list[SearchHit]:
        terms = list(dict.fromkeys(tokenize(query, drop_stopwords=True)))
        if not terms:
            terms = list(dict.fromkeys(tokenize(query)))
        if not terms:
            return []
        expansions = {t: self._expand(t) for t in terms}
        allowed = {s.name for s in candidates} if candidates is not None else None
        phrase = "-".join(terms)
        q_lower = " ".join(query.lower().split())

        hits: list[SearchHit] = []
        for doc in self.docs:
            if allowed is not None and doc.skill.name not in allowed:
                continue
            score = 0.0
            matched: list[str] = []
            covered = 0
            for t, exp in expansions.items():
                best, best_term = 0.0, None
                for et, factor in exp.items():
                    s = self._term_score(doc, et) * factor
                    if s > best:
                        best, best_term = s, et
                if best > 0:
                    score += best
                    covered += 1
                    matched.append(t if best_term == t else f"{t}→{best_term}")
            if not score:
                continue
            coverage = covered / len(terms)
            score *= 0.4 + 0.6 * coverage * coverage
            if phrase and phrase in doc.name_text:
                score += 15
            elif len(q_lower) > 3 and q_lower in doc.desc_text:
                score += 6
            hits.append(SearchHit(doc.skill, score, matched))

        hits.sort(key=lambda h: (-h.score, h.skill.name))
        return hits[: max(limit, 0)]
