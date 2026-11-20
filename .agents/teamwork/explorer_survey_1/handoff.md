# Repository Architecture, Database Schema, and Pipeline Technical Survey

**Explorer**: `explorer_survey_1`  
**Date**: 2026-11-20  
**Project Root**: `/home/nirjhar/Python Codes/Einstein/Databases`  
**Working Directory**: `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_1`  
**Status**: Completed (Hard Handoff)

---

## 1. Observation

### 1.1 Repository Structure and File Inventory
The project is a local SQLite-backed educational and web-based SQL playground centered on Genshin Impact patch data.
Direct inspection via filesystem listing (`list_dir`) reveals the following relevant files:

| File Path | Size (Bytes) | Role / Responsibility |
|---|---|---|
| `genshin_learning.db` | 106,496 | Primary SQLite 3 database file containing 4 relational tables. |
| `init_db.py` | 7,162 | DDL definition and CSV loader script; drops and rebuilds database from `data/*.csv`. |
| `generate_csvs.py` | 57,065 | Generator script holding hardcoded Python data structures and serializing `data/*.csv`. |
| `verify_db.py` | 4,052 | Verification test suite asserting foreign keys, table row counts, regions, and 4 sample queries. |
| `test_security_oom.py` | 5,388 | Flask application integration test suite testing security authorizers, OOM capping, and CTE timeouts. |
| `app.py` | 14,045 | Flask web application providing the "Kaedehara Kazuha SQL Sanctuary" interactive UI and streaming API. |
| `main.py` | 3,976 | CLI interactive terminal SQL playground executing sample and custom queries. |
| `run_web.sh` | 636 | Shell launcher running `app.py` on fixed port 12000 using `.venv/bin/python`. |
| `requirements.txt` | 16 | Declares `Flask>=3.0,<4.0`. |
| `SQL_COMMANDS_GUIDE.md` | 13,143 | User SQL tutorial documentation (contains outdated counts: 105 characters, 69 weapons). |
| `templates/index.html` | 19,864 | Single-page UI template (contains hardcoded fallback stat pills: 114, 103, 64, 107). |
| `static/css/kazuha.css` | 18,740 | Themed styling for the web console and ER diagram. |
| `static/js/kazuha.js` | 27,249 | Client-side query streaming, autocomplete, ER rendering, and schema caching. |
| `data/characters.csv` | 9,799 | CSV source containing 114 character records (12 columns). |
| `data/weapons.csv` | 5,737 | CSV source containing 103 weapon records (9 columns). |
| `data/artifact_sets.csv` | 9,209 | CSV source containing 64 artifact set records (6 columns). |
| `data/character_builds.csv` | 16,546 | CSV source containing 107 build loadout records (11 columns). |

---

### 1.2 Database Technical Parameters (`genshin_learning.db`)
Direct PRAGMA query results executed against `genshin_learning.db`:
- `PRAGMA page_size`: `4096`
- `PRAGMA page_count`: `26` (Total size: ~104 KB)
- `PRAGMA encoding`: `'UTF-8'`
- `PRAGMA user_version`: `0`
- `PRAGMA journal_mode`: `'delete'`
- `PRAGMA foreign_keys`: `0` (foreign keys disabled by default per SQLite session; must be explicitly enabled via `PRAGMA foreign_keys = ON;` per connection)
- `PRAGMA foreign_key_check`: `[]` (0 violations currently detected)

---

### 1.3 Exact Schema Definition and Constraint Inventory

