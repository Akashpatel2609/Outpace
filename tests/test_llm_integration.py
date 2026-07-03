import os
import pytest
import json
from agents import call_llm, CompetitorSpyAgent, CounterCopywriterAgent, OutpaceOrchestrator

def test_call_llm_missing_key():
    """Verify that call_llm raises ValueError if LLM_API_KEY is not set."""
    if "LLM_API_KEY" in os.environ:
        del os.environ["LLM_API_KEY"]
    
    with pytest.raises(ValueError, match="LLM_API_KEY is not set or is empty"):
        call_llm("Find competitors in legal industry")

def test_call_llm_empty_key():
    """Verify that call_llm raises ValueError if LLM_API_KEY is empty."""
    os.environ["LLM_API_KEY"] = ""
    with pytest.raises(ValueError, match="LLM_API_KEY is not set or is empty"):
        call_llm("Find competitors in legal industry")
    del os.environ["LLM_API_KEY"]

def test_call_llm_dummy_key():
    """Verify that call_llm returns simulated LLM response when LLM_API_KEY='dummy'."""
    os.environ["LLM_API_KEY"] = "dummy"
    try:
        res = call_llm("Find competitors in legal industry")
        assert "[LLM]" in res
    finally:
        del os.environ["LLM_API_KEY"]

def test_spy_agent_llm_path_and_fallback():
    """Verify CompetitorSpyAgent uses LLM when key is dummy, and falls back if LLM fails or is missing."""
    spy = CompetitorSpyAgent()
    
    # 1. Test LLM path active
    os.environ["LLM_API_KEY"] = "dummy"
    try:
        comps = spy.spy("legal", "New York")
        assert len(comps) > 0
        # All returned competitors from the dummy LLM path have "[LLM]" in their competitor name
        assert any("[LLM]" in c["competitor_name"] for c in comps)
    finally:
        del os.environ["LLM_API_KEY"]
        
    # 2. Test fallback when key is missing
    if "LLM_API_KEY" in os.environ:
        del os.environ["LLM_API_KEY"]
    comps = spy.spy("legal", "New York")
    assert len(comps) > 0
    # Output should come from combinatorial generator (no "[LLM]" prefix)
    assert not any("[LLM]" in c["competitor_name"] for c in comps)
    
    # 3. Test fallback when LLM API fails (e.g. error_trigger)
    os.environ["LLM_API_KEY"] = "error_trigger"
    try:
        comps = spy.spy("legal", "New York")
        assert len(comps) > 0
        # Should gracefully fallback and not contain "[LLM]"
        assert not any("[LLM]" in c["competitor_name"] for c in comps)
    finally:
        del os.environ["LLM_API_KEY"]

def test_copywriter_agent_llm_path_and_fallback():
    """Verify CounterCopywriterAgent uses LLM when key is dummy, and falls back if LLM fails or is missing."""
    copywriter = CounterCopywriterAgent()
    mock_competitors = [{
        "competitor_name": "Test Competitor",
        "headline": "Test Headline",
        "description": "Test Desc",
        "channels": ["Google Search"],
        "estimated_monthly_spend": 2000,
        "weaknesses": ["high retainer fees"]
    }]
    
    # 1. Test LLM path active
    os.environ["LLM_API_KEY"] = "dummy"
    try:
        ads = copywriter.generate_counter_ads("MyBusiness", "legal", mock_competitors)
        assert len(ads) > 0
        # Dummy copywriter response has '[LLM]' in headlines
        assert any("[LLM]" in ad["headline"] for ad in ads)
    finally:
        del os.environ["LLM_API_KEY"]
        
    # 2. Test fallback when key is missing
    if "LLM_API_KEY" in os.environ:
        del os.environ["LLM_API_KEY"]
    ads = copywriter.generate_counter_ads("MyBusiness", "legal", mock_competitors)
    assert len(ads) > 0
    assert not any("[LLM]" in ad["headline"] for ad in ads)
    
    # 3. Test fallback when LLM API fails
    os.environ["LLM_API_KEY"] = "error_trigger"
    try:
        ads = copywriter.generate_counter_ads("MyBusiness", "legal", mock_competitors)
        assert len(ads) > 0
        assert not any("[LLM]" in ad["headline"] for ad in ads)
    finally:
        del os.environ["LLM_API_KEY"]

def test_orchestrator_e2e_integration_fallback():
    """Verify the orchestrator integrates both agents and runs without error under all states."""
    orchestrator = OutpaceOrchestrator()
    
    # E2E - no key (standard test_e2e.py environment)
    if "LLM_API_KEY" in os.environ:
        del os.environ["LLM_API_KEY"]
    res = orchestrator.run_arbitrage_strategy("MyBusiness", "legal", "New York")
    assert res["business_name"] == "MyBusiness"
    assert len(res["competitors"]) > 0
    assert len(res["all_proposed_ads"]) > 0
    
    # E2E - with dummy key
    os.environ["LLM_API_KEY"] = "dummy"
    try:
        res_llm = orchestrator.run_arbitrage_strategy("MyBusiness", "legal", "New York")
        assert res_llm["business_name"] == "MyBusiness"
        assert any("[LLM]" in c["competitor_name"] for c in res_llm["competitors"])
        assert any("[LLM]" in ad["headline"] for ad in res_llm["all_proposed_ads"])
    finally:
        del os.environ["LLM_API_KEY"]

def test_agents_fallback_on_invalid_json():
    """Verify that agents fallback gracefully to combinatorial engine when LLM returns invalid JSON."""
    from unittest.mock import patch
    
    os.environ["LLM_API_KEY"] = "dummy"
    try:
        with patch("agents.call_llm", return_value="This is not valid JSON"):
            # 1. CompetitorSpyAgent fallback
            spy = CompetitorSpyAgent()
            comps = spy.spy("legal", "New York")
            assert len(comps) > 0
            # Output should come from combinatorial generator (no "[LLM]" prefix)
            assert not any("[LLM]" in c["competitor_name"] for c in comps)
            
            # 2. CounterCopywriterAgent fallback
            copywriter = CounterCopywriterAgent()
            mock_competitors = [{
                "competitor_name": "Test Competitor",
                "headline": "Test Headline",
                "description": "Test Desc",
                "channels": ["Google Search"],
                "estimated_monthly_spend": 2000,
                "weaknesses": ["high retainer fees"]
            }]
            ads = copywriter.generate_counter_ads("MyBusiness", "legal", mock_competitors)
            assert len(ads) > 0
            assert not any("[LLM]" in ad["headline"] for ad in ads)
    finally:
        del os.environ["LLM_API_KEY"]

