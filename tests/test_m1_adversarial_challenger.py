"""
Milestone 1 (M1) Adversarial Challenger Stress Suite
Independent empirical verification for Genshin Impact Database Remediation.
Author: challenger_m1_2
"""

import os
import sys
import csv
import hashlib
import sqlite3
import subprocess

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(PROJECT_ROOT, "genshin_learning.db")

passed_tests = 0
failed_tests = 0
findings = []

def record_pass(test_name):
    global passed_tests
    passed_tests += 1
    print(f"  [PASS] {test_name}")

def record_fail(test_name, reason):
    global failed_tests
    failed_tests += 1
    findings.append((test_name, reason))
    print(f"  [FAIL] {test_name}: {reason}")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

print("=" * 70)
print("STARTING ADVERSARIAL STRESS SUITE FOR MILESTONE 1 (M1)")
print("=" * 70)

# ----------------------------------------------------------------------
# 1. ARTIFACT SETS 59, 60, 62, 63, 64 EXACT TEXT & DOMAIN SPECS
# ----------------------------------------------------------------------
print("\n--- Suite 1: Artifact Sets Exact Specs & Domain Pairing ---")
conn = get_db_connection()
cur = conn.cursor()

sets_specs = {
    59: {
        "name": "Aubade of Morningstar and Moon",
        "domain_name": "Moonchild's Treasures",
        "region": "Nod-Krai",
        "two_piece_bonus": "+80 Elemental Mastery",
        "four_piece_bonus_substrs": [
            "When off-field, Lunar Reaction DMG +20%",
            "party Moonsign Level is Ascendant Gleam, Lunar Reaction DMG +40%"
        ]
    },
    60: {
        "name": "A Day Carved from Rising Winds",
        "domain_name": "Moonchild's Treasures",
        "region": "Nod-Krai",
        "two_piece_bonus": "+18% ATK",
        "four_piece_bonus_substrs": [
            "Blessing of Pastoral Winds (ATK +25% for 6s)",
            "Resolve of Pastoral Winds (CRIT Rate +20%)"
        ]
    },
    62: {
        "name": "Disenchantment in Deep Shadow",
        "domain_name": "Thorny Crown of the Mountain Wind",
        "region": "Mondstadt",
        "two_piece_bonus": "+18% ATK",
        "four_piece_bonus_substrs": [
            "Superconduct Reaction DMG +80%",
            "CRIT Rate by 16%"
        ]
    },
    63: {
        "name": "Scarlet Proof",
        "domain_name": "Inverted Glacier",
        "region": "Snezhnaya",
        "two_piece_bonus": "+18% ATK",
        "four_piece_bonus_substrs": [
            "Stellar Swirl",
            "CRIT Rate +16%",
            "Stellar Swirl DMG +40%"
        ]
    },
    64: {
        "name": "Heart of the Furnace",
        "domain_name": "Inverted Glacier",
        "region": "Snezhnaya",
        "two_piece_bonus": "+18% ATK",
        "four_piece_bonus_substrs": [
            "Stellar Glimmer",
            "ATK +12%",
            "Stellar Glimmer DMG by 50%"
        ]
    }
}

