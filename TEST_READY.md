# E2E Test Suite Ready

## Test Runner
- Command: `python run_tests.py` or `pytest -v tests/test_e2e.py`
- Expected: Under baseline conditions, 41/49 tests pass and 8/49 tests fail. Once alignment and budget allocator bugs are corrected, all tests pass with exit code 0.

## Coverage Summary
| Tier | Count | Description |
|------|------:|-------------|
| 1. Feature Coverage | 20 | 5 test cases per feature (F1, F2, F3, F4) |
| 2. Boundary & Corner | 20 | 5 boundary/corner test cases per feature |
| 3. Cross-Feature | 4 | Pairwise combination verification of major feature flows |
| 4. Real-World Application | 5 | Scenario-level campaigns (Dentist, Legal, Real Estate, Offline Fallback, E2E flow) |
| **Total** | **49** | |

## Feature Checklist
| Feature | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---------|:------:|:------:|:------:|:------:|
| F1: Competitor Discovery | 5 | 5 | ✓ | ✓ |
| F2: Counter-Ad & Policy | 5 | 5 | ✓ | ✓ |
| F3: Allocation & Telemetry | 5 | 5 | ✓ | ✓ |
| F4: Premium Dashboard UI | 5 | 5 | ✓ | ✓ |
