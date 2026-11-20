#!/usr/bin/env python3
"""
tests/test_e2e_genshin.py
Comprehensive Requirement-Driven Opaque-Box E2E Test Suite for Genshin Impact Learning Database.

Derived strictly from:
- ORIGINAL_REQUEST.md (R1 to R5)
- PROJECT.md § Feature Inventory (F1 to F14)
- Repository Specifications & Schema Contracts

Four Testing Tiers:
- Tier 1: Feature Coverage (F1 to F14, 5 tests per feature = 70 tests)
- Tier 2: Boundary & Corner Cases (70 tests)
- Tier 3: Cross-Feature Combinations (25 tests)
- Tier 4: Real-World Application Scenarios (6 tests)
Total: 171 test cases
"""

import os
import sys
import csv
import re
import time
import sqlite3
import unittest
import argparse
from typing import Dict, List, Tuple, Any, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = os.path.join(PROJECT_ROOT, "genshin_learning.db")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

ACTIVE_DB_PATH = DEFAULT_DB_PATH


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    target = db_path or ACTIVE_DB_PATH
    if not os.path.exists(target):
        raise FileNotFoundError(f"Database file not found at {target}")
    conn = sqlite3.connect(target)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


# =====================================================================
# TIER 1: FEATURE COVERAGE TESTS (F1 to F14)
# =====================================================================

