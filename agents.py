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
        # Dynamic pools for combinatorial generation
        self.pain_points = [
            "high cost", "slow service", "poor customer support", 
            "outdated technology", "lack of transparency", "hidden fees",
            "pushy sales tactics", "unreliable availability", "long wait times",
            "generic solutions", "inflexible contracts", "hard to reach",
            "inconsistent quality", "expensive retainer", "no weekend availability"
        ]
        
        self.ad_headlines = [
            "Premium {Industry} Services", "Top Rated {Industry} Near You",
            "Expert {Industry} Solutions", "Affordable {Industry} Professionals",
            "Your Local {Industry} Experts", "Fast & Reliable {Industry}",
            "#1 Choice for {Industry}", "Award-Winning {Industry}"
        ]
        
        self.ad_descriptions = [
            "Contact us today for the best {industry} service. Highly rated by locals.",
            "We provide top-tier {industry} solutions. Call now for a free quote.",
            "Looking for reliable {industry}? We have you covered with our expert team.",
            "Professional {industry} services at competitive rates. Book online today.",
            "Get started with the industry standard in {industry}. Satisfaction guaranteed.",
            "Transform your experience with our premium {industry} platform. Reach out now."
        ]
        
        self.comp_prefixes = ["Apex", "Prime", "Elite", "Summit", "Vanguard", "Horizon", "Pinnacle", "Local", "First Choice", "Pro"]
        self.comp_suffixes = ["Solutions", "Group", "Services", "Partners", "Associates", "Corp", "Inc", "Professionals"]

    def spy(self, industry: str, location: str, competitor: Optional[str] = None) -> List[Dict[str, Any]]:
        logger.info(f"Spying on competitors in industry '{industry}' at location '{location}'...")
        competitors_data = []
        
        # Clean up industry string for templating
        ind_title = industry.title()
        ind_lower = industry.lower()

        num_competitors = random.randint(3, 5)
        
        # If a specific competitor is provided, make sure they are in the list
        if competitor:
            comp_headline = random.choice(self.ad_headlines).replace("{Industry}", ind_title)
            comp_desc = f"Looking for {competitor} in {location}? Contact us."[:90]
            competitors_data.append({
                "competitor_name": f"{competitor} {location}",
                "headline": comp_headline[:30],
                "description": comp_desc,
                "channels": ["Google Search", "Meta Ads"],
                "estimated_monthly_spend": random.randint(1500, 8500),
                "weaknesses": random.sample(self.pain_points, 2)
            })
            num_competitors -= 1
            
        for _ in range(num_competitors):
            comp_name = f"{random.choice(self.comp_prefixes)} {random.choice(self.comp_suffixes)}"
            headline = random.choice(self.ad_headlines).replace("{Industry}", ind_title)[:30]
            description = random.choice(self.ad_descriptions).replace("{industry}", ind_lower)[:90]
            monthly_spend = random.randint(1500, 8500)
            
            competitors_data.append({
                "competitor_name": f"{comp_name} {location}",
                "headline": headline,
                "description": description,
                "channels": ["Google Search", "Meta Ads"],
                "estimated_monthly_spend": monthly_spend,
                "weaknesses": random.sample(self.pain_points, 2)
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
        # Track used headlines to guarantee uniqueness
        used_headlines: set = set()

        # Variant suffixes to differentiate ads with the same angle across competitors
        google_suffixes = ["", " — Book Now", " Today", " Guaranteed", " Near You", " Free Consult"]
        meta_suffixes   = ["", " — Try It Free", " — See Reviews", " — No Commitment", " — Act Now"]

        for comp_idx, comp in enumerate(competitors):
            comp_name = comp["competitor_name"]
            # Strip location suffix for cleaner ad copy
            short_comp = comp_name.split(" ")[0] if len(comp_name.split(" ")) > 0 else comp_name
            if len(short_comp) > 12:
                short_comp = short_comp[:12]

            for weakness in comp["weaknesses"]:
                # --- Combinatorial Generator for 100% Unique Ads ---
                import hashlib
                
                # We build the ad out of 3 parts: Hook, Value, CTA
                
                if "retainer" in weakness or "price" in weakness or "expensive" in weakness or "commission" in weakness or "pricing" in weakness or "cost" in weakness:
                    angle = "Pricing Advantage"
                    g_hooks = ["Flat-Rate.", "No Surprises.", "Transparent Pricing.", "Stop Overpaying."]
                    g_values = [f"{business_name} offers flat-rate pricing.", f"No lock-ins with {business_name}.", f"We beat {short_comp} on price.", f"Save money with {business_name}."]
                    
                    m_hooks = ["No Hidden Fees", "Zero Hidden Costs", "Fair Pricing", "Keep Your Money"]
                    m_values = [f"Clear pricing, zero surprises.", f"Why pay {short_comp}'s rates?", f"Get premium service for less.", f"Switch to honest pricing."]

                elif "slow" in weakness or "waiting" in weakness or "response" in weakness or "wait" in weakness:
                    angle = "Speed and Responsiveness"
                    g_hooks = ["Same-Day Appointments", "Fast Response Times", "Instant Booking", "Don't Wait Weeks"]
                    g_values = [f"{business_name} offers same-day bookings.", f"Faster than {short_comp}.", f"Get help immediately.", f"No more waiting rooms."]
                    
                    m_hooks = ["Skip the Waitlist", "Fast Track Access", "Available Today", "Instant Approvals"]
                    m_values = [f"We book you in today.", f"24/7 scheduling available.", f"{short_comp} too slow? Try us.", f"Instant confirmation guaranteed."]

                elif "weekend" in weakness or "availability" in weakness or "reach" in weakness:
                    angle = "Convenience & Availability"
                    g_hooks = ["Open Weekends", "Evening Slots", "7-Day Service", "Always Available"]
                    g_values = [f"{business_name} is open when you need.", f"Flexible slots that fit your life.", f"We work around your schedule.", f"Unlike {short_comp}, we're open."]
                    
                    m_hooks = ["Here When You Need Us", "Weekend Appointments", "After-Hours Support", "Total Convenience"]
                    m_values = [f"Stop rescheduling.", f"Evening and weekend slots.", f"Book outside business hours.", f"We fit into your busy life."]

                elif "painful" in weakness or "quality" in weakness or "generic" in weakness or "poor" in weakness:
                    angle = "Quality & Comfort"
                    g_hooks = ["5-Star Care", "Premium Quality", "Award-Winning", "Top Rated Service"]
                    g_values = [f"{business_name} uses modern techniques.", f"A completely different experience.", f"Highly rated by our customers.", f"Don't settle for less."]
                    
                    m_hooks = ["Comfort is Priority", "Exceptional Service", "The Best in Town", "Quality Guaranteed"]
                    m_values = [f"Switch from {short_comp} today.", f"See why locals love us.", f"Premium service, guaranteed.", f"Experience the difference."]

                elif "pushy" in weakness or "sales" in weakness or "tactics" in weakness or "transparency" in weakness:
                    angle = "Trust & Transparency"
                    g_hooks = ["No Pressure.", "Honest Advice.", "Just Results.", "Transparent Service."]
                    g_values = [f"{business_name} lets results speak.", f"No upsells, no pressure.", f"Honest service you can trust.", f"We put your needs first."]
                    
                    m_hooks = ["Zero Pressure", "Trusted Professionals", "Honest & Reliable", "Straightforward Service"]
                    m_values = [f"Tired of being sold to?", f"Get honest advice free.", f"Try us with no commitment.", f"We don't do pushy sales."]

                elif "contract" in weakness or "lock" in weakness or "inflexible" in weakness:
                    angle = "Flexibility"
                    g_hooks = ["No Contracts.", "Cancel Anytime.", "Month-to-Month.", "Total Flexibility."]
                    g_values = [f"{business_name} is completely flexible.", f"Pay only for what you use.", f"Don't get locked in.", f"Freedom to choose."]
                    
                    m_hooks = ["Zero Contract Required", "No Lock-Ins", "Stay Because You Want To", "100% Flexible"]
                    m_values = [f"We don't trap you.", f"Cancel anytime, no fees.", f"Month-to-month freedom.", f"Switch from {short_comp} easily."]

                else:
                    angle = "General Counter-Arbitrage"
                    g_hooks = ["The Smarter Choice", "Better Service", "Upgrade Today", "Switch & Save"]
                    g_values = [f"{business_name} solves the hard problems.", f"Better service, better results.", f"Try {business_name} free today.", f"Join our happy customers."]
                    
                    m_hooks = ["Make the Switch", "A Better Alternative", "Why Settle?", "Experience Better"]
                    m_values = [f"Join hundreds who switched.", f"Superior service awaits.", f"Zero commitment needed.", f"See what you've been missing."]
                    
                g_ctas = [" Book now.", " Try it free.", " Learn more.", " Contact us.", " Get a quote."]
                m_ctas = [" Click here.", " Sign up today.", " Get started.", " Learn more now.", " Claim offer."]

                # Generate Google Ad
                g_headline = f"{random.choice(g_hooks)} {random.choice(['—', '|', '-'])} {short_comp} Alternative"[:30]
                g_description = f"{random.choice(g_values)} {random.choice(g_ctas)}"[:90]

                # Generate Meta Ad
                m_headline = f"{random.choice(m_hooks)}"[:30]
                m_description = f"{random.choice(m_values)} {random.choice(m_ctas)}"[:90]

                # Ensure Uniqueness with a fallback salt if needed
                def ensure_unique(text: str, max_len: int) -> str:
                    original = text
                    attempts = 0
                    while text in used_headlines and attempts < 10:
                        salt = str(random.randint(10, 99))
                        text = f"{original} {salt}"[:max_len]
                        attempts += 1
                    used_headlines.add(text)
                    return text

                g_headline = ensure_unique(g_headline, 30)
                m_headline = ensure_unique(m_headline, 30)

                counter_ads.append({
                    "target_competitor": comp_name,
                    "target_channel": "Google Search",
                    "angle": angle,
                    "headline": g_headline,
                    "description": g_description,
                    "proposed_by": "CounterCopywriterAgent"
                })

                counter_ads.append({
                    "target_competitor": comp_name,
                    "target_channel": "Meta Ads",
                    "angle": angle,
                    "headline": m_headline,
                    "description": m_description,
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
            # Simulate progressive improvement over the campaign
            # CTR and conversions ramp up as the campaign optimises
            day_factor = day / days_to_simulate  # 0.07 → 1.0
            noise = random.uniform(-0.05, 0.05)

            # Google Search daily performance — CTR grows from ~4% to ~12%
            g_daily_budget = google_budget / days_to_simulate
            g_ctr = round(min(0.12, max(0.03, 0.04 + 0.08 * day_factor + noise * 0.01)), 4)
            g_cpc = round(max(1.8, 4.5 - 1.5 * day_factor + noise * 0.2), 2)
            g_clicks = int(g_daily_budget / g_cpc * (1 + noise))
            g_conversions = max(0, int(g_clicks * (0.06 + 0.08 * day_factor)))
            g_revenue = g_conversions * random.randint(80, 150)

            # Meta Ads daily performance
            m_daily_budget = meta_budget / days_to_simulate
            m_ctr = round(min(0.05, max(0.01, 0.015 + 0.025 * day_factor + noise * 0.005)), 4)
            m_cpc = round(max(0.8, 1.8 - 0.5 * day_factor + noise * 0.1), 2)
            m_clicks = int(m_daily_budget / m_cpc * (1 + noise))
            m_conversions = max(0, int(m_clicks * (0.04 + 0.06 * day_factor)))
            m_revenue = m_conversions * random.randint(70, 130)

            # Local SEO — slow start, strong finish
            seo_daily_budget = seo_budget / days_to_simulate
            seo_impressions = int(random.randint(150, 350) * (1.0 + day * 0.04))
            seo_conversions = max(0, int(seo_impressions * (0.02 + 0.04 * day_factor)))
            seo_revenue = seo_conversions * random.randint(100, 180)

            total_daily_cost = g_daily_budget + m_daily_budget + seo_daily_budget
            total_daily_revenue = g_revenue + m_revenue + seo_revenue
            # Realistic ROI: starts ~1x, grows to ~3-5x by day 14
            daily_roi = round((total_daily_revenue - total_daily_cost) / max(1.0, total_daily_cost), 2)
            
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
