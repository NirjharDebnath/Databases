#!/usr/bin/env python3
"""
tests/test_m2_adversarial_challenger.py
Empirical Adversarial Stress Suite for Milestone 2 (M2): Characters & Weapons Ingestion.

Author: challenger_m2_2 (Empirical Challenger)
Coverage:
- Suite 1: CSV Regeneration Determinism & Bit-for-Bit Hash Invariance
- Suite 2: Playable Characters (F5 - 16 characters, IDs 115-130) Data Integrity & Boundary Stress
- Suite 3: 5-Star Signature Weapons (F6 - 24 weapons, IDs 204-227) Integrity & Weapon-Type Compatibility
- Suite 4: Regional Craftable Weapons (F7 - 19 weapons, IDs 228-246) Ingestion & Origin Distribution
- Suite 5: Key Meta Staples & Event Weapons (F8 - 9 weapons, IDs 247-255) Data Integrity
- Suite 6: Relational Foreign Key, Schema Constraints & Orphan Verification
- Suite 7: Complex Edge Queries, Aggregations & String Escaping Stress
"""

import os
import sys
import csv
import hashlib
import sqlite3
import subprocess
from typing import Dict, List, Tuple, Any, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(PROJECT_ROOT, "genshin_learning.db")

passed_tests = 0
failed_tests = 0
findings = []

def record_pass(test_name: str, detail: str = ""):
    global passed_tests
    passed_tests += 1
    info = f" - {detail}" if detail else ""
    print(f"  [PASS] {test_name}{info}")

def record_fail(test_name: str, reason: str):
    global failed_tests
    failed_tests += 1
    findings.append((test_name, reason))
    print(f"  [FAIL] {test_name}: {reason}")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

print("=" * 80)
print("STARTING ADVERSARIAL EMPIRICAL STRESS SUITE FOR MILESTONE 2 (M2)")
print("Project Root:", PROJECT_ROOT)
print("Database Path:", DB_PATH)
print("=" * 80)

# =====================================================================
# SUITE 1: CSV REGENERATION DETERMINISM & HASH INVARIANCE
# =====================================================================
print("\n--- Suite 1: CSV Regeneration Determinism & Hash Invariance ---")

csv_files = [
    "characters.csv",
    "weapons.csv",
    "artifact_sets.csv",
    "character_builds.csv"
]

try:
    initial_hashes = {f: file_sha256(os.path.join(DATA_DIR, f)) for f in csv_files}
    record_pass("Initial CSV Hashes Computed", f"Tracked 4 files in {DATA_DIR}")

    # Run generation 1
    proc1 = subprocess.run(
        [sys.executable, os.path.join(PROJECT_ROOT, "generate_csvs.py")],
        capture_output=True, text=True, cwd=PROJECT_ROOT
    )
    if proc1.returncode != 0:
        record_fail("Run 1 generate_csvs.py Execution", proc1.stderr)
    else:
        run1_hashes = {f: file_sha256(os.path.join(DATA_DIR, f)) for f in csv_files}
        match1 = all(initial_hashes[f] == run1_hashes[f] for f in csv_files)
        if match1:
            record_pass("Run 1 Hash Invariance", "All 4 CSVs bit-for-bit identical to pre-run state")
        else:
            diffs = [f for f in csv_files if initial_hashes[f] != run1_hashes[f]]
            record_fail("Run 1 Hash Invariance", f"Drift detected in: {diffs}")

    # Run generation 2
    proc2 = subprocess.run(
        [sys.executable, os.path.join(PROJECT_ROOT, "generate_csvs.py")],
        capture_output=True, text=True, cwd=PROJECT_ROOT
    )
    if proc2.returncode != 0:
        record_fail("Run 2 generate_csvs.py Execution", proc2.stderr)
    else:
        run2_hashes = {f: file_sha256(os.path.join(DATA_DIR, f)) for f in csv_files}
        match2 = all(run1_hashes[f] == run2_hashes[f] for f in csv_files)
        if match2:
            record_pass("Run 2 Repeated Determinism", "Zero drift across successive runs")
        else:
            diffs = [f for f in csv_files if run1_hashes[f] != run2_hashes[f]]
            record_fail("Run 2 Repeated Determinism", f"Drift between runs in: {diffs}")

    # Verify newline discipline and CSV format (RFC 4180 compliant)
    for f in csv_files:
        full_path = os.path.join(DATA_DIR, f)
        with open(full_path, "rb") as raw:
            content = raw.read()
            # RFC 4180 specifies CRLF as the standard CSV line break
            if b"\r\n" in content:
                record_pass(f"Line Endings in {f}", "RFC 4180 standard CRLF line endings verified")
            elif b"\n" in content:
                record_pass(f"Line Endings in {f}", "Standard LF line endings verified")
            else:
                record_fail(f"Line Endings in {f}", "No recognized line breaks found")
            if not content.endswith(b"\n"):
                record_fail(f"Trailing Newline in {f}", "Missing final newline")
            else:
                record_pass(f"Trailing Newline in {f}", "Proper trailing newline confirmed")
