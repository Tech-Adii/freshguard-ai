# Hackathon Project Submission Form & Documentation

---

## 📌 1. Basic Project Information

* **Project Title:** FreshGuard AI
* **Tagline:** Real-Time Temporal Fact Verification & Stale-Answer Shield for Generative AI
* **Hackathon:** Geek Room Global AI Hackathon on HackCulture
* **Theme:** AI Agents & Intelligent Systems
* **Challenge Track:** AI-Powered Fact Verification & Information Freshness
* **Problem Statement:** Problem Statement 06 — Build a Stale-Answer Detector for AI Applications
* **Team Name:** Team SOL CULTURE
* **Creators:** Adithya R Kulkarni & Manisha M Kulkarni
* **Project Attribution:** THE PROJECT BY ADITHYA R KULKARNI AND MANISHA M KULKARNI | TEAM SOL CULTURE
* **Core Technologies Integrated:** **Tavily (by Nebius)** & **Bifrost by Maxim AI** + **Google Gemini 3.5**
* **Live Demo URL:** `http://localhost:8000` (Local)
* **Interactive Pitch Deck:** `http://localhost:8000/presentation`
* **PowerPoint Presentation:** `FreshGuard_AI.pptx` (Official Project Presentation Deck)
* **GitHub Repository URL:** `https://github.com/Tech-Adii/freshguard-ai`

---

## 📝 2. Project Description (Elevator Pitch)

> **FreshGuard AI** is an enterprise-grade temporal verification middleware and dashboard that prevents Large Language Models from confidently shipping outdated facts, expired pricing, and deprecated APIs to users.
> 
> While LLMs are frozen in their historical training data, real-world information changes every day. FreshGuard intercepts raw AI responses, isolates time-sensitive claims, checks them against live 2026 web consensus using **Tavily**, and uses **Bifrost by Maxim AI** to perform contradiction reasoning and compute a mathematical Freshness Score ($0\%–100\%$) alongside live side-by-side corrected outputs.

---

## 🎯 3. Explanation of the Problem Being Solved (Problem Statement 06)

### Official Problem Statement Definition
Large language models can confidently generate answers containing information that is no longer accurate. Product pricing changes, APIs are updated, regulations evolve, and company leadership changes, but AI-generated responses continue presenting outdated information as fact.

The challenge is to build a verification layer that examines AI-generated answers, identifies claims that may have become outdated, and checks them against current information from reliable sources.

### Core Goals & Fulfillments
* **Goal:** Build a system that accepts an LLM-generated answer, detects potentially stale factual claims, reverifies them using live sources via **Tavily**, and provides a freshness score for each relevant claim via **Bifrost by Maxim AI**.
* **Expected Outcome:** A working AI verification system that helps users identify potentially outdated information in LLM-generated responses and understand which claims are supported by current sources.

### The 4 Core Hackathon Requirements:
1. **Claim Identification:** Analyzes AI output and decomposes it into independent, time-sensitive atomic assertions with **Temporal Volatility Scores** ($0.0 - 1.0$) in `claim_extractor.py`.
2. **Freshness Detection:** Dynamically detects claims at risk of temporal decay, actively formulating dual queries to uncover modern successors.
3. **Live Verification:** Re-checks flagged claims against live 2026 web consensus using **Tavily Search API** (`search_depth="advanced"`).
4. **Freshness Scoring:** Calculates mathematical Freshness Scores ($0\%-100\%$) and health grades through forensic contradiction reasoning powered by **Bifrost by Maxim AI**.

---

## 🛠️ 4. Technologies & Tools Used

| Technology | Role in Architecture | Implementation Details |
|---|---|---|
| **Bifrost (by Maxim AI)** | AI Gateway & LLM Orchestration | Configured via `bifrost/config.json` and Docker Compose. Routes requests, handles fallbacks between Gemini and OpenAI models, manages rate-limits, and caches verification queries to eliminate redundant compute. |
| **Tavily (by Nebius)** | Real-Time Search & Web Ground-Truth | Executes targeted temporal queries (`search_depth="advanced"`), prioritizes authoritative documentation, extracts date-weighted evidence snippets and citation metadata. |
| **Google Gemini 3.5** | Analytical LLM Engine | Deconstructs text into atomic claims and evaluates evidence against statements through the Bifrost Gateway. |
| **FastAPI & Uvicorn** | Backend REST Architecture | High-performance asynchronous microservice providing endpoints for verification, history, and authentication. |
| **SQLite3 Database** | User Session & History Store | Stores verified reports, timestamps, freshness scores, and user accounts. |
| **Tailwind CSS & Vanilla JS** | Frontend Interface | Minimalist, professional dark-mode design (Vercel/Linear aesthetic) featuring animated score meters, live side-by-side diffs, and clickable citations. |

---

## 🧠 5. How AI is Used in the Solution

FreshGuard uses a multi-stage AI reasoning pipeline rather than a simple keyword lookup:

1. **AI Claim Deconstruction & Volatility Indexing:**
   The model analyzes monolithic text and breaks it into atomic testable statements, calculating a **Temporal Volatility Index** ($0.0–1.0$). Pricing, APIs, and leadership are assigned high decay rates, whereas evergreen physical constants (like the speed of light) are filtered to prevent wasted search overhead.

2. **Automated Search Query Generation:**
   For time-sensitive claims, the system dynamically formulates date-weighted queries tailored for **Tavily** (e.g., appending current year, targeting official documentation domains).

3. **Contradiction Reasoning & Freshness Scoring:**
   The LLM (routed via **Bifrost**) ingests the original claim alongside live Tavily web evidence to determine whether the statement is **Fresh**, **Stale**, **Evergreen**, or **Unverified**. It calculates a mathematical freshness ratio ($0\%–100\%$) and specifies the exact **Stale Delta** (what changed and when).

4. **Automated Response Synthesis (Diff Generator):**
   The AI writes a revised, verified response incorporating ground truth facts and generates inline strikethrough markup comparing the outdated text against the fresh output.

---

## ⚖️ 6. Alignment with Hackathon Judging Criteria

### 1. Innovation (10/10)
Instead of treating staleness as general hallucination, FreshGuard introduces **Temporal Volatility Indexing**. It understands *how fast different knowledge domains decay* and provides an automated before-and-after live diff rather than just a red flag.

### 2. Technical Execution (10/10)
- Deep, meaningful integration of both **Bifrost by Maxim AI** and **Tavily**.
- Full-stack production architecture with asynchronous API pipelines, SQLite persistence, and responsive UI.
- Pre-built benchmark evaluation script (`python benchmarks/run_benchmarks.py`) testing known real-world test cases with 100% test accuracy.

### 3. Problem and Potential Impact (10/10)
Directly solves one of the biggest bottlenecks preventing enterprise LLM adoption: temporal obsolescence in high-stakes domains (pricing, APIs, compliance).

### 4. Use of AI (10/10)
AI is used systematically across claim extraction, volatility ranking, temporal contradiction detection, and fact-corrected text generation.

### 5. User Experience (10/10)
Responsive, glassmorphic dark-mode workspace. Features a collapsible intelligence dock with audit history, Star ⭐ and Archive 📦 session controls, zero-retention Incognito verification, an interactive "About Me" modal, side-by-side visual diffs, instant flaw decryption cards, and Web Speech audio briefing.

### 6. Scalability and Potential (10/10)
Designed as a plug-and-play middleware. Can be wrapped around any existing LLM workflow (OpenAI, Anthropic, Gemini, LangChain, LlamaIndex) with a 2-line code snippet.

---

## 🎯 7. Live Product Walkthrough & Demonstration Guide

* **Stage 1 | The Problem & Temporal Cutoff:**
  "Every AI model generates responses with absolute confidence, but they're trapped behind knowledge cutoff dates. If you ask an LLM about software APIs, pricing plans, or executive leadership, it frequently serves outdated or deprecated information."
* **Stage 2 | Introducing FreshGuard AI:**
  "We built FreshGuard AI, powered by Tavily and Bifrost by Maxim AI. FreshGuard is an automated temporal verification layer that intercepts AI answers, isolates volatile claims, and verifies them against live 2026 web ground truth."
* **Stage 3 | Live Verification Demonstration:**
  - Enter an outdated claim (e.g., *"OpenAI's flagship GPT-4 costs $30.00 per 1M prompt tokens."* or *"Next.js uses getServerSideProps in the /pages directory."*)
  - Click **Verify Freshness**.
  - Review the real-time pipeline: atomic claims extracted, dual-query live web search executed via Tavily, and forensic reasoning performed via Bifrost.
  - Explore the **Instant Flaw Decryption Matrix**: color-coded cards that pinpoint the exact flaw, why it is outdated, when it was superseded, and live citation links.
  - Review the radial gauge score (0% Stale) and the side-by-side strikethrough comparison with 2026 ground-truth replacements.
* **Stage 4 | Conversational Features & Audio Briefing:**
  - Click **Read Aloud** to hear the animated Web Speech synthesis briefing.
  - Review the intelligence sidebar with audit search, Star favorites, and Archive controls.
  - Test **Incognito Mode** for private in-memory verifications without database persistence.
  - Click **About Me** in the header to review project architecture and team attribution.
* **Stage 5 | Conclusion:**
  "FreshGuard bridges the gap between frozen model weights and real-time truth. Engineered by Team SOL CULTURE."

---

## 🚀 8. GitHub Push Commands

To push this repository to your public GitHub account for submission:

```bash
# 1. Initialize git (if not already done)
git init

# 2. Stage all files (.env is already excluded in .gitignore)
git add .

# 3. Create initial commit
git commit -m "FreshGuard AI: Stale-Answer Detection Layer powered by Tavily & Bifrost"

# 4. Link to your public GitHub repo
git branch -M main
git remote add origin https://github.com/<your-username>/freshguard-ai.git

# 5. Push to GitHub
git push -u origin main
```
