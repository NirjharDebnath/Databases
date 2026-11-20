# TEST READY: Comprehensive E2E Testing Suite

**Status**: READY FOR VERIFICATION  
**Test Harness & Runner**: `tests/test_e2e_genshin.py`  
**Test Architecture Documentation**: `TEST_INFRA.md`  
**Total Test Cases**: 171 tests across 4 tiers  

---

## 1. Quick Start Execution Commands

Execute the test suite using standard Python 3 or the project virtual environment:

```bash
# Full E2E Test Suite Run:
python3 tests/test_e2e_genshin.py

# Using project virtualenv:
./.venv/bin/python tests/test_e2e_genshin.py

# Standard unittest runner:
python3 -m unittest tests/test_e2e_genshin.py
```

### Exit Code Contract
- **`0`**: All tests passed (Target state post-remediation for Milestone `M_FINAL`).
- **`1`**: Failures encountered (Reports exact diagnostic failure traces).

---

## 2. Granular & Milestone-Filtered Execution

The test harness supports selective execution by Tier, Feature, or Milestone:

```bash
# Verify Milestone 1 (F1 to F4):
python3 tests/test_e2e_genshin.py --tier 1 --feature F1,F2,F3,F4

# Verify Milestone 2 (F5 to F8):
python3 tests/test_e2e_genshin.py --tier 1 --feature F5,F6,F7,F8

# Verify Milestone 3 (F9 to F12):
python3 tests/test_e2e_genshin.py --tier 1 --feature F9,F10,F11,F12

# Verify Milestone 4 (F13 to F14):
python3 tests/test_e2e_genshin.py --tier 1 --feature F13,F14

# Verify specific tiers:
python3 tests/test_e2e_genshin.py --tier 4        # Real-World Scenarios (6 tests)
python3 tests/test_e2e_genshin.py --tier 2        # Boundary & Corner Cases (70 tests)
python3 tests/test_e2e_genshin.py --tier 3        # Cross-Feature Relational (25 tests)

# Verbose output mode:
python3 tests/test_e2e_genshin.py -v
```

---

## 3. Four-Tier Coverage Inventory

| Tier | Category | Test Count | Description & Scope |
|:---:|:---|:---:|:---|
| **Tier 1** | **Feature Coverage** | **70 Tests** | 5 comprehensive tests per feature across all 14 features (F1 through F14) specified in `PROJECT.md`. |
| **Tier 2** | **Boundary & Corner Cases** | **70 Tests** | Statistical extremes (HP, ATK, DEF, CRIT, ER bounds), CHECK constraints (vision, weapon_type, tier_rating), nullability, Aloy's region, string escaping (apostrophes, hyphens), and CSV parsing boundaries. |
| **Tier 3** | **Cross-Feature Relational** | **25 Tests** | Pairwise consistency, character-weapon type compatibility, cascade/restrict deletion rules, multi-build role divergence, and full 4-table relational joins. |
| **Tier 4** | **Real-World Scenarios** | **6 Tests** | End-to-end multi-table queries: 4-member elemental reaction team builder, theoretical maximum base attack scaling, artifact domain route optimization, F2P recommendation engine, regional dashboard rollup, and window function meta matrix. |
| **Total** | **Comprehensive Suite** | **171 Tests** | Exceeds minimum threshold (>=150 tests) with complete opaque-box coverage. |

---

## 4. Feature Coverage Checklist (Tier 1 Breakdown)

- [x] **F1: Artifact Sets 59, 60, 62, 63, 64 Remediation** (5 tests)
  - `test_f1_set_59_aubade_mechanics`: +80 EM 2pc bonus and Moonsign 4pc
  - `test_f1_set_60_rising_winds_scaling`: +18% ATK and Pastoral Winds scaling
  - `test_f1_set_62_mondstadt_region_deep_shadow`: Region Mondstadt and Thorny Crown domain
  - `test_f1_set_63_inverted_glacier_scarlet_proof`: Domain Inverted Glacier, +18% ATK, Stellar Swirl
  - `test_f1_set_64_inverted_glacier_heart_furnace`: Domain Inverted Glacier, +18% ATK, Stellar Glimmer
