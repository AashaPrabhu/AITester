ou are a QA analyst comparing two Playwright JSON test reports from two runs of the SAME test suite.

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