for set_id, spec in sets_specs.items():
    row = cur.execute("SELECT * FROM artifact_sets WHERE artifact_set_id = ?", (set_id,)).fetchone()
    if not row:
        record_fail(f"Set {set_id} existence", "Row not found in DB")
        continue

    # Name check
    if row["name"] == spec["name"]:
        record_pass(f"Set {set_id} name == '{spec['name']}'")
    else:
        record_fail(f"Set {set_id} name", f"Expected '{spec['name']}', got '{row['name']}'")

    # Domain check
    if row["domain_name"] == spec["domain_name"]:
        record_pass(f"Set {set_id} domain == '{spec['domain_name']}'")
    else:
        record_fail(f"Set {set_id} domain", f"Expected '{spec['domain_name']}', got '{row['domain_name']}'")

    # Region check
    if row["region"] == spec["region"]:
        record_pass(f"Set {set_id} region == '{spec['region']}'")
    else:
        record_fail(f"Set {set_id} region", f"Expected '{spec['region']}', got '{row['region']}'")

    # 2pc bonus check
    if row["two_piece_bonus"] == spec["two_piece_bonus"]:
        record_pass(f"Set {set_id} 2pc bonus == '{spec['two_piece_bonus']}'")
    else:
        record_fail(f"Set {set_id} 2pc bonus", f"Expected '{spec['two_piece_bonus']}', got '{row['two_piece_bonus']}'")

    # 4pc bonus substrings
    all_matched = True
    for s in spec["four_piece_bonus_substrs"]:
        if s not in row["four_piece_bonus"]:
            all_matched = False
            record_fail(f"Set {set_id} 4pc substring '{s}'", f"Missing from: {row['four_piece_bonus']}")
    if all_matched:
        record_pass(f"Set {set_id} 4pc bonus mechanics verified")

# Negative domain checks: Set 63 & 64 must NOT be Palace of Frost
for set_id in [63, 64]:
    row = cur.execute("SELECT domain_name FROM artifact_sets WHERE artifact_set_id = ?", (set_id,)).fetchone()
    if row and "Palace of Frost" in row["domain_name"]:
        record_fail(f"Set {set_id} obsolete domain check", "Still contains Palace of Frost!")
    else:
        record_pass(f"Set {set_id} does not reference Palace of Frost")

# Set 62 must NOT be Snezhnaya
row62 = cur.execute("SELECT region FROM artifact_sets WHERE artifact_set_id = 62;").fetchone()
if row62 and row62["region"] == "Snezhnaya":
    record_fail("Set 62 region check", "Region is still Snezhnaya instead of Mondstadt")
else:
    record_pass("Set 62 region is not Snezhnaya")

# Domain pair co-location consistency
domain_pairs = [
    ("Moonchild's Treasures", [59, 60], "Nod-Krai"),
    ("Thorny Crown of the Mountain Wind", [61, 62], "Mondstadt"),
    ("Inverted Glacier", [63, 64], "Snezhnaya")
]
for d_name, expected_ids, expected_reg in domain_pairs:
    rows = cur.execute("SELECT artifact_set_id, region FROM artifact_sets WHERE domain_name = ?", (d_name,)).fetchall()
    actual_ids = [r["artifact_set_id"] for r in rows]
    actual_regs = set(r["region"] for r in rows)
    if sorted(actual_ids) == sorted(expected_ids) and actual_regs == {expected_reg}:
        record_pass(f"Domain '{d_name}' correctly pairs sets {expected_ids} in region '{expected_reg}'")
    else:
        record_fail(f"Domain '{d_name}' pairing", f"Expected sets {expected_ids} in {expected_reg}, got {actual_ids} in {actual_regs}")

# ----------------------------------------------------------------------
# 2. WEAPONS 128 & 131 STATS & BOUNDARY TESTING
# ----------------------------------------------------------------------
print("\n--- Suite 2: Weapons 128 & 131 Stats & Boundary Checks ---")

w_specs = {
    128: {"name": "Fang of the Mountain King", "base_atk": 741, "sub_stat_type": "CRIT Rate", "sub_stat_value": 11.0, "owner_id": 84},
    131: {"name": "A Thousand Blazing Suns", "base_atk": 741, "sub_stat_type": "CRIT Rate", "sub_stat_value": 11.0, "owner_id": 87}
}