except Exception as e:
    record_fail("Suite 1 Execution Exception", str(e))

# =====================================================================
# SUITE 2: PLAYABLE CHARACTERS (F5 - 16 CHARACTERS) DATA INTEGRITY
# =====================================================================
print("\n--- Suite 2: Playable Characters (F5 - 16 Characters) Data Integrity & Boundaries ---")

conn = get_connection()
cur = conn.cursor()

NEW_CHAR_SPECS = {
    115: ("Ifa", 4, "Anemo", "Catalyst", "Natlan", "Healer", 11201, 193, 655, "Skill > Burst > Normal", 5.6),
    116: ("Escoffier", 5, "Cryo", "Polearm", "Fontaine", "Sub-DPS", 12907, 337, 789, "Skill > Burst > Normal", 5.6),
    117: ("Dahlia", 4, "Hydro", "Sword", "Mondstadt", "Support", 11962, 196, 713, "Burst > Skill > Normal", 5.7),
    118: ("Skirk", 5, "Cryo", "Sword", "Outlander", "Main DPS", 13103, 349, 799, "Normal > Skill > Burst", 5.7),
    119: ("Wonderland Manekin", 5, "Anemo", "Sword", "Outlander", "Main DPS", 10875, 297, 683, "Skill = Burst > Normal", 6.1),
    120: ("Durin", 5, "Pyro", "Sword", "Mondstadt", "Main DPS", 13348, 342, 784, "Skill > Burst > Normal", 6.2),
    121: ("Varka", 5, "Anemo", "Claymore", "Mondstadt", "Main DPS", 13864, 359, 799, "Normal = Skill > Burst", 6.4),
    122: ("Nicole", 5, "Pyro", "Catalyst", "Mondstadt", "Support", 12907, 268, 696, "Burst > Skill > Normal", 6.6),
    123: ("Prune", 4, "Anemo", "Catalyst", "Nod-Krai", "Sub-DPS", 9787, 225, 628, "Skill > Burst > Normal", 6.6),
    124: ("Lohen", 5, "Cryo", "Polearm", "Nod-Krai", "Main DPS", 13103, 342, 789, "Normal > Skill > Burst", 6.6),
    125: ("Alyosha", 4, "Electro", "Polearm", "Snezhnaya", "Support", 11636, 212, 751, "Burst > Skill > Normal", 7.0),
    126: ("Odette", 5, "Cryo", "Sword", "Snezhnaya", "Sub-DPS", 12858, 337, 784, "Skill > Burst > Normal", 7.0),
    127: ("Vesna", 5, "Anemo", "Sword", "Nod-Krai", "Main DPS", 13348, 342, 807, "Normal > Skill > Burst", 7.1),
    128: ("Vodyanitsa", 5, "Hydro", "Catalyst", "Snezhnaya", "Healer", 14695, 234, 657, "Skill > Burst > Normal", 7.1),
    129: ("Mitya", 5, "Electro", "Catalyst", "Snezhnaya", "Main DPS", 12858, 342, 765, "Normal > Skill > Burst", 7.2),
    130: ("Valeriy", 4, "Electro", "Sword", "Snezhnaya", "Shielder", 12397, 202, 771, "Skill > Burst > Normal", 7.2),
}

# 1. Total character count
total_chars = cur.execute("SELECT COUNT(*) FROM characters;").fetchone()[0]
if total_chars == 129:
    record_pass("Total Character Count is 129", "129 playable characters present")
else:
    record_fail("Total Character Count", f"Expected 129, got {total_chars}")

# 2. Capitano Purge verification
cap_char = cur.execute("SELECT COUNT(*) FROM characters WHERE name = 'Capitano' OR character_id = 104;").fetchone()[0]
cap_build = cur.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = 104 OR build_id = 381;").fetchone()[0]
cap_weap = cur.execute("SELECT COUNT(*) FROM weapons WHERE signature_character_id = 104;").fetchone()[0]
if cap_char == 0 and cap_build == 0 and cap_weap == 0:
    record_pass("Capitano Purge Complete", "0 instances in characters, builds, or weapons")
else:
    record_fail("Capitano Purge", f"Found remnants: chars={cap_char}, builds={cap_build}, weap={cap_weap}")

# 3. All 16 characters exact attributes check
valid_visions = {'Pyro', 'Hydro', 'Anemo', 'Electro', 'Dendro', 'Cryo', 'Geo'}
valid_weapons = {'Sword', 'Claymore', 'Polearm', 'Bow', 'Catalyst'}
valid_roles = {'Main DPS', 'Sub-DPS', 'Support', 'Healer', 'Shielder'}