```sql
PRAGMA foreign_keys = ON;

-- 1. Characters Dimension Table
CREATE TABLE characters (
    character_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    rarity INTEGER NOT NULL CHECK (rarity IN (4, 5)),
    vision TEXT NOT NULL CHECK (vision IN ('Pyro', 'Hydro', 'Anemo', 'Electro', 'Dendro', 'Cryo', 'Geo')),
    weapon_type TEXT NOT NULL CHECK (weapon_type IN ('Sword', 'Claymore', 'Polearm', 'Bow', 'Catalyst')),
    region TEXT NOT NULL,
    default_role TEXT NOT NULL,
    base_hp INTEGER NOT NULL,
    base_atk INTEGER NOT NULL,
    base_def INTEGER NOT NULL,
    talent_priority TEXT NOT NULL,
    release_patch REAL NOT NULL
);

-- 2. Weapons Dimension Table
CREATE TABLE weapons (
    weapon_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    weapon_type TEXT NOT NULL CHECK (weapon_type IN ('Sword', 'Claymore', 'Polearm', 'Bow', 'Catalyst')),
    rarity INTEGER NOT NULL CHECK (rarity IN (3, 4, 5)),
    base_atk INTEGER NOT NULL,
    sub_stat_type TEXT NOT NULL,
    sub_stat_value REAL NOT NULL,
    is_craftable INTEGER NOT NULL CHECK (is_craftable IN (0, 1)),
    signature_character_id INTEGER REFERENCES characters(character_id) ON DELETE SET NULL
);

-- 3. Artifact Sets Dimension Table
CREATE TABLE artifact_sets (
    artifact_set_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    domain_name TEXT NOT NULL,
    region TEXT NOT NULL,
    two_piece_bonus TEXT NOT NULL,
    four_piece_bonus TEXT NOT NULL
);

-- 4. Character Builds Relational Bridge Table (Game8 Meta Builds)
CREATE TABLE character_builds (
    build_id INTEGER PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters(character_id) ON DELETE CASCADE,
    build_name TEXT NOT NULL,
    role TEXT NOT NULL,
    recommended_weapon_id INTEGER NOT NULL REFERENCES weapons(weapon_id) ON DELETE RESTRICT,
    recommended_artifact_id INTEGER NOT NULL REFERENCES artifact_sets(artifact_set_id) ON DELETE RESTRICT,
    sands_stat TEXT NOT NULL,
    goblet_stat TEXT NOT NULL,
    circlet_stat TEXT NOT NULL,
    tier_rating TEXT NOT NULL CHECK (tier_rating IN ('SS', 'S+', 'S', 'A')),
    playstyle_notes TEXT
);
```

#### Detailed Column & Constraint Breakdown by Table:

#### Table: `characters`
- **Current Row Count**: 114
- **Primary Key**: `character_id` (INTEGER PRIMARY KEY)
- **Foreign Keys**: None
- **Constraints**:
  - `name TEXT NOT NULL UNIQUE` (enforced via SQLite autoindex `sqlite_autoindex_characters_1`)
  - `rarity INTEGER NOT NULL CHECK (rarity IN (4, 5))`
  - `vision TEXT NOT NULL CHECK (vision IN ('Pyro', 'Hydro', 'Anemo', 'Electro', 'Dendro', 'Cryo', 'Geo'))`
  - `weapon_type TEXT NOT NULL CHECK (weapon_type IN ('Sword', 'Claymore', 'Polearm', 'Bow', 'Catalyst'))`
  - `region TEXT NOT NULL` (no CHECK constraint; Aloy requires string `'None'`)
  - `default_role TEXT NOT NULL`
  - `base_hp INTEGER NOT NULL`
  - `base_atk INTEGER NOT NULL`
  - `base_def INTEGER NOT NULL`
  - `talent_priority TEXT NOT NULL`
  - `release_patch REAL NOT NULL`
- **User-Defined Indexes**:
  - `idx_characters_region ON characters(region)`
  - `idx_characters_vision ON characters(vision)`

#### Table: `weapons`
- **Current Row Count**: 103
- **Primary Key**: `weapon_id` (INTEGER PRIMARY KEY)
- **Foreign Keys**:
  - `signature_character_id REFERENCES characters(character_id) ON DELETE SET NULL ON UPDATE NO ACTION` (nullable)
- **Constraints**:
  - `name TEXT NOT NULL UNIQUE` (enforced via SQLite autoindex `sqlite_autoindex_weapons_1`)
  - `weapon_type TEXT NOT NULL CHECK (weapon_type IN ('Sword', 'Claymore', 'Polearm', 'Bow', 'Catalyst'))`
  - `rarity INTEGER NOT NULL CHECK (rarity IN (3, 4, 5))`
  - `base_atk INTEGER NOT NULL`
  - `sub_stat_type TEXT NOT NULL`
  - `sub_stat_value REAL NOT NULL`
  - `is_craftable INTEGER NOT NULL CHECK (is_craftable IN (0, 1))`
