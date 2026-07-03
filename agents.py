import re
import random
import logging
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Outpace.Agents")

class CompetitorSpyAgent:
    """
    Scrapes/mocks competitor ad information based on industry and location.
    Provides realistic competitors, their current ads, channels, and weaknesses.
    """
    def __init__(self):
        # Predefined templates for common industries to make the mockup highly realistic
        self.industry_templates = {
            "legal": {
                "competitors": ["Apex Law Group", "Justice Associates", "The Vanguard Firm"],
                "weaknesses": ["high retainer fees", "slow communication", "complex pricing structure", "lack of mobile app"],
                "ad_headlines": ["Need Legal Help?", "Top Rated Attorneys", "Experienced Lawyers Near You"],
                "ad_descriptions": ["Contact us today for a consultation. High success rate, premium legal counsel.", "Professional legal defense and representation. Call for a premium retainer options."]
            },
            "dentist": {
                "competitors": ["Bright Smile Dental", "Metro Dental Care", "Family Dentistry Clinic"],
                "weaknesses": ["no weekend availability", "long waiting times", "painful procedures reported", "high cosmetic pricing"],
                "ad_headlines": ["Gentle Family Dental Care", "Affordable Cosmetic Dentist", "Get Your Brightest Smile Today"],
                "ad_descriptions": ["We accept most insurances. Book your appointment online today.", "Transform your smile with premium veneers and cleaning services. High-end modern clinic."]
            },
            "real estate": {
                "competitors": ["Premier Realty", "Apex Home Finders", "Horizon Estates"],
                "weaknesses": ["slow agent response", "pushy sales tactics", "limited listings in hot zones", "high commission rates"],
                "ad_headlines": ["Find Your Dream Home", "Sell Your House Fast", "Top Rated Real Estate Agents"],
                "ad_descriptions": ["Check out our exclusive local listings. Free home valuation today.", "Expert real estate agents helping you buy or sell. 5% standard commission rates."]
            },
            "default": {
                "competitors": ["Market Leader Corp", "Standard Solutions Inc.", "Global Services Group"],
                "weaknesses": ["generic customer service", "expensive contract lock-ins", "outdated web platform", "no free trial"],
                "ad_headlines": ["Number 1 Choice in Industry", "Professional Services", "Leading Solutions for You"],
                "ad_descriptions": ["Scale your operations with the most expensive and premium provider in town.", "Get started with the industry standard. High contracts required."]
            }
        }

    def spy(self, industry: str, location: str, competitor: Optional[str] = None) -> List[Dict[str, Any]]:
        logger.info(f"Spying on competitors in industry '{industry}' at location '{location}'...")
        
        # Match industry templates
        ind_key = "default"
        for key in self.industry_templates:
            if key in industry.lower():
                ind_key = key
                break
        
        template = self.industry_templates[ind_key]
        competitors_data = []
        
        if competitor:
            # Dynamically construct and prepend custom competitor
            if ind_key == "legal":
                pricing_options = [w for w in template["weaknesses"] if "retainer" in w or "pricing" in w]
                non_pricing_options = [w for w in template["weaknesses"] if "retainer" not in w and "pricing" not in w]
                pricing_weak = random.choice(pricing_options)
                non_pricing_weak = random.choice(non_pricing_options)
                comp_weaknesses = [pricing_weak, non_pricing_weak]
            else:
                comp_weaknesses = random.sample(template["weaknesses"], 2)
            
            comp_headline = f"Official {competitor}"[:30]
            comp_desc = f"Looking for {competitor} in {location}? Contact us."[:90]
            
            competitors_data.append({
                "competitor_name": f"{competitor} {location}",
                "headline": comp_headline,
                "description": comp_desc,
                "channels": ["Google Search", "Meta Ads"],
                "estimated_monthly_spend": random.randint(1500, 8500),
                "weaknesses": comp_weaknesses
            })
            
        for comp in template["competitors"]:
            if ind_key == "legal":
                pricing_options = [w for w in template["weaknesses"] if "retainer" in w or "pricing" in w]
                non_pricing_options = [w for w in template["weaknesses"] if "retainer" not in w and "pricing" not in w]
                pricing_weak = random.choice(pricing_options)
                non_pricing_weak = random.choice(non_pricing_options)
                weaknesses = [pricing_weak, non_pricing_weak]
            else:
                weaknesses = random.sample(template["weaknesses"], 2)
                
            headline = random.choice(template["ad_headlines"])
            description = random.choice(template["ad_descriptions"])
            monthly_spend = random.randint(1500, 8500)
            
            competitors_data.append({
                "competitor_name": f"{comp} {location}",
                "headline": headline,
                "description": description,
                "channels": ["Google Search", "Meta Ads"],
                "estimated_monthly_spend": monthly_spend,
                "weaknesses": weaknesses
            })
            
        logger.info(f"Discovered {len(competitors_data)} competitors in {location}.")
        return competitors_data


