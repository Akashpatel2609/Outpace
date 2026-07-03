# Outpace 🎯

> **Autonomous Competitor Ad Arbitrage & Counter-Campaign Optimization System**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-green.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal.svg)](https://fastapi.tiangolo.com)

---

## What is Outpace?

Outpace is an autonomous multi-agent system that detects what local competitors are actively advertising, reverse-engineers their strategy, and autonomously launches targeted counter-campaigns designed to steal their traffic.

Think of it as a **real-time competitive ad intelligence engine** with a built-in AI copywriter, policy compliance critic, and dynamic budget portfolio allocator — all working autonomously in a closed-loop.

---

## The Problem

Local businesses (dentists, lawyers, real estate agents, plumbers) collectively spend **billions of dollars on digital ads** every year, but most compete blindly. They have no visibility into:
- What their competitors are actively promoting right now
- Which weaknesses those ads expose (e.g., expensive pricing, slow service)
- How to quickly generate compelling counter-ads that exploit those gaps
- How to optimally shift budget across channels (Google vs. Meta vs. SEO) based on performance

Outpace solves all four problems with a single autonomous agent pipeline.

---

## Agent Architecture

Outpace uses a **4-agent orchestration pipeline** powered by a FastAPI backend:

```
┌──────────────────────────────────────────────────────┐
│                 Outpace Frontend               │
│   (Dark-mode glassmorphism dashboard, Chart.js)      │
└─────────────────────┬────────────────────────────────┘
                      │ REST API (polling + on-demand)
┌─────────────────────▼────────────────────────────────┐
│                Outpace Backend (FastAPI)        │
│      /api/analyze  /api/status  /api/telemetry       │
└─────────────────────┬────────────────────────────────┘
                      │ Orchestrator runs pipeline
┌─────────────────────▼────────────────────────────────┐
│              OutpaceOrchestrator               │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ 1. CompetitorSpyAgent                         │   │
│  │    Discovers local competitors, extracts      │   │
│  │    active ads, channels & weaknesses          │   │
│  └───────────────────┬──────────────────────────┘   │
│                      ▼                               │
│  ┌──────────────────────────────────────────────┐   │
│  │ 2. CounterCopywriterAgent                     │   │
│  │    Drafts targeted counter-ads exploiting     │   │
│  │    competitor weaknesses (Google + Meta)      │   │
│  └───────────────────┬──────────────────────────┘   │
│                      ▼                               │
│  ┌──────────────────────────────────────────────┐   │
│  │ 3. CreativeCriticAgent                        │   │
│  │    Validates copy against ad platform rules  │   │
│  │    (30-char headline, 90-char description,   │   │
│  │    banned terms, trademark checks)            │   │
│  └───────────────────┬──────────────────────────┘   │
│                      ▼                               │
│  ┌──────────────────────────────────────────────┐   │
│  │ 4. BudgetAllocatorAgent                       │   │
│  │    Simulates 14-day bidding campaign,         │   │
│  │    dynamically shifting budget across         │   │
│  │    Google Search, Meta Ads & Local SEO        │   │
│  └──────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────┘
```

---

## Key Features

| Feature | Description |
|---|---|
| 🕵️ **Competitor Spy Agent** | Detects active competitor ads by industry & location |
| ✍️ **Counter-Copywriter Agent** | Drafts targeted counter-ads based on competitor weaknesses |
| ✅ **Creative Critic Agent** | Validates all copy against Google/Meta ad policy rules |
| 📊 **Budget Allocator Agent** | Runs a 14-day bidding simulation with dynamic channel allocation |
| 🎨 **Premium Dashboard** | Glassmorphism UI with real-time Chart.js graphs and agent logs |
| 🆓 **100% Free to Run** | Zero external API keys needed — runs fully locally in mock mode |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11+, FastAPI, Uvicorn |
| **Agent Engine** | Custom modular Python agent classes |
| **Data Layer** | In-memory state (no database required) |
| **Frontend** | HTML5, Vanilla JS (ES6+), Vanilla CSS |
| **Charting** | Chart.js (CDN) |
| **Testing** | pytest, fastapi.testclient, BeautifulSoup4 |
| **Hosting** | Vercel (frontend static) + local Python server |

---

## Setup & Local Development

### Prerequisites
- Python 3.11+
- pip

### 1. Clone the Repository
```bash
git clone https://github.com/Akashpatel2609/Outpace.git
cd Outpace
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Backend Server
```bash
python app.py
```
The API server will start at `http://localhost:8000`.  
API docs available at: `http://localhost:8000/docs`

### 4. Open the Frontend
Open `index.html` directly in your browser, **or** serve it with any static file server:
```bash
# Using Python's built-in server
python -m http.server 3000
```
Then visit `http://localhost:3000`.

> **Note**: The frontend automatically falls back to a local simulation engine if the backend API is not running, so you can demo it standalone too.

---

## API Reference

### `GET /api/status`
Returns the current system state.

```json
{
  "status": "Ready",
  "runs_completed": 1,
  "has_analyzed_data": true,
  "last_analysis_summary": {
    "business_name": "Apex Dental",
    "industry": "dentist",
    "location": "Austin TX",
    "competitors_found": 4,
    "approved_variants": 12
  }
}
```

### `POST /api/analyze`
Triggers the full 4-agent arbitrage pipeline.

**Request Body:**
```json
{
  "businessName": "Apex Dental",
  "niche": "dentist",
  "competitor": "Bright Smile Dental",
  "location": "Austin TX"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Arbitrage analysis and simulation completed successfully.",
  "business_name": "Apex Dental",
  "competitors_detected": ["Bright Smile Dental Austin TX", "Metro Dental Care Austin TX"],
  "approved_ads_count": 12,
  "budget_allocation": { ... }
}
```

### `GET /api/telemetry`
Returns the next day's simulated campaign performance frame (session-aware, polls sequentially through all 14 days).

---

## Running the Test Suite

```bash
pytest -v tests/test_e2e.py
```

The test suite contains **49 E2E tests** covering:
- Competitor discovery across industries (dentist, legal, real estate)
- Counter-ad generation and policy compliance checks
- Budget allocation weights and telemetry structure
- UI DOM structure validation
- Full end-to-end API flow scenarios

Expected result: `49 passed`

---

## Deployment (Vercel)

The frontend (`index.html`, `style.css`) can be deployed for free on Vercel.

1. Push your repo to GitHub
2. Import the repo on [vercel.com](https://vercel.com)
3. Set the output directory to `.` (root)
4. Deploy — done!

For the Python backend, deploy using [Railway](https://railway.app), [Render](https://render.com), or [Fly.io](https://fly.io) (all have free tiers).

---

## Project Structure

```
Outpace/
├── agents.py               # Core agent classes (Spy, Copywriter, Critic, Allocator, Orchestrator)
├── app.py                  # FastAPI backend server
├── index.html              # Frontend dashboard (single-page app)
├── style.css               # Premium dark-mode glassmorphism styles
├── run_tests.py            # Test runner script
├── requirements.txt        # Python dependencies
├── tests/
│   └── test_e2e.py         # 49-case E2E test suite
├── TEST_INFRA.md           # Test architecture documentation
└── README.md               # This file
```

---

## Kaggle Capstone — Freestyle Track

This project was built for the **Kaggle 5-Day AI Agents Intensive Capstone Project** (Freestyle Track).

**Agent concepts demonstrated:**
- ✅ Multi-agent system with specialized roles (ADK pattern)
- ✅ Sequential agent orchestration with feedback loops
- ✅ Self-correcting creative critic loop (policy compliance)
- ✅ Simulated real-world tool use (competitor scraping, ad library analysis)
- ✅ Deployability (FastAPI + Vercel)
- ✅ Security: No API keys stored or required; input validation on all endpoints

---

## License

MIT License — see [LICENSE](LICENSE) for details.
