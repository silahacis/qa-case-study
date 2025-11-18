# QA Engineer Case Study – Public APIs x K6 + Playwright

This repository demonstrates a complete QA automation setup across **API** and **UI** layers,  
using two widely adopted tools:

- **K6 (JavaScript)** → REST + GraphQL API integration tests  
- **Playwright (Python)** → Browser-based E2E tests  
- **GitHub Actions CI** → Automated runs on every pull request  

The goal is to show real-world QA practices:  
clear test design, meaningful assertions, stable execution, and CI readiness.

---

# 📁 Project Deliverables

- **K6 integration tests**  
  - REST + GraphQL  
  - Happy path, edge cases, performance thresholds, basic load profile  

- **Playwright (Python) E2E tests**  
  - Login, inventory, product detail, add-to-cart, checkout (pre-payment)  
  - Screenshots on failure  

- **GitHub Actions Workflows**  
  - Separate pipelines for K6 & Playwright  

- **Local runner script**  
  - `bash scripts/run_local.sh` → Runs ALL tests with one command  

---

# 🔵 K6 Integration Tests (REST + GraphQL)

K6 is used to test two public APIs:

| Type     | Endpoint |
|----------|----------|
| REST     | https://restcountries.com |
| GraphQL  | https://rickandmortyapi.com/graphql |

## ✔ Functional (Happy Path)

### RESTCountries
- `200 OK`  
- Valid JSON  
- Required fields exist (`name.official`, `capital[]`, `region`)  
- Business check: **official name must be “Republic of Turkey”**  

### Rick & Morty GraphQL
- `200 OK`  
- Valid JSON  
- `data.character.id === "1"`  
- Character name: **“Rick Sanchez”**  
- `origin.name` exists  
- No GraphQL errors for valid queries  

---

## ⚠ Edge Case Coverage

### REST
- Invalid country name  
- Partial search (`"tur"`)  
- Numeric input  
- Special characters  
- Empty query (`/name/`)  

### GraphQL
- Invalid character ID → `null` or `errors[]`  
- Invalid field → schema error  
- GraphQL `errors[]` validation  

All tests follow the case study guideline:

---

## 📊 Performance Thresholds (SLAs)

Thresholds are applied **only to happy-path requests**.

| API | SLA |
|-----|-----|
| REST | **p95 < 600ms** |
| GraphQL | **p95 < 800ms** |

### Why different values?
- REST is simple JSON → naturally faster  
- GraphQL has resolvers, nested fields → slower by design  

### Why p95?
- Industry standard percentile  
- More stable than max/avg  
- Less sensitive to network spikes  

---

## 🧩 Threshold Tuning Strategy  

- Start conservative (600–800ms)  
- Collect CI data  
- Gradually tighten  
  - REST: 600 → 500 → 400  
  - GraphQL: 800 → 700 → 600  
- Freeze SLAs once stable  

---

## 🛡 Flakiness Controls

- Thresholds apply to `group:happy` only  
- JSON parsing wrapped in `try/catch`  
- Edge cases do not break SLAs  
- Low VU load to avoid rate limits  
- No external state dependency  

---

# 🟣 Playwright E2E Tests (Python)

UI tests are implemented using **SauceDemo**, a common app for QA exercises.

## ✔ Covered Scenarios

### Login Tests
- Successful login  
- Locked-out user  
- Invalid credentials  

### Inventory Page
- Validate product listing  
- Open product details  

### Add to Cart
- Add first product  
- Cart badge update  
- Item appears on cart page  

### Checkout (Pre-payment)
- Fill user information  
- Validate summary page  
- Confirm item & prices  

### Stability
- Screenshots saved **only on failure**  
- Auto-wait built into Playwright (no sleeps)  
- Deterministic selectors (`data-test=` attributes)  

---

# ▶️ Running Tests Locally

This project includes a **local runner script**:

```
bash scripts/run_local.sh
```

This script runs:

- K6 REST tests  
- K6 GraphQL tests  
- Playwright E2E tests  

BUT:  
Playwright lives inside a **virtual environment**,  
so you must **activate venv first**, or pytest won’t be found.

---

## 🔧 1) First-Time Setup

```bash
cd playwright-python
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash/WSL)
pip install -r requirements.txt
playwright install --with-deps
cd ..
```

> ⚠ Windows PowerShell does **not** support `source`.  
> Use **Git Bash**, **WSL**, or CMD.

---

## ▶️ 2) Run All Tests with One Command

From project root:

```bash
# activate virtual environment
cd playwright-python
source venv/Scripts/activate
cd ..

# run all tests
bash scripts/run_local.sh
```

### The script will:
✔ Run K6 REST tests  
✔ Run K6 GraphQL tests  
✔ Run Playwright tests in your active venv  
✔ Save screenshots on failures  
✔ Generate JSON outputs  

---

# 🤖 GitHub Actions (CI)

CI pipelines run automatically on every pull request:

```
.github/workflows/
│── k6-integration.yml
└── playwright-e2e.yml
```

Artifacts uploaded:

- K6 JSON results  
- Playwright screenshots (on failure)  

---

# 🎉 Summary

This case study demonstrates:

- Strong separation of API + UI testing  
- Clean K6 test design (happy path, edge cases, thresholds, load)  
- Stable Playwright E2E structure  
- Full CI automation  
- Local runner for convenience  
- Conservative + explainable performance decisions
