# E2E Test Infra: CounterStrike

## Test Philosophy
- **Opaque-box, requirement-driven**: Tests verify the core requirements (R1-R4) via backend API endpoints and index.html UI structures without relying on internal code implementation details.
- **Methodology**: Category-Partition + Boundary Value Analysis + Pairwise + Real-World Workload Testing.
- **Contract Gating**: Tests check compliance against the documented API interface contracts in `PROJECT.md` to ensure the frontend and backend are aligned.

## Feature Inventory
| # | Feature | Source (requirement) | Tier 1 (Coverage) | Tier 2 (Boundaries) | Tier 3 (Cross) | Tier 4 (Workloads) |
|---|---------|---------------------|:-----------------:|:------------------:|:--------------:|:------------------:|
| 1 | Competitor Discovery | ORIGINAL_REQUEST R1 | 5 | 5 | ✓ | ✓ |
| 2 | Counter-Ad & Policy | ORIGINAL_REQUEST R2 | 5 | 5 | ✓ | ✓ |
| 3 | Allocation & Telemetry | ORIGINAL_REQUEST R3 | 5 | 5 | ✓ | ✓ |
| 4 | Premium Dashboard UI | ORIGINAL_REQUEST R4 | 5 | 5 | ✓ | ✓ |

## Test Architecture
- **Test Runner**: A python-based test execution script `run_tests.py` using `pytest`.
- **Test Suite Location**: The tests are written under the `tests/` directory as `tests/test_e2e.py`.
- **FastAPI Testing**: Uses `fastapi.testclient.TestClient` for synchronous API requests validation and direct server simulation.
- **UI Validation**: Uses python-based file parsing (`BeautifulSoup` or raw parsing) to verify DOM elements and inline JavaScript callbacks in `index.html` and `style.css`.
- **Pass/Fail Semantics**: The exit code of `pytest tests/` must be 0 for all tests.

## Detailed Test Case Inventory

### Tier 1 - Feature Coverage (5 per feature, 20 total)
- **F1 (Competitor Discovery)**:
  - `test_discovery_legal`: Verify competitor discovery and name formatting when industry is "legal".
  - `test_discovery_dentist`: Verify competitor discovery and name formatting when industry is "dentist".
  - `test_discovery_real_estate`: Verify competitor discovery and name formatting when industry is "real estate".
  - `test_discovery_default`: Verify competitor discovery falls back gracefully for unknown industries.
  - `test_discovery_location_suffix`: Verify competitor names include the target location suffix.
- **F2 (Counter-Ad & Compliance)**:
  - `test_counter_ad_pricing_angle`: Verify "Pricing Advantage" hook and angle generation for pricing weaknesses.
  - `test_counter_ad_speed_angle`: Verify "Speed and Responsiveness" hook for response-related weaknesses.
  - `test_counter_ad_convenience_angle`: Verify "Convenience & Availability" hook for availability weaknesses.
  - `test_counter_ad_quality_angle`: Verify "Quality & Comfort" hook for quality weaknesses.
  - `test_counter_ad_default_angle`: Verify fallback to general copywriting angles for default weaknesses.
- **F3 (Dynamic Budget Allocation & Telemetry)**:
  - `test_budget_weight_dentist`: Verify budget weighs Meta Ads higher (45%) for dentistry industries.
  - `test_budget_weight_legal`: Verify budget weighs Google Search higher (60%) for legal/law industries.
  - `test_budget_weight_default`: Verify default budget allocation split (50% Google Search, 30% Meta Ads, 20% Local SEO).
  - `test_telemetry_days_count`: Verify simulation runs for exactly 14 simulated days of telemetry logs.
  - `test_telemetry_metrics_presence`: Verify presence of CTR, conversions, ROI, and spend metrics in daily logs.
- **F4 (UI Structure & Integration)**:
  - `test_ui_onboarding_form`: Verify `index.html` has form fields for business name, niche, competitor, and location.
  - `test_ui_launch_button`: Verify `index.html` has the launch button element with correct ID.
  - `test_ui_chartjs_imported`: Verify `index.html` includes Chart.js script tag.
  - `test_ui_performance_chart_canvas`: Verify canvas element for performanceChart is present.
  - `test_ui_agent_status_cards`: Verify DOM status elements exist for all 4 subagents.

