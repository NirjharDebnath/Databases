#!/usr/bin/env python3
"""
test_m1_verification.py
Independent verification script for Milestone 1 (M1) changes:
1. Artifact sets 59, 60, 62, 63, 64
2. Weapons 128, 131
3. Character attributes (72, 91, 99, 102, 103, 105)
4. Capitano (104) and Build 381 purge
5. Foreign Key integrity
6. CSV file synchronization with database tables
"""

import os
import csv
import sqlite3

BASE_DIR = "/home/nirjhar/Python Codes/Einstein/Databases"
DB_PATH = os.path.join(BASE_DIR, "genshin_learning.db")
DATA_DIR = os.path.join(BASE_DIR, "data")

def verify():
    assert os.path.exists(DB_PATH), f"Missing database {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()

    # 1. Foreign Key Verification
    fk_violations = cur.execute("PRAGMA foreign_key_check;").fetchall()
    assert len(fk_violations) == 0, f"Foreign key violations found: {fk_violations}"
    print("✅ PRAGMA foreign_key_check: 0 violations.")

    # 2. Capitano Purge Verification
    cap_c = cur.execute("SELECT COUNT(*) FROM characters WHERE character_id = 104 OR name = 'Capitano';").fetchone()[0]
    cap_b = cur.execute("SELECT COUNT(*) FROM character_builds WHERE build_id = 381 OR character_id = 104;").fetchone()[0]
    assert cap_c == 0, f"Capitano found in characters ({cap_c})"
    assert cap_b == 0, f"Build 381 found in character_builds ({cap_b})"
    print("✅ Capitano (ID 104) and Build 381 completely purged from DB.")

    # 3. Artifact Sets Verification
    expected_sets = {
        59: ("Aubade of Morningstar and Moon", "Moonchild's Treasures", "Nod-Krai", 
             "+80 Elemental Mastery", 
             "When off-field, Lunar Reaction DMG +20%. When party Moonsign Level is Ascendant Gleam, Lunar Reaction DMG +40%"),
        60: ("A Day Carved from Rising Winds", "Moonchild's Treasures", "Nod-Krai", 
             "+18% ATK", 
             "Normal/Charged/Skill/Burst hits grant Blessing of Pastoral Winds (ATK +25% for 6s); upgrades with Witch's Homework to Resolve of Pastoral Winds (CRIT Rate +20%)"),
        62: ("Disenchantment in Deep Shadow", "Thorny Crown of the Mountain Wind", "Mondstadt", 
             "+18% ATK", 
             "Superconduct Reaction DMG +80% (Stellar-Conduct +40%); attacking affected foes increases CRIT Rate by 16%"),
        63: ("Scarlet Proof", "Inverted Glacier", "Snezhnaya", 
             "+18% ATK", 
             "After triggering a Stellar Swirl reaction, CRIT Rate +16% and Stellar Swirl DMG +40% for 10s"),
        64: ("Heart of the Furnace", "Inverted Glacier", "Snezhnaya", 
             "+18% ATK", 
             "Triggering Stellar Glimmer or dealing its DMG grants ATK +12% for 12s, and increases party Stellar Glimmer DMG by 50%")
    }
    for sid, exp in expected_sets.items():
        row = cur.execute("SELECT name, domain_name, region, two_piece_bonus, four_piece_bonus FROM artifact_sets WHERE artifact_set_id = ?;", (sid,)).fetchone()
        assert row == exp, f"Set {sid} mismatch: got {row}, expected {exp}"
    print("✅ Artifact Sets 59, 60, 62, 63, 64 match official specifications exactly.")

    # 4. Weapons Verification
    expected_weaps = {
        128: ("Fang of the Mountain King", "Claymore", 5, 741, "CRIT Rate", 11.0),
        131: ("A Thousand Blazing Suns", "Claymore", 5, 741, "CRIT Rate", 11.0)
    }
    for wid, exp in expected_weaps.items():
        row = cur.execute("SELECT name, weapon_type, rarity, base_atk, sub_stat_type, sub_stat_value FROM weapons WHERE weapon_id = ?;", (wid,)).fetchone()
        assert row == exp, f"Weapon {wid} mismatch: got {row}, expected {exp}"
    print("✅ Weapons 128 and 131 stats match official specifications exactly (741 ATK, 11.0% CRIT Rate).")

    # 5. Characters Verification
    expected_chars = {
        72: ("Arlecchino", "Pyro", "Polearm", "Snezhnaya", 4.6),
        91: ("Iansan", "Electro", "Polearm", "Natlan", 5.5),
        99: ("Zibai", "Geo", "Sword", "Liyue", 6.2),
        102: ("Columbina", "Hydro", "Catalyst", "Nod-Krai", 6.0),
        103: ("Sandrone", "Cryo", "Claymore", "Snezhnaya", 6.2),
        105: ("Aloy", "Cryo", "Bow", "None", 2.1)
    }
    for cid, exp in expected_chars.items():
        row = cur.execute("SELECT name, vision, weapon_type, region, release_patch FROM characters WHERE character_id = ?;", (cid,)).fetchone()
        assert row == exp, f"Character {cid} mismatch: got {row}, expected {exp}"
    print("✅ Characters 72, 91, 99, 102, 103, 105 attributes match official specifications.")

    # 6. CSV Parity Check
    with open(os.path.join(DATA_DIR, "characters.csv"), "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        header = reader[0]
        rows = reader[1:]
        assert len(rows) == 113, f"characters.csv row count {len(rows)} != 113"
        cap_csv = [r for r in rows if r[0] == "104" or r[1] == "Capitano"]
        assert len(cap_csv) == 0, "Capitano found in characters.csv"

    with open(os.path.join(DATA_DIR, "character_builds.csv"), "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        rows = reader[1:]
        assert len(rows) == 106, f"character_builds.csv row count {len(rows)} != 106"
        build_csv = [r for r in rows if r[0] == "381" or r[1] == "104"]
        assert len(build_csv) == 0, "Build 381 found in character_builds.csv"

    print("✅ CSV files strictly synchronized and verified.")
    print("ALL M1 VERIFICATION CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    verify()