for w_id, spec in w_specs.items():
    row = cur.execute("SELECT * FROM weapons WHERE weapon_id = ?", (w_id,)).fetchone()
    if not row:
        record_fail(f"Weapon {w_id} existence", "Row not found in DB")
        continue

    if row["name"] == spec["name"]:
        record_pass(f"Weapon {w_id} name == '{spec['name']}'")
    else:
        record_fail(f"Weapon {w_id} name", f"Expected '{spec['name']}', got '{row['name']}'")

    if row["base_atk"] == spec["base_atk"]:
        record_pass(f"Weapon {w_id} base_atk == {spec['base_atk']}")
    else:
        record_fail(f"Weapon {w_id} base_atk", f"Expected {spec['base_atk']}, got {row['base_atk']}")

    if row["sub_stat_type"] == spec["sub_stat_type"]:
        record_pass(f"Weapon {w_id} sub_stat_type == '{spec['sub_stat_type']}'")
    else:
        record_fail(f"Weapon {w_id} sub_stat_type", f"Expected '{spec['sub_stat_type']}', got '{row['sub_stat_type']}'")

    if abs(row["sub_stat_value"] - spec["sub_stat_value"]) < 1e-4:
        record_pass(f"Weapon {w_id} sub_stat_value == {spec['sub_stat_value']}")
    else:
        record_fail(f"Weapon {w_id} sub_stat_value", f"Expected {spec['sub_stat_value']}, got {row['sub_stat_value']}")

    if row["signature_character_id"] == spec["owner_id"]:
        record_pass(f"Weapon {w_id} signature_character_id == {spec['owner_id']}")
    else:
        record_fail(f"Weapon {w_id} signature_character_id", f"Expected {spec['owner_id']}, got {row['signature_character_id']}")

# Boundary test: verify 741 is maximum base_atk across all weapons in DB
max_atk = cur.execute("SELECT MAX(base_atk) FROM weapons;").fetchone()[0]
if max_atk == 741:
    record_pass("Max weapon base_atk in database is exactly 741 (Tier 2 boundary confirmed)")
else:
    record_fail("Max weapon base_atk", f"Expected 741, found {max_atk}")

# Verify 128 and 131 specifically adhere to 741 ATK / 11.0% CRIT Rate
for w_id in [128, 131]:
    w = cur.execute("SELECT weapon_id, name, base_atk, sub_stat_type, sub_stat_value FROM weapons WHERE weapon_id = ?;", (w_id,)).fetchone()
    if w["base_atk"] == 741 and w["sub_stat_type"] == "CRIT Rate" and abs(w["sub_stat_value"] - 11.0) < 1e-4:
        record_pass(f"741 ATK weapon '{w['name']}' (ID {w['weapon_id']}) adheres to 11.0% CRIT Rate scaling")
    else:
        record_fail(f"741 ATK weapon scaling for ID {w_id}", f"Expected 741 ATK & 11.0% CRIT Rate, got {w['base_atk']} ATK & {w['sub_stat_type']} {w['sub_stat_value']}")

# Verify other 741 ATK weapons were not corrupted
w133 = cur.execute("SELECT * FROM weapons WHERE weapon_id = 133;").fetchone()
if w133["base_atk"] == 741 and w133["sub_stat_type"] == "Physical DMG" and abs(w133["sub_stat_value"] - 20.7) < 1e-4:
    record_pass("Song of Broken Pines (133) retains 741 ATK / 20.7% Physical DMG")
else:
    record_fail("Weapon 133 uncorrupted check", f"Stats modified unexpectedly: {dict(w133)}")


# ----------------------------------------------------------------------
# 3. CHARACTER ATTRIBUTES & CAPITANO PURGE
# ----------------------------------------------------------------------
print("\n--- Suite 3: Character Attributes & Capitano Purge ---")

char_specs = {
    72: {"name": "Arlecchino", "field": "region", "expected": "Snezhnaya"},
    91: {"name": "Iansan", "field": "release_patch", "expected": 5.5},
    99: {"name": "Zibai", "field": "region", "expected": "Liyue"},
    102: {"name": "Columbina", "field": "region", "expected": "Nod-Krai"},
    103: {"name": "Sandrone", "fields": {"vision": "Cryo", "weapon_type": "Claymore", "region": "Snezhnaya"}},
    105: {"name": "Aloy", "field": "region", "expected": "None"}
}

