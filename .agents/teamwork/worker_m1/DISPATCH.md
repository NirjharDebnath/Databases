# Dispatch Task for Worker M1 (Database Defect Remediation)

**Working Directory**: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m1
**Project Root**: /home/nirjhar/Python Codes/Einstein/Databases
**Exclusive Write Ownership**:
- `generate_csvs.py`
- `data/characters.csv` (via `python3 generate_csvs.py`)
- `data/weapons.csv` (via `python3 generate_csvs.py`)
- `data/artifact_sets.csv` (via `python3 generate_csvs.py`)
- `data/character_builds.csv` (via `python3 generate_csvs.py`)
- `genshin_learning.db` (via `python3 init_db.py`)

**Mandatory Integrity Warning**:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

**Mandatory Inputs**:
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/ORIGINAL_REQUEST.md
- /home/nirjhar/Python Codes/Einstein/Databases/PROJECT.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_1/handoff.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_2_gen2/handoff.md

**Detailed Requirements (Milestone 1)**:
Apply all factual and attribute corrections in `generate_csvs.py`:
1. Artifact Sets 59, 60, 62, 63, and 64:
   - Set 59 ("Aubade of Morningstar and Moon"): 2pc = "+80 Elemental Mastery", 4pc = "When off-field, Lunar Reaction DMG +20%. When party Moonsign Level is Ascendant Gleam, Lunar Reaction DMG +40%"
   - Set 60 ("A Day Carved from Rising Winds"): 4pc = "Normal/Charged/Skill/Burst hits grant Blessing of Pastoral Winds (ATK +25% for 6s); upgrades with Witch's Homework to Resolve of Pastoral Winds (CRIT Rate +20%)"
   - Set 62 ("Disenchantment in Deep Shadow"): Region = "Mondstadt", domain = "Thorny Crown of the Mountain Wind", 2pc = "+18% ATK", 4pc = "Superconduct Reaction DMG +80% (Stellar-Conduct +40%); attacking affected foes increases CRIT Rate by 16%"
   - Set 63 ("Scarlet Proof"): Domain = "Inverted Glacier", Region = "Snezhnaya", 2pc = "+18% ATK", 4pc = "After triggering a Stellar Swirl reaction, CRIT Rate +16% and Stellar Swirl DMG +40% for 10s"
   - Set 64 ("Heart of the Furnace"): Domain = "Inverted Glacier", Region = "Snezhnaya", 2pc = "+18% ATK", 4pc = "Triggering Stellar Glimmer or dealing its DMG grants ATK +12% for 12s, and increases party Stellar Glimmer DMG by 50%"
2. Weapon stats for IDs 128 & 131:
   - Fang of the Mountain King (ID 128): Base ATK = 741, sub_stat_type = "CRIT Rate", sub_stat_value = 11.0
   - A Thousand Blazing Suns (ID 131): Base ATK = 741, sub_stat_type = "CRIT Rate", sub_stat_value = 11.0
3. Character attributes:
   - Arlecchino (ID 72): region = "Snezhnaya"
   - Zibai (ID 99): region = "Liyue"
   - Columbina (ID 102): region = "Nod-Krai"
   - Sandrone (ID 103): vision = "Cryo", weapon_type = "Claymore"
   - Iansan (ID 91): release_patch = 5.5
   - Aloy (ID 105): region = "None"
4. Non-playable NPC Capitano (ID 104) removal:
   - Remove row 104 from `CHARACTERS` in `generate_csvs.py`
   - Remove row 381 from `BUILDS` in `generate_csvs.py`
5. Execution & Verification:
   - Run `python3 generate_csvs.py` to overwrite `data/*.csv`.
   - Run `python3 init_db.py` to rebuild `genshin_learning.db`.
   - Run `python3 -c "import sqlite3; conn=sqlite3.connect('genshin_learning.db'); print(conn.execute('PRAGMA foreign_key_check;').fetchall())"` and verify 0 violations.
   - Run `./.venv/bin/python test_security_oom.py` to ensure existing app tests still pass.
   - Document all changes and verification outputs in `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m1/handoff.md`.

