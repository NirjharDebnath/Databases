# Test Infrastructure & E2E Testing Architecture

**Project**: Genshin Impact Database Remediation & Expansion  
**Database**: `genshin_learning.db` (SQLite 3)  
**Test Suite**: `tests/test_e2e_genshin.py`  
**Standard**: Teamwork Project Pattern (Requirement-Driven Opaque-Box E2E Testing)

---

## 1. Overview & Testing Philosophy

The End-to-End (E2E) testing infrastructure provides an independent, authoritative quality gate for the Genshin Impact educational database and SQL playground. Testing is designed strictly **opaque-box** and **requirement-driven**:
- **Authoritative Requirements**: Derived directly from `ORIGINAL_REQUEST.md` (R1–R5) and `PROJECT.md § Feature Inventory` (F1–F14).
- **Implementation Independence**: Tests inspect observable database tables, SQLite relational constraints, CSV seed exports, and query planning behavior without depending on private internal helpers or generator implementations.
- **Zero External Dependencies**: Built entirely on Python's standard library (`sqlite3`, `unittest`, `csv`, `sys`, `os`, `re`), guaranteeing zero dependency friction and seamless execution in any Python 3 environment.

---

## 2. Test Architecture & Runner Design

The test harness resides in `tests/test_e2e_genshin.py` and provides both a standard `unittest` test suite and a high-performance CLI test runner.

```
                    ┌────────────────────────────┐
                    │    ORIGINAL_REQUEST.md     │
                    │         PROJECT.md         │
                    └─────────────┬──────────────┘
                                  │ Requirements & Contracts
                                  ▼
                    ┌────────────────────────────┐
                    │ tests/test_e2e_genshin.py  │
                    │   (4-Tier Test Taxonomy)   │
                    └──────┬──────────────┬──────┘
                           │              │
             Validates DB  │              │ Validates CSVs
                           ▼              ▼
                ┌──────────────────┐  ┌─────────────┐
                │genshin_learning.db│  │  data/*.csv │
                └──────────────────┘  └─────────────┘
```

### CLI Command Support
The runner supports flexible invocation parameters:
- **Full Run (Default)**:
  ```bash
  python3 tests/test_e2e_genshin.py
  # or using project virtual environment:
  ./.venv/bin/python tests/test_e2e_genshin.py
  ```
- **Filter by Tier**:
  ```bash
  python3 tests/test_e2e_genshin.py --tier 1
  python3 tests/test_e2e_genshin.py --tier 2,3
  ```
- **Filter by Feature**:
  ```bash
  python3 tests/test_e2e_genshin.py --feature F1
  python3 tests/test_e2e_genshin.py --feature F2,F3,F4
  ```
- **Custom Database Target**:
  ```bash
  python3 tests/test_e2e_genshin.py --db /path/to/custom_test.db
  ```
- **Verbose Output**:
  ```bash
  python3 tests/test_e2e_genshin.py -v
  ```

### Exit Code Contract
- `0`: All executed tests passed cleanly.
- `1`: One or more test assertions failed, or an unhandled exception occurred.

---

## 3. Four-Tier Test Taxonomy

