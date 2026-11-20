# DISPATCH: Milestone 4 Worker (Pipeline Sync & Verification Suite Upgrade)

You are `worker_m4`, an implementation worker agent.
Working directory: `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m4`
Project root: `/home/nirjhar/Python Codes/Einstein/Databases`

## Exclusive Write Ownership:
- `init_db.py`
- `verify_db.py`
- `genshin_learning.db` (via `python3 init_db.py`)

## Mandatory Reference:
- `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/ORIGINAL_REQUEST.md`

## Supporting Context:
- `/home/nirjhar/Python Codes/Einstein/Databases/PROJECT.md`
- `/home/nirjhar/Python Codes/Einstein/Databases/TEST_READY.md`
- `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m3_iter2/handoff.md`

## MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Task:
Execute Milestone 4 (M4): Pipeline Synchronization & Verification Suite Upgrade (R5):
1. **Update `init_db.py`**:
   - In `SCHEMA_SQL`, append the missing relational indexes:
     ```sql
     CREATE INDEX IF NOT EXISTS idx_weapons_signature ON weapons(signature_character_id);
     CREATE INDEX IF NOT EXISTS idx_builds_weapon ON character_builds(recommended_weapon_id);
     CREATE INDEX IF NOT EXISTS idx_builds_artifact ON character_builds(recommended_artifact_id);
     ```
   - Ensure `init_db.py` executes cleanly and builds all tables and indexes.

2. **Update `verify_db.py`**:
   Upgrade `verify_db.py` to implement the comprehensive assertion suites per `ORIGINAL_REQUEST.md § R5`:
   - Exact row counts:
     * `characters`: 129
     * `weapons`: 155
     * `artifact_sets`: 64
     * `character_builds`: 168
   - Foreign key integrity:
     * `PRAGMA foreign_key_check;` returns strictly 0 violations
   - Zero orphaned characters:
     * `SELECT c.character_id FROM characters c LEFT JOIN character_builds cb ON c.character_id = cb.character_id WHERE cb.build_id IS NULL;` returns 0 rows
   - Regional distribution check across all 10 regions:
     * Mondstadt: 23
     * Liyue: 22
     * Inazuma: 17
     * Sumeru: 14
     * Fontaine: 13
     * Nod-Krai: 12
     * Natlan: 11
     * Outlander: 8
     * Snezhnaya: 8
     * None: 1 (Aloy)
   - Valid weapon type matching:
     * 100% of builds have matching `c.weapon_type == w.weapon_type` (0 mismatches)
   - 1:1 CSV-to-DB record parity:
     * Verify row counts and cell parity between each CSV (`data/characters.csv`, `data/weapons.csv`, `data/artifact_sets.csv`, `data/character_builds.csv`) and the corresponding SQLite tables.
   - Core SQL learning queries test suite (multi-table join, aggregations, 1-piece tiaras, window functions) to ensure query plans execute smoothly.

3. **Execute Pipeline & Verification**:
   - Run `python3 generate_csvs.py` to verify CSV generation determinism.
   - Run `python3 init_db.py` to drop and recreate `genshin_learning.db` cleanly with indexes.
   - Run `python3 verify_db.py` and ensure 100% green exit code 0.
   - Run `python3 tests/test_e2e_genshin.py` and verify that all 171 tests across Tiers 1–4 pass (100% PASS, Exit Code 0).
   - Run `./.venv/bin/python test_security_oom.py` and verify all 22 tests pass cleanly (Exit Code 0).

4. **Handoff & Reporting**:
   - Periodically update `progress.md` with `Last visited: [timestamp]`.
   - Write comprehensive handoff report to `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m4/handoff.md`.
   - Send completion message to parent when finished.

## 2026-11-20T18:12:27Z
You are worker_m4, an implementation worker agent.
Working directory: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m4
Project root: /home/nirjhar/Python Codes/Einstein/Databases
Exclusive write ownership:
- init_db.py
- verify_db.py
- genshin_learning.db (via init_db.py)

Mandatory reference: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/ORIGINAL_REQUEST.md
Supporting context:
- /home/nirjhar/Python Codes/Einstein/Databases/PROJECT.md
- /home/nirjhar/Python Codes/Einstein/Databases/TEST_READY.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m4/DISPATCH.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m3_iter2/handoff.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Task:
Execute Milestone 4 (M4): Pipeline Synchronization & Verification Suite Upgrade (R5):
1. Update `init_db.py`:
   - In `SCHEMA_SQL`, append the missing relational indexes:
     ```sql
     CREATE INDEX IF NOT EXISTS idx_weapons_signature ON weapons(signature_character_id);
     CREATE INDEX IF NOT EXISTS idx_builds_weapon ON character_builds(recommended_weapon_id);
     CREATE INDEX IF NOT EXISTS idx_builds_artifact ON character_builds(recommended_artifact_id);
     ```
2. Update `verify_db.py`:
   - Upgrade assertions per ORIGINAL_REQUEST.md § R5:
     * Exact row counts: characters == 129, weapons == 155, artifact_sets == 64, character_builds == 168
     * PRAGMA foreign_key_check == 0
     * Zero orphaned characters without builds (0 rows)
     * Regional distribution across all 10 regions: Mondstadt (23), Liyue (22), Inazuma (17), Sumeru (14), Fontaine (13), Nod-Krai (12), Natlan (11), Outlander (8), Snezhnaya (8), None (1)
     * Valid weapon type matching between characters and builds (0 mismatches across 168 builds)
     * 1:1 CSV-to-DB record parity across all 4 tables
     * Core SQL learning queries
3. Run verification and pipeline commands:
   - python3 generate_csvs.py
   - python3 init_db.py
   - python3 verify_db.py (ensure 100% green exit code 0)
   - python3 tests/test_e2e_genshin.py (ensure all 171 tests pass with exit code 0)
   - ./.venv/bin/python test_security_oom.py (ensure 22/22 tests pass with exit code 0)
4. Periodically update `progress.md` with `Last visited: [timestamp]`.
5. Write your comprehensive handoff report to `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m4/handoff.md`.
6. Send completion message to parent when finished.