- **User-Defined Indexes**:
  - `idx_weapons_type ON weapons(weapon_type)`

#### Table: `artifact_sets`
- **Current Row Count**: 64
- **Primary Key**: `artifact_set_id` (INTEGER PRIMARY KEY)
- **Foreign Keys**: None
- **Constraints**:
  - `name TEXT NOT NULL UNIQUE` (enforced via SQLite autoindex `sqlite_autoindex_artifact_sets_1`)
  - `domain_name TEXT NOT NULL`
  - `region TEXT NOT NULL`
  - `two_piece_bonus TEXT NOT NULL`
  - `four_piece_bonus TEXT NOT NULL`
- **User-Defined Indexes**: None

#### Table: `character_builds`
- **Current Row Count**: 107
- **Primary Key**: `build_id` (INTEGER PRIMARY KEY)
- **Foreign Keys**:
  - `character_id REFERENCES characters(character_id) ON DELETE CASCADE ON UPDATE NO ACTION`
  - `recommended_weapon_id REFERENCES weapons(weapon_id) ON DELETE RESTRICT ON UPDATE NO ACTION`
  - `recommended_artifact_id REFERENCES artifact_sets(artifact_set_id) ON DELETE RESTRICT ON UPDATE NO ACTION`
- **Constraints**:
  - `character_id INTEGER NOT NULL`
  - `build_name TEXT NOT NULL`
  - `role TEXT NOT NULL`
  - `recommended_weapon_id INTEGER NOT NULL`
  - `recommended_artifact_id INTEGER NOT NULL`
  - `sands_stat TEXT NOT NULL`
  - `goblet_stat TEXT NOT NULL`
  - `circlet_stat TEXT NOT NULL`
  - `tier_rating TEXT NOT NULL CHECK (tier_rating IN ('SS', 'S+', 'S', 'A'))`
  - `playstyle_notes TEXT` (nullable, but currently all 107 rows are populated)
- **User-Defined Indexes**:
  - `idx_builds_character ON character_builds(character_id)`
  - `idx_builds_tier ON character_builds(tier_rating)`

#### Triggers and Views:
- **Triggers**: 0 (no triggers defined in `sqlite_master`)
- **Views**: 0 (no views defined in `sqlite_master`)

---

### 1.4 Data Pipeline and Synchronization Architecture
The data flow operates in a strict 3-step unidirectional pipeline:

```
[ generate_csvs.py ]
   │
   │ writes CSV files via write_csv()
   ▼
[ data/*.csv ]
   │  - characters.csv (114 rows)
   │  - weapons.csv (103 rows)
   │  - artifact_sets.csv (64 rows)
   │  - character_builds.csv (107 rows)
   │
   │ read via init_db.py (load_csv + executescript)
   ▼
[ genshin_learning.db ]
   ▲
   │ validates schema, FKs, counts, queries
[ verify_db.py ]
```

1. **Generation (`generate_csvs.py`)**:
   - Contains hardcoded Python in-memory lists: `CHARACTERS` (114 items), `WEAPONS` (103 items), `ARTIFACT_SETS` (64 items), `BUILDS` (107 items).
   - Writes directly to `data/*.csv` with standard `csv.writer`, converting `None` to empty string `""`.
2. **Database Ingestion (`init_db.py`)**:
   - Drops existing tables and recreates `SCHEMA_SQL`.
   - Reads `data/*.csv` using `csv.reader`.
   - Handles `weapons.csv` nullable column `signature_character_id` by converting `""` to Python `None` (SQL `NULL`).
   - Inserts records via `cursor.executemany()`.
   - Executes `PRAGMA foreign_key_check;` and commits transaction.
3. **Verification (`verify_db.py`)**:
   - Connects with `PRAGMA foreign_keys = ON;`.
   - Verifies 0 FK violations via `PRAGMA foreign_key_check;`.
   - Asserts rigid table row counts: `characters == 114`, `weapons == 103`, `artifact_sets == 64`, `character_builds == 107`.
   - Asserts exact 64 artifact sets.
   - Asserts rigid regional breakdown:
     - `Liyue: 21, Mondstadt: 19, Inazuma: 17, Sumeru: 14, Fontaine: 13, Natlan: 10, Nod-Krai: 9, Outlander: 7, Snezhnaya: 4`
   - Executes 4 sample SQL queries (`Multi-table INNER JOIN`, `Craftable vs Non-Craftable Aggregation`, `1-Piece Tiaras Query`, `CTE with DENSE_RANK Window Function`) and asserts non-empty results.
