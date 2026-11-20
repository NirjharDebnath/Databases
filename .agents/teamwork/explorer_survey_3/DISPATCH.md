## 2026-11-20T16:18:40Z
You are explorer_survey_3, an exploration agent.
Working directory: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_3
Project root: /home/nirjhar/Python Codes/Einstein/Databases
Mandatory reference: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/ORIGINAL_REQUEST.md

Task:
Perform a detailed requirements and data specification survey for R4 and R5:
1. R4 Character Builds Backfill & Role Variety:
   - Identify all characters currently in `characters` (and all 16 new characters from R2) that are missing builds in `character_builds` (the prompt notes 43 existing missing builds e.g. Barbara, Noelle, Beidou, Rosaria, Ororon, Yaoyao, Diona, Qiqi, etc., plus the 16 new ones).
   - Formulate verified meta builds for every single character lacking a build: role, recommended weapon (must resolve to valid weapon in weapons table), recommended artifact set (must resolve to valid artifact set), main stats (sands, goblet, circlet), sub-stats priority.
   - Specify alternative meta roles for key characters: Mavuika (Support/Sub-DPS with 4pc Scroll of the Hero of Cinder City), Citlali (F2P variants), Chasca (F2P variants).
   - Specify build re-linking for Furina, Albedo, Shenhe to their proper signature and BiS weapons.
2. R5 Data Synchronization & Automated Verification:
   - Check `data/*.csv` regeneration requirements and schema match with DB tables.
   - Check `init_db.py` and `generate_csvs.py` synchronization logic: how changes should be reflected in seed data or scripts to guarantee 100% reproducibility.
   - Check `verify_db.py`: inspect its current checks and identify what new checks, tests, or assertions are needed to guarantee 0 foreign key violations, 0 orphaned records, and complete schema integrity.

Constraints:
- You are read-only. DO NOT modify any code, database, or CSV files.
- Periodically update `progress.md` in your working directory with `Last visited: [timestamp]` for liveness heartbeat.
- Write your comprehensive, structured report to `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_3/handoff.md`.
- When finished, send a completion message to parent with a summary of findings and the path to your handoff.md.
