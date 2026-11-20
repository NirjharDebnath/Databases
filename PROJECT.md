# Project: Genshin Impact Database Remediation & Expansion

## Architecture
- **Data Pipeline**: Unidirectional single source of truth:
  `generate_csvs.py` (Python data structures) ➔ `data/*.csv` ➔ `init_db.py` (DDL + CSV loader) ➔ `genshin_learning.db` (SQLite database) ➔ `verify_db.py` (Automated verification) & `app.py` / `test_security_oom.py` (Flask educational web app).
- **Relational Tables**:
  - `characters` (129 playable characters, 0 NPCs): `character_id`, `name`, `rarity`, `vision`, `weapon_type`, `region`, `default_role`, `base_hp`, `base_atk`, `base_def`, `talent_priority`, `release_patch`.
  - `weapons` (155 weapons): `weapon_id`, `name`, `weapon_type`, `rarity`, `base_atk`, `sub_stat_type`, `sub_stat_value`, `is_craftable`, `signature_character_id` (FK -> characters.character_id ON DELETE SET NULL).
  - `artifact_sets` (64 sets): `artifact_set_id`, `name`, `domain_name`, `region`, `two_piece_bonus`, `four_piece_bonus`.
  - `character_builds` (168 builds): `build_id`, `character_id` (FK -> characters.character_id ON DELETE CASCADE), `build_name`, `role`, `recommended_weapon_id` (FK -> weapons.weapon_id ON DELETE RESTRICT), `recommended_artifact_id` (FK -> artifact_sets.artifact_set_id ON DELETE RESTRICT), `sands_stat`, `goblet_stat`, `circlet_stat`, `tier_rating`, `playstyle_notes`.
- **Relational Indexes**:
  - `idx_characters_region`, `idx_characters_vision`
  - `idx_weapons_type`, `idx_weapons_signature`
  - `idx_builds_character`, `idx_builds_tier`, `idx_builds_weapon`, `idx_builds_artifact`

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F1 | Artifact Sets 59, 60, 62, 63, 64 Remediation | Fix names, regions (Mondstadt for 62), domains (Inverted Glacier for 63/64), 2pc (+18% ATK for 60/62/63/64, +80 EM for 59) and official 4pc scaling | M1 | Survey (R1) |
| F2 | Weapon Stats Correction (128 & 131) | Fang of the Mountain King (128) & A Thousand Blazing Suns (131) to 741 Base ATK and 11.0% CRIT Rate | M1 | Survey (R1) |
| F3 | Character Attributes Correction | Arlecchino (Snezhnaya), Zibai (Liyue), Columbina (Nod-Krai), Sandrone (Cryo Claymore), Iansan (5.5), Aloy (None) | M1 | Survey (R1) |
| F4 | Capitano Purge | Delete non-playable NPC Capitano (104) and Build 381 cleanly from DB and CSV generator | M1 | Survey (R1) |
| F5 | Missing Characters Ingestion (16 chars) | Add Ifa, Escoffier, Dahlia, Skirk, Wonderland Manekin, Durin, Varka, Nicole, Prune, Lohen, Alyosha, Odette, Vesna, Vodyanitsa, Mitya, Valeriy (IDs 115–130) | M2 | Survey (R2) |
| F6 | Missing 5-Star Signatures (24 weapons) | Ingest Calamity Queller, Everlasting Moonglow, Sunny Morning Sleep-In, Vivid Notions, Azurelight, and 19 others (IDs 204–227) | M2 | Survey (R3) |
| F7 | Missing Craftables Ingestion (19 weapons) | Ingest Dragonspine (3), Sumeru (4), Fontaine (2), Nod-Krai (5), Snezhnaya (5) craftables (IDs 228–246) | M2 | Survey (R3) |
| F8 | Meta Staples & Event Weapons (9 weapons) | Ingest Fleuve Cendre Ferryman (247), The Stringless (248), Cinnabar Spindle (249), Natlan gacha/event series (250–255) | M2 | Survey (R3) |
| F9 | Missing Character Builds Backfill (43 chars) | Backfill verified meta builds for all 43 existing characters lacking builds (Barbara, Noelle, Beidou, Yaoyao, etc.) (IDs 408–450) | M3 | Survey (R4) |
| F10 | New Characters Builds Ingestion (16 chars) | Ingest verified meta builds for all 16 new characters from R2 (IDs 451–466) | M3 | Survey (R4) |
| F11 | Alternative Meta Roles (3 builds) | Ingest Mavuika Cinder City Support (467), Citlali F2P (468), Chasca F2P (469) | M3 | Survey (R4) |
| F12 | Build Re-linking | Re-link Furina (305 -> 247), Albedo (387 -> 249), Shenhe (392 -> 204) to authentic BiS weapons | M3 | Survey (R4) |
| F13 | Data Pipeline Synchronization | Update `generate_csvs.py`, regenerate all 4 CSVs in `data/`, rebuild `genshin_learning.db` via `init_db.py` | M4 | Survey (R5) |
| F14 | Database Verification Suite Upgrade | Upgrade `verify_db.py` with 7 assertion suites: 0 FK violations, 0 orphans, exact table counts (129, 155, 64, 168), CSV parity | M4 | Survey (R5) |
| F15 | E2E Testing Suite (Tiers 1-4) | Independent opaque-box test suite covering all features, boundaries, cross-feature pairs, and real queries | M_E2E | Survey (E2E Track) |
| F16 | Final Acceptance & Adversarial Hardening | Pass 100% E2E tests + Tier 5 adversarial stress testing | M_FINAL | Project Pattern |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M_E2E | E2E Testing Suite Creation | Independent test harness, test runner, Tiers 1-4 test cases, TEST_READY.md | none | DONE |
| M1 | Database Defect Remediation | Fix artifact sets 59/60/62/63/64, weapon stats 128/131, character attributes, purge Capitano & build 381 | none | DONE |
| M2 | Characters & Weapons Catalog Ingestion | Ingest 16 characters (115–130) and 52 weapons (204–255) into seed data and CSVs | M1 | DONE |
| M3 | Character Builds Backfill & Role Variety | Ingest 62 builds (408–469: 43 backfill + 16 new + 3 alt), re-link Furina/Albedo/Shenhe/Sandrone | M2 | DONE |
| M4 | Pipeline Sync & Verification Upgrade | Add schema indexes in init_db.py, update verify_db.py with complete assertions, run green tests | M3 | DONE |
| M_FINAL | E2E Acceptance & Adversarial Hardening | Execute full E2E test suite (100% pass) and Tier 5 adversarial coverage hardening | M4, M_E2E | DONE |

