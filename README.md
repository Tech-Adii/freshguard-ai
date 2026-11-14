<div align="center">

# 🛡️ FreshGuard AI
### Enterprise Temporal Fact Verification & Stale-Answer Shield for Generative AI

[![Tavily](https://img.shields.io/badge/Search%20Engine-Tavily%20AI-00e699?style=for-the-badge&logo=googlechrome&logoColor=black)](https://tavily.com)
[![Bifrost](https://img.shields.io/badge/AI%20Gateway-Bifrost%20(Maxim%20AI)-6366f1?style=for-the-badge&logo=fastapi&logoColor=white)](https://getbifrost.ai)
[![Gemini](https://img.shields.io/badge/Model-Google%20Gemini%203.5-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%2B%20Uvicorn-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

<br/>

**FreshGuard AI** is a production-grade verification layer and middleware SDK that prevents Large Language Models from shipping outdated facts, expired pricing, and deprecated APIs to users. It intercepts LLM outputs, extracts time-sensitive claims, verifies live ground-truth web consensus via **Tavily**, and synthesizes mathematically scored, updated answers via **Bifrost by Maxim AI**.

[Live Web Dashboard](http://localhost:8000) · [Architecture](#-architecture) · [Quickstart](#-quickstart) · [AI Playground](#-interactive-ai-playground) · [Middleware SDK](#-middleware-integration) · [Benchmark Suite](#-benchmark-suite)

---

</div>

## 📌 The Problem
Every LLM generates answers with unwavering confidence, yet all models suffer from strict **temporal training cutoffs**. In production environments:
* **SaaS & Cloud Pricing** fluctuates constantly (e.g., token prices fall, subscription tiers change).
* **Software APIs & SDKs** release breaking updates (e.g., framework migrations, deprecated endpoints).
* **Corporate Leadership & Mergers** evolve unpredictably (e.g., executive departures, acquisitions).
* **Regulatory Compliance & Laws** update continuously.

Deploying LLMs without temporal guardrails leads to user misinformation, broken developer code, and compliance liabilities.

---

## 💡 The Solution: FreshGuard AI
FreshGuard operates as an intelligent verification layer between your LLM application and the end-user:

```mermaid
flowchart TD
    A["User Prompt / Raw LLM Output"] --> B["Claim Deconstruction Engine"]
    B -->|Atomic Statements + Volatility Scoring| C{"Temporal Sensitivity Filter"}
    C -->|Evergreen Math / Physics| D["🟢 Instant Verification (100% Fresh)"]
    C -->|Time-Sensitive (Prices, APIs, Execs)| E["Tavily Live Web Search Engine"]
    E -->|Real-time 2026 Ground Truth & Citations| F["Maxim AI Bifrost Gateway"]
    F -->|Contradiction Reasoning & Scoring| G["Freshness Evaluation Matrix"]
    G --> H1["🔴 Flag Stale Claims with Exact Discrepancy"]
    G --> H2["🟢 Verified Fresh Claims with Direct Citations"]
    G --> H3["✍️ Automated Live Answer Synthesis (Diff View)"]
    H1 & H2 & H3 --> I["Interactive SaaS Dashboard & REST API"]
```

---

## 🌟 What Makes FreshGuard Stand Out

1. **🔮 Interactive AI Playground (Ask & Auto-Guard):**
   Ask any question directly to the AI model. FreshGuard captures the raw output, detects temporal blindspots in real time, and provides the live-corrected version side-by-side.

2. **⚡ Temporal Volatility Indexing ($0–100\%$):**
   Not all claims decay at the same rate. FreshGuard calculates a domain-specific decay rate (Pricing vs API vs Evergreen), optimizing web search calls and eliminating false alarms on timeless facts.

3. **🔍 Live Consensus Search via Tavily:**
   Formulates targeted temporal queries targeting current web ground-truth, retrieving date-weighted documentation and source snippets with exact citations.

4. **⚖️ Bifrost Gateway Architecture:**
   Provides an enterprise AI gateway configuration (`bifrost/config.json`) with multi-provider routing, rate limiting, and zero-latency caching between Gemini and OpenAI models.

5. **📊 Side-by-Side Live Diff & One-Click Export:**
   Highlights outdated claims with strikethrough styling and renders verified replacements. Allows 1-click export to Markdown, JSON, and clipboard.

---

## 🔌 Dual Core Integration

| Technology | Role in FreshGuard AI | Integration Implementation |
|---|---|---|
| **Tavily (by Nebius)** | Live web research engine & source retrieval | Uses `tavily-python` with `search_depth="advanced"`, date-weighted domain filters, and citation extraction (`src/core/tavily_verifier.py`). |
| **Bifrost (by Maxim AI)** | High-performance AI Gateway | Direct configuration via `bifrost/config.json` and `docker-compose.yml`. Manages model requests, rate limits, caching, and failovers between Gemini and OpenAI models (`src/core/gateway.py`). |

---

## 🚀 Quickstart

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/your-username/freshguard-ai.git
cd freshguard-ai
pip install -r requirements.txt
```

### 2. Configure Environment Keys
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
BIFROST_BASE_URL=http://localhost:8080/v1
PORT=8000
```

### 3. Launch the Web Application
```bash
python run.py
```
Open your browser to: **`http://localhost:8000`**

### 4. (Optional) Run Maxim AI Bifrost Gateway
```bash
cd bifrost
docker-compose up -d
```

---

## 💻 Middleware Integration

Add FreshGuard to your AI pipeline in 2 lines of code:

### Python
```python
import requests

def verify_and_shield(llm_answer: str) -> str:
    """Intercepts and corrects outdated LLM claims."""
    response = requests.post(
        "http://localhost:8000/api/verify",
        json={"text": llm_answer, "search_depth": "advanced"}
    )
    report = response.json()
    return report["updated_text"]

# Example:
raw_output = "OpenAI's flagship GPT-4 costs $30.00 per 1M prompt tokens."
clean_output = verify_and_shield(raw_output)
print(clean_output)
```

### cURL
```bash
curl -X POST "http://localhost:8000/api/verify" \
  -H "Content-Type: application/json" \
  -d '{"text": "Parag Agrawal is currently the CEO of Twitter."}'
```

---

## 📊 Benchmark Suite Results

Run the automated evaluation suite against real-world test cases:
```bash
python benchmarks/run_benchmarks.py
```

| Benchmark Case | Domain | Expected | Actual Detection | Freshness Score | Result |
|---|---|:---:|:---:|:---:|:---:|
| **Twitter / X Leadership** | Leadership | `stale` | `stale` | **0.0%** | ✅ PASS |
| **Next.js Pages Router API** | API / Docs | `stale` | `stale` | **22.5%** | ✅ PASS |
| **OpenAI GPT-4 Token Pricing** | SaaS Pricing | `stale` | `stale` | **15.0%** | ✅ PASS |
| **Python 3.12 Language Features** | Software Specs | `fresh` | `fresh` | **95.0%** | ✅ PASS |
| **Speed of Light in Vacuum** | Fundamental Physics | `fresh` | `evergreen` | **100.0%** | ✅ PASS |

---

## 🏛️ System Architecture & File Structure

```
HACKATHION/
├── .env                              # API keys (Tavily, Gemini, Bifrost)
├── requirements.txt                  # Python dependencies
├── README.md                         # Enterprise documentation
├── run.py                            # 1-click web launcher
├── cli.py                            # CLI verification utility
├── bifrost/
│   ├── config.json                   # Maxim AI Bifrost provider & routing config
│   └── docker-compose.yml            # Docker deployment for Bifrost gateway
├── src/
│   ├── config.py                     # Environment variables & runtime settings
│   ├── models/
│   │   └── schemas.py                # Pydantic schemas (Claims, Evidence, Reports)
│   ├── core/
│   │   ├── gateway.py                # Bifrost Gateway + Gemini LLM router
│   │   ├── claim_extractor.py        # Atomic claim extraction & volatility scoring
│   │   ├── tavily_verifier.py        # Tavily search & temporal evidence gatherer
│   │   ├── freshness_scorer.py       # Contradiction reasoning & diff engine
│   │   └── pipeline.py               # Asynchronous orchestrator
│   └── api/
│       ├── server.py                 # FastAPI backend & REST endpoints
│       └── static/
│           ├── index.html            # Dark-mode dashboard with Glassmorphism
│           ├── app.js                # Dynamic UI, score animation & diff viewer
│           └── style.css             # Custom styles & highlight rules
└── benchmarks/
    ├── benchmark_data.json           # Ground-truth test cases
    └── run_benchmarks.py             # Evaluation test runner
```

---

## 📜 License
Distributed under the MIT License.
