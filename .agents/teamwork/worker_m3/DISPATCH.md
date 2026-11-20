# Dispatch Task for Worker M3 (Character Builds Backfill & Role Variety)

**Working Directory**: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m3
**Project Root**: /home/nirjhar/Python Codes/Einstein/Databases
**Exclusive Write Ownership**:
- `generate_csvs.py`
- `data/character_builds.csv` (via `python3 generate_csvs.py`)
- `genshin_learning.db` (via `python3 init_db.py`)

**Mandatory Integrity Warning**:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

**Mandatory Inputs**:
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/ORIGINAL_REQUEST.md
- /home/nirjhar/Python Codes/Einstein/Databases/PROJECT.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_3/handoff.md
- /home/nirjhar/Python Codes/Einstein/Databases/TEST_READY.md

**Detailed Requirements (Milestone 3)**:
Implement all character build backfills, alternative meta roles, and build re-linking in `generate_csvs.py`:

1. Append 62 New Builds (IDs 408 to 469) to `BUILDS` in `generate_csvs.py` exactly per `explorer_survey_3/handoff.md § 3.1`:
   - 43 Backfilled builds for existing characters lacking builds (IDs 408–450: Barbara, Razor, Noelle, Kaeya, Lisa, Amber, Diona, Rosaria, Mika, Qiqi, Ningguang, Beidou, Chongyun, Xinyan, Yanfei, Yun Jin, Yaoyao, Kujou Sara, Sayu, Thoma, Gorou, Heizou, Kirara, Collei, Dori, Candace, Layla, Kaveh, Sethos, Lynette, Freminet, Charlotte, Ororon, Iansan, Aino, Nefer, Jahoda, Illuga, Zibai, Linnea, Aloy, Traveler Electro, Traveler Hydro).
   - 16 Backfilled builds for new characters from R2 (IDs 451–466: Ifa, Escoffier, Dahlia, Skirk, Wonderland Manekin, Durin, Varka, Nicole, Prune, Lohen, Alyosha, Odette, Vesna, Vodyanitsa, Mitya, Valeriy).
   - 3 Alternative Meta Roles:
     - Build 467: Mavuika (Support/Sub-DPS with 4pc Scroll of the Hero of Cinder City, weapon 131)
     - Build 468: Citlali (F2P Sacrificial Cryo Buffer with weapon 194 Sacrificial Fragments, 4pc Cinder City)
     - Build 469: Chasca (F2P Chain Breaker Soulsnatcher with weapon 185 Chain Breaker, 4pc Obsidian Codex)

2. Re-link Existing Mismatched Builds:
   - Furina (Build 305): Update `recommended_weapon_id` to `247` (*Fleuve Cendre Ferryman*).
   - Albedo (Build 387): Update `recommended_weapon_id` to `249` (*Cinnabar Spindle*).
   - Shenhe (Build 392): Update `recommended_weapon_id` to `204` (*Calamity Queller*).
   - Sandrone (Build 380): Update `recommended_weapon_id` to `213` (*A Teaspoon of Transcendence*), `goblet_stat` to `"Cryo DMG"`, and `role` to `"Support"`.

3. For all 62 new builds, link weapons to their authentic BiS/Signature weapons where applicable:
   - Ensure weapon types strictly match character weapon types.
   - Ensure all recommended_weapon_id and recommended_artifact_id exist in `weapons` and `artifact_sets`.

4. Run build/regeneration commands:
   - `python3 generate_csvs.py` to regenerate `data/character_builds.csv` (168 rows total).
   - `python3 init_db.py` to rebuild `genshin_learning.db`.
   - Verify `PRAGMA foreign_key_check;` returns 0 violations.
   - Verify zero characters lacking builds (100% playable character build coverage).
   - Run `python3 tests/test_e2e_genshin.py --tier 1 --feature F9,F10,F11,F12` and ensure 20/20 tests pass.
   - Run `python3 tests/test_e2e_genshin.py --tier 1` and ensure all 60 tests (F1–F12) pass.
   - Run `./.venv/bin/python test_security_oom.py` and ensure 22/22 tests pass.

5. Document all changes and verification outputs in `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m3/handoff.md`.

## 2026-11-20T17:32:53Z
You are worker_m3, an implementation worker agent.
Working directory: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m3
Project root: /home/nirjhar/Python Codes/Einstein/Databases
Exclusive write ownership:
- generate_csvs.py
- data/character_builds.csv (via generate_csvs.py)
- genshin_learning.db (via init_db.py)

Mandatory reference: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/ORIGINAL_REQUEST.md
Supporting context:
- /home/nirjhar/Python Codes/Einstein/Databases/PROJECT.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m3/DISPATCH.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_3/handoff.md
- /home/nirjhar/Python Codes/Einstein/Databases/TEST_READY.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Task:
Execute Milestone 3 (M3): Character Builds Backfill & Role Variety:
1. Append 62 New Builds (IDs 408 to 469) to `BUILDS` in `generate_csvs.py` exactly per `explorer_survey_3/handoff.md § 3.1`.
2. Re-link existing mismatched builds in `generate_csvs.py`:
   - Furina (Build 305): recommended_weapon_id = 247 (Fleuve Cendre Ferryman)
   - Albedo (Build 387): recommended_weapon_id = 249 (Cinnabar Spindle)
   - Shenhe (Build 392): recommended_weapon_id = 204 (Calamity Queller)
   - Sandrone (Build 380): recommended_weapon_id = 213 (A Teaspoon of Transcendence), goblet_stat = "Cryo DMG", role = "Support"
3. Run regeneration and build commands:
   - `python3 generate_csvs.py` to regenerate `data/character_builds.csv` (168 rows total).
   - `python3 init_db.py` to rebuild `genshin_learning.db`.
   - Verify `PRAGMA foreign_key_check;` returns 0 violations.
   - Run `python3 tests/test_e2e_genshin.py --tier 1 --feature F9,F10,F11,F12` and ensure 20/20 tests pass.
   - Run `python3 tests/test_e2e_genshin.py --tier 1` and ensure 60/60 tests (F1–F12) pass.
   - Run `./.venv/bin/python test_security_oom.py` and ensure 22/22 tests pass.
4. Periodically update `progress.md` in your working directory with `Last visited: [timestamp]`.
5. Write your comprehensive handoff report to `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m3/handoff.md`.
6. Send completion message to parent when finished.