4. **Web Interface & OOM Safeguards (`app.py` & `test_security_oom.py`)**:
   - `app.py` opens `file:{DB_PATH}?mode=ro` (read-only SQLite).
   - Installs C-level engine authorizer (`read_only_authorizer`) allowing only SELECT, READ, FUNCTION, and RECURSIVE actions. Blocks DROP, INSERT, UPDATE, DELETE, CREATE, ATTACH, DETACH, PRAGMA, VACUUM, REINDEX.
   - Installs progress handler watchdog (`make_progress_handler`) aborting runaway queries after `QUERY_TIMEOUT_SECONDS = 3.0`.
   - Streams results via `stream_with_context` in batches of `RESULT_BATCH_SIZE = 250`, capping stream at `MAX_STREAM_ROWS = 5000`.
   - Exposes REST endpoints: `/api/query`, `/api/schema`, `/api/table/<name>/preview`, `/api/samples`.

---

### 1.5 Verification of Existing Tests and Test Execution Command
Tests in the repository are executed via standard Python CLI:

1. **Database Integrity Verification**:
   ```bash
   python3 verify_db.py
   # Or using the local virtualenv:
   ./.venv/bin/python verify_db.py
   ```
   *Current Result*: Exits `0` with all checks passing (matching current 114 characters, 103 weapons, 64 artifact sets, 107 builds).

2. **Web API Security & OOM Test Suite**:
   ```bash
   ./.venv/bin/python test_security_oom.py
   ```
   *Current Result*: Exits `0` with `22 PASSED, 0 FAILED`.  
   *Note*: Running with system `python3 test_security_oom.py` fails with `ModuleNotFoundError: No module named 'flask'` because Flask is installed in `.venv`.

3. **Interactive SQL CLI Verification**:
   ```bash
   ./.venv/bin/python main.py
   ```
   Executes 4 showcase queries and provides an interactive `SQL>` prompt.

---

### 1.6 Current Database State vs Identified Requirements