class CounterCopywriterAgent:
    """
    Creates high-converting counter ad variants targeting competitor weaknesses.
    """
    def __init__(self):
        pass

    def generate_counter_ads(self, business_name: str, industry: str, competitors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        logger.info(f"Generating counter-ad copy for '{business_name}'...")
        counter_ads = []
        
        for comp in competitors:
            comp_name = comp["competitor_name"]
            for weakness in comp["weaknesses"]:
                # Generate custom counter hooks based on the weakness
                if "retainer" in weakness or "price" in weakness or "expensive" in weakness or "commission" in weakness:
                    headline = "No Retainers. Pay As You Go"
                    description = f"Tired of high costs at {comp_name}? Get flat-rate pricing with {business_name}."
                    angle = "Pricing Advantage"
                elif "slow" in weakness or "waiting" in weakness or "response" in weakness:
                    headline = "Get Support in 5 Mins"
                    description = f"Tired of waiting for {comp_name}? {business_name} offers 24/7 instant booking."
                    angle = "Speed and Responsiveness"
                elif "weekend" in weakness or "availability" in weakness:
                    headline = "Open Weekends & Late Nights"
                    description = f"Unlike {comp_name}, {business_name} offers flexible weekend slots. Book now!"
                    angle = "Convenience & Availability"
                elif "painful" in weakness or "quality" in weakness or "generic" in weakness:
                    headline = "Pain-Free & Gentle Care"
                    description = f"Experience premium care at {business_name}. We solve what {comp_name} misses."
                    angle = "Quality & Comfort"
                else:
                    headline = "Better Choice Today"
                    description = f"Switch to {business_name} today for superior service and no contracts."
                    angle = "General Counter-Arbitrage"
                
                # Apply strict truncation
                headline = headline[:30]
                description = description[:90]
                
                counter_ads.append({
                    "target_competitor": comp_name,
                    "target_channel": "Google Search",
                    "angle": angle,
                    "headline": headline,
                    "description": description,
                    "proposed_by": "CounterCopywriterAgent"
                })
                
                # Add a Meta Ads variant
                meta_headline = f"Tired of {comp_name}?"
                meta_description = f"Switch to {business_name} today and experience the best {industry} services in your area. Zero hassle, maximum satisfaction guaranteed!"
                
                meta_headline = meta_headline[:30]
                meta_description = meta_description[:90]
                
                counter_ads.append({
                    "target_competitor": comp_name,
                    "target_channel": "Meta Ads",
                    "angle": angle,
                    "headline": meta_headline,
                    "description": meta_description,
                    "proposed_by": "CounterCopywriterAgent"
                })
                
        logger.info(f"Generated {len(counter_ads)} ad variants.")
        return counter_ads


class CreativeCriticAgent:
    """
    Verifies copy limits:
    - Google Headlines: max 30 characters.
    - Google Descriptions: max 90 characters.
    Scores quality (0-100) and detects banned words (competitor names in Google Search headlines is often flagged, trademark issues, policy violations, etc.).
    """
    def __init__(self):
        # Keywords that might trigger regulatory issues or poor quality flags
        self.banned_keywords = ["guaranteed success", "cheapest", "absolute best", "bannedword"]

    def critique(self, ad_variants: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        logger.info("Running quality critique and character count audits on proposed copy...")
        critiqued_variants = []
        
        for variant in ad_variants:
            headline = variant["headline"]
            description = variant["description"]
            channel = variant["target_channel"]
            
            issues = []
            
            # 1. Character length checks
            if channel == "Google Search":
                if len(headline) > 30:
                    issues.append(f"Google headline exceeds 30 chars (actual: {len(headline)})")
                if len(description) > 90:
                    issues.append(f"Google description exceeds 90 chars (actual: {len(description)})")
            
            # 2. Banned words detection
            for banned in self.banned_keywords:
                if banned in headline.lower() or banned in description.lower():
                    issues.append(f"Contains policy-violating or low-quality term: '{banned}'")
            
            # 3. Competitor trademark check (e.g. including competitor names in google ad headline)
            comp_name = variant["target_competitor"].lower()
            # extract clean name without location suffix
            clean_comp_name = comp_name.split(" ")[0]
            if clean_comp_name in headline.lower() and channel == "Google Search":
                issues.append("Trademark risk: competitor name used in Google Headline.")
            
            # Quality scoring logic
            score = 100
            if len(issues) > 0:
                score -= 25 * len(issues)
            
            # Reward good counter copy hooks
            if "no" in headline.lower() or "free" in headline.lower() or "instant" in headline.lower():
                score += 5
            
            score = max(10, min(100, score))
            
            critiqued_variants.append({
                **variant,
                "headline_len": len(headline),
                "description_len": len(description),
                "score": score,
                "approved": len(issues) == 0 and score >= 70,
                "issues": issues
            })
            
        logger.info(f"Critique complete. Approved {sum(1 for v in critiqued_variants if v['approved'])} of {len(critiqued_variants)} variants.")
        return critiqued_variants


class BudgetAllocatorAgent:
    """
    Simulates budget shifts across Google Search, Meta Ads, and Local SEO.
    Generates a recommended budget plan and telemetry logs simulating day-by-day performance.
    """
    def __init__(self):
        pass

    def allocate(self, business_name: str, industry: str, location: str, approved_variants: List[Dict[str, Any]]) -> Dict[str, Any]:
        logger.info("Computing optimal budget allocations across channels...")
        
        # Calculate scores or channel strength based on industry
        # Real Estate/Legal tends to perform well on Google Search. Dentistry/E-comm on Meta Ads. Local SEO is universally important.
        google_weight = 0.50
        meta_weight = 0.30
        seo_weight = 0.20
        
        ind_lower = industry.lower()
        if "dentist" in ind_lower or "dental" in ind_lower:
            meta_weight = 0.45
            google_weight = 0.35
        elif "legal" in ind_lower or "law" in ind_lower:
            google_weight = 0.60
            meta_weight = 0.20
            
        total_budget = 5000.0
        google_budget = total_budget * google_weight
        meta_budget = total_budget * meta_weight
        seo_budget = total_budget * seo_weight
        
        allocation = {
            "Google Search": {
                "budget": google_budget,
                "percentage": int(google_weight * 100),
                "description": "Targeting high-intent search keywords with active competitor arbitrage copy."
            },
            "Meta Ads": {
                "budget": meta_budget,
                "percentage": int(meta_weight * 100),
                "description": "Visual retargeting and local demographic matches targeting competitor service gaps."
            },
            "Local SEO": {
                "budget": seo_budget,
                "percentage": int(seo_weight * 100),
                "description": "Optimizing local citations and landing pages for organic map pack takeover."
            }
        }
        
        # Generate day-by-day telemetry logs
        telemetry_logs = []
        days_to_simulate = 14
        
        # Performance multipliers depending on presence of approved variants
        multiplier = 1.0 + (0.05 * len(approved_variants))
        
        for day in range(1, days_to_simulate + 1):
            # Simulate slight day-to-day fluctuations
            noise = random.uniform(-0.15, 0.15)
            
            # Google Search daily performance
            g_daily_budget = (google_budget / days_to_simulate)
            g_ctr = min(0.18, max(0.04, 0.08 + (0.01 * len(approved_variants)) + noise * 0.02))
            g_cpc = max(1.5, 3.5 - (0.1 * len(approved_variants)) + noise * 0.3)
            g_clicks = int((google_budget / days_to_simulate / g_cpc) * (1.0 + noise) * multiplier)
            g_conversions = int(g_clicks * 0.12)
            g_revenue = g_conversions * random.randint(80, 150)
            
            # Meta Ads daily performance
            m_daily_budget = (meta_budget / days_to_simulate)
            m_ctr = min(0.08, max(0.01, 0.025 + noise * 0.005))
            m_cpc = max(0.6, 1.2 + noise * 0.15)
            m_clicks = int((meta_budget / days_to_simulate / m_cpc) * (1.0 + noise) * multiplier)
            m_conversions = int(m_clicks * 0.08)
            m_revenue = m_conversions * random.randint(70, 130)
            
            # Local SEO daily performance (low direct cost, high conversion)
            seo_daily_budget = (seo_budget / days_to_simulate)
            seo_impressions = int(random.randint(200, 500) * (1.0 + day * 0.02) * multiplier)
            seo_conversions = int(seo_impressions * 0.05)
            seo_revenue = seo_conversions * random.randint(100, 200)
            
            total_daily_cost = g_daily_budget + m_daily_budget + seo_daily_budget
            total_daily_revenue = g_revenue + m_revenue + seo_revenue
            daily_roi = (total_daily_revenue - total_daily_cost) / max(1.0, total_daily_cost)
            
            telemetry_logs.append({
                "day": day,
                "google_search": {
                    "spend": round(g_daily_budget, 2),
                    "clicks": g_clicks,
                    "ctr": round(g_ctr, 4),
                    "cpc": round(g_cpc, 2),
                    "conversions": g_conversions
                },
                "meta_ads": {
                    "spend": round(m_daily_budget, 2),
                    "clicks": m_clicks,
                    "ctr": round(m_ctr, 4),
                    "cpc": round(m_cpc, 2),
                    "conversions": m_conversions
                },
                "local_seo": {
                    "spend": round(seo_daily_budget, 2),
                    "impressions": seo_impressions,
                    "conversions": seo_conversions
                },
                "total_spend": round(total_daily_cost, 2),
                "total_conversions": g_conversions + m_conversions + seo_conversions,
                "roi": round(daily_roi, 2)
            })
            
        return {
            "allocation": allocation,
            "telemetry_logs": telemetry_logs
        }


class OutpaceOrchestrator:
    """
    Orchestrates the autonomous competitor ad arbitrage workflow:
    1. Spies on competitors.
    2. Generates counter copies.
    3. Critiques copy against guidelines.
    4. Computes budget allocations and performance telemetry.
    """
    def __init__(self):
        self.spy_agent = CompetitorSpyAgent()
        self.copywriter_agent = CounterCopywriterAgent()
        self.critic_agent = CreativeCriticAgent()
        self.allocator_agent = BudgetAllocatorAgent()

    def run_arbitrage_strategy(self, business_name: str, industry: str, location: str, competitor: Optional[str] = None) -> Dict[str, Any]:
        logger.info(f"Running Outpace strategy for: {business_name} ({industry}) in {location}")
        
        # 1. Spy
        competitors = self.spy_agent.spy(industry, location, competitor)
        
        # 2. Counter-copywriting
        proposed_ads = self.copywriter_agent.generate_counter_ads(business_name, industry, competitors)
        
        # 3. Critique
        critiqued_ads = self.critic_agent.critique(proposed_ads)
        approved_ads = [ad for ad in critiqued_ads if ad["approved"]]
        
        # 4. Budget Allocation & Telemetry simulation
        alloc_results = self.allocator_agent.allocate(business_name, industry, location, approved_ads)
        
        strategy_result = {
            "business_name": business_name,
            "industry": industry,
            "location": location,
            "competitors": competitors,
            "all_proposed_ads": critiqued_ads,
            "approved_ads": approved_ads,
            "budget_allocation": alloc_results["allocation"],
            "telemetry_logs": alloc_results["telemetry_logs"]
        }
        
        logger.info("Outpace strategy run successfully completed.")
        return strategy_result