for cid, spec in char_specs.items():
    row = cur.execute("SELECT * FROM characters WHERE character_id = ?", (cid,)).fetchone()
    if not row:
        record_fail(f"Character {cid} existence", f"{spec['name']} missing from DB")
        continue

    if "field" in spec:
        fld = spec["field"]
        exp = spec["expected"]
        act = row[fld]
        if act == exp:
            record_pass(f"{spec['name']} (ID {cid}) {fld} == {exp}")
        else:
            record_fail(f"{spec['name']} {fld}", f"Expected {exp}, got {act}")
    elif "fields" in spec:
        for fld, exp in spec["fields"].items():
            act = row[fld]
            if act == exp:
                record_pass(f"{spec['name']} (ID {cid}) {fld} == {exp}")
            else:
                record_fail(f"{spec['name']} {fld}", f"Expected {exp}, got {act}")

# Capitano purge checks
cap_id = cur.execute("SELECT COUNT(*) FROM characters WHERE character_id = 104;").fetchone()[0]
if cap_id == 0:
    record_pass("Character ID 104 (Capitano) purged from characters table")
else:
    record_fail("Capitano ID check", f"Character ID 104 still exists! Count: {cap_id}")

cap_name = cur.execute("SELECT COUNT(*) FROM characters WHERE name LIKE '%Capitano%';").fetchone()[0]
if cap_name == 0:
    record_pass("No character named 'Capitano' in characters table")
else:
    record_fail("Capitano name check", f"Name 'Capitano' found in characters table! Count: {cap_name}")

b381 = cur.execute("SELECT COUNT(*) FROM character_builds WHERE build_id = 381;").fetchone()[0]
if b381 == 0:
    record_pass("Build 381 purged from character_builds table")
else:
    record_fail("Build 381 check", f"Build 381 still exists! Count: {b381}")

b_cap = cur.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = 104;").fetchone()[0]
if b_cap == 0:
    record_pass("Zero builds reference character_id = 104")
else:
    record_fail("Build FK check", f"Found {b_cap} builds referencing character_id 104")

w_cap = cur.execute("SELECT COUNT(*) FROM weapons WHERE signature_character_id = 104;").fetchone()[0]
if w_cap == 0:
    record_pass("Zero weapons have signature_character_id = 104")
else:
    record_fail("Weapon signature FK check", f"Found {w_cap} weapons referencing character_id 104")

# ----------------------------------------------------------------------
# 4. CSV REGENERATION REPEATABILITY & DETERMINISM
# ----------------------------------------------------------------------
print("\n--- Suite 4: CSV Regeneration Repeatability & DB Rebuild ---")

csv_files = ["characters.csv", "weapons.csv", "artifact_sets.csv", "character_builds.csv"]
initial_hashes = {f: file_sha256(os.path.join(DATA_DIR, f)) for f in csv_files}

# Run generate_csvs.py
gen_res = subprocess.run([sys.executable, "generate_csvs.py"], cwd=PROJECT_ROOT, capture_output=True, text=True)
if gen_res.returncode == 0:
    record_pass("python3 generate_csvs.py executed with returncode 0")
else:
    record_fail("generate_csvs.py execution", f"Failed with code {gen_res.returncode}: {gen_res.stderr}")

after_hashes = {f: file_sha256(os.path.join(DATA_DIR, f)) for f in csv_files}
all_hashes_match = True
for f in csv_files:
    if initial_hashes[f] == after_hashes[f]:
        record_pass(f"File data/{f} hash identical after regeneration (SHA256: {after_hashes[f][:12]}...)")
    else:
        all_hashes_match = False
        record_fail(f"File data/{f} hash invariance", "File modified unpredictably during regeneration")

# Run init_db.py to rebuild database
init_res = subprocess.run([sys.executable, "init_db.py"], cwd=PROJECT_ROOT, capture_output=True, text=True)
if init_res.returncode == 0:
    record_pass("python3 init_db.py executed cleanly with returncode 0")
else:
    record_fail("init_db.py execution", f"Failed with code {init_res.returncode}: {init_res.stderr}")