| Domain | Entity / Field | Current Database State (`genshin_learning.db`) | Target State (per Requirements) | Defect Confirmed |
|---|---|---|---|---|
| **Weapons** | ID 128 (*Fang of the Mountain King*) | `base_atk = 608`, `sub_stat_value = 33.1` (CRIT Rate) | `base_atk = 741`, `sub_stat_value = 11.0` (CRIT Rate) | **YES** (corrupted stats) |
| **Weapons** | ID 131 (*A Thousand Blazing Suns*) | `base_atk = 608`, `sub_stat_value = 33.1` (CRIT Rate) | `base_atk = 741`, `sub_stat_value = 11.0` (CRIT Rate) | **YES** (corrupted stats) |
| **Characters** | ID 72 (*Arlecchino*) | `region = 'Fontaine'` | `region = 'Snezhnaya'` | **YES** (wrong region) |
| **Characters** | ID 99 (*Zibai*) | `region = 'Nod-Krai'` | `region = 'Liyue'` | **YES** (wrong region) |
| **Characters** | ID 102 (*Columbina*) | `region = 'Snezhnaya'` | `region = 'Nod-Krai'` | **YES** (wrong region) |
| **Characters** | ID 103 (*Sandrone*) | `vision = 'Geo'`, `weapon_type = 'Catalyst'` | `vision = 'Cryo'`, `weapon_type = 'Claymore'` | **YES** (wrong element & weapon) |
| **Characters** | ID 91 (*Iansan*) | `release_patch = 5.4` | `release_patch = 5.5` | **YES** (wrong patch) |
| **Characters** | ID 105 (*Aloy*) | `region = 'Outlander'` | `region = 'None'` | **YES** (wrong region) |
| **Characters** | ID 104 (*Capitano*) | Present in `characters` (ID 104) and `character_builds` (build 381) | Must be removed from both tables | **YES** (non-playable NPC present) |
| **Artifact Sets** | Set 59 (*Aubade of Morningstar and Moon*) | `region = 'Nod-Krai'`, `domain_name = "Moonchild's Treasures"` | Correct domain, region, casing, official scaling | **YES** (inaccurate patch details) |
| **Artifact Sets** | Set 60 (*A Day Carved from Rising Winds*) | `region = 'Nod-Krai'`, `domain_name = "Moonchild's Treasures"` | Correct domain, region, casing, official scaling | **YES** (inaccurate patch details) |
| **Artifact Sets** | Set 62 (*Disenchantment in Deep Shadow*) | `region = 'Snezhnaya'`, `domain_name = 'Thorny Crown of the Mountain Wind'` | Correct domain, region, casing, official scaling | **YES** (inaccurate patch details) |
| **Artifact Sets** | Set 63 (*Scarlet Proof*) | `region = 'Snezhnaya'`, `domain_name = 'Palace of Frost'` | Correct domain, region, casing, official scaling | **YES** (inaccurate patch details) |
| **Artifact Sets** | Set 64 (*Heart of the Furnace*) | `region = 'Snezhnaya'`, `domain_name = 'Palace of Frost'` | Correct domain, region, casing, official scaling | **YES** (inaccurate patch details) |
| **Characters** | 16 Missing Playable Characters | 0 present in `characters` | All 16 must be ingested | **YES** (missing from roster) |
| **Weapons** | 24 Missing Signatures + 19 Craftables + Staples | None of the 43+ missing weapons are present | All must be ingested | **YES** (missing from catalog) |
| **Builds** | Characters without any build | 43 characters have 0 builds in `character_builds` | 100% of playable characters must have >= 1 build | **YES** (43 missing builds) |
| **Builds** | Mismatched builds (*Furina*, *Albedo*, *Shenhe*) | Furina build 305 uses Favonius Sword (188); Albedo build 387 uses Flute of Ezpitzal (182); Shenhe build 392 uses PJWS (135) | Re-link to proper signature and BiS weapons | **YES** (mismatched weapons) |

---

## 2. Logic Chain

1. **Dual Source of Truth and Pipeline Order**:
   - *Observation*: `generate_csvs.py` contains in-memory data structures and writes directly to `data/*.csv`. `init_db.py` reads `data/*.csv` and populates `genshin_learning.db`.
   - *Inference*: Any changes made directly to `data/*.csv` or `genshin_learning.db` without updating `generate_csvs.py` will be irreversibly overwritten the next time `generate_csvs.py` is executed.
   - *Conclusion*: `generate_csvs.py` is the root generator. To achieve 100% reproducibility and prevent desynchronization, all modifications must be implemented in `generate_csvs.py`, then exported to `data/*.csv`, and then loaded into `genshin_learning.db` via `init_db.py`.

2. **Foreign Key Deletion Dependencies**:
   - *Observation*: `character_builds.character_id` has `ON DELETE CASCADE`, while `recommended_weapon_id` and `recommended_artifact_id` have `ON DELETE RESTRICT`. In `weapons`, `signature_character_id` has `ON DELETE SET NULL`.
   - *Inference*: If Capitano (ID 104) is deleted from `characters.csv` without removing build 381 from `character_builds.csv`, running `init_db.py` will fail with `sqlite3.IntegrityError: FOREIGN KEY constraint failed` when inserting `character_builds`.
   - *Conclusion*: Capitano's build (ID 381) must be explicitly deleted from `generate_csvs.py` / `character_builds.csv` in lockstep with Capitano's removal from `characters.csv`.

3. **Fragility of `verify_db.py` Assertions**:
   - *Observation*: `verify_db.py` asserts exact counts: `characters == 114`, `weapons == 103`, `character_builds == 107`, and exact regional counts (`Liyue: 21, Mondstadt: 19, Inazuma: 17, Sumeru: 14, Fontaine: 13, Natlan: 10, Nod-Krai: 9, Outlander: 7, Snezhnaya: 4`).
   - *Inference*: Modifying character regions (Arlecchino to Snezhnaya, Zibai to Liyue, Columbina to Nod-Krai, Aloy to None), removing Capitano (-1), adding 16 characters (+16), adding weapons (+43+), and adding builds (+43+) will immediately cause multiple assertion failures in `verify_db.py`.
   - *Conclusion*: `verify_db.py` must be upgraded to dynamically validate relational consistency, or its expected constants must be updated to match the post-expansion counts, and additional semantic assertions (e.g. 0 characters without builds, weapon stat validity) must be added.