The test suite organizes test cases into 4 distinct verification tiers exceeding 170+ total test cases:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        E2E Test Hierarchy                              │
├────────────────────────────────┬───────────────────────────────────────┤
│ Tier 1: Feature Coverage       │ >=5 test cases per feature (F1–F14)   │
│                                │ Total: 70 test cases                  │
├────────────────────────────────┼───────────────────────────────────────┤
│ Tier 2: Boundary & Corner Cases│ Bounds, constraints, nullability,     │
│                                │ escaping, types, edge values          │
│                                │ Total: 70+ test cases                 │
├────────────────────────────────┼───────────────────────────────────────┤
│ Tier 3: Cross-Feature Pairs    │ Relational joins, weapon-class match, │
│                                │ cascade/restrict, multi-build coherency│
│                                │ Total: 25+ test cases                 │
├────────────────────────────────┼───────────────────────────────────────┤
│ Tier 4: Real-World Scenarios   │ Complex SQL queries, team builders,   │
│                                │ damage rankings, domain routing       │
│                                │ Total: 6+ test cases                  │
└────────────────────────────────┴───────────────────────────────────────┘
```

### Tier 1: Feature Coverage (F1 to F14)
- **F1: Artifact Sets Remediation**: Sets 59, 60, 62, 63, 64 naming, Mondstadt domain pairing for Set 62, Inverted Glacier for 63/64, official 2pc (+80 EM for 59, +18% ATK for 60/62/63/64) and 4pc mechanics.
- **F2: Weapon Stats Correction**: Weapons 128 (*Fang of the Mountain King*) and 131 (*A Thousand Blazing Suns*) verified at 741 Base ATK and 11.0% CRIT Rate.
- **F3: Character Attributes**: Arlecchino (Snezhnaya), Zibai (Liyue), Columbina (Nod-Krai), Sandrone (Cryo Claymore), Iansan (5.5), Aloy (None).
- **F4: Capitano Purge**: Verified non-playable NPC Capitano (104) and Build 381 purged completely from DB and FK references.
- **F5: Missing Playable Characters**: Ingestion of 16 characters (IDs 115–130) with valid visions, weapon types, base stats, and patches.
- **F6: Missing 5-Star Signatures**: Ingestion of 24 5★ signature weapons (IDs 204–227) with non-null `signature_character_id` foreign keys.
- **F7: Missing Regional Craftables**: Ingestion of 19 craftables (IDs 228–246) across Dragonspine, Sumeru, Fontaine, Nod-Krai, and Snezhnaya.
- **F8: Meta Staples & Event Weapons**: Ingestion of 9 staple weapons (IDs 247–255), including *Fleuve Cendre Ferryman*, *The Stringless*, *Cinnabar Spindle*, and Natlan series.
- **F9: Missing Character Builds Backfill**: Backfill of 43 character builds (IDs 408–450) achieving 0 orphaned characters.
- **F10: New Characters Builds Ingestion**: Verified builds for all 16 new characters (IDs 451–466).
- **F11: Alternative Meta Roles**: Multi-build variants for Mavuika (Build 467 Support), Citlali (Build 468 F2P), and Chasca (Build 469 F2P).
- **F12: Build Re-linking**: Corrected weapon links for Furina (Build 305 -> 247 Ferryman), Albedo (Build 387 -> 249 Cinnabar), Shenhe (Build 392 -> 204 Calamity Queller).
- **F13: Data Pipeline Synchronization**: 1:1 row and column parity between all CSV files in `data/` and SQLite tables.
- **F14: Database Verification Suite & Constraints**: Verification of schema indexes, `PRAGMA foreign_key_check`, and exact regional distributions.

### Tier 2: Boundary & Corner Cases
- **Statistical Extremes**: Max weapon base ATK (741), min character base ATK (150), stat caps (CRIT Rate <= 44.1%, CRIT DMG <= 88.2%, ER <= 61.3%).
- **Categorical Domain Integrity**: `CHECK` constraints strictly enforced for `rarity` (4, 5 for chars; 3, 4, 5 for weapons), `vision` (7 elements), `weapon_type` (5 types), `tier_rating` ('SS', 'S+', 'S', 'A').
- **Regional Edge Cases**: Aloy's region strictly string `'None'` (not SQL NULL or empty string); total regional sum equals 129.
- **String Escaping & Quoting**: Safe handling of names containing single quotes, hyphens, and parentheses without syntax errors.
- **Nullability & Foreign Key Constraints**: `signature_character_id` nullability handling (empty string `""` in CSV ➔ SQL `NULL`).

### Tier 3: Cross-Feature Combinations
- **Weapon-Character Compatibility**: 100% of rows in `character_builds` have `characters.weapon_type == weapons.weapon_type`.
- **Relational Cascade & Restrict**:
  - `character_builds.character_id` ON DELETE CASCADE.
  - `character_builds.recommended_weapon_id` ON DELETE RESTRICT.
  - `character_builds.recommended_artifact_id` ON DELETE RESTRICT.
  - `weapons.signature_character_id` ON DELETE SET NULL.
- **Complete Relational 4-Table Join**: INNER JOIN across `characters`, `weapons`, `artifact_sets`, and `character_builds` preserves all 168 builds without data loss.
- **Multi-Role Divergence**: Verification that characters with multiple builds maintain valid independent loadouts.

### Tier 4: Real-World Application Scenarios
- **Scenario 1**: 4-member elemental reaction team composition query (Main DPS, Sub-DPS, Support, Healer across complementary visions).
- **Scenario 2**: Theoretical maximum base attack ranking and scaling calculation.
- **Scenario 3**: Artifact domain route optimization and resin-efficiency analysis by region.
- **Scenario 4**: F2P equipment recommendation engine (budget craftable and 4★ builds for every element).
- **Scenario 5**: Regional character roster & material planning dashboard.
- **Scenario 6**: High-tier meta matrix query using SQL window functions (`DENSE_RANK`).

---

## 4. Coverage Thresholds & Quality Gates

To achieve `TEST_READY` status and pass Milestone `M_FINAL`, the database and pipeline must satisfy the following strict quantitative criteria:

| Metric | Target Threshold | Scope / Validation |
|---|---|---|
| **Total Test Count** | **>= 150 Tests** (Actual: 171) | Entire test suite across Tiers 1–4 |
| **Tier 1 Coverage** | **>= 70 Tests** (5 per F1–F14) | Features F1 through F14 |
| **Tier 2 Coverage** | **>= 70 Tests** | Bounds, checks, types, escaping |
| **Tier 3 Coverage** | **>= 25 Tests** | Cross-feature & relational pairs |
| **Tier 4 Coverage** | **>= 6 Tests** | Realistic multi-table query scenarios |
| **Pass Rate** | **100%** | Zero failures or errors |
| **FK Violations** | **0** | `PRAGMA foreign_key_check` |
| **Orphaned Characters** | **0** | Characters without builds |
| **Table Row Counts** | `characters: 129`<br>`weapons: 155`<br>`artifact_sets: 64`<br>`character_builds: 168` | Exact schema counts |
| **CSV Parity** | **1:1 Exact Match** | `data/*.csv` vs DB tables |

---

## 5. Verification Commands

Run the test suite via either command:
```bash
python3 tests/test_e2e_genshin.py
./.venv/bin/python tests/test_e2e_genshin.py
```
Expected output upon test completion:
```
======================================================================
GENSHIN IMPACT DATABASE E2E TEST RUNNER
======================================================================
Running 171 test cases across 4 tiers...
  [Tier 1] Feature Coverage Tests: 70/70 PASSED
  [Tier 2] Boundary & Corner Case Tests: 70/70 PASSED
  [Tier 3] Cross-Feature Relational Tests: 25/25 PASSED
  [Tier 4] Real-World Application Scenarios: 6/6 PASSED
======================================================================
OVERALL SUMMARY: 171 PASSED, 0 FAILED (Duration: 0.18s)
EXIT CODE: 0
======================================================================
```
