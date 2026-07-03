# Original User Request

## Initial Request — 2026-07-02T23:35:08-04:00

An autonomous competitor ad arbitrage and counter-campaign optimization system named "CounterStrike". It monitors local competitor ads, drafts targeted counter-offers to exploit competitor weaknesses, and runs a simulated campaign bidding optimization loop.

Working directory: c:/Users/akash/OneDrive/Desktop/Work/Projects/Data Analysis/AllStack/Kaggle Capstone Project
Integrity mode: demo

## Requirements

### R1. Competitor Search and Ad Scraping
The system must discover local competitors and identify active ad offers based on target niche and location inputs.

### R2. Counter-Ad Creation and Compliance Audit
The system must generate highly competitive counter-ad variants targeting identified competitor weaknesses, scoring each variant against standard ad policy rules (e.g. Google Search ad headline limits of 30 characters, descriptions of 90 characters).

### R3. Dynamic Budget Allocation and Campaign Simulation
The system must run a simulated bidding loop that shifts budgets dynamically across Google Search, Meta Ads, and Local SEO, displaying performance metrics (CTR, conversions, ROI) over time.

### R4. Premium Dashboard Interface
The system must present a beautiful, responsive, dark-mode glassmorphism dashboard visualization connecting to the backend endpoints.

## Acceptance Criteria

### Execution & Visual Integrity
- [ ] Competitor ads are successfully detected and mock-presented in the UI.
- [ ] Generated counter-ads are output with policy compliance scorecards.
- [ ] Budget distribution chart visualizes optimization progression using Chart.js.
- [ ] Backend API endpoints (/api/status, /api/analyze, /api/telemetry) function correctly and integrate with the frontend.