- [x] **F2: Weapon Stats Correction (128 & 131)** (5 tests)
  - `test_f2_weapon_128_base_atk_741`: Fang of the Mountain King base_atk = 741
  - `test_f2_weapon_128_crit_rate_11`: Sub-stat CRIT Rate = 11.0%
  - `test_f2_weapon_131_base_atk_741`: A Thousand Blazing Suns base_atk = 741
  - `test_f2_weapon_131_crit_rate_11`: Sub-stat CRIT Rate = 11.0%
  - `test_f2_weapons_128_131_rarity_and_owners`: 5★ Claymores linked to Kinich (84) and Mavuika (87)
- [x] **F3: Character Attributes Correction** (5 tests)
  - `test_f3_arlecchino_snezhnaya_region`: Arlecchino (72) region Snezhnaya
  - `test_f3_zibai_liyue_region`: Zibai (99) region Liyue
  - `test_f3_columbina_nod_krai_region`: Columbina (102) region Nod-Krai
  - `test_f3_sandrone_cryo_claymore`: Sandrone (103) vision Cryo, weapon Claymore
  - `test_f3_iansan_patch_and_aloy_none_region`: Iansan patch 5.5, Aloy region 'None'
- [x] **F4: Capitano Purge** (5 tests)
  - `test_f4_capitano_character_name_purged`: Character 'Capitano' purged
  - `test_f4_capitano_character_id_104_purged`: Character ID 104 purged
  - `test_f4_capitano_build_381_purged`: Build ID 381 purged
  - `test_f4_no_builds_reference_id_104`: 0 builds reference character_id 104
  - `test_f4_no_weapons_signature_id_104`: 0 weapons signature_character_id 104
- [x] **F5: Missing Playable Characters Ingestion** (5 tests)
  - `test_f5_all_16_new_character_names_exist`: 16 characters exist in characters table
  - `test_f5_total_character_count_is_129`: Total character count = 129
  - `test_f5_new_characters_visions_accurate`: Accurate visions for new characters
  - `test_f5_new_characters_weapon_types_accurate`: Accurate weapon types
  - `test_f5_new_characters_base_stats_valid`: Valid base stats and release patch >= 5.5
- [x] **F6: Missing 5-Star Signatures** (5 tests)
  - `test_f6_all_24_signatures_names_exist`: 24 signature names exist (IDs 204–227)
  - `test_f6_signatures_rarity_5_non_craftable`: Rarity 5, is_craftable = 0
  - `test_f6_signatures_foreign_keys_not_null`: Non-null signature_character_id foreign keys
  - `test_f6_signature_stat_profiles_verified`: Stats match high base ATK / sub-stat profiles
  - `test_f6_signatures_weapon_type_matches_owner`: Weapon type matches owner character
- [x] **F7: Missing Craftables Ingestion** (5 tests)
  - `test_f7_all_19_craftables_names_exist`: 19 craftable names exist (IDs 228–246)
  - `test_f7_all_19_craftables_flagged_is_craftable`: is_craftable = 1, rarity = 4
  - `test_f7_craftables_signature_id_is_null`: signature_character_id IS NULL
  - `test_f7_craftables_regional_distribution`: Dragonspine (3), Sumeru (4), Fontaine (2), Nod-Krai (5), Snezhnaya (5)
  - `test_f7_craftables_all_5_weapon_types_represented`: All 5 weapon types present
- [x] **F8: Meta Staples & Event Weapons** (5 tests)
  - `test_f8_all_9_staple_weapon_names_exist`: 9 staple names exist (IDs 247–255)
  - `test_f8_cinnabar_spindle_stats_and_albedo_signature`: Cinnabar Spindle DEF% 69.0 and Albedo FK
  - `test_f8_fleuve_cendre_ferryman_stats`: Fleuve Cendre Ferryman ER sub-stat and 510 ATK
  - `test_f8_the_stringless_stats`: The Stringless EM 165.0 and 510 ATK
  - `test_f8_natlan_series_rarity_and_non_craftable`: Natlan series rarity 4 and non-craftable
- [x] **F9: Missing Character Builds Backfill** (5 tests)
  - `test_f9_all_43_backfilled_characters_have_builds`: 43 characters have >= 1 build
  - `test_f9_build_ids_408_to_450_exist`: Build IDs 408–450 present
  - `test_f9_zero_orphaned_characters_in_database`: 0 orphaned characters without builds
  - `test_f9_backfilled_builds_valid_tier_ratings`: Tier ratings in ('SS', 'S+', 'S', 'A')
  - `test_f9_backfilled_builds_playstyle_notes_populated`: Non-empty playstyle notes