4. **Regional Constraints and Aloy Region Assignment**:
   - *Observation*: The `characters` table definition has `region TEXT NOT NULL`, with no `CHECK (region IN (...))` constraint.
   - *Inference*: Storing string `'None'` for Aloy is fully compatible with SQLite's schema and will not violate the `NOT NULL` constraint because `'None'` is a non-empty `TEXT` value.
   - *Conclusion*: Aloy's region must be set to the string `'None'` in `characters`, and verification logic in `verify_db.py` must account for `'None'` as a distinct regional category with 1 character.

5. **Missing Indexes on Foreign Key Columns**:
   - *Observation*: In `character_builds`, indexes exist for `character_id` and `tier_rating`, but NOT for `recommended_weapon_id` or `recommended_artifact_id`. In `weapons`, `signature_character_id` is unindexed.
   - *Inference*: Multi-table JOIN queries joining `character_builds` with `weapons` and `artifact_sets` require scanning unindexed columns or scanning child tables.
   - *Conclusion*: Adding `CREATE INDEX idx_builds_weapon ON character_builds(recommended_weapon_id)` and `CREATE INDEX idx_builds_artifact ON character_builds(recommended_artifact_id)` in `SCHEMA_SQL` will improve query planning for educational SQL exploration.

---

## 3. Potential Architecture and Integrity Issues

1. **Dual Source of Truth / Desynchronization Vulnerability**:
   - Data exists in Python lists in `generate_csvs.py`, in CSV files in `data/`, and in SQLite binary `genshin_learning.db`.
   - There is no automated bidirectional synchronization. If one is edited without the others, data pipelines drift silently.
2. **Hardcoded Test Constraints in `verify_db.py`**:
   - `verify_db.py` currently relies on brittle hardcoded integers (`114`, `103`, `64`, `107`).
   - It fails to verify business rules: 0 playable characters without builds, valid weapon stat combinations, correct domain associations, or CSV-to-DB equality.
3. **Missing Foreign Key Indexes**:
   - Lack of indexes on `character_builds(recommended_weapon_id)` and `character_builds(recommended_artifact_id)` is an educational anti-pattern in a database designed to teach `EXPLAIN QUERY PLAN` and relational optimization.
4. **Session-Dependent Foreign Key Enforcement**:
   - SQLite does not enforce foreign keys unless `PRAGMA foreign_keys = ON;` is executed on each opened connection. Any script connecting without this pragma can corrupt relational integrity undetected.
5. **Permissive Schema on Categorical Columns**:
   - While `vision`, `weapon_type`, and `tier_rating` have `CHECK` constraints, columns such as `region`, `default_role`, `role`, `sub_stat_type`, `sands_stat`, `goblet_stat`, and `circlet_stat` have no domain constraints, allowing arbitrary strings or formatting typos.
6. **Incomplete Coverage of Meta Builds**:
   - 43 out of 114 playable characters (37.7%) have no corresponding loadouts in `character_builds`.
7. **Execution Environment Sensitivity**:
   - `test_security_oom.py` relies on packages in `.venv` and fails under standard system Python. Commands should explicitly invoke `./.venv/bin/python`.
8. **Outdated Secondary Artifacts**:
   - `SQL_COMMANDS_GUIDE.md` references obsolete database counts (105 characters, 69 weapons, 34 artifact sets, 97 builds).
   - `templates/index.html` contains static initial values in HTML spans (`114`, `103`, `64`, `107`). While updated via JavaScript after `/api/schema` loads, they can cause visual layout shift.

---

## 4. Caveats

