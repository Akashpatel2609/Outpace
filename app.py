import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from agents import OutpaceOrchestrator

app = FastAPI(
    title="Outpace API",
    description="Autonomous competitor ad arbitrage tool backend",
    version="1.0.0"
)

# In-memory storage for workspace state and simulated telemetry
app_state = {
    "system_status": "Ready",
    "runs_count": 0,
    "last_analysis": None,
    "telemetry_logs": [],
    "sessions": {}
}

class AnalyzeRequest(BaseModel):
    businessName: str
    niche: str
    competitor: str
    location: str

@app.get("/api/status")
def get_status() -> Dict[str, Any]:
    """
    Returns the current workspace/system state, including details of the last analysis if any.
    """
    return {
        "status": app_state["system_status"],
        "runs_completed": app_state["runs_count"],
        "has_analyzed_data": app_state["last_analysis"] is not None,
        "last_analysis_summary": {
            "business_name": app_state["last_analysis"]["business_name"],
            "industry": app_state["last_analysis"]["industry"],
            "location": app_state["last_analysis"]["location"],
            "competitors_found": len(app_state["last_analysis"]["competitors"]),
            "approved_variants": len(app_state["last_analysis"]["approved_ads"])
        } if app_state["last_analysis"] else None
    }

@app.post("/api/analyze")
def analyze(payload: AnalyzeRequest) -> Dict[str, Any]:
    """
    Triggers the Outpace orchestrator to run competitor spying, counter copywriting,
    critic checks, budget allocation, and telemetry generation.
    """
    if not payload.businessName.strip():
        raise HTTPException(status_code=400, detail="businessName cannot be empty")
    if not payload.niche.strip():
        raise HTTPException(status_code=400, detail="niche cannot be empty")
    if not payload.competitor.strip():
        raise HTTPException(status_code=400, detail="competitor cannot be empty")
    if not payload.location.strip():
        raise HTTPException(status_code=400, detail="location cannot be empty")

    app_state["sessions"] = {}
    app_state["system_status"] = "Analyzing"
    try:
        orchestrator = OutpaceOrchestrator()
        result = orchestrator.run_arbitrage_strategy(
            business_name=payload.businessName,
            industry=payload.niche,
            location=payload.location,
            competitor=payload.competitor
        )
        
        # Save run data into in-memory state
        app_state["last_analysis"] = result
        
        # Transform the raw logs returned by orchestrator.run_arbitrage_strategy 
        # into a list of 14 single-day frame dictionaries under app_state["telemetry_logs"].
        telemetry_frames = []
        
        # Guard: if no competitors were found, skip frame construction entirely
        if not result.get("competitors"):
            app_state["telemetry_logs"] = []
            app_state["runs_count"] += 1
            app_state["system_status"] = "Ready"
            return {
                "success": True,
                "message": "No competitors detected. Analysis complete.",
                "business_name": result["business_name"],
                "competitors_detected": [],
                "approved_ads_count": 0,
                "budget_allocation": result.get("budget_allocation", {})
            }
        
        for day in range(1, 15):
            log = result["telemetry_logs"][day - 1]
            
            # Agent statuses and logs
            spy_status = "running" if day % 3 == 1 else "idle"
            copywriter_status = "running" if day % 3 == 2 else "idle"
            critic_status = "running" if day % 3 == 0 else "idle"
            bidding_status = "running"
            
            # newCompetitorAd — always show one, rotate through competitors
            comp = result["competitors"][day % len(result["competitors"])]
            platform = comp["channels"][0] if comp.get("channels") else "Google Search"
            newCompetitorAd = {
                "platform": platform,
                "title": comp["headline"],
                "body": comp["description"],
                "competitor_name": comp["competitor_name"]
            }
                
            spy_log = f"Scanning Google Search for {comp['competitor_name']} keywords..." if spy_status == "running" else "Listening for fresh ad deployments..."
            copywriter_log = "Drafting counter ad copy based on competitor weakness..." if copywriter_status == "running" else "Standby. Ready to receive targets."
            critic_log = "Verifying compliance against Google & Meta Ad Policies..." if critic_status == "running" else "Scorecard engine active."
            bidding_log = "Real-time allocating budget. Last event: ROI threshold shift (+8%)"
            
            agents = {
                "spy": {"status": spy_status, "lastLog": spy_log},
                "copywriter": {"status": copywriter_status, "lastLog": copywriter_log},
                "critic": {"status": critic_status, "lastLog": critic_log},
                "bidding": {"status": bidding_status, "lastLog": bidding_log}
            }
                
            # newCounterAd — always show one, rotate through approved ads
            newCounterAd = None
            if result.get("approved_ads"):
                ad = result["approved_ads"][day % len(result["approved_ads"])]
                newCounterAd = {
                    "platform": ad["target_channel"],
                    "title": ad["headline"],
                    "body": ad["description"],
                    "score": f"{ad['score']}/100",
                    "scorecard": {
                        "length": f"Optimal ({ad.get('headline_len', len(ad['headline']))} ch)",
                        "clickbait": "Low (12%)" if ad.get("score", 100) > 80 else "Medium (35%)",
                        "policy": "Pass"
                    }
                }
                
            # budget
            g_share = result["budget_allocation"].get("Google Search", {}).get("percentage", 50)
            m_share = result["budget_allocation"].get("Meta Ads", {}).get("percentage", 30)
            s_share = result["budget_allocation"].get("Local SEO", {}).get("percentage", 20)
            
            g_log = log["google_search"]
            m_log = log["meta_ads"]
            s_log = log["local_seo"]
            
            g_spend = g_log["spend"]
            g_conv = g_log["conversions"]
            # Compute ROI from daily log data
            g_revenue = g_conv * 115.0
            g_roi = g_revenue / max(1.0, g_spend)
            
            m_spend = m_log["spend"]
            m_conv = m_log["conversions"]
            m_revenue = m_conv * 100.0
            m_roi = m_revenue / max(1.0, m_spend)
            
            s_spend = s_log["spend"]
            s_conv = s_log["conversions"]
            s_revenue = s_conv * 150.0
            s_roi = s_revenue / max(1.0, s_spend)
            
            s_ctr = (s_conv / max(1, s_log["impressions"])) * 100
            
            budget = {
                "google": {
                    "share": g_share,
                    "ctr": f"{g_log['ctr'] * 100:.2f}",
                    "conversions": g_conv,
                    "roi": f"{g_roi:.1f}x"
                },
                "meta": {
                    "share": m_share,
                    "ctr": f"{m_log['ctr'] * 100:.2f}",
                    "conversions": m_conv,
                    "roi": f"{m_roi:.1f}x"
                },
                "seo": {
                    "share": s_share,
                    "ctr": f"{s_ctr:.2f}",
                    "conversions": s_conv,
                    "roi": f"{s_roi:.1f}x"
                }
            }
            
            # performance
            performance = {
                "ctr": g_log["ctr"] * 100,
                "conversions": log["total_conversions"]
            }
            
            telemetry_frames.append({
                "agents": agents,
                "newCompetitorAd": newCompetitorAd,
                "newCounterAd": newCounterAd,
                "budget": budget,
                "performance": performance
            })
            
        app_state["telemetry_logs"] = telemetry_frames
        app_state["runs_count"] += 1
        app_state["system_status"] = "Ready"
        
        # Return summary and recommendations to client
        return {
            "success": True,
            "message": "Arbitrage analysis and simulation completed successfully.",
            "business_name": result["business_name"],
            "competitors_detected": [c["competitor_name"] for c in result["competitors"]],
            "approved_ads_count": len(result["approved_ads"]),
            "budget_allocation": result["budget_allocation"]
        }
    except Exception as e:
        app_state["system_status"] = "Error"
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/telemetry")
def get_telemetry(request: Request) -> Dict[str, Any]:
    """
    Fetches simulated day-by-day bidding tracking logs from the latest run.
    """
    if "sessions" not in app_state:
        app_state["sessions"] = {}
    if not app_state["telemetry_logs"]:
        raise HTTPException(
            status_code=404, 
            detail="No telemetry data found. Please run an /api/analyze request first."
        )
    session_id = request.headers.get("x-mock-client-ip") or request.headers.get("x-test-client-ip")
    if not session_id:
        session_id = request.client.host if (request.client and request.client.host) else "default"
    idx = app_state["sessions"].get(session_id, 0)
    
    if idx >= len(app_state["telemetry_logs"]):
        result_log = app_state["telemetry_logs"][-1]
    else:
        result_log = app_state["telemetry_logs"][idx]
        
    app_state["sessions"][session_id] = idx + 1
    return result_log

if __name__ == "__main__":
    # Allow running server directly using: python app.py
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
