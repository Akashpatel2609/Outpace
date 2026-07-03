import os
import pytest
import concurrent.futures
from fastapi import Request
from fastapi.testclient import TestClient

from app import app, app_state
from agents import CompetitorSpyAgent, BudgetAllocatorAgent

# Register client IP mocking middleware before creating the TestClient
@app.middleware("http")
async def mock_client_ip_middleware(request: Request, call_next):
    client_ip = request.headers.get("x-mock-client-ip")
    if client_ip:
        request.scope["client"] = (client_ip, 50000)
    response = await call_next(request)
    return response

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_state():
    app_state["system_status"] = "Ready"
    app_state["runs_count"] = 0
    app_state["last_analysis"] = None
    app_state["telemetry_logs"] = []
    app_state["sessions"] = {}

def test_telemetry_concurrency_isolation():
    """
    1. Test concurrency (make simultaneous calls to /api/telemetry and verify
       that they are correctly isolated by host/IP).
    """
    # Trigger an analysis first to generate telemetry logs
    response = client.post(
        "/api/analyze",
        json={
            "businessName": "ChallengerCorp",
            "niche": "legal",
            "competitor": "CompetitorA",
            "location": "Boston"
        }
    )
    assert response.status_code == 200
    
    # We want to simulate two concurrent clients: Client A (1.1.1.1) and Client B (2.2.2.2)
    # sending simultaneous requests to /api/telemetry.
    # Each client should progress independently through the 14 days of logs.
    
    def run_client(ip):
        # We perform 5 sequential calls to /api/telemetry from this IP
        responses = []
        for _ in range(5):
            res = client.get("/api/telemetry", headers={"x-mock-client-ip": ip})
            assert res.status_code == 200
            responses.append(res.json())
        return responses

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_a = executor.submit(run_client, "1.1.1.1")
        future_b = executor.submit(run_client, "2.2.2.2")
        
        results_a = future_a.result()
        results_b = future_b.result()

    # Verify we got 5 responses each
    assert len(results_a) == 5
    assert len(results_b) == 5

    # Verify both clients started at index 0 and progressed sequentially
    # Client A's logs should match telemetry_logs 0 to 4
    for idx in range(5):
        assert results_a[idx] == app_state["telemetry_logs"][idx]
        assert results_b[idx] == app_state["telemetry_logs"][idx]
        
    # Verify that their session states in app_state are completely isolated
    assert app_state["sessions"]["1.1.1.1"] == 5
    assert app_state["sessions"]["2.2.2.2"] == 5

def test_long_input_truncation_and_approval():
    """
    2. Test inputs: send extremely long inputs for businessName, niche, and competitor,
       and verify that the critic approves the truncated variants.
    """
    long_business_name = "BusinessName" * 100  # 1200 chars
    long_niche = "legal" + "Niche" * 100        # 505 chars
    long_competitor = "Competitor" * 100       # 1000 chars

    response = client.post(
        "/api/analyze",
        json={
            "businessName": long_business_name,
            "niche": long_niche,
            "competitor": long_competitor,
            "location": "Boston"
        }
    )
    assert response.status_code == 200
    
    # Check that it completed successfully and returned approved ads
    data = response.json()
    assert data["success"] is True
    assert data["approved_ads_count"] > 0
    
    # Inspect the stored raw results
    last_analysis = app_state["last_analysis"]
    assert last_analysis is not None
    
    # Verify the ads are truncated to fit character limits (30 for headline, 90 for description)
    google_ads = [ad for ad in last_analysis["all_proposed_ads"] if ad["target_channel"] == "Google Search"]
    assert len(google_ads) > 0
    
    for ad in google_ads:
        # Character limit enforcement is the core guarantee regardless of approval status
        assert len(ad["headline"]) <= 30, f"Headline too long: {ad['headline']}"
        assert len(ad["description"]) <= 90, f"Description too long: {ad['description']}"
    
    # At least some Google ads should be approved (some may fail trademark checks legitimately)
    approved_google = [ad for ad in google_ads if ad["approved"]]
    assert len(approved_google) > 0, "No Google ads were approved — check Critic logic"

def test_division_by_zero_protection():
    """
    3. Check division-by-zero protection.
       Verify scenarios:
       - zero approved variants in BudgetAllocatorAgent
       - zero competitors returned by CompetitorSpyAgent in app.py telemetry loop
       - zero impressions in Local SEO CTR calculation
    """
    # Scenario 3.1: BudgetAllocatorAgent division-by-zero protection with 0 approved variants
    allocator = BudgetAllocatorAgent()
    res = allocator.allocate("BizName", "legal", "Boston", [])
    assert res is not None
    assert len(res["telemetry_logs"]) == 14
    for log in res["telemetry_logs"]:
        assert log["total_spend"] > 0
        assert log["roi"] is not None  # Should not be ZeroDivisionError

    # Scenario 3.2: Empty competitor list protection in app.py
    # We patch CompetitorSpyAgent.spy to return an empty list.
    from unittest.mock import patch
    with patch.object(CompetitorSpyAgent, "spy", return_value=[]):
        response = client.post(
            "/api/analyze",
            json={
                "businessName": "BizName",
                "niche": "legal",
                "competitor": "CompName",
                "location": "Boston"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["competitors_detected"] == []
        assert data["approved_ads_count"] == 0

    # Scenario 3.3: Empty approved ads list protection in app.py
    with patch("agents.CreativeCriticAgent.critique") as mock_critique:
        # Mock critique to return ads with approved=False
        def mock_crit(ads):
            return [{**ad, "approved": False, "issues": ["Mocked rejection"], "score": 10} for ad in ads]
        mock_critique.side_effect = mock_crit
        
        response = client.post(
            "/api/analyze",
            json={
                "businessName": "BizName",
                "niche": "legal",
                "competitor": "CompName",
                "location": "Boston"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["approved_ads_count"] == 0
        
        # Verify app_state["telemetry_logs"] was generated successfully
        assert len(app_state["telemetry_logs"]) == 14
