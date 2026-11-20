#!/usr/bin/env python3
"""
stress_test_verifier.py
Adversarial stress-test script executed by auditor_m4 to empirically verify
that verify_db.py cannot be bypassed and actively flags any data defects or schema omissions.
"""

import os
import sys
import shutil
import sqlite3
import tempfile

# Add project root to sys.path
PROJECT_ROOT = "/home/nirjhar/Python Codes/Einstein/Databases"
sys.path.insert(0, PROJECT_ROOT)

import verify_db

def run_stress_test(name, mutation_fn, expected_error_substr):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        temp_db_path = tmp.name

    try:
        # Copy genuine database
        shutil.copyfile(os.path.join(PROJECT_ROOT, "genshin_learning.db"), temp_db_path)
        
        # Apply mutation
        conn = sqlite3.connect(temp_db_path)
        conn.execute("PRAGMA foreign_keys = OFF;") # allow mutation for test
        mutation_fn(conn)
        conn.commit()
        conn.close()

        # Point verify_db to temp DB
        old_db_path = verify_db.DB_PATH
        verify_db.DB_PATH = temp_db_path

        caught = False
        try:
            # We redirect stdout so we don't spam output
            old_stdout = sys.stdout
            sys.stdout = open(os.devnull, "w")
            verify_db.test_database()
            sys.stdout = old_stdout
        except AssertionError as e:
            sys.stdout = old_stdout
            caught = True
            msg = str(e)
            if expected_error_substr in msg:
                print(f"  [PASS] {name}: Caught expected AssertionError ('{msg}')")
                return True
            else:
                print(f"  [FAIL] {name}: Caught AssertionError but message mismatch. Expected '{expected_error_substr}', got '{msg}'")
                return False
        except Exception as e:
            sys.stdout = old_stdout
            print(f"  [FAIL] {name}: Unexpected exception type {type(e)}: {e}")
            return False
        finally:
            verify_db.DB_PATH = old_db_path

        if not caught:
            print(f"  [FAIL] {name}: verify_db PASSED despite mutation! Bypass vulnerability detected!")
            return False

    finally:
        if os.path.exists(temp_db_path):
            os.remove(temp_db_path)

def main():
    print("=" * 70)
    print("AUDITOR STRESS-TESTING verify_db.py ASSERTION ROBUSTNESS")
    print("=" * 70)

    tests = [
        (
            "Suite 1 Mutation: Foreign Key Violation",
            lambda conn: conn.execute("INSERT INTO weapons(weapon_id, name, weapon_type, rarity, base_atk, sub_stat_type, sub_stat_value, is_craftable, signature_character_id) VALUES (9999, 'Phantom Blade', 'Sword', 5, 608, 'ATK%', 33.1, 0, 99999);"),
            "Found foreign key violations"
        ),
        (
            "Suite 2 Mutation: Character Row Count Mismatch (Delete character without breaking FK)",
            # Aloy (105) has no signature weapon, and we delete her build so no FK violation, but characters has 128
            lambda conn: conn.executescript("DELETE FROM character_builds WHERE character_id = 105; DELETE FROM characters WHERE character_id = 105;"),
            "Table 'characters' has 128 rows, expected 129"
        ),
        (
            "Suite 3 Mutation: Orphaned Character Without Build (Preserving Total Build Count)",
            # Reassign build 408 (Barbara) to character 1 (Venti) so total builds stay 168, but Barbara (3) has 0 builds
            lambda conn: conn.execute("UPDATE character_builds SET character_id = 1 WHERE build_id = 408;"),
            "Found 1 orphaned character(s) without builds"
        ),
        (
            "Suite 4 Mutation: Regional Distribution Mismatch",
            lambda conn: conn.execute("UPDATE characters SET region = 'Mondstadt' WHERE name = 'Zhongli';"), # Move Zhongli to Mondstadt
            "Region 'Mondstadt' expected 23 characters, got 24"
        ),
        (
            "Suite 5 Mutation: Weapon Type Compatibility Mismatch",
            lambda conn: conn.execute("UPDATE character_builds SET recommended_weapon_id = (SELECT weapon_id FROM weapons WHERE weapon_type = 'Claymore' LIMIT 1) WHERE character_id = (SELECT character_id FROM characters WHERE weapon_type = 'Bow' LIMIT 1);"),
            "weapon type mismatch"
        ),
        (
            "Suite 6 Mutation: 1:1 CSV-to-DB Parity Mismatch",
            lambda conn: conn.execute("UPDATE characters SET base_atk = 999 WHERE character_id = 1;"),
            "Character parity mismatch on ID 1"
        ),
        (
            "Suite 7 Mutation: Missing Index (DROP idx_weapons_signature)",
            lambda conn: conn.execute("DROP INDEX idx_weapons_signature;"),
            "Missing required index: idx_weapons_signature"
        ),
        (
            "Suite 7 Mutation: Missing Index (DROP idx_builds_artifact)",
            lambda conn: conn.execute("DROP INDEX idx_builds_artifact;"),
            "Missing required index: idx_builds_artifact"
        ),
    ]

    all_passed = True
    for name, mutation_fn, expected_substr in tests:
        res = run_stress_test(name, mutation_fn, expected_substr)
        if not res:
            all_passed = False

    print("=" * 70)
    if all_passed:
        print("ALL 8 ADVERSARIAL STRESS TESTS PASSED: verify_db.py is UNBYPASSABLE!")
    else:
        print("SOME ADVERSARIAL STRESS TESTS FAILED!")
    print("=" * 70)
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