## Interface Contracts
### `generate_csvs.py` ➔ `data/*.csv`
- `CHARACTERS`: list of 12-element tuples. Exported to `data/characters.csv` with headers. Total count: 129.
- `WEAPONS`: list of 9-element tuples. Nullable `signature_character_id` exported as `""`. Exported to `data/weapons.csv`. Total count: 155.
- `ARTIFACT_SETS`: list of 6-element tuples. Exported to `data/artifact_sets.csv`. Total count: 64.
- `BUILDS`: list of 11-element tuples. Exported to `data/character_builds.csv`. Total count: 168.

### `data/*.csv` ➔ `init_db.py` ➔ `genshin_learning.db`
- `init_db.py` recreates schema with `PRAGMA foreign_keys = ON;`.
- Parses empty strings `""` in `signature_character_id` to `None` (SQL NULL).
- Inserts via `executemany` and executes `PRAGMA foreign_key_check;`. Must return 0 violations.

### `genshin_learning.db` ➔ `verify_db.py` / `test_security_oom.py`
- `verify_db.py` connects with foreign keys enabled, verifies 129 characters, 155 weapons, 64 artifact sets, 168 builds, 0 orphans, CSV-DB parity, and sample queries.
- `test_security_oom.py` continues passing 22/22 tests with `./.venv/bin/python`.

## Code Layout
- `generate_csvs.py`: Root generator and single source of truth for in-memory seed data.
- `init_db.py`: Database DDL schema definition and CSV batch ingestion loader.
- `verify_db.py`: Relational integrity and business rule assertion suite.
- `data/characters.csv`, `data/weapons.csv`, `data/artifact_sets.csv`, `data/character_builds.csv`: Synchronized relational CSV exports.
- `test_security_oom.py`: Flask web application security and OOM integration test suite.
- `tests/test_e2e_genshin.py` (or `test_e2e.py`): E2E test harness and test runner.