## 2026-11-20T16:57:38Z
You are worker_m1, an implementation worker agent.
Working directory: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m1
Project root: /home/nirjhar/Python Codes/Einstein/Databases
Exclusive write ownership:
- generate_csvs.py
- data/characters.csv (via generate_csvs.py)
- data/weapons.csv (via generate_csvs.py)
- data/artifact_sets.csv (via generate_csvs.py)
- data/character_builds.csv (via generate_csvs.py)
- genshin_learning.db (via init_db.py)

Mandatory reference: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/ORIGINAL_REQUEST.md
Supporting context:
- /home/nirjhar/Python Codes/Einstein/Databases/PROJECT.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m1/DISPATCH.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_1/handoff.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_2_gen2/handoff.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Task:
Execute Milestone 1 (M1): Database Defect Remediation & Capitano Purge:
1. Update Artifact Sets 59, 60, 62, 63, and 64 in `generate_csvs.py` (official names, domains, regions, 2pc/4pc scaling per explorer_survey_2_gen2 handoff § 3.1):
   - Set 59 ("Aubade of Morningstar and Moon"): 2pc = "+80 Elemental Mastery", 4pc = "When off-field, Lunar Reaction DMG +20%. When party Moonsign Level is Ascendant Gleam, Lunar Reaction DMG +40%"
   - Set 60 ("A Day Carved from Rising Winds"): 4pc = "Normal/Charged/Skill/Burst hits grant Blessing of Pastoral Winds (ATK +25% for 6s); upgrades with Witch's Homework to Resolve of Pastoral Winds (CRIT Rate +20%)"
   - Set 62 ("Disenchantment in Deep Shadow"): Region = "Mondstadt", domain = "Thorny Crown of the Mountain Wind", 2pc = "+18% ATK", 4pc = "Superconduct Reaction DMG +80% (Stellar-Conduct +40%); attacking affected foes increases CRIT Rate by 16%"
   - Set 63 ("Scarlet Proof"): Domain = "Inverted Glacier", Region = "Snezhnaya", 2pc = "+18% ATK", 4pc = "After triggering a Stellar Swirl reaction, CRIT Rate +16% and Stellar Swirl DMG +40% for 10s"
   - Set 64 ("Heart of the Furnace"): Domain = "Inverted Glacier", Region = "Snezhnaya", 2pc = "+18% ATK", 4pc = "Triggering Stellar Glimmer or dealing its DMG grants ATK +12% for 12s, and increases party Stellar Glimmer DMG by 50%"
2. Correct weapon stats for IDs 128 & 131 in `generate_csvs.py`:
   - Fang of the Mountain King (ID 128): Base ATK = 741, sub_stat_type = "CRIT Rate", sub_stat_value = 11.0
   - A Thousand Blazing Suns (ID 131): Base ATK = 741, sub_stat_type = "CRIT Rate", sub_stat_value = 11.0
3. Correct character attributes in `generate_csvs.py`:
   - Arlecchino (ID 72): region = "Snezhnaya"
   - Zibai (ID 99): region = "Liyue"
   - Columbina (ID 102): region = "Nod-Krai"
   - Sandrone (ID 103): vision = "Cryo", weapon_type = "Claymore"
   - Iansan (ID 91): release_patch = 5.5
   - Aloy (ID 105): region = "None"
4. Purge non-playable NPC Capitano (ID 104) and Build 381 synchronously from `generate_csvs.py`:
   - Remove Capitano row from `CHARACTERS`
   - Remove Build 381 row from `BUILDS`
5. Run build/regeneration commands:
   - `python3 generate_csvs.py` to overwrite `data/*.csv`.
   - `python3 init_db.py` to drop and rebuild `genshin_learning.db`.
   - Verify `PRAGMA foreign_key_check;` returns 0 violations.
   - Run `./.venv/bin/python test_security_oom.py` to ensure web tests remain green (22 passed).
6. Periodically update `progress.md` with `Last visited: [timestamp]`.
7. Write comprehensive handoff report to `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/worker_m1/handoff.md`.
8. Send completion message to parent when finished.