for cid, spec in NEW_CHAR_SPECS.items():
    name, exp_rarity, exp_vis, exp_wt, exp_reg, exp_role, exp_hp, exp_atk, exp_def, exp_tal, exp_patch = spec
    row = cur.execute("SELECT * FROM characters WHERE character_id = ?;", (cid,)).fetchone()
    if not row:
        record_fail(f"Character ID {cid} ({name})", "Record missing from characters table")
        continue

    mismatches = []
    if row["name"] != name: mismatches.append(f"name: {row['name']} != {name}")
    if row["rarity"] != exp_rarity: mismatches.append(f"rarity: {row['rarity']} != {exp_rarity}")
    if row["vision"] != exp_vis: mismatches.append(f"vision: {row['vision']} != {exp_vis}")
    if row["weapon_type"] != exp_wt: mismatches.append(f"weapon_type: {row['weapon_type']} != {exp_wt}")
    if row["region"] != exp_reg: mismatches.append(f"region: {row['region']} != {exp_reg}")
    if row["default_role"] != exp_role: mismatches.append(f"default_role: {row['default_role']} != {exp_role}")
    if row["base_hp"] != exp_hp: mismatches.append(f"base_hp: {row['base_hp']} != {exp_hp}")
    if row["base_atk"] != exp_atk: mismatches.append(f"base_atk: {row['base_atk']} != {exp_atk}")
    if row["base_def"] != exp_def: mismatches.append(f"base_def: {row['base_def']} != {exp_def}")
    if row["talent_priority"] != exp_tal: mismatches.append(f"talent_priority: {row['talent_priority']} != {exp_tal}")
    if abs(row["release_patch"] - exp_patch) > 0.01: mismatches.append(f"release_patch: {row['release_patch']} != {exp_patch}")

    if mismatches:
        record_fail(f"Character {name} (ID {cid}) Attributes", ", ".join(mismatches))
    else:
        record_pass(f"Character {name} (ID {cid}) Verified", f"{exp_rarity}★ {exp_vis} {exp_wt} from {exp_reg} (Patch {exp_patch})")