- [x] **F10: New Characters Builds Ingestion** (5 tests)
  - `test_f10_all_16_new_characters_have_builds`: 16 new characters have >= 1 build
  - `test_f10_build_ids_451_to_466_exist`: Build IDs 451–466 present
  - `test_f10_new_character_build_roles_and_tiers`: Specific roles and tier ratings verified
  - `test_f10_new_character_build_weapon_type_match`: Weapon type compatibility
  - `test_f10_new_character_build_artifacts_valid`: Recommended artifact foreign keys resolve
- [x] **F11: Alternative Meta Roles** (5 tests)
  - `test_f11_mavuika_cinder_city_support_build_467`: Mavuika 4pc Cinder City Support build 467
  - `test_f11_citlali_f2p_build_468`: Citlali F2P Sacrificial Fragments build 468
  - `test_f11_chasca_f2p_build_469`: Chasca F2P Chain Breaker build 469
  - `test_f11_mavuika_has_multiple_builds`: Mavuika >= 2 builds
  - `test_f11_citlali_and_chasca_multi_build_diversity`: Citlali and Chasca multi-build diversity
- [x] **F12: Build Re-linking** (5 tests)
  - `test_f12_furina_build_305_relinked_to_ferryman_247`: Furina 305 -> 247 Ferryman
  - `test_f12_albedo_build_387_relinked_to_cinnabar_249`: Albedo 387 -> 249 Cinnabar
  - `test_f12_shenhe_build_392_relinked_to_calamity_204`: Shenhe 392 -> 204 Calamity Queller
  - `test_f12_relinked_weapons_match_character_weapon_type`: Weapon type compatibility
  - `test_f12_relinked_builds_retain_correct_artifacts`: Correct artifact sets preserved
- [x] **F13: Data Pipeline Synchronization & Parity** (5 tests)
  - `test_f13_characters_csv_db_count_parity`: characters.csv == DB (129)
  - `test_f13_weapons_csv_db_count_parity`: weapons.csv == DB (155)
  - `test_f13_artifact_sets_csv_db_count_parity`: artifact_sets.csv == DB (64)
  - `test_f13_character_builds_csv_db_count_parity`: character_builds.csv == DB (168)
  - `test_f13_csv_primary_key_and_name_parity`: 1:1 cell equality on PK and names
- [x] **F14: Database Verification Suite & Constraints** (5 tests)
  - `test_f14_pragma_foreign_key_check_zero_violations`: PRAGMA foreign_key_check = 0 violations
  - `test_f14_exact_table_counts_129_155_64_168`: 129, 155, 64, 168 exact counts
  - `test_f14_regional_character_distribution_counts`: Regional breakdown matches target
  - `test_f14_relational_indexes_exist`: All 8 schema indexes confirmed
  - `test_f14_foreign_keys_pragmas_enforced`: foreign_keys enabled on connection

---

## 5. Current Baseline Test Run Results (Pre-Remediation Verification)

Executed against repository baseline (`genshin_learning.db`):
- **Tier 1 (Feature Coverage)**: 29/70 passing (F1, F2, F3, F4 remediations pass 100%; F5–F14 await M2–M4 implementation).
- **Tier 2 (Boundary & Corner Cases)**: 69/70 passing (All stat boundaries, CHECK constraints, nullability, and escaping tests pass; 1 failure pending 129 characters expansion).
- **Tier 3 (Cross-Feature Combinations)**: 20/25 passing (Relational joins and cascades pass; 5 failures pending new weapons/builds backfill).
- **Tier 4 (Real-World Application Scenarios)**: 6/6 passing (100% PASS - complex team builder, base ATK ranking, domain routing, F2P recommendations, regional dashboard, and window function rankings).
- **Overall Baseline**: **124/171 Passing**, **47 Failing** (All 47 failures map directly to pending work in Milestones M2, M3, and M4).

When all implementation milestones (M1–M4) are complete, `python3 tests/test_e2e_genshin.py` will exit with code `0`.