### Tier 2 - Boundary & Corner Cases (5 per feature, 20 total)
- **F1 (Competitor Discovery)**:
  - `test_discovery_empty_industry`: Verify error handling or graceful recovery with empty/missing industry field.
  - `test_discovery_empty_location`: Verify error handling or fallback with empty/missing location field.
  - `test_discovery_extreme_long_input`: Verify system stability under extremely long industry/location input strings.
  - `test_discovery_special_characters`: Verify system handles punctuation and special characters safely.
  - `test_discovery_case_insensitivity`: Verify industry matching is case-insensitive (e.g. "DENTIST" maps to "dentist").
- **F2 (Counter-Ad & Compliance)**:
  - `test_ad_critic_google_headline_max_bound`: Verify headline exactly at 30 characters passes length validation.
  - `test_ad_critic_google_headline_out_of_bound`: Verify headline exceeding 30 characters fails validation and sets approved to False.
  - `test_ad_critic_google_description_max_bound`: Verify description exactly at 90 characters passes validation.
  - `test_ad_critic_google_description_out_of_bound`: Verify description exceeding 90 characters fails validation.
  - `test_ad_critic_banned_keyword`: Verify score and approval drops when banned keywords are present in copy.
- **F3 (Dynamic Budget Allocation & Telemetry)**:
  - `test_allocation_no_approved_variants`: Verify simulation metrics handle 0 approved variants without division by zero.
  - `test_allocation_high_approved_variants`: Verify simulation metrics scale properly under high variant approvals.
  - `test_telemetry_noise_fluctuation_bounds`: Verify telemetry daily logic keeps CTR and CPC within realistic positive bounds.
  - `test_telemetry_pre_analysis_error`: Verify GET `/api/telemetry` returns 404 error if run before an analysis.
  - `test_telemetry_zero_budget_graceful`: Verify allocation simulation does not crash if total budget is zero.
- **F4 (UI Structure & Integration)**:
  - `test_ui_fields_required`: Verify input elements in `index.html` have `required` attribute.
  - `test_ui_initial_status_idle`: Verify initial dashboard status defaults to "System Standby" and idle badge classes.
  - `test_ui_fallback_api_offline_analyze`: Verify javascript code triggers local simulation fallback on POST failure.
  - `test_ui_fallback_api_offline_telemetry`: Verify javascript code triggers local mock data on GET telemetry failure.
  - `test_ui_stylesheet_linked`: Verify `style.css` is linked correctly.

### Tier 3 - Cross-Feature Combinations (4 total)
- `test_cross_f1_f2_weakness_flow`: Verify discovered competitor weaknesses flow directly to target copywriting angles.
- `test_cross_f2_f3_approval_multiplier`: Verify number of approved ads scales simulated performance metrics.
- `test_cross_f3_f4_telemetry_binding`: Verify telemetry fields are bound and map to UI progress bars and text nodes.
- `test_cross_f1_f4_competitor_feed_binding`: Verify competitor names render dynamically in the frontend Target Ads Feed.

### Tier 4 - Real-World Application Scenarios (5 total)
- `test_scenario_dentist_campaign`: Austin, TX Dentist campaign. Checks dental competitors, Meta-heavy budget weight, and 14 days of simulation metrics.
- `test_scenario_legal_campaign`: New York Law firm campaign. Checks legal competitors, Google-heavy budget weight, and 14 days of simulation metrics.
- `test_scenario_real_estate_campaign`: Seattle Real Estate campaign. Checks real estate competitors, default budget weight, and 14 days of simulation metrics.
- `test_scenario_ui_offline_fallback`: Simulates complete offline frontend operation and local JS simulation execution.
- `test_scenario_end_to_end_api_flow`: Full backend integration flow: POST `/api/analyze` -> GET `/api/status` -> GET `/api/telemetry` validating the frame-by-frame data contract.

## Coverage Thresholds
- Tier 1: ≥5 per feature (Met: 20 test cases)
- Tier 2: ≥5 per feature (Met: 20 test cases)
- Tier 3: pairwise coverage of major feature interactions (Met: 4 test cases)
- Tier 4: ≥5 realistic application scenarios (Met: 5 test cases)
- Total: 49 test cases