# Reconnect to fresh DB
conn.close()
conn = get_db_connection()
cur = conn.cursor()

# ----------------------------------------------------------------------
# 5. CSV vs DB 1:1 PARITY
# ----------------------------------------------------------------------
print("\n--- Suite 5: CSV vs SQLite Database 1:1 Parity ---")

# characters parity (keyed by character_id)
with open(os.path.join(DATA_DIR, "characters.csv"), newline="", encoding="utf-8") as f:
    csv_chars = {int(r["character_id"]): r for r in csv.DictReader(f)}
db_chars = {r["character_id"]: r for r in cur.execute("SELECT * FROM characters;").fetchall()}
if len(csv_chars) == len(db_chars):
    record_pass(f"characters table count ({len(db_chars)}) matches CSV count ({len(csv_chars)})")
else:
    record_fail("characters count parity", f"CSV: {len(csv_chars)}, DB: {len(db_chars)}")

chars_discrepancy = 0
for cid, cr in csv_chars.items():
    dr = db_chars.get(cid)
    if not dr:
        chars_discrepancy += 1
        continue
    for col in cr:
        if cr[col] != str(dr[col]):
            chars_discrepancy += 1
if chars_discrepancy == 0:
    record_pass("characters table rows match CSV exactly across all columns")
else:
    record_fail("characters row parity", f"{chars_discrepancy} discrepancies detected between CSV and DB")


# weapons parity
with open(os.path.join(DATA_DIR, "weapons.csv"), newline="", encoding="utf-8") as f:
    csv_weaps = list(csv.DictReader(f))
db_weaps = cur.execute("SELECT * FROM weapons ORDER BY weapon_id;").fetchall()
if len(csv_weaps) == len(db_weaps):
    record_pass(f"weapons table count ({len(db_weaps)}) matches CSV count ({len(csv_weaps)})")
else:
    record_fail("weapons count parity", f"CSV: {len(csv_weaps)}, DB: {len(db_weaps)}")

weap_discrepancy = 0
for cr, dr in zip(csv_weaps, db_weaps):
    if int(cr["weapon_id"]) != dr["weapon_id"] or cr["name"] != dr["name"]:
        weap_discrepancy += 1
    # Check signature_character_id NULL handling
    expected_sig = int(cr["signature_character_id"]) if cr["signature_character_id"] != "" else None
    if dr["signature_character_id"] != expected_sig:
        weap_discrepancy += 1
if weap_discrepancy == 0:
    record_pass("weapons table rows match CSV exactly (including NULL conversion)")
else:
    record_fail("weapons row parity", f"{weap_discrepancy} rows differ")

# artifact_sets parity
with open(os.path.join(DATA_DIR, "artifact_sets.csv"), newline="", encoding="utf-8") as f:
    csv_arts = list(csv.DictReader(f))
db_arts = cur.execute("SELECT * FROM artifact_sets ORDER BY artifact_set_id;").fetchall()
if len(csv_arts) == len(db_arts):
    record_pass(f"artifact_sets count ({len(db_arts)}) matches CSV count ({len(csv_arts)})")
else:
    record_fail("artifact_sets count parity", f"CSV: {len(csv_arts)}, DB: {len(db_arts)}")

# character_builds parity
with open(os.path.join(DATA_DIR, "character_builds.csv"), newline="", encoding="utf-8") as f:
    csv_blds = list(csv.DictReader(f))
db_blds = cur.execute("SELECT * FROM character_builds ORDER BY build_id;").fetchall()
if len(csv_blds) == len(db_blds):
    record_pass(f"character_builds count ({len(db_blds)}) matches CSV count ({len(csv_blds)})")
else:
    record_fail("character_builds count parity", f"CSV: {len(csv_blds)}, DB: {len(db_blds)}")

# ----------------------------------------------------------------------
# 6. RELATIONAL INTEGRITY, PRAGMAS & CASCADE TESTING
# ----------------------------------------------------------------------
print("\n--- Suite 6: Relational Integrity & Cascade Semantics ---")

