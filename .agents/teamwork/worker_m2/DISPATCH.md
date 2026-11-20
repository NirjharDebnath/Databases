# Dispatch Task for Worker M2 (Characters & Weapons Ingestion)

**Working Directory**: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m2
**Project Root**: /home/nirjhar/Python Codes/Einstein/Databases
**Exclusive Write Ownership**:
- `generate_csvs.py`
- `data/characters.csv` (via `python3 generate_csvs.py`)
- `data/weapons.csv` (via `python3 generate_csvs.py`)
- `genshin_learning.db` (via `python3 init_db.py`)

**Mandatory Integrity Warning**:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

**Mandatory Inputs**:
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/ORIGINAL_REQUEST.md
- /home/nirjhar/Python Codes/Einstein/Databases/PROJECT.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_2_gen2/handoff.md
- /home/nirjhar/Python Codes/Einstein/Databases/TEST_READY.md

**Detailed Requirements (Milestone 2)**:
Ingest all 16 missing playable characters and all 52 missing weapons into `generate_csvs.py`:

1. Append 16 Missing Playable Characters (IDs 115 to 130) to `CHARACTERS` list in `generate_csvs.py` (per `explorer_survey_2_gen2/handoff.md § 3.2`):
   - (115, "Ifa", 4, "Anemo", "Catalyst", "Natlan", "Healer", 11201, 193, 655, "Skill > Burst > Normal", 5.6)
   - (116, "Escoffier", 5, "Cryo", "Polearm", "Fontaine", "Sub-DPS", 12907, 337, 789, "Skill > Burst > Normal", 5.6)
   - (117, "Dahlia", 4, "Hydro", "Sword", "Mondstadt", "Support", 11962, 196, 713, "Burst > Skill > Normal", 5.7)
   - (118, "Skirk", 5, "Cryo", "Sword", "Outlander", "Main DPS", 13103, 349, 799, "Normal > Skill > Burst", 5.7)
   - (119, "Wonderland Manekin", 5, "Anemo", "Sword", "Outlander", "Main DPS", 10875, 297, 683, "Skill = Burst > Normal", 6.1)
   - (120, "Durin", 5, "Pyro", "Sword", "Mondstadt", "Main DPS", 13348, 342, 784, "Skill > Burst > Normal", 6.2)
   - (121, "Varka", 5, "Anemo", "Claymore", "Mondstadt", "Main DPS", 13864, 359, 799, "Normal = Skill > Burst", 6.4)
   - (122, "Nicole", 5, "Pyro", "Catalyst", "Mondstadt", "Support", 12907, 268, 696, "Burst > Skill > Normal", 6.6)
   - (123, "Prune", 4, "Anemo", "Catalyst", "Nod-Krai", "Sub-DPS", 9787, 225, 628, "Skill > Burst > Normal", 6.6)
   - (124, "Lohen", 5, "Cryo", "Polearm", "Nod-Krai", "Main DPS", 13103, 342, 789, "Normal > Skill > Burst", 6.6)
   - (125, "Alyosha", 4, "Electro", "Polearm", "Snezhnaya", "Support", 11636, 212, 751, "Burst > Skill > Normal", 7.0)
   - (126, "Odette", 5, "Cryo", "Sword", "Snezhnaya", "Sub-DPS", 12858, 337, 784, "Skill > Burst > Normal", 7.0)
   - (127, "Vesna", 5, "Anemo", "Sword", "Nod-Krai", "Main DPS", 13348, 342, 807, "Normal > Skill > Burst", 7.1)
   - (128, "Vodyanitsa", 5, "Hydro", "Catalyst", "Snezhnaya", "Healer", 14695, 234, 657, "Skill > Burst > Normal", 7.1)
   - (129, "Mitya", 5, "Electro", "Catalyst", "Snezhnaya", "Main DPS", 12858, 342, 765, "Normal > Skill > Burst", 7.2)
   - (130, "Valeriy", 4, "Electro", "Sword", "Snezhnaya", "Shielder", 12397, 202, 771, "Skill > Burst > Normal", 7.2)

2. Append 52 Missing Weapons (IDs 204 to 255) to `WEAPONS` list in `generate_csvs.py` (per `explorer_survey_2_gen2/handoff.md § 3.3`):
   - 24 5-star signatures (IDs 204 to 227) with proper signature_character_id linking to character IDs
   - 19 regional craftables (IDs 228 to 246) across Dragonspine, Sumeru, Fontaine, Nod-Krai, Snezhnaya (is_craftable = 1, signature_character_id = None)
   - 9 key meta staples & event weapons (IDs 247 to 255): Fleuve Cendre Ferryman (247), The Stringless (248), Cinnabar Spindle (249, linked to Albedo 6), Mountain-Bracing Bolt (250), Sturdy Bone (251), Fruitful Hook (252), Flower-Wreathed Feathers (253), Waveriding Whirl (254), Calamity of Eshu (255)

3. Run build/regeneration commands:
   - `python3 generate_csvs.py` to regenerate `data/*.csv`.
   - `python3 init_db.py` to drop and rebuild `genshin_learning.db`.
   - Verify `PRAGMA foreign_key_check;` returns 0 violations.
   - Run Milestone 2 E2E tests: `python3 tests/test_e2e_genshin.py --tier 1 --feature F5,F6,F7,F8` and ensure 20/20 tests pass.
   - Run `./.venv/bin/python test_security_oom.py` to ensure web tests pass (22/22).
4. Document all changes and verification outputs in `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m2/handoff.md`.

## 2026-11-20T17:15:22Z
You are worker_m2, an implementation worker agent.
Working directory: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m2
Project root: /home/nirjhar/Python Codes/Einstein/Databases
Exclusive write ownership:
- generate_csvs.py
- data/characters.csv (via generate_csvs.py)
- data/weapons.csv (via generate_csvs.py)
- genshin_learning.db (via init_db.py)

Mandatory reference: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/ORIGINAL_REQUEST.md
Supporting context:
- /home/nirjhar/Python Codes/Einstein/Databases/PROJECT.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m2/DISPATCH.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_2_gen2/handoff.md
- /home/nirjhar/Python Codes/Einstein/Databases/TEST_READY.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Task:
Execute Milestone 2 (M2): Characters & Weapons Catalog Ingestion:
1. Append 16 Missing Playable Characters (IDs 115 to 130) to `CHARACTERS` list in `generate_csvs.py` exactly per `explorer_survey_2_gen2/handoff.md § 3.2`.
2. Append 52 Missing Weapons (IDs 204 to 255: 24 Signatures, 19 Craftables, 9 Staples) to `WEAPONS` list in `generate_csvs.py` exactly per `explorer_survey_2_gen2/handoff.md § 3.3`.
3. Run regeneration and build commands:
   - `python3 generate_csvs.py` to overwrite `data/*.csv`.
   - `python3 init_db.py` to rebuild `genshin_learning.db`.
   - Verify `PRAGMA foreign_key_check;` returns 0 violations.
   - Run `python3 tests/test_e2e_genshin.py --tier 1 --feature F5,F6,F7,F8` and ensure all 20 tests pass.
   - Run `./.venv/bin/python test_security_oom.py` and ensure all 22 tests pass.
4. Periodically update `progress.md` in your working directory with `Last visited: [timestamp]`.
5. Write your comprehensive handoff report to `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m2/handoff.md`.
6. Send completion message to parent when finished.
