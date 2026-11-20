# Dispatch for Milestone 1 Sub-Orchestrator

**Working Directory**: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/sub_orch_m1
**Project Root**: /home/nirjhar/Python Codes/Einstein/Databases
**Role**: Milestone 1 Sub-Orchestrator (Database Defect Remediation)
**Parent Conversation ID**: a6a497b1-b1f9-4f4e-becb-39785ade3dd2

**Mandatory Inputs**:
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/ORIGINAL_REQUEST.md
- /home/nirjhar/Python Codes/Einstein/Databases/PROJECT.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_1/handoff.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_2_gen2/handoff.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_3/handoff.md

**Scope (M1)**:
Execute R1 Database Defect Remediation:
1. Update Artifact Sets 59, 60, 62, 63, 64 in `generate_csvs.py` (official names, domains, regions, 2pc/4pc scaling per `explorer_survey_2_gen2/handoff.md § 3.1`).
2. Correct weapon stats for ID 128 (*Fang of the Mountain King*) and 131 (*A Thousand Blazing Suns*) to Base ATK = 741, Sub-stat = 11.0% CRIT Rate in `generate_csvs.py`.
3. Correct character attributes in `generate_csvs.py`:
   - Arlecchino (ID 72): region = "Snezhnaya"
   - Zibai (ID 99): region = "Liyue"
   - Columbina (ID 102): region = "Nod-Krai"
   - Sandrone (ID 103): vision = "Cryo", weapon_type = "Claymore"
   - Iansan (ID 91): release_patch = 5.5
   - Aloy (ID 105): region = "None"
4. Purge non-playable NPC Capitano (ID 104) and Build 381 synchronously from `generate_csvs.py` and `data/character_builds.csv`.
5. Run `python3 generate_csvs.py` and `python3 init_db.py` to regenerate CSVs and reload `genshin_learning.db`.
6. Verify `PRAGMA foreign_key_check;` returns 0 violations.
7. Execute standard verification loop: Explorer -> Worker -> Reviewer -> Challenger -> Auditor.
8. Report completion back to parent orchestrator.