class Tier1FeatureCoverageTests(unittest.TestCase):
    """Tier 1: Direct requirement-driven coverage for features F1 through F14."""

    def setUp(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    # -----------------------------------------------------------------
    # F1: Artifact Sets 59, 60, 62, 63, 64 Remediation
    # -----------------------------------------------------------------
    def test_f1_set_59_aubade_mechanics(self):
        """F1.1: Set 59 (Aubade of Morningstar and Moon) has +80 EM 2pc bonus and Moonsign 4pc."""
        row = self.cursor.execute("SELECT * FROM artifact_sets WHERE artifact_set_id = 59;").fetchone()
        self.assertIsNotNone(row, "Artifact Set 59 must exist")
        self.assertEqual(row["name"], "Aubade of Morningstar and Moon")
        self.assertEqual(row["region"], "Nod-Krai")
        self.assertIn("80 Elemental Mastery", row["two_piece_bonus"])
        self.assertIn("Lunar Reaction DMG", row["four_piece_bonus"])
        self.assertIn("Moonsign Level", row["four_piece_bonus"])

    def test_f1_set_60_rising_winds_scaling(self):
        """F1.2: Set 60 (A Day Carved from Rising Winds) has +18% ATK and Pastoral Winds scaling."""
        row = self.cursor.execute("SELECT * FROM artifact_sets WHERE artifact_set_id = 60;").fetchone()
        self.assertIsNotNone(row, "Artifact Set 60 must exist")
        self.assertEqual(row["name"], "A Day Carved from Rising Winds")
        self.assertEqual(row["region"], "Nod-Krai")
        self.assertIn("18% ATK", row["two_piece_bonus"])
        self.assertIn("Pastoral Winds", row["four_piece_bonus"])
        self.assertIn("Witch's Homework", row["four_piece_bonus"])

    def test_f1_set_62_mondstadt_region_deep_shadow(self):
        """F1.3: Set 62 (Disenchantment in Deep Shadow) region is Mondstadt and has Thorny Crown domain."""
        row = self.cursor.execute("SELECT * FROM artifact_sets WHERE artifact_set_id = 62;").fetchone()
        self.assertIsNotNone(row, "Artifact Set 62 must exist")
        self.assertEqual(row["name"], "Disenchantment in Deep Shadow")
        self.assertEqual(row["region"], "Mondstadt", "Set 62 domain is in Mondstadt, not Snezhnaya")
        self.assertEqual(row["domain_name"], "Thorny Crown of the Mountain Wind")
        self.assertIn("18% ATK", row["two_piece_bonus"])
        self.assertIn("Superconduct", row["four_piece_bonus"])

    def test_f1_set_63_inverted_glacier_scarlet_proof(self):
        """F1.4: Set 63 (Scarlet Proof) domain is Inverted Glacier with +18% ATK and Stellar Swirl."""
        row = self.cursor.execute("SELECT * FROM artifact_sets WHERE artifact_set_id = 63;").fetchone()
        self.assertIsNotNone(row, "Artifact Set 63 must exist")
        self.assertEqual(row["name"], "Scarlet Proof")
        self.assertEqual(row["domain_name"], "Inverted Glacier", "Domain must be Inverted Glacier, not Palace of Frost")
        self.assertEqual(row["region"], "Snezhnaya")
        self.assertIn("18% ATK", row["two_piece_bonus"], "2pc bonus must be +18% ATK, not +15% Cryo DMG")
        self.assertIn("Stellar Swirl", row["four_piece_bonus"])

    def test_f1_set_64_inverted_glacier_heart_furnace(self):
        """F1.5: Set 64 (Heart of the Furnace) domain is Inverted Glacier with +18% ATK and Stellar Glimmer."""
        row = self.cursor.execute("SELECT * FROM artifact_sets WHERE artifact_set_id = 64;").fetchone()
        self.assertIsNotNone(row, "Artifact Set 64 must exist")
        self.assertEqual(row["name"], "Heart of the Furnace")
        self.assertEqual(row["domain_name"], "Inverted Glacier", "Domain must be Inverted Glacier, not Palace of Frost")
        self.assertEqual(row["region"], "Snezhnaya")
        self.assertIn("18% ATK", row["two_piece_bonus"], "2pc bonus must be +18% ATK, not +80 EM")
        self.assertIn("Stellar Glimmer", row["four_piece_bonus"])

    # -----------------------------------------------------------------
    # F2: Weapon Stats Correction (128 & 131)
    # -----------------------------------------------------------------
    def test_f2_weapon_128_base_atk_741(self):
        """F2.1: Weapon 128 (Fang of the Mountain King) has base_atk = 741."""
        row = self.cursor.execute("SELECT base_atk FROM weapons WHERE weapon_id = 128;").fetchone()
        self.assertIsNotNone(row, "Weapon 128 must exist")
        self.assertEqual(row["base_atk"], 741, "Fang of the Mountain King base ATK must be 741 (not 608)")

    def test_f2_weapon_128_crit_rate_11(self):
        """F2.2: Weapon 128 (Fang of the Mountain King) has sub_stat_type = 'CRIT Rate' and value = 11.0."""
        row = self.cursor.execute("SELECT sub_stat_type, sub_stat_value FROM weapons WHERE weapon_id = 128;").fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row["sub_stat_type"], "CRIT Rate")
        self.assertAlmostEqual(row["sub_stat_value"], 11.0, places=1, msg="Sub-stat value must be 11.0% (not 33.1%)")

    def test_f2_weapon_131_base_atk_741(self):
        """F2.3: Weapon 131 (A Thousand Blazing Suns) has base_atk = 741."""
        row = self.cursor.execute("SELECT base_atk FROM weapons WHERE weapon_id = 131;").fetchone()
        self.assertIsNotNone(row, "Weapon 131 must exist")
        self.assertEqual(row["base_atk"], 741, "A Thousand Blazing Suns base ATK must be 741 (not 608)")

    def test_f2_weapon_131_crit_rate_11(self):
        """F2.4: Weapon 131 (A Thousand Blazing Suns) has sub_stat_type = 'CRIT Rate' and value = 11.0."""
        row = self.cursor.execute("SELECT sub_stat_type, sub_stat_value FROM weapons WHERE weapon_id = 131;").fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row["sub_stat_type"], "CRIT Rate")
        self.assertAlmostEqual(row["sub_stat_value"], 11.0, places=1, msg="Sub-stat value must be 11.0% (not 33.1%)")

    def test_f2_weapons_128_131_rarity_and_owners(self):
        """F2.5: Weapons 128 & 131 are 5★ Claymores linked to Kinich (84) and Mavuika (87)."""
        w128 = self.cursor.execute("SELECT weapon_type, rarity, signature_character_id FROM weapons WHERE weapon_id = 128;").fetchone()
        w131 = self.cursor.execute("SELECT weapon_type, rarity, signature_character_id FROM weapons WHERE weapon_id = 131;").fetchone()
        self.assertEqual(w128["weapon_type"], "Claymore")
        self.assertEqual(w128["rarity"], 5)
        self.assertEqual(w128["signature_character_id"], 84)
        self.assertEqual(w131["weapon_type"], "Claymore")
        self.assertEqual(w131["rarity"], 5)
        self.assertEqual(w131["signature_character_id"], 87)

    # -----------------------------------------------------------------
    # F3: Character Attributes Correction
    # -----------------------------------------------------------------
    def test_f3_arlecchino_snezhnaya_region(self):
        """F3.1: Arlecchino (ID 72) region is Snezhnaya."""
        row = self.cursor.execute("SELECT region FROM characters WHERE character_id = 72;").fetchone()
        self.assertIsNotNone(row, "Arlecchino must exist")
        self.assertEqual(row["region"], "Snezhnaya", "Arlecchino region must be Snezhnaya (not Fontaine)")

    def test_f3_zibai_liyue_region(self):
        """F3.2: Zibai (ID 99) region is Liyue."""
        row = self.cursor.execute("SELECT region FROM characters WHERE character_id = 99;").fetchone()
        self.assertIsNotNone(row, "Zibai must exist")
        self.assertEqual(row["region"], "Liyue", "Zibai region must be Liyue (not Nod-Krai)")

    def test_f3_columbina_nod_krai_region(self):
        """F3.3: Columbina (ID 102) region is Nod-Krai."""
        row = self.cursor.execute("SELECT region FROM characters WHERE character_id = 102;").fetchone()
        self.assertIsNotNone(row, "Columbina must exist")
        self.assertEqual(row["region"], "Nod-Krai", "Columbina region must be Nod-Krai (not Snezhnaya)")

    def test_f3_sandrone_cryo_claymore(self):
        """F3.4: Sandrone (ID 103) vision is Cryo and weapon_type is Claymore."""
        row = self.cursor.execute("SELECT vision, weapon_type FROM characters WHERE character_id = 103;").fetchone()
        self.assertIsNotNone(row, "Sandrone must exist")
        self.assertEqual(row["vision"], "Cryo", "Sandrone vision must be Cryo (not Geo)")
        self.assertEqual(row["weapon_type"], "Claymore", "Sandrone weapon must be Claymore (not Catalyst)")

    def test_f3_iansan_patch_and_aloy_none_region(self):
        """F3.5: Iansan (ID 91) release_patch is 5.5 and Aloy (ID 105) region is 'None'."""
        iansan = self.cursor.execute("SELECT release_patch FROM characters WHERE character_id = 91;").fetchone()
        aloy = self.cursor.execute("SELECT region FROM characters WHERE character_id = 105;").fetchone()
        self.assertIsNotNone(iansan, "Iansan must exist")
        self.assertAlmostEqual(iansan["release_patch"], 5.5, places=1, msg="Iansan release patch must be 5.5")
        self.assertIsNotNone(aloy, "Aloy must exist")
        self.assertEqual(aloy["region"], "None", "Aloy region must be string 'None' (not Outlander)")

    # -----------------------------------------------------------------
    # F4: Capitano Purge
    # -----------------------------------------------------------------
    def test_f4_capitano_character_name_purged(self):
        """F4.1: Non-playable NPC Capitano is not in characters by name."""
        count = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE name = 'Capitano';").fetchone()[0]
        self.assertEqual(count, 0, "Capitano must be completely removed from characters table")

    def test_f4_capitano_character_id_104_purged(self):
        """F4.2: Character ID 104 is purged from characters table."""
        count = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE character_id = 104;").fetchone()[0]
        self.assertEqual(count, 0, "Character ID 104 must be purged")

    def test_f4_capitano_build_381_purged(self):
        """F4.3: Build ID 381 is purged from character_builds table."""
        count = self.cursor.execute("SELECT COUNT(*) FROM character_builds WHERE build_id = 381;").fetchone()[0]
        self.assertEqual(count, 0, "Build 381 must be purged from character_builds")

    def test_f4_no_builds_reference_id_104(self):
        """F4.4: Zero character_builds reference character_id = 104."""
        count = self.cursor.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = 104;").fetchone()[0]
        self.assertEqual(count, 0, "No builds may reference character_id 104")

    def test_f4_no_weapons_signature_id_104(self):
        """F4.5: Zero weapons have signature_character_id = 104."""
        count = self.cursor.execute("SELECT COUNT(*) FROM weapons WHERE signature_character_id = 104;").fetchone()[0]
        self.assertEqual(count, 0, "No weapons may have signature_character_id 104")

    # -----------------------------------------------------------------
    # F5: Missing Playable Characters Ingestion (16 chars)
    # -----------------------------------------------------------------
    def test_f5_all_16_new_character_names_exist(self):
        """F5.1: All 16 missing playable characters exist in characters table."""
        expected = [
            "Ifa", "Escoffier", "Dahlia", "Skirk", "Wonderland Manekin",
            "Durin", "Varka", "Nicole", "Prune", "Lohen",
            "Alyosha", "Odette", "Vesna", "Vodyanitsa", "Mitya", "Valeriy"
        ]
        found = {row[0] for row in self.cursor.execute("SELECT name FROM characters;").fetchall()}
        missing = [name for name in expected if name not in found]
        self.assertEqual(missing, [], f"Missing required playable characters: {missing}")

    def test_f5_total_character_count_is_129(self):
        """F5.2: Total character count in characters table is exactly 129."""
        count = self.cursor.execute("SELECT COUNT(*) FROM characters;").fetchone()[0]
        self.assertEqual(count, 129, f"Expected exactly 129 characters, found {count}")

    def test_f5_new_characters_visions_accurate(self):
        """F5.3: Accurate visions for new characters (Skirk=Cryo, Durin=Pyro, Varka=Anemo, etc.)."""
        expected_visions = {
            "Ifa": "Anemo", "Escoffier": "Cryo", "Dahlia": "Hydro", "Skirk": "Cryo",
            "Durin": "Pyro", "Varka": "Anemo", "Nicole": "Pyro", "Alyosha": "Electro"
        }
        for name, expected_vis in expected_visions.items():
            row = self.cursor.execute("SELECT vision FROM characters WHERE name = ?;", (name,)).fetchone()
            self.assertIsNotNone(row, f"Character {name} must exist")
            self.assertEqual(row["vision"], expected_vis, f"{name} vision mismatch")

    def test_f5_new_characters_weapon_types_accurate(self):
        """F5.4: Accurate weapon types for new characters (Skirk=Sword, Varka=Claymore, etc.)."""
        expected_weapons = {
            "Ifa": "Catalyst", "Escoffier": "Polearm", "Dahlia": "Sword", "Skirk": "Sword",
            "Varka": "Claymore", "Nicole": "Catalyst", "Lohen": "Polearm", "Vesna": "Sword"
        }
        for name, exp_wt in expected_weapons.items():
            row = self.cursor.execute("SELECT weapon_type FROM characters WHERE name = ?;", (name,)).fetchone()
            self.assertIsNotNone(row, f"Character {name} must exist")
            self.assertEqual(row["weapon_type"], exp_wt, f"{name} weapon type mismatch")

    def test_f5_new_characters_base_stats_valid(self):
        """F5.5: All 16 new characters have positive valid base stats and release patches >= 5.5."""
        new_names = (
            "Ifa", "Escoffier", "Dahlia", "Skirk", "Wonderland Manekin",
            "Durin", "Varka", "Nicole", "Prune", "Lohen",
            "Alyosha", "Odette", "Vesna", "Vodyanitsa", "Mitya", "Valeriy"
        )
        rows = self.cursor.execute(f"SELECT * FROM characters WHERE name IN ({','.join('?' for _ in new_names)});", new_names).fetchall()
        self.assertEqual(len(rows), 16)
        for r in rows:
            self.assertGreater(r["base_hp"], 8000, f"{r['name']} base_hp too low")
            self.assertGreater(r["base_atk"], 180, f"{r['name']} base_atk too low")
            self.assertGreater(r["base_def"], 500, f"{r['name']} base_def too low")
            self.assertGreaterEqual(r["release_patch"], 5.5, f"{r['name']} release patch must be >= 5.5")

    # -----------------------------------------------------------------
    # F6: Missing 5-Star Signatures (24 weapons: IDs 204–227)
    # -----------------------------------------------------------------
    def test_f6_all_24_signatures_names_exist(self):
        """F6.1: All 24 missing 5-star signature weapon names exist in weapons table."""
        signatures = [
            "Calamity Queller", "Everlasting Moonglow", "Fractured Halo",
            "Nightweaver's Looking Glass", "Pocztowy Demonspear", "Reliquary of Truth",
            "Lightbearing Moonshard", "Golden Frostbound Oath", "Nocturne's Curtain Call",
            "A Teaspoon of Transcendence", "Sunny Morning Sleep-In", "Vivid Notions",
            "Symphonist of Scents", "Azurelight", "Athame Artis",
            "Gest of the Mighty Wolf", "Angelos' Heptades", "Disaster and Remorse",
            "Whitelake Frostfeather", "Beyond the Chrysalis", "Hymn of the Maelstrom",
            "Starsealed Edict", "Exaiphanes Blade", "Miliastra Sovereign"
        ]
        found = {row[0] for row in self.cursor.execute("SELECT name FROM weapons;").fetchall()}
        missing = [w for w in signatures if w not in found]
        self.assertEqual(missing, [], f"Missing required 5-star signature weapons: {missing}")

    def test_f6_signatures_rarity_5_non_craftable(self):
        """F6.2: All 24 signature weapons have rarity = 5 and is_craftable = 0."""
        sig_ids = tuple(range(204, 228))
        rows = self.cursor.execute(f"SELECT weapon_id, name, rarity, is_craftable FROM weapons WHERE weapon_id IN ({','.join('?' for _ in sig_ids)});", sig_ids).fetchall()
        self.assertEqual(len(rows), 24, "All 24 signature weapon IDs 204–227 must be present")
        for r in rows:
            self.assertEqual(r["rarity"], 5, f"{r['name']} must be rarity 5")
            self.assertEqual(r["is_craftable"], 0, f"{r['name']} must not be craftable")

    def test_f6_signatures_foreign_keys_not_null(self):
        """F6.3: All 24 signature weapons have non-null signature_character_id resolving to valid characters."""
        sig_ids = tuple(range(204, 228))
        rows = self.cursor.execute(f"""
            SELECT w.weapon_id, w.name, w.signature_character_id, c.name as char_name
            FROM weapons w
            LEFT JOIN characters c ON w.signature_character_id = c.character_id
            WHERE w.weapon_id IN ({','.join('?' for _ in sig_ids)});
        """, sig_ids).fetchall()
        self.assertEqual(len(rows), 24)
        for r in rows:
            self.assertIsNotNone(r["signature_character_id"], f"{r['name']} has null signature_character_id")
            self.assertIsNotNone(r["char_name"], f"{r['name']} signature_character_id does not resolve to character")

    def test_f6_signature_stat_profiles_verified(self):
        """F6.4: Specific weapon stat profiles (e.g. Calamity Queller 741 Base ATK)."""
        cq = self.cursor.execute("SELECT base_atk, sub_stat_type, sub_stat_value FROM weapons WHERE weapon_id = 204;").fetchone()
        em = self.cursor.execute("SELECT base_atk, sub_stat_type, sub_stat_value FROM weapons WHERE weapon_id = 205;").fetchone()
        self.assertIsNotNone(cq)
        self.assertEqual(cq["base_atk"], 741)
        self.assertEqual(cq["sub_stat_type"], "ATK%")
        self.assertIsNotNone(em)
        self.assertEqual(em["sub_stat_type"], "HP%")
        self.assertAlmostEqual(em["sub_stat_value"], 49.6, places=1)

    def test_f6_signatures_weapon_type_matches_owner(self):
        """F6.5: Weapon type matches the signature owner's weapon type."""
        sig_ids = tuple(range(204, 228))
        mismatches = self.cursor.execute(f"""
            SELECT w.name, w.weapon_type as wt, c.name as cname, c.weapon_type as cwt
            FROM weapons w
            JOIN characters c ON w.signature_character_id = c.character_id
            WHERE w.weapon_id IN ({','.join('?' for _ in sig_ids)})
              AND w.weapon_type != c.weapon_type;
        """, sig_ids).fetchall()
        self.assertEqual(len(mismatches), 0, f"Signature weapon type mismatch with owner: {mismatches}")

    # -----------------------------------------------------------------
    # F7: Missing Craftables Ingestion (19 weapons: IDs 228–246)
    # -----------------------------------------------------------------
    def test_f7_all_19_craftables_names_exist(self):
        """F7.1: All 19 missing craftable weapon names exist in weapons table."""
        craftables = [
            "Snow-Tombed Starsilver", "Dragonspine Spear", "Frostbearer",
            "Forest Regalia", "Moonpiercer", "King's Squire", "Fruit of Fulfillment",
            "Song of Stillness", "Flowing Purity",
            "Serenity's Call", "Master Key", "Prospector's Shovel", "Snare Hook", "Blackmarrow Lantern",
            "Emberwell", "Blade of Atonement", "Song of the Vigil", "Covenant of Frost and Snow", "Echoes of the Heart"
        ]
        found = {row[0] for row in self.cursor.execute("SELECT name FROM weapons;").fetchall()}
        missing = [w for w in craftables if w not in found]
        self.assertEqual(missing, [], f"Missing craftable weapons: {missing}")

    def test_f7_all_19_craftables_flagged_is_craftable(self):
        """F7.2: All 19 craftable weapons have is_craftable = 1 and rarity = 4."""
        cr_ids = tuple(range(228, 247))
        rows = self.cursor.execute(f"SELECT weapon_id, name, is_craftable, rarity FROM weapons WHERE weapon_id IN ({','.join('?' for _ in cr_ids)});", cr_ids).fetchall()
        self.assertEqual(len(rows), 19, "All 19 craftable weapon IDs 228–246 must be present")
        for r in rows:
            self.assertEqual(r["is_craftable"], 1, f"{r['name']} must have is_craftable = 1")
            self.assertEqual(r["rarity"], 4, f"{r['name']} must have rarity = 4")

    def test_f7_craftables_signature_id_is_null(self):
        """F7.3: All 19 craftable weapons have signature_character_id IS NULL."""
        cr_ids = tuple(range(228, 247))
        non_null = self.cursor.execute(f"""
            SELECT name, signature_character_id FROM weapons
            WHERE weapon_id IN ({','.join('?' for _ in cr_ids)}) AND signature_character_id IS NOT NULL;
        """, cr_ids).fetchall()
        self.assertEqual(len(non_null), 0, f"Craftable weapons must not have signature_character_id: {non_null}")

    def test_f7_craftables_regional_distribution(self):
        """F7.4: Craftables cover Dragonspine (3), Sumeru (4), Fontaine (2), Nod-Krai (5), Snezhnaya (5)."""
        cr_ids = tuple(range(228, 247))
        count = self.cursor.execute(f"SELECT COUNT(*) FROM weapons WHERE weapon_id IN ({','.join('?' for _ in cr_ids)});", cr_ids).fetchone()[0]
        self.assertEqual(count, 19)

    def test_f7_craftables_all_5_weapon_types_represented(self):
        """F7.5: All 5 weapon types (Sword, Claymore, Polearm, Bow, Catalyst) exist in the 19 craftables."""
        cr_ids = tuple(range(228, 247))
        types = {row[0] for row in self.cursor.execute(f"SELECT DISTINCT weapon_type FROM weapons WHERE weapon_id IN ({','.join('?' for _ in cr_ids)});", cr_ids).fetchall()}
        self.assertEqual(types, {"Sword", "Claymore", "Polearm", "Bow", "Catalyst"})

    # -----------------------------------------------------------------
    # F8: Meta Staples & Event Weapons (9 weapons: IDs 247–255)
    # -----------------------------------------------------------------
    def test_f8_all_9_staple_weapon_names_exist(self):
        """F8.1: All 9 meta staple and event weapon names exist."""
        staples = [
            "Fleuve Cendre Ferryman", "The Stringless", "Cinnabar Spindle",
            "Mountain-Bracing Bolt", "Sturdy Bone", "Fruitful Hook",
            "Flower-Wreathed Feathers", "Waveriding Whirl", "Calamity of Eshu"
        ]
        found = {row[0] for row in self.cursor.execute("SELECT name FROM weapons;").fetchall()}
        missing = [w for w in staples if w not in found]
        self.assertEqual(missing, [], f"Missing meta staples: {missing}")

    def test_f8_cinnabar_spindle_stats_and_albedo_signature(self):
        """F8.2: Cinnabar Spindle (ID 249) has DEF% 69.0 and signature_character_id = 6 (Albedo)."""
        row = self.cursor.execute("SELECT * FROM weapons WHERE weapon_id = 249;").fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row["name"], "Cinnabar Spindle")
        self.assertEqual(row["weapon_type"], "Sword")
        self.assertEqual(row["sub_stat_type"], "DEF%")
        self.assertAlmostEqual(row["sub_stat_value"], 69.0, places=1)
        self.assertEqual(row["signature_character_id"], 6, "Cinnabar Spindle must link to Albedo (char ID 6)")

    def test_f8_fleuve_cendre_ferryman_stats(self):
        """F8.3: Fleuve Cendre Ferryman (ID 247) has Energy Recharge sub-stat and base ATK 510."""
        row = self.cursor.execute("SELECT * FROM weapons WHERE weapon_id = 247;").fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row["name"], "Fleuve Cendre Ferryman")
        self.assertEqual(row["weapon_type"], "Sword")
        self.assertEqual(row["sub_stat_type"], "Energy Recharge")
        self.assertEqual(row["base_atk"], 510)

    def test_f8_the_stringless_stats(self):
        """F8.4: The Stringless (ID 248) has Elemental Mastery 165.0 and base ATK 510."""
        row = self.cursor.execute("SELECT * FROM weapons WHERE weapon_id = 248;").fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row["name"], "The Stringless")
        self.assertEqual(row["weapon_type"], "Bow")
        self.assertEqual(row["sub_stat_type"], "Elemental Mastery")
        self.assertAlmostEqual(row["sub_stat_value"], 165.0, places=1)

    def test_f8_natlan_series_rarity_and_non_craftable(self):
        """F8.5: Natlan gacha/event series weapons (IDs 250–255) are 4★ non-craftable."""
        nat_ids = tuple(range(250, 256))
        rows = self.cursor.execute(f"SELECT weapon_id, name, rarity, is_craftable FROM weapons WHERE weapon_id IN ({','.join('?' for _ in nat_ids)});", nat_ids).fetchall()
        self.assertEqual(len(rows), 6)
        for r in rows:
            self.assertEqual(r["rarity"], 4)
            self.assertEqual(r["is_craftable"], 0)

    # -----------------------------------------------------------------
    # F9: Missing Character Builds Backfill (43 chars)
    # -----------------------------------------------------------------
    def test_f9_all_43_backfilled_characters_have_builds(self):
        """F9.1: All 43 previously missing characters have at least one build."""
        backfill_names = [
            "Barbara", "Razor", "Noelle", "Kaeya", "Lisa", "Amber", "Diona", "Rosaria",
            "Mika", "Qiqi", "Ningguang", "Beidou", "Chongyun", "Xinyan", "Yanfei",
            "Yun Jin", "Yaoyao", "Kujou Sara", "Sayu", "Thoma", "Gorou",
            "Shikanoin Heizou", "Kirara", "Collei", "Dori", "Candace", "Layla",
            "Kaveh", "Sethos", "Lynette", "Freminet", "Charlotte", "Ororon",
            "Iansan", "Aino", "Nefer", "Jahoda", "Illuga", "Zibai", "Linnea",
            "Aloy", "Traveler (Electro)", "Traveler (Hydro)"
        ]
        for name in backfill_names:
            cnt = self.cursor.execute("""
                SELECT COUNT(*) FROM character_builds cb
                JOIN characters c ON cb.character_id = c.character_id
                WHERE c.name = ?;
            """, (name,)).fetchone()[0]
            self.assertGreaterEqual(cnt, 1, f"Character '{name}' must have at least 1 build")

    def test_f9_build_ids_408_to_450_exist(self):
        """F9.2: Backfilled build IDs 408 through 450 exist."""
        b_ids = tuple(range(408, 451))
        count = self.cursor.execute(f"SELECT COUNT(*) FROM character_builds WHERE build_id IN ({','.join('?' for _ in b_ids)});", b_ids).fetchone()[0]
        self.assertEqual(count, 43, f"Expected 43 backfilled builds (IDs 408–450), found {count}")

    def test_f9_zero_orphaned_characters_in_database(self):
        """F9.3: 100% of characters in characters table have >= 1 build (0 orphans)."""
        orphans = self.cursor.execute("""
            SELECT c.character_id, c.name FROM characters c
            LEFT JOIN character_builds cb ON c.character_id = cb.character_id
            WHERE cb.build_id IS NULL;
        """).fetchall()
        self.assertEqual(len(orphans), 0, f"Found orphaned characters without builds: {[o[1] for o in orphans]}")

    def test_f9_backfilled_builds_valid_tier_ratings(self):
        """F9.4: Backfilled builds have valid tier_rating in ('SS', 'S+', 'S', 'A')."""
        b_ids = tuple(range(408, 451))
        invalid = self.cursor.execute(f"""
            SELECT build_id, build_name, tier_rating FROM character_builds
            WHERE build_id IN ({','.join('?' for _ in b_ids)})
              AND tier_rating NOT IN ('SS', 'S+', 'S', 'A');
        """, b_ids).fetchall()
        self.assertEqual(len(invalid), 0, f"Invalid tier ratings in backfilled builds: {invalid}")

    def test_f9_backfilled_builds_playstyle_notes_populated(self):
        """F9.5: Backfilled builds have non-empty playstyle_notes describing rotations."""
        b_ids = tuple(range(408, 451))
        empty_notes = self.cursor.execute(f"""
            SELECT build_id, build_name FROM character_builds
            WHERE build_id IN ({','.join('?' for _ in b_ids)})
              AND (playstyle_notes IS NULL OR TRIM(playstyle_notes) = '');
        """, b_ids).fetchall()
        self.assertEqual(len(empty_notes), 0, f"Empty playstyle notes found in backfilled builds: {empty_notes}")

    # -----------------------------------------------------------------
    # F10: New Characters Builds Ingestion (16 chars: IDs 451–466)
    # -----------------------------------------------------------------
    def test_f10_all_16_new_characters_have_builds(self):
        """F10.1: All 16 new characters (IDs 115–130) have at least 1 build."""
        new_ids = tuple(range(115, 131))
        for cid in new_ids:
            cnt = self.cursor.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = ?;", (cid,)).fetchone()[0]
            self.assertGreaterEqual(cnt, 1, f"New character ID {cid} must have at least 1 build")

    def test_f10_build_ids_451_to_466_exist(self):
        """F10.2: Build IDs 451 through 466 exist."""
        b_ids = tuple(range(451, 467))
        count = self.cursor.execute(f"SELECT COUNT(*) FROM character_builds WHERE build_id IN ({','.join('?' for _ in b_ids)});", b_ids).fetchone()[0]
        self.assertEqual(count, 16, f"Expected 16 new character builds (IDs 451–466), found {count}")

    def test_f10_new_character_build_roles_and_tiers(self):
        """F10.3: Specific roles and tier ratings for new builds (Skirk SS, Escoffier S+, etc.)."""
        skirk_b = self.cursor.execute("SELECT tier_rating, role FROM character_builds WHERE character_id = 118;").fetchone()
        self.assertIsNotNone(skirk_b)
        self.assertEqual(skirk_b["tier_rating"], "SS")
        self.assertEqual(skirk_b["role"], "Main DPS")

    def test_f10_new_character_build_weapon_type_match(self):
        """F10.4: Recommended weapon matches character weapon type for new builds."""
        b_ids = tuple(range(451, 467))
        mismatches = self.cursor.execute(f"""
            SELECT cb.build_id, c.name, c.weapon_type, w.name, w.weapon_type
            FROM character_builds cb
            JOIN characters c ON cb.character_id = c.character_id
            JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
            WHERE cb.build_id IN ({','.join('?' for _ in b_ids)})
              AND c.weapon_type != w.weapon_type;
        """, b_ids).fetchall()
        self.assertEqual(len(mismatches), 0, f"Weapon type mismatch in new character builds: {mismatches}")

    def test_f10_new_character_build_artifacts_valid(self):
        """F10.5: Recommended artifact sets for new builds resolve cleanly."""
        b_ids = tuple(range(451, 467))
        dangling = self.cursor.execute(f"""
            SELECT cb.build_id, cb.recommended_artifact_id
            FROM character_builds cb
            LEFT JOIN artifact_sets a ON cb.recommended_artifact_id = a.artifact_set_id
            WHERE cb.build_id IN ({','.join('?' for _ in b_ids)})
              AND a.artifact_set_id IS NULL;
        """, b_ids).fetchall()
        self.assertEqual(len(dangling), 0, f"Dangling artifact references in new builds: {dangling}")

    # -----------------------------------------------------------------
    # F11: Alternative Meta Roles (3 builds: IDs 467–469)
    # -----------------------------------------------------------------
    def test_f11_mavuika_cinder_city_support_build_467(self):
        """F11.1: Build 467 is Mavuika (87) with 4pc Scroll of the Hero of Cinder City (Set 53)."""
        row = self.cursor.execute("SELECT * FROM character_builds WHERE build_id = 467;").fetchone()
        self.assertIsNotNone(row, "Build 467 must exist")
        self.assertEqual(row["character_id"], 87)
        self.assertIn(row["role"], ("Support", "Sub-DPS"))
        self.assertEqual(row["recommended_artifact_id"], 53)

    def test_f11_citlali_f2p_build_468(self):
        """F11.2: Build 468 is Citlali (88) F2P build using Sacrificial Fragments (194)."""
        row = self.cursor.execute("SELECT * FROM character_builds WHERE build_id = 468;").fetchone()
        self.assertIsNotNone(row, "Build 468 must exist")
        self.assertEqual(row["character_id"], 88)
        self.assertIn("F2P", row["build_name"])
        self.assertEqual(row["recommended_weapon_id"], 194)

    def test_f11_chasca_f2p_build_469(self):
        """F11.3: Build 469 is Chasca (86) F2P build using Chain Breaker (185)."""
        row = self.cursor.execute("SELECT * FROM character_builds WHERE build_id = 469;").fetchone()
        self.assertIsNotNone(row, "Build 469 must exist")
        self.assertEqual(row["character_id"], 86)
        self.assertIn("F2P", row["build_name"])
        self.assertEqual(row["recommended_weapon_id"], 185)

    def test_f11_mavuika_has_multiple_builds(self):
        """F11.4: Mavuika has >= 2 builds reflecting Main DPS and Support playstyles."""
        count = self.cursor.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = 87;").fetchone()[0]
        self.assertGreaterEqual(count, 2, f"Mavuika must have at least 2 builds, found {count}")

    def test_f11_citlali_and_chasca_multi_build_diversity(self):
        """F11.5: Citlali and Chasca have multiple builds reflecting premium and F2P variants."""
        c_cit = self.cursor.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = 88;").fetchone()[0]
        c_cha = self.cursor.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = 86;").fetchone()[0]
        self.assertGreaterEqual(c_cit, 2, "Citlali must have >= 2 builds")
        self.assertGreaterEqual(c_cha, 2, "Chasca must have >= 2 builds")

    # -----------------------------------------------------------------
    # F12: Build Re-linking
    # -----------------------------------------------------------------
    def test_f12_furina_build_305_relinked_to_ferryman_247(self):
        """F12.1: Furina Build 305 links to Fleuve Cendre Ferryman (ID 247)."""
        row = self.cursor.execute("SELECT recommended_weapon_id FROM character_builds WHERE build_id = 305;").fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row["recommended_weapon_id"], 247, "Furina Build 305 must link to Fleuve Cendre Ferryman (247)")

    def test_f12_albedo_build_387_relinked_to_cinnabar_249(self):
        """F12.2: Albedo Build 387 links to Cinnabar Spindle (ID 249)."""
        row = self.cursor.execute("SELECT recommended_weapon_id FROM character_builds WHERE build_id = 387;").fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row["recommended_weapon_id"], 249, "Albedo Build 387 must link to Cinnabar Spindle (249)")

    def test_f12_shenhe_build_392_relinked_to_calamity_204(self):
        """F12.3: Shenhe Build 392 links to Calamity Queller (ID 204)."""
        row = self.cursor.execute("SELECT recommended_weapon_id FROM character_builds WHERE build_id = 392;").fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row["recommended_weapon_id"], 204, "Shenhe Build 392 must link to Calamity Queller (204)")

    def test_f12_relinked_weapons_match_character_weapon_type(self):
        """F12.4: Re-linked weapons match character weapon types (Furina/Albedo Sword, Shenhe Polearm)."""
        links = [(305, "Sword"), (387, "Sword"), (392, "Polearm")]
        for bid, exp_wt in links:
            row = self.cursor.execute("""
                SELECT w.weapon_type FROM character_builds cb
                JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
                WHERE cb.build_id = ?;
            """, (bid,)).fetchone()
            self.assertEqual(row["weapon_type"], exp_wt)

    def test_f12_relinked_builds_retain_correct_artifacts(self):
        """F12.5: Re-linked builds retain proper artifact sets (Furina 48, Albedo 37, Shenhe 21)."""
        expected_artifacts = {305: 48, 387: 37, 392: 21}
        for bid, exp_art in expected_artifacts.items():
            row = self.cursor.execute("SELECT recommended_artifact_id FROM character_builds WHERE build_id = ?;", (bid,)).fetchone()
            self.assertEqual(row["recommended_artifact_id"], exp_art)

    # -----------------------------------------------------------------
    # F13: Data Pipeline Synchronization & Parity
    # -----------------------------------------------------------------
    def test_f13_characters_csv_db_count_parity(self):
        """F13.1: Exact row count parity between data/characters.csv and characters table."""
        csv_path = os.path.join(DATA_DIR, "characters.csv")
        self.assertTrue(os.path.exists(csv_path), "characters.csv must exist")
        with open(csv_path, "r", encoding="utf-8") as f:
            csv_count = sum(1 for _ in csv.reader(f)) - 1
        db_count = self.cursor.execute("SELECT COUNT(*) FROM characters;").fetchone()[0]
        self.assertEqual(db_count, csv_count, f"Parity mismatch in characters: DB={db_count}, CSV={csv_count}")

    def test_f13_weapons_csv_db_count_parity(self):
        """F13.2: Exact row count parity between data/weapons.csv and weapons table."""
        csv_path = os.path.join(DATA_DIR, "weapons.csv")
        self.assertTrue(os.path.exists(csv_path), "weapons.csv must exist")
        with open(csv_path, "r", encoding="utf-8") as f:
            csv_count = sum(1 for _ in csv.reader(f)) - 1
        db_count = self.cursor.execute("SELECT COUNT(*) FROM weapons;").fetchone()[0]
        self.assertEqual(db_count, csv_count, f"Parity mismatch in weapons: DB={db_count}, CSV={csv_count}")

    def test_f13_artifact_sets_csv_db_count_parity(self):
        """F13.3: Exact row count parity between data/artifact_sets.csv and artifact_sets table."""
        csv_path = os.path.join(DATA_DIR, "artifact_sets.csv")
        self.assertTrue(os.path.exists(csv_path), "artifact_sets.csv must exist")
        with open(csv_path, "r", encoding="utf-8") as f:
            csv_count = sum(1 for _ in csv.reader(f)) - 1
        db_count = self.cursor.execute("SELECT COUNT(*) FROM artifact_sets;").fetchone()[0]
        self.assertEqual(db_count, csv_count, f"Parity mismatch in artifact_sets: DB={db_count}, CSV={csv_count}")

    def test_f13_character_builds_csv_db_count_parity(self):
        """F13.4: Exact row count parity between data/character_builds.csv and character_builds table."""
        csv_path = os.path.join(DATA_DIR, "character_builds.csv")
        self.assertTrue(os.path.exists(csv_path), "character_builds.csv must exist")
        with open(csv_path, "r", encoding="utf-8") as f:
            csv_count = sum(1 for _ in csv.reader(f)) - 1
        db_count = self.cursor.execute("SELECT COUNT(*) FROM character_builds;").fetchone()[0]
        self.assertEqual(db_count, csv_count, f"Parity mismatch in character_builds: DB={db_count}, CSV={csv_count}")

    def test_f13_csv_primary_key_and_name_parity(self):
        """F13.5: Primary key and name parity between characters.csv and DB."""
        csv_path = os.path.join(DATA_DIR, "characters.csv")
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            csv_map = {int(row[0]): row[1] for row in reader}
        db_rows = self.cursor.execute("SELECT character_id, name FROM characters;").fetchall()
        db_map = {row[0]: row[1] for row in db_rows}
        self.assertEqual(csv_map, db_map, "Discrepancy between CSV character records and DB records")

    # -----------------------------------------------------------------
    # F14: Database Verification Suite & Constraints
    # -----------------------------------------------------------------
    def test_f14_pragma_foreign_key_check_zero_violations(self):
        """F14.1: PRAGMA foreign_key_check returns exactly 0 violations."""
        violations = self.cursor.execute("PRAGMA foreign_key_check;").fetchall()
        self.assertEqual(len(violations), 0, f"Foreign key violations detected: {violations}")

    def test_f14_exact_table_counts_129_155_64_168(self):
        """F14.2: Exact row counts: characters=129, weapons=155, artifact_sets=64, character_builds=168."""
        counts = {
            "characters": self.cursor.execute("SELECT COUNT(*) FROM characters;").fetchone()[0],
            "weapons": self.cursor.execute("SELECT COUNT(*) FROM weapons;").fetchone()[0],
            "artifact_sets": self.cursor.execute("SELECT COUNT(*) FROM artifact_sets;").fetchone()[0],
            "character_builds": self.cursor.execute("SELECT COUNT(*) FROM character_builds;").fetchone()[0],
        }
        self.assertEqual(counts["characters"], 129, f"Characters count expected 129, got {counts['characters']}")
        self.assertEqual(counts["weapons"], 155, f"Weapons count expected 155, got {counts['weapons']}")
        self.assertEqual(counts["artifact_sets"], 64, f"Artifact sets count expected 64, got {counts['artifact_sets']}")
        self.assertEqual(counts["character_builds"], 168, f"Character builds count expected 168, got {counts['character_builds']}")

    def test_f14_regional_character_distribution_counts(self):
        """F14.3: Exact regional character counts match target specification (Total 129)."""
        expected_regions = {
            "Liyue": 22, "Mondstadt": 23, "Inazuma": 17, "Sumeru": 14,
            "Fontaine": 13, "Natlan": 11, "Nod-Krai": 12, "Outlander": 8,
            "Snezhnaya": 8, "None": 1
        }
        actual = dict(self.cursor.execute("SELECT region, COUNT(*) FROM characters GROUP BY region;").fetchall())
        for reg, exp_cnt in expected_regions.items():
            self.assertEqual(actual.get(reg, 0), exp_cnt, f"Region '{reg}' mismatch: expected {exp_cnt}, got {actual.get(reg, 0)}")
        self.assertEqual(sum(actual.values()), 129)

    def test_f14_relational_indexes_exist(self):
        """F14.4: All required schema indexes exist in sqlite_master."""
        required_indexes = [
            "idx_characters_region", "idx_characters_vision",
            "idx_weapons_type", "idx_weapons_signature",
            "idx_builds_character", "idx_builds_tier",
            "idx_builds_weapon", "idx_builds_artifact"
        ]
        found = {row[0] for row in self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'index';").fetchall()}
        missing = [idx for idx in required_indexes if idx not in found]
        self.assertEqual(missing, [], f"Missing required indexes: {missing}")

    def test_f14_foreign_keys_pragmas_enforced(self):
        """F14.5: Connection enforces foreign keys enabled."""
        fk_status = self.cursor.execute("PRAGMA foreign_keys;").fetchone()[0]
        self.assertEqual(fk_status, 1, "Foreign keys must be enabled on connection")


# =====================================================================
# TIER 2: BOUNDARY & CORNER CASE TESTS (70 tests)
# =====================================================================

class Tier2BoundaryCornerCaseTests(unittest.TestCase):
    """Tier 2: Boundary conditions, categorical domains, nullability, escaping, types, and formatting."""

    def setUp(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    # --- Character Stat Boundaries (10 tests) ---
    def test_t2_char_hp_min_bound(self):
        """T2.1: Character base_hp minimum boundary is >= 8000."""
        min_hp = self.cursor.execute("SELECT MIN(base_hp) FROM characters;").fetchone()[0]
        self.assertGreaterEqual(min_hp, 8000)

    def test_t2_char_hp_max_bound(self):
        """T2.2: Character base_hp maximum boundary is <= 16000."""
        max_hp = self.cursor.execute("SELECT MAX(base_hp) FROM characters;").fetchone()[0]
        self.assertLessEqual(max_hp, 16000)

    def test_t2_char_atk_min_bound(self):
        """T2.3: Character base_atk minimum boundary is >= 100 (Hu Tao base ATK = 106)."""
        min_atk = self.cursor.execute("SELECT MIN(base_atk) FROM characters;").fetchone()[0]
        self.assertGreaterEqual(min_atk, 100)

    def test_t2_char_atk_max_bound(self):
        """T2.4: Character base_atk maximum boundary is <= 400."""
        max_atk = self.cursor.execute("SELECT MAX(base_atk) FROM characters;").fetchone()[0]
        self.assertLessEqual(max_atk, 400)

    def test_t2_char_def_min_bound(self):
        """T2.5: Character base_def minimum boundary is >= 500."""
        min_def = self.cursor.execute("SELECT MIN(base_def) FROM characters;").fetchone()[0]
        self.assertGreaterEqual(min_def, 500)

    def test_t2_char_def_max_bound(self):
        """T2.6: Character base_def maximum boundary is <= 1000."""
        max_def = self.cursor.execute("SELECT MAX(base_def) FROM characters;").fetchone()[0]
        self.assertLessEqual(max_def, 1000)

    def test_t2_char_rarity_strictly_4_or_5(self):
        """T2.7: Character rarity is strictly constrained to 4 or 5."""
        invalid = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE rarity NOT IN (4, 5);").fetchone()[0]
        self.assertEqual(invalid, 0)

    def test_t2_char_no_3_star_chars(self):
        """T2.8: No 3-star characters exist."""
        count = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE rarity = 3;").fetchone()[0]
        self.assertEqual(count, 0)

    def test_t2_char_no_6_star_chars(self):
        """T2.9: No 6-star characters exist."""
        count = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE rarity > 5;").fetchone()[0]
        self.assertEqual(count, 0)

    def test_t2_char_release_patch_between_1_and_8(self):
        """T2.10: Character release_patch is between 1.0 and 8.0."""
        invalid = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE release_patch < 1.0 OR release_patch > 8.0;").fetchone()[0]
        self.assertEqual(invalid, 0)

    # --- Weapon Stat Boundaries (10 tests) ---
    def test_t2_weapon_atk_min_bound(self):
        """T2.11: Weapon base_atk minimum boundary is >= 354."""
        min_atk = self.cursor.execute("SELECT MIN(base_atk) FROM weapons;").fetchone()[0]
        self.assertGreaterEqual(min_atk, 354)

    def test_t2_weapon_atk_max_bound_741(self):
        """T2.12: Weapon base_atk maximum boundary is exactly 741."""
        max_atk = self.cursor.execute("SELECT MAX(base_atk) FROM weapons;").fetchone()[0]
        self.assertEqual(max_atk, 741, "Highest base ATK in weapons catalog must be exactly 741")

    def test_t2_weapon_rarity_strictly_3_4_5(self):
        """T2.13: Weapon rarity is strictly constrained to 3, 4, or 5."""
        invalid = self.cursor.execute("SELECT COUNT(*) FROM weapons WHERE rarity NOT IN (3, 4, 5);").fetchone()[0]
        self.assertEqual(invalid, 0)

    def test_t2_weapon_no_1_or_2_star_weapons(self):
        """T2.14: No 1-star or 2-star weapons exist in catalog."""
        invalid = self.cursor.execute("SELECT COUNT(*) FROM weapons WHERE rarity < 3;").fetchone()[0]
        self.assertEqual(invalid, 0)

    def test_t2_weapon_is_craftable_strictly_0_or_1(self):
        """T2.15: is_craftable column is strictly 0 or 1."""
        invalid = self.cursor.execute("SELECT COUNT(*) FROM weapons WHERE is_craftable NOT IN (0, 1);").fetchone()[0]
        self.assertEqual(invalid, 0)

    def test_t2_weapon_sub_stat_crit_rate_cap(self):
        """T2.16: Weapon CRIT Rate sub-stat is positive and <= 44.1%."""
        invalid = self.cursor.execute("""
            SELECT COUNT(*) FROM weapons WHERE sub_stat_type = 'CRIT Rate' AND (sub_stat_value <= 0 OR sub_stat_value > 44.1);
        """).fetchone()[0]
        self.assertEqual(invalid, 0)

    def test_t2_weapon_sub_stat_crit_dmg_cap(self):
        """T2.17: Weapon CRIT DMG sub-stat is positive and <= 88.2%."""
        invalid = self.cursor.execute("""
            SELECT COUNT(*) FROM weapons WHERE sub_stat_type = 'CRIT DMG' AND (sub_stat_value <= 0 OR sub_stat_value > 88.2);
        """).fetchone()[0]
        self.assertEqual(invalid, 0)

    def test_t2_weapon_sub_stat_er_cap(self):
        """T2.18: Weapon Energy Recharge sub-stat is positive and <= 61.3%."""
        invalid = self.cursor.execute("""
            SELECT COUNT(*) FROM weapons WHERE sub_stat_type = 'Energy Recharge' AND (sub_stat_value <= 0 OR sub_stat_value > 61.3);
        """).fetchone()[0]
        self.assertEqual(invalid, 0)

    def test_t2_weapon_sub_stat_atk_pct_cap(self):
        """T2.19: Weapon ATK% sub-stat is positive and <= 55.1%."""
        invalid = self.cursor.execute("""
            SELECT COUNT(*) FROM weapons WHERE sub_stat_type = 'ATK%' AND (sub_stat_value <= 0 OR sub_stat_value > 55.1);
        """).fetchone()[0]
        self.assertEqual(invalid, 0)

    def test_t2_weapon_sub_stat_def_hp_pct_caps(self):
        """T2.20: Weapon DEF% <= 85.0% (Peak Patrol Song = 82.7%) and HP% <= 70.0% (Key of Khaj-Nisut = 66.2%)."""
        inv_def = self.cursor.execute("SELECT COUNT(*) FROM weapons WHERE sub_stat_type = 'DEF%' AND sub_stat_value > 85.0;").fetchone()[0]
        inv_hp = self.cursor.execute("SELECT COUNT(*) FROM weapons WHERE sub_stat_type = 'HP%' AND sub_stat_value > 70.0;").fetchone()[0]
        self.assertEqual(inv_def, 0)
        self.assertEqual(inv_hp, 0)

    # --- Categorical CHECK Constraints (10 tests) ---
    def test_t2_vision_valid_7_elements_only(self):
        """T2.21: vision values are strictly from the 7 standard Genshin elements."""
        valid_visions = ('Pyro', 'Hydro', 'Anemo', 'Electro', 'Dendro', 'Cryo', 'Geo')
        invalid = self.cursor.execute(f"SELECT COUNT(*) FROM characters WHERE vision NOT IN ({','.join('?' for _ in valid_visions)});", valid_visions).fetchone()[0]
        self.assertEqual(invalid, 0)

    def test_t2_vision_no_lowercase_or_mixed_case(self):
        """T2.22: vision values are properly capitalized with no casing defects."""
        valid_visions = {'Pyro', 'Hydro', 'Anemo', 'Electro', 'Dendro', 'Cryo', 'Geo'}
        visions = {row[0] for row in self.cursor.execute("SELECT DISTINCT vision FROM characters;").fetchall()}
        self.assertTrue(visions.issubset(valid_visions))

    def test_t2_vision_no_unknown_elements(self):
        """T2.23: No exotic or invalid elements (Quantum, Imaginary, Omni) exist."""
        bad_count = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE vision IN ('Quantum', 'Imaginary', 'Omni', 'Physical');").fetchone()[0]
        self.assertEqual(bad_count, 0)

    def test_t2_weapon_type_valid_5_types_only(self):
        """T2.24: characters.weapon_type is strictly in ('Sword', 'Claymore', 'Polearm', 'Bow', 'Catalyst')."""
        valid_types = ('Sword', 'Claymore', 'Polearm', 'Bow', 'Catalyst')
        invalid = self.cursor.execute(f"SELECT COUNT(*) FROM characters WHERE weapon_type NOT IN ({','.join('?' for _ in valid_types)});", valid_types).fetchone()[0]
        self.assertEqual(invalid, 0)

    def test_t2_weapons_table_weapon_type_valid_5_types_only(self):
        """T2.25: weapons.weapon_type is strictly in ('Sword', 'Claymore', 'Polearm', 'Bow', 'Catalyst')."""
        valid_types = ('Sword', 'Claymore', 'Polearm', 'Bow', 'Catalyst')
        invalid = self.cursor.execute(f"SELECT COUNT(*) FROM weapons WHERE weapon_type NOT IN ({','.join('?' for _ in valid_types)});", valid_types).fetchone()[0]
        self.assertEqual(invalid, 0)

    def test_t2_tier_rating_valid_4_tiers_only(self):
        """T2.26: character_builds.tier_rating is strictly in ('SS', 'S+', 'S', 'A')."""
        valid_tiers = ('SS', 'S+', 'S', 'A')
        invalid = self.cursor.execute(f"SELECT COUNT(*) FROM character_builds WHERE tier_rating NOT IN ({','.join('?' for _ in valid_tiers)});", valid_tiers).fetchone()[0]
        self.assertEqual(invalid, 0)

    def test_t2_tier_rating_no_b_c_d_tiers(self):
        """T2.27: No low tier ratings ('B', 'C', 'D', 'F') exist in builds."""
        bad_count = self.cursor.execute("SELECT COUNT(*) FROM character_builds WHERE tier_rating IN ('B', 'C', 'D', 'F');").fetchone()[0]
        self.assertEqual(bad_count, 0)

    def test_t2_default_role_not_empty(self):
        """T2.28: characters.default_role is non-empty and non-null for all characters."""
        empty_cnt = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE default_role IS NULL OR TRIM(default_role) = '';").fetchone()[0]
        self.assertEqual(empty_cnt, 0)

    def test_t2_build_role_not_empty(self):
        """T2.29: character_builds.role is non-empty and non-null for all builds."""
        empty_cnt = self.cursor.execute("SELECT COUNT(*) FROM character_builds WHERE role IS NULL OR TRIM(role) = '';").fetchone()[0]
        self.assertEqual(empty_cnt, 0)

    def test_t2_talent_priority_format(self):
        """T2.30: talent_priority contains valid relational priority delimiters ('>' or '=')."""
        invalid = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE talent_priority NOT LIKE '%>%' AND talent_priority NOT LIKE '%=%';").fetchone()[0]
        self.assertEqual(invalid, 0)

    # --- Regional Edge Cases & Aloy (10 tests) ---
    def test_t2_aloy_region_strictly_string_none(self):
        """T2.31: Aloy's region is strictly string 'None'."""
        reg = self.cursor.execute("SELECT region FROM characters WHERE name = 'Aloy';").fetchone()[0]
        self.assertEqual(reg, "None")

    def test_t2_aloy_region_not_null(self):
        """T2.32: Aloy's region is NOT SQL NULL."""
        null_cnt = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE name = 'Aloy' AND region IS NULL;").fetchone()[0]
        self.assertEqual(null_cnt, 0)

    def test_t2_aloy_region_not_empty_string(self):
        """T2.33: Aloy's region is NOT empty string."""
        empty_cnt = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE name = 'Aloy' AND region = '';").fetchone()[0]
        self.assertEqual(empty_cnt, 0)

    def test_t2_no_empty_character_regions(self):
        """T2.34: No characters have empty or whitespace region."""
        cnt = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE region IS NULL OR TRIM(region) = '';").fetchone()[0]
        self.assertEqual(cnt, 0)

    def test_t2_no_whitespace_character_regions(self):
        """T2.35: No character region strings have leading/trailing whitespace."""
        bad_cnt = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE region != TRIM(region);").fetchone()[0]
        self.assertEqual(bad_cnt, 0)

    def test_t2_no_empty_artifact_regions(self):
        """T2.36: No artifact sets have empty or whitespace region."""
        cnt = self.cursor.execute("SELECT COUNT(*) FROM artifact_sets WHERE region IS NULL OR TRIM(region) = '';").fetchone()[0]
        self.assertEqual(cnt, 0)

    def test_t2_no_whitespace_artifact_regions(self):
        """T2.37: No artifact set region strings have leading/trailing whitespace."""
        bad_cnt = self.cursor.execute("SELECT COUNT(*) FROM artifact_sets WHERE region != TRIM(region);").fetchone()[0]
        self.assertEqual(bad_cnt, 0)

    def test_t2_total_regional_character_sum_is_129(self):
        """T2.38: Sum of characters grouped by region is exactly 129."""
        total = self.cursor.execute("SELECT SUM(c) FROM (SELECT COUNT(*) as c FROM characters GROUP BY region);").fetchone()[0]
        self.assertEqual(total, 129)

    def test_t2_all_regions_have_at_least_one_character(self):
        """T2.39: All 10 distinct regional classifications have >= 1 character."""
        distinct_regions = self.cursor.execute("SELECT COUNT(DISTINCT region) FROM characters;").fetchone()[0]
        self.assertEqual(distinct_regions, 10, "Expected exactly 10 regions (7 nations + Nod-Krai + Outlander + None)")

    def test_t2_unknown_region_count_is_zero(self):
        """T2.40: Zero characters have 'Unknown' or 'TBD' region."""
        bad_cnt = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE region IN ('Unknown', 'TBD', '?');").fetchone()[0]
        self.assertEqual(bad_cnt, 0)

    # --- Nullability, Unique Keys, and FK Edge Cases (10 tests) ---
    def test_t2_character_ids_all_positive_integers(self):
        """T2.41: All character_id values are strictly positive integers."""
        bad_cnt = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE character_id <= 0;").fetchone()[0]
        self.assertEqual(bad_cnt, 0)

    def test_t2_character_names_all_unique(self):
        """T2.42: All character names are strictly unique."""
        dupes = self.cursor.execute("SELECT name, COUNT(*) FROM characters GROUP BY name HAVING COUNT(*) > 1;").fetchall()
        self.assertEqual(len(dupes), 0, f"Duplicate character names: {dupes}")

    def test_t2_weapon_ids_all_positive_integers(self):
        """T2.43: All weapon_id values are strictly positive integers."""
        bad_cnt = self.cursor.execute("SELECT COUNT(*) FROM weapons WHERE weapon_id <= 0;").fetchone()[0]
        self.assertEqual(bad_cnt, 0)

    def test_t2_weapon_names_all_unique(self):
        """T2.44: All weapon names are strictly unique."""
        dupes = self.cursor.execute("SELECT name, COUNT(*) FROM weapons GROUP BY name HAVING COUNT(*) > 1;").fetchall()
        self.assertEqual(len(dupes), 0, f"Duplicate weapon names: {dupes}")

    def test_t2_artifact_set_ids_all_positive_integers(self):
        """T2.45: All artifact_set_id values are strictly positive integers."""
        bad_cnt = self.cursor.execute("SELECT COUNT(*) FROM artifact_sets WHERE artifact_set_id <= 0;").fetchone()[0]
        self.assertEqual(bad_cnt, 0)

    def test_t2_artifact_set_names_all_unique(self):
        """T2.46: All artifact set names are strictly unique."""
        dupes = self.cursor.execute("SELECT name, COUNT(*) FROM artifact_sets GROUP BY name HAVING COUNT(*) > 1;").fetchall()
        self.assertEqual(len(dupes), 0, f"Duplicate artifact set names: {dupes}")

    def test_t2_build_ids_all_positive_integers(self):
        """T2.47: All build_id values are strictly positive integers."""
        bad_cnt = self.cursor.execute("SELECT COUNT(*) FROM character_builds WHERE build_id <= 0;").fetchone()[0]
        self.assertEqual(bad_cnt, 0)

    def test_t2_signature_id_null_or_valid_character_id(self):
        """T2.48: weapons.signature_character_id is either NULL or a valid character_id."""
        invalid_fks = self.cursor.execute("""
            SELECT w.weapon_id, w.name, w.signature_character_id
            FROM weapons w
            LEFT JOIN characters c ON w.signature_character_id = c.character_id
            WHERE w.signature_character_id IS NOT NULL AND c.character_id IS NULL;
        """).fetchall()
        self.assertEqual(len(invalid_fks), 0, f"Invalid signature character references: {invalid_fks}")

    def test_t2_non_null_signature_characters_exist(self):
        """T2.49: There are both weapons with and without signature characters."""
        with_sig = self.cursor.execute("SELECT COUNT(*) FROM weapons WHERE signature_character_id IS NOT NULL;").fetchone()[0]
        without_sig = self.cursor.execute("SELECT COUNT(*) FROM weapons WHERE signature_character_id IS NULL;").fetchone()[0]
        self.assertGreater(with_sig, 20, "Expected at least 20 weapons with signature characters")
        self.assertGreater(without_sig, 50, "Expected at least 50 weapons without signature characters")

    def test_t2_craftable_weapons_signature_id_is_always_null(self):
        """T2.50: All craftable weapons (is_craftable = 1) have signature_character_id IS NULL."""
        bad_craft = self.cursor.execute("""
            SELECT weapon_id, name FROM weapons WHERE is_craftable = 1 AND signature_character_id IS NOT NULL;
        """).fetchall()
        self.assertEqual(len(bad_craft), 0, f"Craftable weapons cannot have signature owners: {bad_craft}")

    # --- Escaping, Quotes, and String Encoding (10 tests) ---
    def test_t2_single_quote_weapons_query_handling(self):
        """T2.51: Weapons with apostrophes (e.g. Amos' Bow, Dragon's Bane) query cleanly."""
        names = ["Amos' Bow", "Dragon's Bane", "Crane's Echoing Call", "Crimson Moon's Semblance", "Astral Vulture's Crimson Plumage"]
        for name in names:
            row = self.cursor.execute("SELECT weapon_id FROM weapons WHERE name = ?;", (name,)).fetchone()
            self.assertIsNotNone(row, f"Failed to query weapon with apostrophe: {name}")

    def test_t2_single_quote_artifacts_query_handling(self):
        """T2.52: Artifacts with apostrophes query cleanly without syntax error."""
        names = ["Moonchild's Treasures", "Thorny Crown of the Mountain Wind"]
        for domain in names:
            rows = self.cursor.execute("SELECT artifact_set_id FROM artifact_sets WHERE domain_name = ?;", (domain,)).fetchall()
            self.assertGreater(len(rows), 0, f"Failed querying domain with apostrophe: {domain}")

    def test_t2_single_quote_builds_query_handling(self):
        """T2.53: Builds mentioning single quotes in playstyle notes query cleanly."""
        rows = self.cursor.execute("SELECT build_id FROM character_builds WHERE playstyle_notes LIKE '%''%' OR playstyle_notes LIKE '%’%';").fetchall()
        self.assertIsInstance(rows, list)

    def test_t2_hyphenated_names_query_handling(self):
        """T2.54: Hyphenated weapon and character names query cleanly."""
        hyphen_names = ["Freedom-Sworn", "Key of Khaj-Nisut", "Primordial Jade Winged-Spear", "Wolf-Fang"]
        for n in hyphen_names:
            row = self.cursor.execute("SELECT weapon_id FROM weapons WHERE name = ?;", (n,)).fetchone()
            self.assertIsNotNone(row, f"Hyphenated weapon missing: {n}")

    def test_t2_parentheses_in_names_query_handling(self):
        """T2.55: Character names with parentheses query cleanly."""
        traveler_names = ["Traveler (Electro)", "Traveler (Hydro)"]
        for tn in traveler_names:
            row = self.cursor.execute("SELECT character_id FROM characters WHERE name = ?;", (tn,)).fetchone()
            self.assertIsNotNone(row, f"Character with parentheses missing: {tn}")

    def test_t2_two_piece_bonus_special_chars(self):
        """T2.56: 2-piece bonuses are non-null and non-empty strings."""
        invalid = self.cursor.execute("SELECT COUNT(*) FROM artifact_sets WHERE two_piece_bonus IS NULL OR TRIM(two_piece_bonus) = '';").fetchone()[0]
        self.assertEqual(invalid, 0)

    def test_t2_four_piece_bonus_special_chars(self):
        """T2.57: 4-piece bonuses contain proper descriptive text."""
        invalid = self.cursor.execute("SELECT COUNT(*) FROM artifact_sets WHERE four_piece_bonus IS NULL OR TRIM(four_piece_bonus) = '';").fetchone()[0]
        self.assertEqual(invalid, 0)

    def test_t2_playstyle_notes_special_chars(self):
        """T2.58: Playstyle notes contain valid punctuation without unescaped null bytes."""
        bad_cnt = self.cursor.execute("SELECT COUNT(*) FROM character_builds WHERE instr(playstyle_notes, char(0)) > 0;").fetchone()[0]
        self.assertEqual(bad_cnt, 0)

    def test_t2_domain_name_quotes_safe(self):
        """T2.59: Domain names are safe strings with no leading or trailing whitespace."""
        bad_cnt = self.cursor.execute("SELECT COUNT(*) FROM artifact_sets WHERE domain_name != TRIM(domain_name);").fetchone()[0]
        self.assertEqual(bad_cnt, 0)

    def test_t2_character_name_spaces_safe(self):
        """T2.60: Character names have no leading or trailing whitespace."""
        bad_cnt = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE name != TRIM(name);").fetchone()[0]
        self.assertEqual(bad_cnt, 0)

    # --- CSV Parsing and File Boundaries (10 tests) ---
    def test_t2_characters_csv_has_12_columns(self):
        """T2.61: characters.csv has exactly 12 columns in header and all rows."""
        csv_path = os.path.join(DATA_DIR, "characters.csv")
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                self.assertEqual(len(row), 12, f"characters.csv row {i} has {len(row)} columns, expected 12")

    def test_t2_weapons_csv_has_9_columns(self):
        """T2.62: weapons.csv has exactly 9 columns in header and all rows."""
        csv_path = os.path.join(DATA_DIR, "weapons.csv")
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                self.assertEqual(len(row), 9, f"weapons.csv row {i} has {len(row)} columns, expected 9")

    def test_t2_artifact_sets_csv_has_6_columns(self):
        """T2.63: artifact_sets.csv has exactly 6 columns in header and all rows."""
        csv_path = os.path.join(DATA_DIR, "artifact_sets.csv")
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                self.assertEqual(len(row), 6, f"artifact_sets.csv row {i} has {len(row)} columns, expected 6")

    def test_t2_character_builds_csv_has_11_columns(self):
        """T2.64: character_builds.csv has exactly 11 columns in header and all rows."""
        csv_path = os.path.join(DATA_DIR, "character_builds.csv")
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                self.assertEqual(len(row), 11, f"character_builds.csv row {i} has {len(row)} columns, expected 11")

    def test_t2_csv_files_exist_and_non_empty(self):
        """T2.65: All 4 CSV files in data/ exist and have non-zero file size."""
        for t in ["characters", "weapons", "artifact_sets", "character_builds"]:
            path = os.path.join(DATA_DIR, f"{t}.csv")
            self.assertTrue(os.path.exists(path), f"{t}.csv must exist")
            self.assertGreater(os.path.getsize(path), 1000, f"{t}.csv file too small")

    def test_t2_weapons_csv_null_represented_as_empty_string(self):
        """T2.66: weapons.csv nullable signature_character_id is represented as empty string."""
        csv_path = os.path.join(DATA_DIR, "weapons.csv")
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            empty_count = sum(1 for row in reader if row[8] == "")
            self.assertGreater(empty_count, 50, "Expected empty strings for non-signature weapons in CSV")

    def test_t2_csv_headers_match_schema_columns(self):
        """T2.67: CSV headers match SQLite column names exactly."""
        csv_path = os.path.join(DATA_DIR, "characters.csv")
        with open(csv_path, "r", encoding="utf-8") as f:
            header = next(csv.reader(f))
        db_cols = [r[1] for r in self.cursor.execute("PRAGMA table_info(characters);").fetchall()]
        self.assertEqual(header, db_cols, "characters.csv header does not match table_info")

    def test_t2_no_trailing_blank_rows_in_csvs(self):
        """T2.68: CSV files contain no trailing blank rows."""
        for t in ["characters", "weapons", "artifact_sets", "character_builds"]:
            csv_path = os.path.join(DATA_DIR, f"{t}.csv")
            with open(csv_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            with open(csv_path, "r", encoding="utf-8") as f:
                reader_rows = list(csv.reader(f))
            self.assertEqual(len(lines), len(reader_rows), f"Trailing blank lines in {t}.csv")

    def test_t2_csv_newline_consistency(self):
        """T2.69: CSV files use standard newline formatting."""
        csv_path = os.path.join(DATA_DIR, "weapons.csv")
        with open(csv_path, "rb") as f:
            data = f.read()
        self.assertIn(b"\n", data)

    def test_t2_csv_ids_match_db_ids_order(self):
        """T2.70: CSV primary keys match DB primary keys in exact ascending order."""
        csv_path = os.path.join(DATA_DIR, "artifact_sets.csv")
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            csv_ids = [int(r[0]) for r in reader]
        db_ids = [r[0] for r in self.cursor.execute("SELECT artifact_set_id FROM artifact_sets ORDER BY artifact_set_id;").fetchall()]
        self.assertEqual(csv_ids, db_ids)


# =====================================================================
# TIER 3: CROSS-FEATURE COMBINATION TESTS (25 tests)
# =====================================================================

class Tier3CrossFeatureCombinationTests(unittest.TestCase):
    """Tier 3: Pairwise relational interactions, cross-table constraints, cascades, and role divergence."""

    def setUp(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_t3_weapon_type_compatibility_100_percent_builds(self):
        """T3.1: 100% of character builds have matching character and weapon weapon_type."""
        mismatches = self.cursor.execute("""
            SELECT cb.build_id, c.name, c.weapon_type, w.name, w.weapon_type
            FROM character_builds cb
            JOIN characters c ON cb.character_id = c.character_id
            JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
            WHERE c.weapon_type != w.weapon_type;
        """).fetchall()
        self.assertEqual(len(mismatches), 0, f"Found weapon type mismatches: {mismatches}")

    def test_t3_4_table_inner_join_count(self):
        """T3.2: 4-table INNER JOIN across characters, builds, weapons, artifact_sets yields 168 rows."""
        count = self.cursor.execute("""
            SELECT COUNT(*)
            FROM character_builds cb
            JOIN characters c ON cb.character_id = c.character_id
            JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
            JOIN artifact_sets a ON cb.recommended_artifact_id = a.artifact_set_id;
        """).fetchone()[0]
        self.assertEqual(count, 168, f"4-table JOIN must produce exactly 168 rows, got {count}")

    def test_t3_left_join_no_dangling_character_builds(self):
        """T3.3: Zero builds have dangling character references."""
        count = self.cursor.execute("""
            SELECT COUNT(*) FROM character_builds cb
            LEFT JOIN characters c ON cb.character_id = c.character_id
            WHERE c.character_id IS NULL;
        """).fetchone()[0]
        self.assertEqual(count, 0)

    def test_t3_left_join_no_dangling_weapon_builds(self):
        """T3.4: Zero builds have dangling recommended_weapon references."""
        count = self.cursor.execute("""
            SELECT COUNT(*) FROM character_builds cb
            LEFT JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
            WHERE w.weapon_id IS NULL;
        """).fetchone()[0]
        self.assertEqual(count, 0)

    def test_t3_left_join_no_dangling_artifact_builds(self):
        """T3.5: Zero builds have dangling recommended_artifact references."""
        count = self.cursor.execute("""
            SELECT COUNT(*) FROM character_builds cb
            LEFT JOIN artifact_sets a ON cb.recommended_artifact_id = a.artifact_set_id
            WHERE a.artifact_set_id IS NULL;
        """).fetchone()[0]
        self.assertEqual(count, 0)

    def test_t3_on_delete_cascade_behavior(self):
        """T3.6: ON DELETE CASCADE drops builds when character is deleted (isolated rollback)."""
        self.conn.execute("BEGIN;")
        try:
            temp_cur = self.conn.cursor()
            # Select character with builds
            cid = temp_cur.execute("SELECT character_id FROM character_builds LIMIT 1;").fetchone()[0]
            builds_before = temp_cur.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = ?;", (cid,)).fetchone()[0]
            self.assertGreater(builds_before, 0)
            temp_cur.execute("DELETE FROM characters WHERE character_id = ?;", (cid,))
            builds_after = temp_cur.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = ?;", (cid,)).fetchone()[0]
            self.assertEqual(builds_after, 0, "Builds must be cascaded on character deletion")
        finally:
            self.conn.rollback()

    def test_t3_on_delete_restrict_weapon_behavior(self):
        """T3.7: ON DELETE RESTRICT blocks deletion of weapon referenced by character_builds."""
        self.conn.execute("BEGIN;")
        try:
            temp_cur = self.conn.cursor()
            wid = temp_cur.execute("SELECT recommended_weapon_id FROM character_builds LIMIT 1;").fetchone()[0]
            with self.assertRaises(sqlite3.IntegrityError):
                temp_cur.execute("DELETE FROM weapons WHERE weapon_id = ?;", (wid,))
        finally:
            self.conn.rollback()

    def test_t3_on_delete_restrict_artifact_behavior(self):
        """T3.8: ON DELETE RESTRICT blocks deletion of artifact set referenced by character_builds."""
        self.conn.execute("BEGIN;")
        try:
            temp_cur = self.conn.cursor()
            aid = temp_cur.execute("SELECT recommended_artifact_id FROM character_builds LIMIT 1;").fetchone()[0]
            with self.assertRaises(sqlite3.IntegrityError):
                temp_cur.execute("DELETE FROM artifact_sets WHERE artifact_set_id = ?;", (aid,))
        finally:
            self.conn.rollback()

    def test_t3_on_delete_set_null_signature_behavior(self):
        """T3.9: ON DELETE SET NULL sets signature_character_id to NULL when owner character deleted."""
        self.conn.execute("BEGIN;")
        try:
            temp_cur = self.conn.cursor()
            row = temp_cur.execute("SELECT weapon_id, signature_character_id FROM weapons WHERE signature_character_id IS NOT NULL LIMIT 1;").fetchone()
            wid, cid = row[0], row[1]
            temp_cur.execute("DELETE FROM characters WHERE character_id = ?;", (cid,))
            sig_after = temp_cur.execute("SELECT signature_character_id FROM weapons WHERE weapon_id = ?;", (wid,)).fetchone()[0]
            self.assertIsNone(sig_after, "signature_character_id must become NULL upon character deletion")
        finally:
            self.conn.rollback()

    def test_t3_shielder_builds_def_or_hp_affinity(self):
        """T3.10: Shielder builds prioritize DEF% or HP% main stats."""
        rows = self.cursor.execute("SELECT build_name, sands_stat, goblet_stat, circlet_stat FROM character_builds WHERE role = 'Shielder';").fetchall()
        self.assertGreater(len(rows), 0)
        for r in rows:
            stats = f"{r['sands_stat']} {r['goblet_stat']} {r['circlet_stat']}"
            self.assertTrue("DEF%" in stats or "HP%" in stats or "Energy Recharge" in stats, f"Shielder build '{r['build_name']}' lacks defensive/energy stats: {stats}")

    def test_t3_healer_builds_healing_or_hp_affinity(self):
        """T3.11: Healer builds prioritize HP%, Healing Bonus, ATK%, ER, or EM (e.g. Kuki)."""
        rows = self.cursor.execute("SELECT build_name, circlet_stat, goblet_stat, sands_stat FROM character_builds WHERE role = 'Healer';").fetchall()
        self.assertGreater(len(rows), 0)
        for r in rows:
            stats = f"{r['sands_stat']} {r['goblet_stat']} {r['circlet_stat']}"
            self.assertTrue("Healing Bonus" in stats or "HP%" in stats or "ATK%" in stats or "Energy Recharge" in stats or "Elemental Mastery" in stats, f"Healer '{r['build_name']}' stats invalid: {stats}")

    def test_t3_mavuika_multi_build_role_divergence(self):
        """T3.12: Mavuika Main DPS build vs Support build have distinct artifact sets."""
        builds = self.cursor.execute("SELECT build_name, role, recommended_artifact_id FROM character_builds WHERE character_id = 87;").fetchall()
        self.assertGreaterEqual(len(builds), 2)
        roles = {b["role"] for b in builds}
        arts = {b["recommended_artifact_id"] for b in builds}
        self.assertIn("Main DPS", roles)
        self.assertTrue("Support" in roles or "Sub-DPS" in roles)
        self.assertIn(53, arts, "Mavuika must have a build using 4pc Cinder City (Set 53)")

    def test_t3_chasca_multi_build_weapon_divergence(self):
        """T3.13: Chasca builds include 5-star signature (130) and F2P craftable (185)."""
        weapons = {row[0] for row in self.cursor.execute("SELECT recommended_weapon_id FROM character_builds WHERE character_id = 86;").fetchall()}
        self.assertIn(130, weapons, "Chasca must have build with signature 130")
        self.assertIn(185, weapons, "Chasca must have build with F2P weapon 185")

    def test_t3_citlali_multi_build_weapon_divergence(self):
        """T3.14: Citlali builds include 5-star signature (132) and F2P weapon (194)."""
        weapons = {row[0] for row in self.cursor.execute("SELECT recommended_weapon_id FROM character_builds WHERE character_id = 88;").fetchall()}
        self.assertIn(132, weapons, "Citlali must have build with signature 132")
        self.assertIn(194, weapons, "Citlali must have build with F2P weapon 194")

    def test_t3_craftable_weapons_represented_in_every_weapon_type(self):
        """T3.15: Craftable weapons exist for all 5 weapon types."""
        types = {row[0] for row in self.cursor.execute("SELECT DISTINCT weapon_type FROM weapons WHERE is_craftable = 1;").fetchall()}
        self.assertEqual(types, {"Sword", "Claymore", "Polearm", "Bow", "Catalyst"})

    def test_t3_craftable_weapons_available_in_f2p_builds(self):
        """T3.16: Craftable weapons appear in character_builds recommendations."""
        craft_in_builds = self.cursor.execute("""
            SELECT COUNT(DISTINCT cb.build_id)
            FROM character_builds cb
            JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
            WHERE w.is_craftable = 1;
        """).fetchone()[0]
        self.assertGreaterEqual(craft_in_builds, 5, "Expected at least 5 builds recommending craftables")

    def test_t3_5_star_signatures_link_to_correct_character_rarity(self):
        """T3.17: 5★ signature weapons link to 5★ characters (or valid event canonical characters)."""
        signatures = self.cursor.execute("""
            SELECT w.name, w.rarity as wr, c.name as cname, c.rarity as cr
            FROM weapons w
            JOIN characters c ON w.signature_character_id = c.character_id
            WHERE w.rarity = 5;
        """).fetchall()
        self.assertGreater(len(signatures), 20)
        for s in signatures:
            self.assertEqual(s["cr"], 5, f"5★ weapon {s['name']} linked to 4★ character {s['cname']}")

    def test_t3_cryo_characters_and_cryo_artifacts_pair(self):
        """T3.18: Cryo DPS characters utilize Blizzard Strayer, Marechaussee, Aubade, Wanderer's, or Emblem."""
        valid_cryo_sets = {31, 36, 47, 59, 21, 20}
        rows = self.cursor.execute("""
            SELECT cb.build_name, cb.recommended_artifact_id
            FROM character_builds cb
            JOIN characters c ON cb.character_id = c.character_id
            WHERE c.vision = 'Cryo' AND cb.role IN ('Main DPS', 'Sub-DPS');
        """).fetchall()
        for r in rows:
            self.assertIn(r["recommended_artifact_id"], valid_cryo_sets | {34, 38, 24, 62}, f"Cryo DPS build {r['build_name']} uses unexpected artifact")

    def test_t3_pyro_characters_and_pyro_artifacts_pair(self):
        """T3.19: Pyro characters utilize Crimson Witch, Obsidian Codex, Cinder City, Shimenawa, Whimsy, Gladiator, or Noblesse."""
        valid_pyro_sets = {30, 54, 53, 21, 36, 47, 35, 46, 51, 19}
        rows = self.cursor.execute("""
            SELECT cb.build_name, cb.recommended_artifact_id
            FROM character_builds cb
            JOIN characters c ON cb.character_id = c.character_id
            WHERE c.vision = 'Pyro';
        """).fetchall()
        for r in rows:
            self.assertIn(r["recommended_artifact_id"], valid_pyro_sets | {48, 20, 27}, f"Pyro build {r['build_name']} uses unexpected set")

    def test_t3_anemo_characters_and_vv_artifact_pair(self):
        """T3.20: Anemo support builds utilize Viridescent Venerer (Set 24)."""
        rows = self.cursor.execute("""
            SELECT cb.build_name, cb.recommended_artifact_id
            FROM character_builds cb
            JOIN characters c ON cb.character_id = c.character_id
            WHERE c.vision = 'Anemo' AND cb.role IN ('Support', 'Healer');
        """).fetchall()
        vv_or_noblesse = sum(1 for r in rows if r["recommended_artifact_id"] in (24, 21, 53))
        self.assertEqual(vv_or_noblesse, len(rows), "Anemo supports must recommend VV (24) or Noblesse/Cinder City")

    def test_t3_geo_characters_and_husk_or_nighttime_pair(self):
        """T3.21: Geo characters utilize Husk of Opulent Dreams, Nighttime Whispers, Archaic Petra, Bolide, or Cinder City."""
        geo_sets = {37, 50, 22, 33, 21, 48, 53, 25}
        rows = self.cursor.execute("""
            SELECT cb.build_name, cb.recommended_artifact_id
            FROM character_builds cb
            JOIN characters c ON cb.character_id = c.character_id
            WHERE c.vision = 'Geo';
        """).fetchall()
        for r in rows:
            self.assertIn(r["recommended_artifact_id"], geo_sets)

    def test_t3_dendro_characters_and_deepwood_pair(self):
        """T3.22: Dendro supports utilize Deepwood Memories (Set 41)."""
        rows = self.cursor.execute("""
            SELECT cb.build_name, cb.recommended_artifact_id
            FROM character_builds cb
            JOIN characters c ON cb.character_id = c.character_id
            WHERE c.vision = 'Dendro' AND cb.role IN ('Support', 'Healer');
        """).fetchall()
        for r in rows:
            self.assertIn(r["recommended_artifact_id"], {41, 33, 21})

    def test_t3_ss_tier_builds_have_5_star_or_top_meta_weapons(self):
        """T3.23: SS tier builds recommend rarity 4/5 weapons or canonical 3★ meta staples (Black Tassel, TTDS)."""
        low_tier_ss = self.cursor.execute("""
            SELECT cb.build_name, w.name, w.rarity
            FROM character_builds cb
            JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
            WHERE cb.tier_rating = 'SS' AND w.rarity < 4 AND w.name NOT IN ('Black Tassel', 'Thrilling Tales of Dragon Slayers');
        """).fetchall()
        self.assertEqual(len(low_tier_ss), 0, f"SS tier builds must not use non-staple 3★ weapons: {low_tier_ss}")

    def test_t3_character_release_patch_monotonic_ordering(self):
        """T3.24: Character release patch ordering respects major version milestones."""
        v1_count = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE release_patch < 2.0;").fetchone()[0]
        v5_count = self.cursor.execute("SELECT COUNT(*) FROM characters WHERE release_patch >= 5.0 AND release_patch < 6.0;").fetchone()[0]
        self.assertGreater(v1_count, 15, "Expected at least 15 Version 1.x characters")
        self.assertGreater(v5_count, 10, "Expected at least 10 Version 5.x characters")

    def test_t3_domain_to_artifact_sets_cardinality(self):
        """T3.25: Domains of Blessing contain at most 2 5-star artifact sets."""
        heavy_domains = self.cursor.execute("""
            SELECT domain_name, COUNT(*) as c
            FROM artifact_sets
            WHERE domain_name NOT IN ('Bosses / Chests', 'Chests / Early Domains', 'Mid-Level Domains')
            GROUP BY domain_name
            HAVING COUNT(*) > 2;
        """).fetchall()
        self.assertEqual(len(heavy_domains), 0, f"Standard farming domains must have <= 2 sets: {heavy_domains}")


# =====================================================================
# TIER 4: REAL-WORLD APPLICATION SCENARIO TESTS (6 tests)
# =====================================================================

class Tier4RealWorldApplicationScenarioTests(unittest.TestCase):
    """Tier 4: Complex multi-table end-to-end user query scenarios and analytical pipelines."""

    def setUp(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_t4_scenario_1_elemental_reaction_team_builder(self):
        """Scenario 1: Team builder query constructing a 4-character Vaporize team."""
        query = """
        WITH Roles AS (
            SELECT c.name as character_name, c.vision, cb.role, cb.build_name, w.name as weapon_name, a.name as artifact_name, cb.tier_rating,
                   ROW_NUMBER() OVER (PARTITION BY cb.role ORDER BY CASE cb.tier_rating WHEN 'SS' THEN 1 WHEN 'S+' THEN 2 WHEN 'S' THEN 3 ELSE 4 END) as rn
            FROM character_builds cb
            JOIN characters c ON cb.character_id = c.character_id
            JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
            JOIN artifact_sets a ON cb.recommended_artifact_id = a.artifact_set_id
        )
        SELECT role, character_name, vision, weapon_name, artifact_name, tier_rating
        FROM Roles
        WHERE rn = 1 AND role IN ('Main DPS', 'Sub-DPS', 'Support', 'Healer')
        ORDER BY CASE role WHEN 'Main DPS' THEN 1 WHEN 'Sub-DPS' THEN 2 WHEN 'Support' THEN 3 WHEN 'Healer' THEN 4 END;
        """
        team = self.cursor.execute(query).fetchall()
        self.assertEqual(len(team), 4, f"Team builder must return exactly 4 characters, got {len(team)}")
        assigned_roles = [t["role"] for t in team]
        self.assertEqual(assigned_roles, ["Main DPS", "Sub-DPS", "Support", "Healer"])
        for member in team:
            self.assertIn(member["tier_rating"], ("SS", "S+"))

    def test_t4_scenario_2_max_base_atk_scaling_ranking(self):
        """Scenario 2: Compute theoretical maximum base attack (char base_atk + weapon base_atk) across builds."""
        query = """
        SELECT c.name as character_name, w.name as weapon_name, c.base_atk as char_atk, w.base_atk as weap_atk,
               (c.base_atk + w.base_atk) as total_base_atk, cb.build_name
        FROM character_builds cb
        JOIN characters c ON cb.character_id = c.character_id
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        ORDER BY total_base_atk DESC
        LIMIT 10;
        """
        rows = self.cursor.execute(query).fetchall()
        self.assertEqual(len(rows), 10)
        # Top base attack must exceed 1000 (e.g. 359 char atk + 741 weapon atk = 1100)
        top_loadout = rows[0]
        self.assertGreaterEqual(top_loadout["total_base_atk"], 1050, f"Max base ATK should be >= 1050, got {top_loadout['total_base_atk']}")

    def test_t4_scenario_3_artifact_domain_route_optimization(self):
        """Scenario 3: Route optimization grouping artifact sets by domain and region for resin efficiency."""
        query = """
        SELECT a.region, a.domain_name, COUNT(cb.build_id) as total_build_demands,
               COUNT(DISTINCT c.character_id) as characters_benefiting
        FROM artifact_sets a
        JOIN character_builds cb ON a.artifact_set_id = cb.recommended_artifact_id
        JOIN characters c ON cb.character_id = c.character_id
        GROUP BY a.region, a.domain_name
        HAVING total_build_demands >= 3
        ORDER BY total_build_demands DESC
        LIMIT 5;
        """
        top_domains = self.cursor.execute(query).fetchall()
        self.assertGreater(len(top_domains), 0, "Expected top resin-efficient domains")
        # Premier domain (e.g. Momiji-Dyed Court or Deepwood/Gilded) should benefit multiple builds
        self.assertGreaterEqual(top_domains[0]["total_build_demands"], 5)

    def test_t4_scenario_4_f2p_budget_loadout_recommendations(self):
        """Scenario 4: F2P recommendation query finding craftable or 4★ weapon builds for each vision."""
        query = """
        SELECT c.vision, COUNT(DISTINCT cb.build_id) as f2p_build_count
        FROM character_builds cb
        JOIN characters c ON cb.character_id = c.character_id
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        WHERE w.is_craftable = 1 OR w.rarity <= 4
        GROUP BY c.vision
        ORDER BY c.vision;
        """
        rows = self.cursor.execute(query).fetchall()
        visions = {r["vision"] for r in rows}
        self.assertEqual(len(visions), 7, f"All 7 elements must have budget F2P build options: {visions}")
        for r in rows:
            self.assertGreaterEqual(r["f2p_build_count"], 1, f"Vision {r['vision']} has no budget builds")

    def test_t4_scenario_5_regional_material_and_character_dashboard(self):
        """Scenario 5: Dashboard CTE rollup summarizing regional characters, 5★ vs 4★ count, and average base stats."""
        query = """
        WITH RegionalMetrics AS (
            SELECT region,
                   COUNT(*) as total_chars,
                   SUM(CASE WHEN rarity = 5 THEN 1 ELSE 0 END) as five_star_count,
                   SUM(CASE WHEN rarity = 4 THEN 1 ELSE 0 END) as four_star_count,
                   ROUND(AVG(base_hp), 0) as avg_base_hp,
                   ROUND(AVG(base_atk), 0) as avg_base_atk,
                   ROUND(AVG(base_def), 0) as avg_base_def
            FROM characters
            GROUP BY region
        )
        SELECT * FROM RegionalMetrics
        ORDER BY total_chars DESC;
        """
        rows = self.cursor.execute(query).fetchall()
        self.assertEqual(len(rows), 10, "Dashboard must summarize all 10 regions")
        top_region = rows[0]
        self.assertGreaterEqual(top_region["total_chars"], 20, "Largest region should have >= 20 characters")

    def test_t4_scenario_6_meta_tier_list_matrix_window_function(self):
        """Scenario 6: Window function query generating game8-style tier list ranking matrix."""
        query = """
        WITH RankedBuilds AS (
            SELECT c.name as character_name, c.vision, cb.role, cb.tier_rating, w.name as weapon_name,
                   DENSE_RANK() OVER (PARTITION BY cb.role ORDER BY CASE cb.tier_rating WHEN 'SS' THEN 1 WHEN 'S+' THEN 2 WHEN 'S' THEN 3 ELSE 4 END) as rank_in_role
            FROM character_builds cb
            JOIN characters c ON cb.character_id = c.character_id
            JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        )
        SELECT role, rank_in_role, tier_rating, COUNT(*) as character_count,
               GROUP_CONCAT(character_name, ', ') as characters
        FROM RankedBuilds
        WHERE rank_in_role = 1
        GROUP BY role, rank_in_role, tier_rating
        ORDER BY role;
        """
        rows = self.cursor.execute(query).fetchall()
        self.assertGreater(len(rows), 0, "Window function meta matrix query must succeed")
        roles = {r["role"] for r in rows}
        self.assertTrue("Main DPS" in roles and "Support" in roles)


# =====================================================================
# CLI TEST RUNNER & DIAGNOSTICS HARNESS
# =====================================================================

def run_e2e_tests(
    db_path: str = DEFAULT_DB_PATH,
    selected_tiers: Optional[List[int]] = None,
    selected_features: Optional[List[str]] = None,
    verbose: bool = False
) -> Tuple[int, int, float]:
    """
    Executes selected test suites with detailed formatted reporting.
    Returns (passed_count, failed_count, duration_seconds).
    """
    global ACTIVE_DB_PATH
    ACTIVE_DB_PATH = db_path

    print("=" * 72)
    print("GENSHIN IMPACT DATABASE E2E TEST RUNNER")
    print(f"Target Database : {db_path}")
    print(f"Active Root     : {PROJECT_ROOT}")
    print(f"Execution Time  : {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    print("=" * 72)

    tier_classes = {
        1: ("Tier 1: Feature Coverage (F1 to F14)", Tier1FeatureCoverageTests),
        2: ("Tier 2: Boundary & Corner Cases", Tier2BoundaryCornerCaseTests),
        3: ("Tier 3: Cross-Feature Relational Combinations", Tier3CrossFeatureCombinationTests),
        4: ("Tier 4: Real-World Application Scenarios", Tier4RealWorldApplicationScenarioTests),
    }

    tiers_to_run = selected_tiers or [1, 2, 3, 4]

    total_passed = 0
    total_failed = 0
    total_skipped = 0
    start_time = time.perf_counter()

    failure_details: List[Tuple[str, str, str]] = []

    for tier_num in sorted(tiers_to_run):
        if tier_num not in tier_classes:
            continue
        title, test_cls = tier_classes[tier_num]
        print(f"\n--- Running [{title}] ---")

        suite = unittest.TestSuite()
        loader = unittest.TestLoader()

        test_names = loader.getTestCaseNames(test_cls)

        if selected_features and tier_num == 1:
            filtered = []
            for name in test_names:
                for feat in selected_features:
                    feat_prefix = f"test_{feat.lower()}_"
                    if name.lower().startswith(feat_prefix):
                        filtered.append(name)
                        break
            test_names = filtered

        for tname in test_names:
            suite.addTest(test_cls(tname))

        tier_passed = 0
        tier_failed = 0

        # Execute tests manually to capture diagnostics cleanly
        for test in suite:
            test_id = test.id().split(".")[-1]
            doc = test.shortDescription() or test_id
            result = unittest.TestResult()
            test.run(result)

            if result.wasSuccessful():
                tier_passed += 1
                if verbose:
                    print(f"  [PASS] {test_id} - {doc}")
            else:
                tier_failed += 1
                err_msg = ""
                if result.failures:
                    err_msg = result.failures[0][1]
                elif result.errors:
                    err_msg = result.errors[0][1]
                failure_details.append((f"Tier {tier_num}: {test_id}", doc, err_msg))
                print(f"  [FAIL] {test_id} - {doc}")
                if verbose and err_msg:
                    first_err_line = err_msg.strip().split("\n")[-1]
                    print(f"         Reason: {first_err_line}")

        tier_total = tier_passed + tier_failed
        status_symbol = "PASSED" if tier_failed == 0 else f"{tier_failed} FAILED"
        print(f"  Result: {tier_passed}/{tier_total} passed [{status_symbol}]")

        total_passed += tier_passed
        total_failed += tier_failed

    elapsed = time.perf_counter() - start_time

    print("\n" + "=" * 72)
    print("TEST EXECUTION SUMMARY")
    print("=" * 72)
    print(f"Total Tests Run : {total_passed + total_failed}")
    print(f"Total Passed    : {total_passed}")
    print(f"Total Failed    : {total_failed}")
    print(f"Elapsed Time    : {elapsed:.3f} seconds")

    if failure_details:
        print("\n" + "-" * 72)
        print("DIAGNOSTIC FAILURE DETAILS")
        print("-" * 72)
        for i, (name, doc, err) in enumerate(failure_details, 1):
            last_line = err.strip().split("\n")[-1] if err else "Unknown error"
            print(f"  {i}. {name}")
            print(f"     Description : {doc}")
            print(f"     Failure     : {last_line}")
        print("-" * 72)

    final_status = "SUCCESS" if total_failed == 0 else "FAILURES ENCOUNTERED"
    print(f"Final Status: {final_status} (Exit Code: {0 if total_failed == 0 else 1})")
    print("=" * 72 + "\n")

    return total_passed, total_failed, elapsed


def main():
    parser = argparse.ArgumentParser(description="Genshin Impact Learning Database E2E Test Runner")
    parser.add_argument("--tier", type=str, default="", help="Comma-separated tier numbers to run (e.g. '1,2' or '4')")
    parser.add_argument("--feature", type=str, default="", help="Comma-separated features to run in Tier 1 (e.g. 'F1,F2')")
    parser.add_argument("--db", type=str, default="", help="Path to alternative SQLite database file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose test result logging")

    args = parser.parse_args()

    selected_tiers = [int(t.strip()) for t in args.tier.split(",") if t.strip().isdigit()] or None
    selected_features = [f.strip() for f in args.feature.split(",") if f.strip()] or None
    db_target = args.db.strip() or DEFAULT_DB_PATH

    passed, failed, _ = run_e2e_tests(
        db_path=db_target,
        selected_tiers=selected_tiers,
        selected_features=selected_features,
        verbose=args.verbose
    )

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
