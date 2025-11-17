# QA Engineer Case Study – Public APIs x K6 + Playwright

This project demonstrates structured QA automation practices across both API and UI layers,  
leveraging industry-standard tools like **K6** and **Playwright**.

It was built as part of a hands-on QA-focused assignment,  
aimed at validating real-world testing capabilities involving:

- REST and GraphQL API integration testing
- End-to-end browser automation
- Basic performance profiling and CI integration

The goal is to showcase maintainable, scalable, and stable testing strategies suitable for modern QA workflows.

---

## 📌 Project Deliverables

This repository contains:

- **K6 (JS)** integration test scripts for REST + GraphQL  
- **Playwright (Python)** E2E tests and fixtures  
- **GitHub Actions** workflows that run tests on each `pull_request`  
- A clear **README** explaining setup, test strategy, and coverage  

---

# 🔵 K6 Integration Tests

K6 is used for **API-level integration testing** to validate functionality, schema correctness,  
edge-case handling, and basic performance characteristics.

We tested **two public APIs** (one REST, one GraphQL), as required by the case study:

- **REST API:** RestCountries v3  
- **GraphQL API:** Rick & Morty GraphQL  

---

## ✅ What We Verify in K6 Tests

### ✔ Functional & Happy Path
- 200 OK responses  
- Valid JSON structure  
- Required fields exist  
- Functional correctness  
  - **REST:** Country official name = `"Republic of Turkey"`  
  - **GraphQL:** Character name = `"Rick Sanchez"`  

### ✔ Schema & Shape Validation
- Array validations (`capital`, etc.)
- Object field existence (`region`, `origin.name`)
- GraphQL `errors[]` validation

### ✔ Functional & Happy Path
- 200 OK responses  
- JSON structure validation  
- Required fields exist  
- Functional correctness  
  - REST → Country name = *“Republic of Turkey”*
  - GraphQL → Character name = *“Rick Sanchez”*

### ✔ Schema & Shape Validation
- Field existence (`name`, `capital`, `region`, `origin.name`, etc.)
- Array validations
- GraphQL `errors[]` handling

### ✔ Edge Cases

#### REST:
- Invalid country  
- Partial match  
- Numeric input  
- Special characters  
- Empty query (`/name/`)  

#### GraphQL:
- Invalid character ID  
- Invalid fields (schema errors)  
- Requests returning GraphQL-level errors  

### ✔ Performance Signals (Thresholds)

Thresholds applied **only to happy-path groups**:

| API      | Threshold         |
|----------|-------------------|
| REST     | **p95 < 600ms**   |
| GraphQL  | **p95 < 800ms**   |

**Why different?**  
GraphQL public endpoints tend to respond slower because:
- They resolve nested data  
- Have heavier resolver chains  
- Are globally rate-limited  

Therefore, REST gets a stricter threshold, while GraphQL stays conservative.

### ✔ Load Profile
Basic load (per assignment requirement):
- 5s → 1 VU (smoke)
- 10s → 3 VUs (light load)
- 5s → ramp down


---

## 🧩 Why Conservative Thresholds?  
(Performance Strategy Explanation)

The assignment explicitly requires:

> “Start conservative and explain how you’d tune thresholds over time.”

Our approach:

1. **Start with high limits** (600–800ms)  
   → Prevent flaky failures due to network jitter.

2. **Collect real metrics over CI runs**  
   → Observe p95 trends daily or weekly.

3. **Gradually tighten limits**  
   Example progression:
   - REST p95: 600 → 500 → 400ms  
   - GraphQL p95: 800 → 700 → 600ms  

4. **Lock final thresholds once stable**  
   → Ensures tests are meaningful but reliable.

---

## 🛡 Flakiness Controls Used

To ensure stable, CI-friendly tests:

- Thresholds apply **only** to happy-path groups  
- JSON parsing wrapped in `try/catch`  
- Invalid scenarios do **not** trigger SLA failures  
- Low VU count (public APIs)  
- No reliance on server-side state  
- Deterministic grouping for stable metrics  

---

## ▶️ Running K6 Tests

Install k6:  
https://k6.io/docs/get-started/installation/

```bash
Run REST tests:
k6 run k6/rest/restcountries_smoke.js

Run GraphQL tests:
k6 run k6/graphql/rickmorty_smoke.js
```

## 🟣 E2E Tests (Playwright – Python)

Playwright (Python) is used to implement **end-to-end (E2E) tests**, validating UI and user flows in a clean, maintainable, and deterministic way.  
The goal is to demonstrate structure, fixture usage, and stable automation practices as required by the case study.