# 4. Characters CSV parity
with open(os.path.join(DATA_DIR, "characters.csv"), "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    csv_rows = {int(r["character_id"]): r for r in reader}

if len(csv_rows) == 129:
    record_pass("Characters CSV Row Count", "Exactly 129 records in characters.csv")
else:
    record_fail("Characters CSV Row Count", f"Expected 129, got {len(csv_rows)}")

csv_parity_ok = True
for cid, spec in NEW_CHAR_SPECS.items():
    if cid not in csv_rows:
        csv_parity_ok = False
        record_fail(f"CSV Parity ID {cid}", f"{spec[0]} missing from characters.csv")
        continue
    c = csv_rows[cid]
    if c["name"] != spec[0] or int(c["base_hp"]) != spec[6] or float(c["release_patch"]) != spec[10]:
        csv_parity_ok = False
        record_fail(f"CSV Parity ID {cid}", f"Mismatch in CSV content for {spec[0]}")
if csv_parity_ok:
    record_pass("Characters CSV 1:1 Parity", "All 16 new characters verified 1:1 between CSV and DB")

# =====================================================================
# SUITE 3: 5-STAR SIGNATURE WEAPONS (F6 - 24 WEAPONS, IDs 204-227)
# =====================================================================
print("\n--- Suite 3: 5-Star Signature Weapons (F6 - 24 Weapons) Integrity & Compatibility ---")

SIGNATURE_SPECS = {
    204: ("Calamity Queller", "Polearm", 5, 741, "ATK%", 16.5, 0, 27),
    205: ("Everlasting Moonglow", "Catalyst", 5, 608, "HP%", 49.6, 0, 44),
    206: ("Fractured Halo", "Polearm", 5, 608, "CRIT DMG", 66.2, 0, 92),
    207: ("Nightweaver's Looking Glass", "Catalyst", 5, 542, "Elemental Mastery", 265.0, 0, 93),
    208: ("Pocztowy Demonspear", "Polearm", 5, 674, "CRIT Rate", 22.1, 0, 94),
    209: ("Reliquary of Truth", "Catalyst", 5, 542, "CRIT DMG", 88.2, 0, 96),
    210: ("Lightbearing Moonshard", "Sword", 5, 542, "CRIT DMG", 88.2, 0, 99),
    211: ("Golden Frostbound Oath", "Bow", 5, 542, "CRIT DMG", 88.2, 0, 100),
    212: ("Nocturne's Curtain Call", "Catalyst", 5, 542, "CRIT DMG", 88.2, 0, 102),
    213: ("A Teaspoon of Transcendence", "Claymore", 5, 674, "CRIT Rate", 22.1, 0, 103),
    214: ("Sunny Morning Sleep-In", "Catalyst", 5, 542, "Elemental Mastery", 265.0, 0, 107),
    215: ("Vivid Notions", "Catalyst", 5, 674, "CRIT DMG", 44.1, 0, 108),
    216: ("Symphonist of Scents", "Polearm", 5, 608, "CRIT DMG", 66.2, 0, 116),
    217: ("Azurelight", "Sword", 5, 674, "CRIT Rate", 22.1, 0, 118),
    218: ("Athame Artis", "Sword", 5, 608, "CRIT Rate", 33.1, 0, 120),
    219: ("Gest of the Mighty Wolf", "Claymore", 5, 608, "CRIT Rate", 33.1, 0, 121),
    220: ("Angelos' Heptades", "Catalyst", 5, 741, "ATK%", 16.5, 0, 122),
    221: ("Disaster and Remorse", "Polearm", 5, 674, "CRIT Rate", 22.1, 0, 124),
    222: ("Whitelake Frostfeather", "Sword", 5, 608, "CRIT DMG", 66.2, 0, 126),
    223: ("Beyond the Chrysalis", "Sword", 5, 674, "CRIT DMG", 44.1, 0, 127),
    224: ("Hymn of the Maelstrom", "Catalyst", 5, 608, "HP%", 49.6, 0, 128),
    225: ("Starsealed Edict", "Catalyst", 5, 674, "CRIT Rate", 22.1, 0, 129),
    226: ("Exaiphanes Blade", "Sword", 5, 608, "CRIT Rate", 33.1, 0, 114),
    227: ("Miliastra Sovereign", "Sword", 5, 608, "CRIT DMG", 66.2, 0, 119),
}

# 1. Verify exact 24 signature attributes and weapon-type compatibility with character
type_mismatches = []
attr_mismatches = []

for wid, spec in SIGNATURE_SPECS.items():
    wname, exp_wt, exp_rarity, exp_atk, exp_sub_type, exp_sub_val, exp_craft, exp_char_id = spec
    row = cur.execute("SELECT * FROM weapons WHERE weapon_id = ?;", (wid,)).fetchone()
    if not row:
        attr_mismatches.append(f"Weapon ID {wid} ({wname}) missing from weapons table")
        continue

    if row["name"] != wname: attr_mismatches.append(f"ID {wid} name {row['name']} != {wname}")
    if row["weapon_type"] != exp_wt: attr_mismatches.append(f"ID {wid} type {row['weapon_type']} != {exp_wt}")
    if row["rarity"] != exp_rarity: attr_mismatches.append(f"ID {wid} rarity {row['rarity']} != {exp_rarity}")
    if row["base_atk"] != exp_atk: attr_mismatches.append(f"ID {wid} base_atk {row['base_atk']} != {exp_atk}")
    if row["sub_stat_type"] != exp_sub_type: attr_mismatches.append(f"ID {wid} sub_stat_type {row['sub_stat_type']} != {exp_sub_type}")
    if abs(row["sub_stat_value"] - exp_sub_val) > 0.01: attr_mismatches.append(f"ID {wid} sub_stat_val {row['sub_stat_value']} != {exp_sub_val}")
    if row["is_craftable"] != exp_craft: attr_mismatches.append(f"ID {wid} is_craftable {row['is_craftable']} != {exp_craft}")
    if row["signature_character_id"] != exp_char_id: attr_mismatches.append(f"ID {wid} sig_char {row['signature_character_id']} != {exp_char_id}")

    # Check weapon type compatibility with character
    char_row = cur.execute("SELECT weapon_type, name FROM characters WHERE character_id = ?;", (exp_char_id,)).fetchone()
    if not char_row:
        type_mismatches.append(f"Signature weapon {wname} links to non-existent character ID {exp_char_id}")
    elif char_row["weapon_type"] != exp_wt:
        type_mismatches.append(f"Weapon type mismatch: {wname} is {exp_wt} but character {char_row['name']} uses {char_row['weapon_type']}")

if attr_mismatches:
    record_fail("24 Signature Weapons Attributes", "; ".join(attr_mismatches[:5]))
else:
    record_pass("24 Signature Weapons Attributes", "All 24 signature weapon attributes match specification")

if type_mismatches:
    record_fail("Signature Weapon Type Compatibility", "; ".join(type_mismatches))
else:
    record_pass("Signature Weapon Type Compatibility", "100% of 24 signatures match character weapon_type exactly")

# =====================================================================
# SUITE 4: REGIONAL CRAFTABLES (F7 - 19 WEAPONS, IDs 228-246)
# =====================================================================
print("\n--- Suite 4: Regional Craftables (F7 - 19 Weapons) Origin Distribution ---")

CRAFTABLE_SPECS = {
    # Dragonspine (3)
    228: ("Snow-Tombed Starsilver", "Claymore", 4, 565, "Physical DMG", 34.5, "Dragonspine"),
    229: ("Dragonspine Spear", "Polearm", 4, 454, "Physical DMG", 69.0, "Dragonspine"),
    230: ("Frostbearer", "Catalyst", 4, 510, "ATK%", 41.3, "Dragonspine"),
    # Sumeru (4)
    231: ("Forest Regalia", "Claymore", 4, 565, "Energy Recharge", 30.6, "Sumeru"),
    232: ("Moonpiercer", "Polearm", 4, 565, "Elemental Mastery", 110.0, "Sumeru"),
    233: ("King's Squire", "Bow", 4, 454, "ATK%", 55.1, "Sumeru"),
    234: ("Fruit of Fulfillment", "Catalyst", 4, 510, "Energy Recharge", 45.9, "Sumeru"),
    # Fontaine (2)
    235: ("Song of Stillness", "Bow", 4, 510, "ATK%", 41.3, "Fontaine"),
    236: ("Flowing Purity", "Catalyst", 4, 565, "ATK%", 27.6, "Fontaine"),
    # Nod-Krai (5)
    237: ("Serenity's Call", "Sword", 4, 454, "Energy Recharge", 61.3, "Nod-Krai"),
    238: ("Master Key", "Claymore", 4, 454, "Energy Recharge", 61.3, "Nod-Krai"),
    239: ("Prospector's Shovel", "Polearm", 4, 510, "ATK%", 41.3, "Nod-Krai"),
    240: ("Snare Hook", "Bow", 4, 454, "Energy Recharge", 61.3, "Nod-Krai"),
    241: ("Blackmarrow Lantern", "Catalyst", 4, 454, "Elemental Mastery", 221.0, "Nod-Krai"),
    # Snezhnaya (5)
    242: ("Emberwell", "Sword", 4, 510, "Elemental Mastery", 165.0, "Snezhnaya"),
    243: ("Blade of Atonement", "Claymore", 4, 565, "ATK%", 27.6, "Snezhnaya"),
    244: ("Song of the Vigil", "Polearm", 4, 565, "Elemental Mastery", 110.0, "Snezhnaya"),
    245: ("Covenant of Frost and Snow", "Bow", 4, 510, "DEF%", 51.7, "Snezhnaya"),
    246: ("Echoes of the Heart", "Catalyst", 4, 565, "ATK%", 27.6, "Snezhnaya"),
}

craft_mismatches = []
regional_craft_counts = {"Dragonspine": 0, "Sumeru": 0, "Fontaine": 0, "Nod-Krai": 0, "Snezhnaya": 0}
craft_weapon_types = set()

for wid, spec in CRAFTABLE_SPECS.items():
    wname, exp_wt, exp_rarity, exp_atk, exp_sub_type, exp_sub_val, region = spec
    regional_craft_counts[region] += 1
    craft_weapon_types.add(exp_wt)
    row = cur.execute("SELECT * FROM weapons WHERE weapon_id = ?;", (wid,)).fetchone()
    if not row:
        craft_mismatches.append(f"Craftable weapon ID {wid} ({wname}) missing")
        continue

    if row["name"] != wname: craft_mismatches.append(f"ID {wid} name mismatch: {row['name']} != {wname}")
    if row["is_craftable"] != 1: craft_mismatches.append(f"ID {wid} {wname} is_craftable != 1")
    if row["rarity"] != 4: craft_mismatches.append(f"ID {wid} {wname} rarity != 4")
    if row["signature_character_id"] is not None: craft_mismatches.append(f"ID {wid} {wname} signature_character_id IS NOT NULL")
    if row["weapon_type"] != exp_wt: craft_mismatches.append(f"ID {wid} {wname} type != {exp_wt}")
    if row["base_atk"] != exp_atk: craft_mismatches.append(f"ID {wid} {wname} base_atk != {exp_atk}")
    if row["sub_stat_type"] != exp_sub_type: craft_mismatches.append(f"ID {wid} {wname} sub_stat_type != {exp_sub_type}")
    if abs(row["sub_stat_value"] - exp_sub_val) > 0.01: craft_mismatches.append(f"ID {wid} {wname} sub_stat_value != {exp_sub_val}")

if craft_mismatches:
    record_fail("19 Craftable Weapons Specifications", "; ".join(craft_mismatches[:5]))
else:
    record_pass("19 Craftable Weapons Specifications", "All 19 craftables verified (is_craftable=1, rarity=4, sig=NULL)")

# Regional breakdown
exp_regional = {"Dragonspine": 3, "Sumeru": 4, "Fontaine": 2, "Nod-Krai": 5, "Snezhnaya": 5}
if regional_craft_counts == exp_regional:
    record_pass("Craftables Regional Distribution", f"Confirmed: Dragonspine=3, Sumeru=4, Fontaine=2, Nod-Krai=5, Snezhnaya=5")
else:
    record_fail("Craftables Regional Distribution", f"Expected {exp_regional}, got {regional_craft_counts}")

if craft_weapon_types == valid_weapons:
    record_pass("Craftables All 5 Weapon Types Present", "Sword, Claymore, Polearm, Bow, Catalyst all covered")
else:
    record_fail("Craftables All 5 Weapon Types", f"Missing types: {valid_weapons - craft_weapon_types}")

# =====================================================================
# SUITE 5: KEY META STAPLES & EVENT WEAPONS (F8 - 9 WEAPONS, IDs 247-255)
# =====================================================================
print("\n--- Suite 5: Key Meta Staples & Event Weapons (F8 - 9 Weapons) ---")

STAPLE_SPECS = {
    247: ("Fleuve Cendre Ferryman", "Sword", 4, 510, "Energy Recharge", 45.9, 0, None),
    248: ("The Stringless", "Bow", 4, 510, "Elemental Mastery", 165.0, 0, None),
    249: ("Cinnabar Spindle", "Sword", 4, 454, "DEF%", 69.0, 0, 6),
    250: ("Mountain-Bracing Bolt", "Polearm", 4, 565, "Energy Recharge", 30.6, 0, None),
    251: ("Sturdy Bone", "Sword", 4, 565, "ATK%", 27.6, 0, None),
    252: ("Fruitful Hook", "Claymore", 4, 565, "ATK%", 27.6, 0, None),
    253: ("Flower-Wreathed Feathers", "Bow", 4, 510, "ATK%", 41.3, 0, None),
    254: ("Waveriding Whirl", "Catalyst", 4, 454, "Energy Recharge", 61.3, 0, None),
    255: ("Calamity of Eshu", "Sword", 4, 510, "ATK%", 41.3, 0, None),
}

staple_mismatches = []
for wid, spec in STAPLE_SPECS.items():
    wname, exp_wt, exp_rarity, exp_atk, exp_sub_type, exp_sub_val, exp_craft, exp_sig = spec
    row = cur.execute("SELECT * FROM weapons WHERE weapon_id = ?;", (wid,)).fetchone()
    if not row:
        staple_mismatches.append(f"Staple weapon ID {wid} ({wname}) missing")
        continue

    if row["name"] != wname: staple_mismatches.append(f"ID {wid} name mismatch: {row['name']} != {wname}")
    if row["weapon_type"] != exp_wt: staple_mismatches.append(f"ID {wid} type != {exp_wt}")
    if row["rarity"] != exp_rarity: staple_mismatches.append(f"ID {wid} rarity != {exp_rarity}")
    if row["base_atk"] != exp_atk: staple_mismatches.append(f"ID {wid} base_atk != {exp_atk}")
    if row["sub_stat_type"] != exp_sub_type: staple_mismatches.append(f"ID {wid} sub_stat_type != {exp_sub_type}")
    if abs(row["sub_stat_value"] - exp_sub_val) > 0.01: staple_mismatches.append(f"ID {wid} sub_stat_value != {exp_sub_val}")
    if row["is_craftable"] != exp_craft: staple_mismatches.append(f"ID {wid} is_craftable != {exp_craft}")
    if row["signature_character_id"] != exp_sig: staple_mismatches.append(f"ID {wid} signature != {exp_sig}")

if staple_mismatches:
    record_fail("9 Meta Staples Specifications", "; ".join(staple_mismatches))
else:
    record_pass("9 Meta Staples Specifications", "All 9 staples verified (Cinnabar Spindle->Albedo, Ferryman, Stringless, Natlan series)")

# Specifically verify Albedo signature linkage
albedo_row = cur.execute("""
    SELECT w.name as weapon_name, w.sub_stat_type, w.sub_stat_value, c.name as char_name, c.vision, c.weapon_type
    FROM weapons w
    JOIN characters c ON w.signature_character_id = c.character_id
    WHERE w.weapon_id = 249;
""").fetchone()
if albedo_row and albedo_row["char_name"] == "Albedo" and albedo_row["sub_stat_type"] == "DEF%":
    record_pass("Cinnabar Spindle Albedo Signature Linkage", "Correctly linked to Albedo (Geo Sword)")
else:
    record_fail("Cinnabar Spindle Albedo Signature Linkage", f"Unexpected result: {dict(albedo_row) if albedo_row else None}")

# =====================================================================
# SUITE 6: RELATIONAL FOREIGN KEYS & SCHEMA CONSTRAINTS
# =====================================================================
print("\n--- Suite 6: Relational Foreign Keys, Schema Constraints & Orphan Verification ---")

# 1. PRAGMA foreign_key_check
fk_check = cur.execute("PRAGMA foreign_key_check;").fetchall()
if len(fk_check) == 0:
    record_pass("PRAGMA foreign_key_check", "0 foreign key violations across the entire database")
else:
    record_fail("PRAGMA foreign_key_check", f"{len(fk_check)} violations: {fk_check}")

# 2. Total table counts
total_weapons = cur.execute("SELECT COUNT(*) FROM weapons;").fetchone()[0]
if total_weapons == 155:
    record_pass("Total Weapons Count is 155", "Exactly 155 weapons in database")
else:
    record_fail("Total Weapons Count", f"Expected 155, got {total_weapons}")

total_chars = cur.execute("SELECT COUNT(*) FROM characters;").fetchone()[0]
if total_chars == 129:
    record_pass("Total Characters Count is 129", "Exactly 129 characters in database")
else:
    record_fail("Total Characters Count", f"Expected 129, got {total_chars}")

# 3. Weapons ID sequence and gaps check
weapon_ids = [r[0] for r in cur.execute("SELECT weapon_id FROM weapons ORDER BY weapon_id;").fetchall()]
expected_weapon_ids = list(range(101, 256))
if weapon_ids == expected_weapon_ids:
    record_pass("Weapons Primary Key Contiguity", "IDs strictly contiguous from 101 to 255 with 0 gaps")
else:
    record_fail("Weapons Primary Key Contiguity", f"ID mismatch: len={len(weapon_ids)}, min={min(weapon_ids)}, max={max(weapon_ids)}")

# 4. Weapons Name Uniqueness
dup_weapon_names = cur.execute("""
    SELECT name, COUNT(*) FROM weapons GROUP BY name HAVING COUNT(*) > 1;
""").fetchall()
if len(dup_weapon_names) == 0:
    record_pass("Weapons Name Uniqueness", "All 155 weapon names are distinct")
else:
    record_fail("Weapons Name Uniqueness", f"Duplicate weapon names found: {dup_weapon_names}")

# 5. Characters Name Uniqueness
dup_char_names = cur.execute("""
    SELECT name, COUNT(*) FROM characters GROUP BY name HAVING COUNT(*) > 1;
""").fetchall()
if len(dup_char_names) == 0:
    record_pass("Characters Name Uniqueness", "All 129 character names are distinct")
else:
    record_fail("Characters Name Uniqueness", f"Duplicate character names found: {dup_char_names}")

# 6. Orphan Check: weapons pointing to non-existent characters
orphaned_sigs = cur.execute("""
    SELECT w.weapon_id, w.name, w.signature_character_id
    FROM weapons w
    LEFT JOIN characters c ON w.signature_character_id = c.character_id
    WHERE w.signature_character_id IS NOT NULL AND c.character_id IS NULL;
""").fetchall()
if len(orphaned_sigs) == 0:
    record_pass("Orphan Check: Signature Weapons", "Zero weapons reference non-existent character IDs")
else:
    record_fail("Orphan Check: Signature Weapons", f"Found orphaned signature references: {orphaned_sigs}")

# =====================================================================
# SUITE 7: COMPLEX EDGE QUERIES, AGGREGATIONS & STRING ESCAPING
# =====================================================================
print("\n--- Suite 7: Complex Edge Queries, Aggregations & String Escaping ---")

# 1. Craftables vs Non-craftables Aggregation
agg_query = cur.execute("""
    SELECT 
        is_craftable,
        COUNT(*) as total_count,
        ROUND(AVG(base_atk), 2) as avg_atk,
        MIN(base_atk) as min_atk,
        MAX(base_atk) as max_atk,
        COUNT(signature_character_id) as sig_count
    FROM weapons
    GROUP BY is_craftable
    ORDER BY is_craftable;
""").fetchall()

craft_summary = {r["is_craftable"]: dict(r) for r in agg_query}
if craft_summary.get(1, {}).get("total_count") == 43 and craft_summary.get(1, {}).get("sig_count") == 0:
    record_pass("Craftable Aggregation Edge Query", "43 craftables with exactly 0 signatures")
else:
    record_fail("Craftable Aggregation Edge Query", f"Unexpected craftable summary: {craft_summary.get(1)}")

if craft_summary.get(0, {}).get("total_count") == 112 and craft_summary.get(0, {}).get("sig_count") == 65:
    record_pass("Non-Craftable Aggregation Edge Query", "112 non-craftables with exactly 65 signatures")
else:
    record_fail("Non-Craftable Aggregation Edge Query", f"Unexpected non-craftable summary: {craft_summary.get(0)}")

# 2. Regional Weapon Distribution & Character Cross-Analysis
reg_dist = cur.execute("""
    SELECT 
        c.region,
        COUNT(DISTINCT c.character_id) as char_count,
        COUNT(w.weapon_id) as sig_weapons_count
    FROM characters c
    LEFT JOIN weapons w ON c.character_id = w.signature_character_id
    GROUP BY c.region
    ORDER BY char_count DESC, c.region ASC;
""").fetchall()

reg_counts_dict = {r["region"]: r["char_count"] for r in reg_dist}
expected_regions = {
    "Mondstadt": 23, "Liyue": 22, "Inazuma": 17, "Sumeru": 14,
    "Fontaine": 13, "Nod-Krai": 12, "Natlan": 11, "Outlander": 8,
    "Snezhnaya": 8, "None": 1
}
if reg_counts_dict == expected_regions:
    record_pass("Full Regional Character Distribution", f"All 10 regions match exact targets (total {sum(reg_counts_dict.values())})")
else:
    record_fail("Full Regional Character Distribution", f"Expected {expected_regions}, got {reg_counts_dict}")

# 3. Signature Weapon Sub-stat Type Distribution
sub_stat_dist = cur.execute("""
    SELECT sub_stat_type, COUNT(*) as count
    FROM weapons
    WHERE signature_character_id IS NOT NULL
    GROUP BY sub_stat_type
    ORDER BY count DESC;
""").fetchall()
sub_stat_dict = {r["sub_stat_type"]: r["count"] for r in sub_stat_dist}
major_substats = {"CRIT Rate", "CRIT DMG", "ATK%", "HP%", "Energy Recharge", "Elemental Mastery", "DEF%"}
if major_substats.issubset(sub_stat_dict.keys()):
    record_pass("Signature Sub-Stat Variety", f"All major sub-stats present in signatures: {sub_stat_dict}")
else:
    record_fail("Signature Sub-Stat Variety", f"Missing sub-stats: {major_substats - set(sub_stat_dict.keys())}")

# 4. Highest Base ATK Weapons Query (741 ATK tier)
high_atk = cur.execute("""
    SELECT w.weapon_id, w.name, w.weapon_type, w.rarity, c.name as char_name
    FROM weapons w
    LEFT JOIN characters c ON w.signature_character_id = c.character_id
    WHERE w.base_atk = 741
    ORDER BY w.weapon_id;
""").fetchall()

high_atk_names = {r["name"] for r in high_atk}
expected_741_subset = {
    "Calamity Queller", "Angelos' Heptades", "Fang of the Mountain King",
    "A Thousand Blazing Suns", "Song of Broken Pines", "Crane's Echoing Call"
}
if expected_741_subset.issubset(high_atk_names):
    record_pass("741 Base ATK Weapons Tier", f"Verified high ATK weapons ({len(high_atk)} total in 741 tier: {high_atk_names})")
else:
    record_fail("741 Base ATK Weapons Tier", f"Missing from 741 tier: {expected_741_subset - high_atk_names}")

# 5. String Escaping & Special Characters Query
special_names = [
    "King's Squire",
    "Nightweaver's Looking Glass",
    "Nocturne's Curtain Call",
    "Angelos' Heptades",
    "Serenity's Call",
    "Surf's Up",
    "Starcaller's Watch",
    "Amos' Bow",
    "Hunter's Path",
    "Wolf's Gravestone"
]
escaping_ok = True
for name in special_names:
    row = cur.execute("SELECT weapon_id, name, base_atk FROM weapons WHERE name = ?;", (name,)).fetchone()
    if not row or row["name"] != name:
        escaping_ok = False
        record_fail(f"Special Character Lookup: {name}", "Failed to retrieve by parameterized query")
if escaping_ok:
    record_pass("String Escaping & Parameterized Queries", f"All {len(special_names)} weapons with apostrophes successfully queried")

# 6. CTE and Window Function Stress: Regional Top Weapon by Base ATK
cte_res = cur.execute("""
    WITH RankedWeapons AS (
        SELECT 
            w.weapon_id,
            w.name as weapon_name,
            w.base_atk,
            c.name as char_name,
            c.region,
            DENSE_RANK() OVER (PARTITION BY c.region ORDER BY w.base_atk DESC) as rk
        FROM weapons w
        JOIN characters c ON w.signature_character_id = c.character_id
    )
    SELECT region, rk, char_name, weapon_name, base_atk
    FROM RankedWeapons
    WHERE rk = 1
    ORDER BY region;
""").fetchall()

if len(cte_res) >= 7:
    record_pass("Complex Window Function CTE Query", f"Successfully ranked signature weapons across {len(cte_res)} regional entries")
else:
    record_fail("Complex Window Function CTE Query", f"Expected >= 7 regional entries, got {len(cte_res)}")

conn.close()

# =====================================================================
# SUMMARY & FINAL VERDICT
# =====================================================================
print("\n" + "=" * 80)
print("TEST EXECUTION SUMMARY")
print("=" * 80)
print(f"Total Tests Run : {passed_tests + failed_tests}")
print(f"Total Passed    : {passed_tests}")
print(f"Total Failed    : {failed_tests}")

if failed_tests > 0:
    print("\nFAILURES ENCOUNTERED:")
    for name, reason in findings:
        print(f" - {name}: {reason}")
    print("\nOVERALL VERDICT: REJECT")
    sys.exit(1)
else:
    print("\nALL EMPIRICAL TESTS PASSED WITH ZERO DEFECTS!")
    print("OVERALL VERDICT: APPROVE")
    sys.exit(0)
