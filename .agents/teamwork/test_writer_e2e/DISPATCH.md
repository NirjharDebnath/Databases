# Dispatch Task for E2E Test Writer

**Working Directory**: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/test_writer_e2e
**Project Root**: /home/nirjhar/Python Codes/Einstein/Databases
**Exclusive Write Ownership**:
- `TEST_INFRA.md` (at project root)
- `tests/test_e2e_genshin.py`
- `TEST_READY.md` (at project root)

**Mandatory Inputs**:
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/ORIGINAL_REQUEST.md
- /home/nirjhar/Python Codes/Einstein/Databases/PROJECT.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_1/handoff.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_2_gen2/handoff.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_3/handoff.md

**Mission**:
Build the comprehensive requirement-driven, opaque-box E2E test suite:
1. Create `TEST_INFRA.md` at project root documenting test architecture, methodology, and coverage thresholds.
2. Build E2E test harness and runner: `tests/test_e2e_genshin.py`.
3. Implement 4 tiers of test cases derived strictly from `ORIGINAL_REQUEST.md` and `PROJECT.md § Feature Inventory`:
   - Tier 1: Feature Coverage (>=5 test cases per feature across F1–F14)
   - Tier 2: Boundary & Corner Cases (>=5 test cases per feature where boundaries exist)
   - Tier 3: Cross-Feature Combinations (pairwise interactions across major features)
   - Tier 4: Real-World Application Scenarios (>=5 realistic application scenarios: e.g. team building queries, damage calculations, relic farm routing, character progression)
4. Ensure the test runner can be invoked via `python3 tests/test_e2e_genshin.py` or `./.venv/bin/python tests/test_e2e_genshin.py` with exit code 0 when all tests pass.
5. Publish `TEST_READY.md` at project root with exact test runner command and coverage summary.
6. Write a comprehensive completion report to `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/test_writer_e2e/handoff.md`.

## 2026-11-20T16:57:38Z
You are test_writer_e2e, a test writer agent.
Working directory: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/test_writer_e2e
Project root: /home/nirjhar/Python Codes/Einstein/Databases
Exclusive write ownership:
- TEST_INFRA.md (at project root)
- tests/test_e2e_genshin.py
- TEST_READY.md (at project root)

Mandatory reference: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/ORIGINAL_REQUEST.md
Supporting context:
- /home/nirjhar/Python Codes/Einstein/Databases/PROJECT.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/test_writer_e2e/DISPATCH.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_1/handoff.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_2_gen2/handoff.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_3/handoff.md

Task:
Build the comprehensive requirement-driven, opaque-box E2E test suite:
1. Create `TEST_INFRA.md` at project root documenting test architecture, methodology, and coverage thresholds.
2. Build E2E test harness and runner: `tests/test_e2e_genshin.py` (ensure parent directory `tests/` is created if needed).
3. Implement 4 tiers of test cases derived strictly from `ORIGINAL_REQUEST.md` and `PROJECT.md § Feature Inventory`:
   - Tier 1: Feature Coverage (>=5 test cases per feature across F1–F14)
   - Tier 2: Boundary & Corner Cases (>=5 test cases per feature where boundaries exist)
   - Tier 3: Cross-Feature Combinations (pairwise interactions across major features)
   - Tier 4: Real-World Application Scenarios (>=5 realistic application scenarios: e.g. team building queries, damage calculations, relic farm routing, character progression)
   - Total test cases should exceed the minimum thresholds specified in Project Pattern.
4. Ensure the test runner can be invoked via `python3 tests/test_e2e_genshin.py` or `./.venv/bin/python tests/test_e2e_genshin.py` with exit code 0 when all tests pass.
5. Publish `TEST_READY.md` at project root with exact test runner command, expected exit code, and coverage checklist.
6. Periodically update `progress.md` in your working directory with `Last visited: [timestamp]`.
7. Write your handoff report to `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/test_writer_e2e/handoff.md`.
8. Send a completion message to parent when finished.