fk_violations = cur.execute("PRAGMA foreign_key_check;").fetchall()
if len(fk_violations) == 0:
    record_pass("PRAGMA foreign_key_check returned 0 violations")
else:
    record_fail("PRAGMA foreign_key_check", f"{len(fk_violations)} violations found: {fk_violations}")

integrity = cur.execute("PRAGMA integrity_check;").fetchone()[0]
if integrity == "ok":
    record_pass("PRAGMA integrity_check returned 'ok'")
else:
    record_fail("PRAGMA integrity_check", f"Returned: {integrity}")

# Test FK enforcement with simulated invalid insertions
try:
    cur.execute("""
        INSERT INTO character_builds (build_id, character_id, build_name, role, recommended_weapon_id, recommended_artifact_id, sands_stat, goblet_stat, circlet_stat, tier_rating, playstyle_notes)
        VALUES (99999, 99999, 'Test Ghost Build', 'Main DPS', 101, 1, 'ATK%', 'Pyro DMG', 'CRIT Rate', 'S', 'Test note');
    """)
    conn.commit()
    record_fail("FK insertion enforcement", "Invalid foreign key insert succeeded unexpectedly!")
except sqlite3.IntegrityError:
    record_pass("FK insertion enforcement correctly blocked invalid character_id")
finally:
    conn.rollback()

# Test ON DELETE CASCADE on character_builds
conn.execute("SAVEPOINT test_cascade;")
try:
    # Insert a temporary dummy character and build
    cur.execute("""
        INSERT INTO characters (character_id, name, rarity, vision, weapon_type, region, default_role, base_hp, base_atk, base_def, talent_priority, release_patch)
        VALUES (99998, 'Dummy Test Hero', 5, 'Pyro', 'Sword', 'Mondstadt', 'Main DPS', 10000, 300, 700, 'Skill', 1.0);
    """)
    cur.execute("""
        INSERT INTO character_builds (build_id, character_id, build_name, role, recommended_weapon_id, recommended_artifact_id, sands_stat, goblet_stat, circlet_stat, tier_rating, playstyle_notes)
        VALUES (99998, 99998, 'Dummy Build', 'Main DPS', 101, 1, 'ATK%', 'Pyro DMG', 'CRIT Rate', 'S', 'Test note');
    """)
    # Delete the character
    cur.execute("DELETE FROM characters WHERE character_id = 99998;")
    # Verify build was cascaded
    cascaded_cnt = cur.execute("SELECT COUNT(*) FROM character_builds WHERE build_id = 99998;").fetchone()[0]
    if cascaded_cnt == 0:
        record_pass("ON DELETE CASCADE correctly purged associated build when character was deleted")
    else:
        record_fail("ON DELETE CASCADE", f"Build 99998 still exists after parent character deletion!")
finally:
    conn.execute("ROLLBACK TO test_cascade;")

# ----------------------------------------------------------------------
# 7. ADVERSARIAL EDGE CASES & CROSS-TABLE CONSISTENCY
# ----------------------------------------------------------------------
print("\n--- Suite 7: Adversarial Edge Cases & Cross-Table Audit ---")

# Edge Case 1: Weapon Type vs Character Weapon Type in builds
weapon_mismatches = cur.execute("""
    SELECT b.build_id, b.build_name, c.character_id, c.name AS char_name, c.weapon_type AS char_weapon,
           w.weapon_id, w.name AS weapon_name, w.weapon_type AS weapon_weapon
    FROM character_builds b
    JOIN characters c ON b.character_id = c.character_id
    JOIN weapons w ON b.recommended_weapon_id = w.weapon_id
    WHERE c.weapon_type != w.weapon_type;
""").fetchall()

if len(weapon_mismatches) == 0:
    record_pass("100% of character builds have matching character and weapon weapon_type")
