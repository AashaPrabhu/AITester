# Playwright Flaky Test Detector (Langflow)

A no-code Langflow flow that reads two Playwright JSON test reports from two runs of the
same test suite and tells you how many tests are **flaky**.

## What counts as flaky

| Run 1 | Run 2 | Verdict |
|-------|-------|---------|
| passed | passed | Stable |
| failed | passed | **Flaky** |
| passed | failed | **Flaky** |
| failed | failed | Real bug (not flaky) |

A test that Playwright itself marks as `"flaky"` (failed, then passed on retry) is also counted as flaky.

## Flow

```
Read File (result1.json) ──┐
                           ├──> Prompt ──> Google Gemini ──> Chat Output
Read File (result2.json) ──┘
```

| Component | Purpose |
|-----------|---------|
| Read File #1 | Loads `result1.json` (first run) |
| Read File #2 | Loads `result2.json` (rerun) |
| Prompt | Places both reports into `{run1}` and `{run2}` and gives the comparison rules |
| Google Gemini | Compares the runs and identifies flaky tests (temperature 0) |
| Chat Output | Shows the final report in the Playground |

No custom code is used. Every component is built into Langflow.

## Sample data

The `results/` folder contains two reports in the Playwright JSON reporter format.
Each report has 100 tests across 10 spec files.

| File | Passed | Failed |
|------|--------|--------|
| `result1.json` | 97 | 3 |
| `result2.json` | 99 | 1 |

### Expected result: 2 flaky tests

| Test | File | Run 1 | Run 2 | Verdict |
|------|------|-------|-------|---------|
| login via SSO redirects to dashboard | `auth/login.spec.ts` | failed | passed | Flaky |
| autocomplete suggestions appear | `search/search.spec.ts` | failed | passed | Flaky |
| payment with credit card succeeds | `checkout/checkout.spec.ts` | failed | failed | Real bug |

## Prompt used

```
You are a QA analyst comparing two Playwright JSON test reports from two runs of the SAME test suite.

RUN 1 (result1.json):
{run1}

RUN 2 (result2.json):
{run2}

Instructions:
- A test's outcome is in "tests[].status": "expected" means passed, "unexpected" means failed, "flaky" means flaky.
- Identify tests by spec "file" plus spec "title".
- Step 1: List every test that failed in Run 1.
- Step 2: List every test that failed in Run 2.
- Step 3: A test is FLAKY if it passed in one run and failed in the other, or has status "flaky".
  A test that failed in BOTH runs is a real bug, NOT flaky.

Answer in this format:
Total tests per run: X
Run 1: passed / failed
Run 2: passed / failed
Number of flaky tests: N
Flaky tests: a table with test name, file, Run 1 status, Run 2 status, and error message
Consistently failing tests (real bugs): a list
```

## How to run

### Prerequisites
- Langflow installed and running
- A Google Gemini API key

### Option A: import the flow
1. In Langflow, click **New Flow**, then **Import**, and select `langflow/Flaky_Test_Detector.json`.
2. Upload `results/result1.json` to the first Read File node and `results/result2.json` to the second.
3. Add your Gemini API key to the Google Gemini node.
4. Open the **Playground** and send any message (for example `run`).

### Option B: build it by hand
1. Add two **Read File** components. Upload `result1.json` to one and `result2.json` to the other.
2. Add a **Prompt Template** and paste the prompt above. This creates the `run1` and `run2` inputs.
3. Connect Read File #1 to `run1` and Read File #2 to `run2`.
   If the Prompt will not accept the connection, add a **Parser** component (template `{text}`) between each file and the Prompt.
4. Add **Google Generative AI**. Set your API key, choose a Flash model, set temperature to 0, and connect the Prompt to it.
5. Add **Chat Output** and connect the model's response to it.
6. Open the **Playground** and run the flow.

## Why Gemini

The two reports together are about 250 KB (roughly 60,000 to 70,000 tokens).
Gemini Flash models have a large enough context window to read both at once.
Groq's free tier has a low tokens-per-minute limit and will usually reject input this large.

## Screenshots

| Flow | Result |
|------|--------|
| ![Flow](screenshots/flow.png) | ![Result](screenshots/output.png) |

## Generating your own reports

Run your Playwright suite twice with the JSON reporter:

```bash
npx playwright test --reporter=json > results/result1.json
npx playwright test --reporter=json > results/result2.json
```

Then upload the two new files to the Read File nodes.

## Limitations

- The comparison is done by the LLM, so there is a small chance it misses a test in very large reports.
  Temperature 0 and the step-by-step instructions in the prompt keep it reliable for this data.
  Run the flow two or three times to confirm the count is consistent.
- For large suites (thousands of tests), a code-based comparison step before the LLM would be more reliable.

## Repository structure

```
playwright-flaky-detector/
├── README.md
├── results/
│   ├── result1.json              # Run 1: 97 passed, 3 failed
│   └── result2.json              # Run 2: 99 passed, 1 failed
├── langflow/
│   └── Flaky_Test_Detector.json  # Exported Langflow flow (add after export)
└── screenshots/
    ├── flow.png                  # Flow canvas (add your screenshot)
    └── output.png                # Playground result (add your screenshot)
```