- **Scope Boundary**: This survey was conducted in read-only mode. No project code, database tables, or CSV files were altered.
- **Assumptions on Future Roster IDs**: The new 16 playable characters and 43+ weapons will need assigned IDs. Whether they follow contiguous auto-increment numbering or specific regional ranges must be aligned across implementation phases.
- **Flask Server Running Status**: The web server is not running as a persistent daemon during this inspection; all web API tests were executed via the Flask `test_client()` in `test_security_oom.py`.

---

## 5. Conclusion

1. **Repository Readiness**: The database schema in `init_db.py` is structurally solid with robust table definitions, primary keys, and cascade/restrict foreign key constraints.
2. **Immediate Remediation Path**:
   - Step 1: Update in-memory data structures in `generate_csvs.py` to remediate R1 defects, add R2 characters, add R3 weapons, and backfill R4 builds.
   - Step 2: Run `generate_csvs.py` to regenerate `data/*.csv`.
   - Step 3: Run `init_db.py` to rebuild `genshin_learning.db` and confirm 0 FK violations.
   - Step 4: Update `verify_db.py` to test the new counts, 0 orphaned records, 100% build coverage, and CSV-DB parity.
   - Step 5: Run `./.venv/bin/python verify_db.py` and `./.venv/bin/python test_security_oom.py` to achieve 100% green verification.

---

## 6. Verification Method

To independently verify all findings in this survey report, execute the following commands in order:

1. **Inspect Current Database Row Counts**:
   ```bash
   ./.venv/bin/python -c "
   import sqlite3
   conn = sqlite3.connect('genshin_learning.db')
   cur = conn.cursor()
   for t in ['characters', 'weapons', 'artifact_sets', 'character_builds']:
       print(t, cur.execute(f'SELECT count(*) FROM {t};').fetchone()[0])
   "
   ```
   *Expected Output*: `characters 114`, `weapons 103`, `artifact_sets 64`, `character_builds 107`.

2. **Verify Relational Integrity**:
   ```bash
   ./.venv/bin/python -c "
   import sqlite3
   conn = sqlite3.connect('genshin_learning.db')
   cur = conn.cursor()
   print('Violations:', cur.execute('PRAGMA foreign_key_check;').fetchall())
   "
   ```
   *Expected Output*: `Violations: []`.

3. **Verify Existing Database Verification Suite**:
   ```bash
   ./.venv/bin/python verify_db.py
   ```
   *Expected Output*: All checks pass with `ALL EXPANDED DATABASE TESTS PASSED SUCCESSFULLY!`.

4. **Verify Web Security and OOM Test Suite**:
   ```bash
   ./.venv/bin/python test_security_oom.py
   ```
   *Expected Output*: `TEST SUMMARY: 22 PASSED, 0 FAILED`.

5. **Verify Defective Weapon Stats (Weapons 128 & 131)**:
   ```bash
   ./.venv/bin/python -c "
   import sqlite3
   conn = sqlite3.connect('genshin_learning.db')
   cur = conn.cursor()
   print(cur.execute('SELECT weapon_id, name, base_atk, sub_stat_value FROM weapons WHERE weapon_id IN (128, 131);').fetchall())
   "
   ```
   *Expected Output*: Both show `base_atk = 608` and `sub_stat_value = 33.1` (confirming defect).

6. **Verify Capitano and Build 381**:
   ```bash
   ./.venv/bin/python -c "
   import sqlite3
   conn = sqlite3.connect('genshin_learning.db')
   cur = conn.cursor()
   print('Capitano:', cur.execute('SELECT character_id, name FROM characters WHERE character_id = 104;').fetchall())
   print('Build 381:', cur.execute('SELECT build_id, character_id, build_name FROM character_builds WHERE character_id = 104;').fetchall())
   "
   ```
   *Expected Output*: Capitano (104) and Build 381 exist and must be removed.

7. **Verify Characters Lacking Builds (43 Count)**:
   ```bash
   ./.venv/bin/python -c "
   import sqlite3
   conn = sqlite3.connect('genshin_learning.db')
   cur = conn.cursor()
   missing = cur.execute('SELECT count(*) FROM characters c LEFT JOIN character_builds cb ON c.character_id = cb.character_id WHERE cb.build_id IS NULL;').fetchone()[0]
   print('Missing builds count:', missing)
   "
   ```
   *Expected Output*: `Missing builds count: 43`.