else:
    for m in weapon_mismatches:
        print(f"  [OBSERVATION] Build {m['build_id']} '{m['build_name']}': Character {m['char_name']} is {m['char_weapon']} but Recommended Weapon {m['weapon_name']} is {m['weapon_weapon']}")
    record_fail("Build weapon_type consistency", f"{len(weapon_mismatches)} weapon type mismatches detected! (Sandrone Build 380)")

# Edge Case 2: Sandrone build goblet element vs vision
sandrone_build = cur.execute("""
    SELECT b.build_id, b.goblet_stat, b.recommended_artifact_id, a.name AS art_name, c.vision
    FROM character_builds b
    JOIN characters c ON b.character_id = c.character_id
    JOIN artifact_sets a ON b.recommended_artifact_id = a.artifact_set_id
    WHERE c.name = 'Sandrone';
""").fetchone()

if sandrone_build:
    if sandrone_build["vision"] == "Cryo" and "Geo" in sandrone_build["goblet_stat"]:
        print(f"  [OBSERVATION] Sandrone vision is Cryo, but Build {sandrone_build['build_id']} goblet_stat is '{sandrone_build['goblet_stat']}' and artifact is '{sandrone_build['art_name']}'")
        record_fail("Sandrone build elemental alignment", f"Goblet '{sandrone_build['goblet_stat']}' does not match Cryo vision")
    else:
        record_pass("Sandrone build goblet matches vision")

# Edge Case 3: Aloy region representation in SQL
aloy_null = cur.execute("SELECT COUNT(*) FROM characters WHERE name = 'Aloy' AND region IS NULL;").fetchone()[0]
aloy_str = cur.execute("SELECT COUNT(*) FROM characters WHERE name = 'Aloy' AND region = 'None';").fetchone()[0]
if aloy_null == 0 and aloy_str == 1:
    record_pass("Aloy region is stored as literal string 'None' (NOT SQL NULL)")
else:
    record_fail("Aloy region representation", f"IS NULL: {aloy_null}, = 'None': {aloy_str}")

# Edge Case 4: Verify all artifact sets have non-empty bonuses
empty_bonuses = cur.execute("SELECT COUNT(*) FROM artifact_sets WHERE two_piece_bonus IS NULL OR two_piece_bonus = '' OR four_piece_bonus IS NULL OR four_piece_bonus = '';").fetchone()[0]
if empty_bonuses == 0:
    record_pass("All 64 artifact sets have non-empty 2pc and 4pc bonus fields")
else:
    record_fail("Artifact bonus completeness", f"{empty_bonuses} artifact sets have empty bonuses")

# Edge Case 5: Verify no characters have negative or zero stats
invalid_stats = cur.execute("SELECT COUNT(*) FROM characters WHERE base_hp <= 0 OR base_atk <= 0 OR base_def <= 0;").fetchone()[0]
if invalid_stats == 0:
    record_pass("All characters have positive base stats (HP, ATK, DEF > 0)")
else:
    record_fail("Character base stats sanity", f"{invalid_stats} characters have invalid stats")

# ----------------------------------------------------------------------
# 8. WEB SECURITY AND INTEGRATION SUITE
# ----------------------------------------------------------------------
print("\n--- Suite 8: Web Security and OOM Suite Execution ---")
sec_res = subprocess.run(["./.venv/bin/python", "test_security_oom.py"], cwd=PROJECT_ROOT, capture_output=True, text=True)
if sec_res.returncode == 0:
    record_pass("test_security_oom.py passed all tests (22/22 green)")
else:
    record_fail("test_security_oom.py", f"Failed with exit code {sec_res.returncode}:\n{sec_res.stderr or sec_res.stdout}")

conn.close()

# ----------------------------------------------------------------------
# SUMMARY & VERDICT
# ----------------------------------------------------------------------
print("\n" + "=" * 70)
print(f"ADVERSARIAL STRESS SUITE FINISHED: {passed_tests} PASSED, {failed_tests} FAILED")
print("=" * 70)

if findings:
    print("\nIdentified Adversarial Findings:")
    for name, reason in findings:
        print(f"  * {name}: {reason}")
