---
name: k6-load-script-generator
description: >-
  Generate k6 load-test scripts in JavaScript with scenarios, checks, and thresholds. Use
  when an engineer says "write a k6 script", "load test this API with k6", "add thresholds
  for p95", "ramp up to 500 virtual users", or has a performance plan to implement.
  Produces a k6 script with executors/stages, realistic think time, parameterised data,
  checks, and pass/fail thresholds — a draft run against an approved environment.
license: MIT
metadata:
  author: AITesterBlueprint4X
  pack: api
  version: 1.0.0
---

# k6 Load Script Generator

You implement a performance plan as a **k6 script whose thresholds are the pass/fail
criteria** — so CI fails on a regression, not on a human reading graphs.

## When to use
- A performance test plan or workload model needs to be scripted.
- Someone asks for k6, virtual users, ramp-up stages, or latency thresholds.
- A perf regression check should run in CI.

## Workflow
1. **Take inputs from the plan.** Journeys, mix, target RPS/VUs, durations, thresholds.
   If no plan exists, ask for targets — never invent SLAs.
2. **Pick executors.** `ramping-vus` for user-based load, `constant-arrival-rate` /
   `ramping-arrival-rate` for throughput targets; one scenario per journey.
3. **Parameterise data** with `SharedArray` from CSV/JSON; avoid all VUs hitting one record.
4. **Checks & tags.** `check()` on status/body; tag requests by endpoint name for grouped metrics.
5. **Thresholds.** `http_req_duration{p(95)<…}`, `http_req_failed{rate<…}`, per-tag thresholds.
6. **Think time & correlation.** `sleep()` between steps; extract tokens/ids from responses.
7. **Run notes.** Command, env vars, output to Grafana/InfluxDB/cloud, and the approved target env.

## Output shape
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    browse: { executor: 'ramping-vus', stages: [
      { duration: '2m', target: 100 }, { duration: '5m', target: 100 }, { duration: '1m', target: 0 } ] },
  },
  thresholds: { http_req_duration: ['p(95)<400'], http_req_failed: ['rate<0.01'] },
};

export default function () {
  const res = http.get(`${__ENV.BASE_URL}/api/products`, { tags: { name: 'products' } });
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

## Guardrails
- Run only against environments approved for load; never production without sign-off.
- Thresholds come from agreed targets, not invented numbers.
- Base URLs and tokens via `__ENV`, never hard-coded.
- The script is a draft until a baseline run validates it.
