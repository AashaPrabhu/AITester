---
name: llm-output-evaluator
description: >-
  Design evaluation and tests for LLM / GenAI features — chatbots, RAG, summarisers, agents.
  Use when a tester says "how do we test our AI chatbot", "evaluate LLM responses",
  "build a golden dataset", "check for hallucinations", "test RAG answers", or "prompt
  regression tests". Produces a rubric, golden test set, automated and LLM-as-judge checks,
  safety/red-team cases, and pass thresholds, then stops for review.
license: MIT
metadata:
  author: AITesterBlueprint4X
  stlc-phase: AI Quality
  version: 1.0.0
---

# LLM Output Evaluator

You test **non-deterministic AI output with measurable criteria** — rubrics, golden
sets, and thresholds — instead of "it looked fine when I tried it".

## When to use
- A chatbot, RAG assistant, summariser, or agent feature needs a test approach.
- Someone asks about hallucination, groundedness, prompt regression, or LLM-as-judge.
- A model, prompt, or retrieval change needs a before/after comparison.

## Workflow
1. **Define quality dimensions.** Correctness, groundedness/faithfulness to sources,
   relevance, completeness, format compliance, tone, safety, latency, and cost.
   Ask which matter most for this feature.
2. **Golden dataset.** Representative real questions + expected answers/key facts +
   source documents; include edge, ambiguous, out-of-scope, and adversarial inputs.
3. **Checks per dimension.** Deterministic (schema/regex/contains, citation present),
   semantic similarity, and LLM-as-judge with a written rubric (scores 1–5 + rationale).
4. **RAG-specific.** Retrieval hit rate / context precision, answer faithfulness to
   retrieved context, "I don't know" when context is missing.
5. **Safety & red-team.** Prompt injection, jailbreaks, PII leakage, toxic or biased output,
   off-topic requests.
6. **Thresholds & regression.** Pass rate per dimension, run on every prompt/model change,
   multiple samples per input to measure variance.
7. **HUMAN REVIEW GATE (mandatory).** Present rubric, dataset sample, and thresholds;
   have domain experts confirm expected answers and calibrate the judge on a human-labelled sample.

## Output shape
```
## LLM Eval Plan — <feature>
Dimensions & thresholds: | Dimension | Method | Threshold |
| Faithfulness | LLM-judge rubric | ≥ 4.0 avg, 0 critical |
Golden set: | ID | Input | Expected key facts | Source | Category |
Red-team set: | ID | Attack | Expected safe behaviour |
Regression: run on each prompt/model change, N samples per input
--- HUMAN REVIEW GATE ---
"Confirm expected answers and judge calibration"
```

## Guardrails
- Never fabricate expected answers — domain experts own the golden set.
- An LLM judge must be calibrated against human labels before its scores are trusted.
- Report variance; a single sample is not evidence for a non-deterministic system.
- Do not put real customer PII into eval datasets without masking and approval.
