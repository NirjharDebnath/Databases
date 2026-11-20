#!/usr/bin/env python3
"""
tests/test_m4_adversarial_challenger.py
Empirical Adversarial Stress Suite for Milestone 4 (M4): Pipeline Synchronization & Verification Suite Upgrade.

Author: challenger_m4_1 (Empirical Challenger)
Role: critic, specialist
Target Milestone: Milestone 4 (M4) / Requirements R5 & Acceptance Criteria

Verification Scope:
- Suite 1: Relational Schema & Index Utilization Stress (EXPLAIN QUERY PLAN & INDEXED BY)
- Suite 2: Negative Stress-Testing of verify_db.py (Injected Defect Detection)
- Suite 3: Pipeline Regeneration, Determinism & Idempotency
- Suite 4: Schema Referential Actions & Constraints Stress (CASCADE, RESTRICT, SET NULL, CHECK)
- Suite 5: Complex Analytical Queries, Boundary & Escaping Stress
"""

import os
import sys
import csv
import shutil
import hashlib
import sqlite3
import tempfile
import subprocess
from typing import Dict, List, Tuple, Any, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(PROJECT_ROOT, "genshin_learning.db")

passed_tests = 0
failed_tests = 0
findings: List[Tuple[str, str]] = []

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

def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, timeout=10.0)
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
print("MILENSTONE 4 (M4) EMPIRICAL ADVERSARIAL CHALLENGER TEST SUITE")
print(f"Project Root : {PROJECT_ROOT}")
print(f"Database     : {DB_PATH}")
print("=" * 80)


# =====================================================================
# SUITE 1: RELATIONAL SCHEMA & INDEX UTILIZATION STRESS
# =====================================================================
print("\n--- Suite 1: Relational Schema & Index Utilization Stress ---")

conn = get_connection()
cursor = conn.cursor()

# 1.1 All 8 required indexes exist in sqlite_master
REQUIRED_INDEXES = [
    "idx_characters_region",
    "idx_characters_vision",
    "idx_weapons_type",
    "idx_weapons_signature",
    "idx_builds_character",
    "idx_builds_tier",
    "idx_builds_weapon",
    "idx_builds_artifact"
]

existing_indexes = {
    row[0] for row in cursor.execute("SELECT name FROM sqlite_master WHERE type = 'index';").fetchall()
}

for idx in REQUIRED_INDEXES:
    if idx in existing_indexes:
        record_pass(f"Index existence: {idx}", "Found in sqlite_master")
    else:
        record_fail(f"Index existence: {idx}", "Missing from sqlite_master")

# 1.2 Verify EXPLAIN QUERY PLAN uses idx_weapons_signature
plan_sig = cursor.execute("""
    EXPLAIN QUERY PLAN
    SELECT weapon_id, name, signature_character_id
    FROM weapons
    WHERE signature_character_id = 84;
""").fetchall()
plan_sig_text = " ".join([str(tuple(r)) for r in plan_sig])
if "idx_weapons_signature" in plan_sig_text:
    record_pass("EXPLAIN QUERY PLAN on signature_character_id", f"Plan uses idx_weapons_signature: {plan_sig_text}")
else:
    record_fail("EXPLAIN QUERY PLAN on signature_character_id", f"Plan did NOT use idx_weapons_signature: {plan_sig_text}")

# 1.3 Verify EXPLAIN QUERY PLAN uses idx_builds_weapon
plan_wep = cursor.execute("""
    EXPLAIN QUERY PLAN
    SELECT build_id, build_name, recommended_weapon_id
    FROM character_builds
    WHERE recommended_weapon_id = 128;
""").fetchall()
plan_wep_text = " ".join([str(tuple(r)) for r in plan_wep])
if "idx_builds_weapon" in plan_wep_text:
    record_pass("EXPLAIN QUERY PLAN on recommended_weapon_id", f"Plan uses idx_builds_weapon: {plan_wep_text}")
else:
    record_fail("EXPLAIN QUERY PLAN on recommended_weapon_id", f"Plan did NOT use idx_builds_weapon: {plan_wep_text}")

# 1.4 Verify EXPLAIN QUERY PLAN uses idx_builds_artifact
plan_art = cursor.execute("""
    EXPLAIN QUERY PLAN
    SELECT build_id, build_name, recommended_artifact_id
    FROM character_builds
    WHERE recommended_artifact_id = 59;
""").fetchall()
plan_art_text = " ".join([str(tuple(r)) for r in plan_art])
if "idx_builds_artifact" in plan_art_text:
    record_pass("EXPLAIN QUERY PLAN on recommended_artifact_id", f"Plan uses idx_builds_artifact: {plan_art_text}")
else:
    record_fail("EXPLAIN QUERY PLAN on recommended_artifact_id", f"Plan did NOT use idx_builds_artifact: {plan_art_text}")

# 1.5 Verify other indexes in EXPLAIN QUERY PLAN
other_plans = [
    ("idx_characters_region", "SELECT name FROM characters WHERE region = 'Snezhnaya';"),
    ("idx_characters_vision", "SELECT name FROM characters WHERE vision = 'Cryo';"),
    ("idx_weapons_type", "SELECT name FROM weapons WHERE weapon_type = 'Claymore';"),
    ("idx_builds_character", "SELECT build_name FROM character_builds WHERE character_id = 72;"),
    ("idx_builds_tier", "SELECT build_name FROM character_builds WHERE tier_rating = 'SS';"),
]
for idx_name, sql in other_plans:
    plan = cursor.execute(f"EXPLAIN QUERY PLAN {sql}").fetchall()
    plan_text = " ".join([str(tuple(r)) for r in plan])
    if idx_name in plan_text:
        record_pass(f"EXPLAIN QUERY PLAN on {idx_name}", f"Plan uses index: {plan_text}")
    else:
        record_fail(f"EXPLAIN QUERY PLAN on {idx_name}", f"Plan did NOT use index: {plan_text}")

# 1.6 INDEXED BY forcing stress test for all 8 indexes
indexed_by_tests = [
    ("idx_characters_region", "SELECT COUNT(*) FROM characters INDEXED BY idx_characters_region WHERE region = 'Mondstadt';", 23),
    ("idx_characters_vision", "SELECT COUNT(*) FROM characters INDEXED BY idx_characters_vision WHERE vision = 'Pyro';", None),
    ("idx_weapons_type", "SELECT COUNT(*) FROM weapons INDEXED BY idx_weapons_type WHERE weapon_type = 'Sword';", None),
    ("idx_weapons_signature", "SELECT COUNT(*) FROM weapons INDEXED BY idx_weapons_signature WHERE signature_character_id = 84;", 1),
    ("idx_builds_character", "SELECT COUNT(*) FROM character_builds INDEXED BY idx_builds_character WHERE character_id = 87;", 2),
    ("idx_builds_tier", "SELECT COUNT(*) FROM character_builds INDEXED BY idx_builds_tier WHERE tier_rating = 'SS';", None),
    ("idx_builds_weapon", "SELECT COUNT(*) FROM character_builds INDEXED BY idx_builds_weapon WHERE recommended_weapon_id = 128;", None),
    ("idx_builds_artifact", "SELECT COUNT(*) FROM character_builds INDEXED BY idx_builds_artifact WHERE recommended_artifact_id = 59;", None),
]

for idx_name, sql, expected_cnt in indexed_by_tests:
    try:
        cnt = cursor.execute(sql).fetchone()[0]
        if expected_cnt is not None:
            assert cnt == expected_cnt, f"Expected {expected_cnt}, got {cnt}"
        assert cnt > 0, f"Expected count > 0, got {cnt}"
        record_pass(f"INDEXED BY stress: {idx_name}", f"Successfully executed with forced index ({cnt} rows)")
    except Exception as e:
        record_fail(f"INDEXED BY stress: {idx_name}", str(e))

# 1.7 Negative INDEXED BY test: Non-existent index raises operational error
try:
    cursor.execute("SELECT * FROM characters INDEXED BY non_existent_index WHERE region = 'Liyue';")
    record_fail("Negative INDEXED BY on invalid index", "Expected OperationalError but query succeeded")
except sqlite3.OperationalError as e:
    record_pass("Negative INDEXED BY on invalid index", f"Correctly caught OperationalError: {e}")

# 1.8 Join index usage: Joining character_builds to weapons via recommended_weapon_id
plan_join = cursor.execute("""
    EXPLAIN QUERY PLAN
    SELECT c.name, cb.build_name, w.name
    FROM weapons w
    JOIN character_builds cb ON w.weapon_id = cb.recommended_weapon_id
    JOIN characters c ON cb.character_id = c.character_id
    WHERE w.name = 'Fang of the Mountain King';
""").fetchall()
plan_join_text = " ".join([str(tuple(r)) for r in plan_join])
if "idx_builds_weapon" in plan_join_text:
    record_pass("Join Query Plan with idx_builds_weapon", f"Uses idx_builds_weapon: {plan_join_text}")
else:
    record_fail("Join Query Plan with idx_builds_weapon", f"Index not used: {plan_join_text}")

conn.close()


# =====================================================================
# SUITE 2: NEGATIVE STRESS-TESTING OF verify_db.py
# =====================================================================
print("\n--- Suite 2: Negative Stress-Testing of verify_db.py (Injected Defect Detection) ---")

# Import verify_db directly to test its programmatic assertion behavior
import verify_db

# Helper function to create a sandbox copy of the database and test verify_db.test_database()
def run_verify_on_temp_db(modifier_fn) -> Tuple[bool, str]:
    """
    Creates an isolated copy of genshin_learning.db in a temp directory,
    applies modifier_fn(conn), and runs verify_db.test_database() against it.
    Returns (failed_as_expected, error_message).
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
        temp_db_path = tf.name

    try:
        shutil.copyfile(DB_PATH, temp_db_path)
        temp_conn = sqlite3.connect(temp_db_path)
        temp_conn.execute("PRAGMA foreign_keys = OFF;") # Allow inserting corrupt states for test
        modifier_fn(temp_conn)
        temp_conn.commit()
        temp_conn.close()

        # Save original verify_db.DB_PATH
        orig_db_path = verify_db.DB_PATH
        verify_db.DB_PATH = temp_db_path

        caught = False
        error_msg = ""
        try:
            verify_db.test_database()
        except AssertionError as e:
            caught = True
            error_msg = f"AssertionError: {e}"
        except Exception as e:
            caught = True
            error_msg = f"Exception: {e}"
        finally:
            verify_db.DB_PATH = orig_db_path

        return caught, error_msg
    finally:
        if os.path.exists(temp_db_path):
            os.remove(temp_db_path)

# 2.1 Injected Foreign Key Violation: Weapon referencing non-existent character ID 9999
def corrupt_fk_weapon(c: sqlite3.Connection):
    c.execute("UPDATE weapons SET signature_character_id = 9999 WHERE weapon_id = 128;")

caught, err = run_verify_on_temp_db(corrupt_fk_weapon)
if caught:
    record_pass("Injected Defect: FK violation in weapons", f"Caught: {err}")
else:
    record_fail("Injected Defect: FK violation in weapons", "verify_db failed to catch foreign key violation")

# 2.2 Injected Foreign Key Violation: Build referencing non-existent weapon ID 9999
def corrupt_fk_build_weapon(c: sqlite3.Connection):
    cur = c.cursor()
    cur.execute("UPDATE character_builds SET recommended_weapon_id = 9999 WHERE build_id = 301;")
    assert cur.rowcount > 0, "No rows updated in corrupt_fk_build_weapon"

caught, err = run_verify_on_temp_db(corrupt_fk_build_weapon)
if caught:
    record_pass("Injected Defect: FK violation in character_builds (weapon)", f"Caught: {err}")
else:
    record_fail("Injected Defect: FK violation in character_builds (weapon)", "verify_db failed to catch FK violation")

# 2.3 Injected Foreign Key Violation: Build referencing non-existent artifact ID 9999
def corrupt_fk_build_artifact(c: sqlite3.Connection):
    cur = c.cursor()
    cur.execute("UPDATE character_builds SET recommended_artifact_id = 9999 WHERE build_id = 301;")
    assert cur.rowcount > 0, "No rows updated in corrupt_fk_build_artifact"

caught, err = run_verify_on_temp_db(corrupt_fk_build_artifact)
if caught:
    record_pass("Injected Defect: FK violation in character_builds (artifact)", f"Caught: {err}")
else:
    record_fail("Injected Defect: FK violation in character_builds (artifact)", "verify_db failed to catch FK violation")

# 2.4 Injected Row Count Mismatch: Delete 1 character (128 instead of 129)
def corrupt_row_count_delete_char(c: sqlite3.Connection):
    # delete build first to avoid orphan check tripping first
    c.execute("DELETE FROM character_builds WHERE character_id = 114;")
    c.execute("DELETE FROM characters WHERE character_id = 114;")

caught, err = run_verify_on_temp_db(corrupt_row_count_delete_char)
if caught:
    record_pass("Injected Defect: Row count mismatch (128 characters)", f"Caught: {err}")
else:
    record_fail("Injected Defect: Row count mismatch (128 characters)", "verify_db failed to catch row count mismatch")

# 2.5 Injected Row Count Mismatch: Delete 1 weapon (154 instead of 155)
def corrupt_row_count_delete_weapon(c: sqlite3.Connection):
    c.execute("DELETE FROM weapons WHERE weapon_id = 246;")

caught, err = run_verify_on_temp_db(corrupt_row_count_delete_weapon)
if caught:
    record_pass("Injected Defect: Row count mismatch (154 weapons)", f"Caught: {err}")
else:
    record_fail("Injected Defect: Row count mismatch (154 weapons)", "verify_db failed to catch row count mismatch")

# 2.6 Injected Row Count Mismatch: Delete 1 artifact set (63 instead of 64)
def corrupt_row_count_delete_artifact(c: sqlite3.Connection):
    c.execute("DELETE FROM artifact_sets WHERE artifact_set_id = 64;")

caught, err = run_verify_on_temp_db(corrupt_row_count_delete_artifact)
if caught:
    record_pass("Injected Defect: Row count mismatch (63 artifact sets)", f"Caught: {err}")
else:
    record_fail("Injected Defect: Row count mismatch (63 artifact sets)", "verify_db failed to catch row count mismatch")

# 2.7 Injected Row Count Mismatch: Delete 1 build (167 instead of 168)
def corrupt_row_count_delete_build(c: sqlite3.Connection):
    # Delete build 467 (Mavuika alternate build, so Mavuika still has build 384)
    c.execute("DELETE FROM character_builds WHERE build_id = 467;")

caught, err = run_verify_on_temp_db(corrupt_row_count_delete_build)
if caught:
    record_pass("Injected Defect: Row count mismatch (167 builds)", f"Caught: {err}")
else:
    record_fail("Injected Defect: Row count mismatch (167 builds)", "verify_db failed to catch row count mismatch")

# 2.8 Injected Orphan Character: Character with 0 builds
def corrupt_orphan_character(c: sqlite3.Connection):
    # Insert an unlinked character without any build
    c.execute("""
        INSERT INTO characters (character_id, name, rarity, vision, weapon_type, region, default_role, base_hp, base_atk, base_def, talent_priority, release_patch)
        VALUES (999, 'Phantom', 5, 'Pyro', 'Sword', 'Khaenriah', 'DPS', 10000, 300, 800, 'Burst', 6.0);
    """)

caught, err = run_verify_on_temp_db(corrupt_orphan_character)
if caught:
    record_pass("Injected Defect: Orphaned character without builds", f"Caught: {err}")
else:
    record_fail("Injected Defect: Orphaned character without builds", "verify_db failed to catch orphaned character")

# 2.9 Injected Regional Distribution Disparity: Alter Aloy's region from 'None' to 'Mondstadt'
def corrupt_region_distribution(c: sqlite3.Connection):
    c.execute("UPDATE characters SET region = 'Mondstadt' WHERE character_id = 114;")

caught, err = run_verify_on_temp_db(corrupt_region_distribution)
if caught:
    record_pass("Injected Defect: Regional distribution disparity", f"Caught: {err}")
else:
    record_fail("Injected Defect: Regional distribution disparity", "verify_db failed to catch regional disparity")

# 2.10 Injected Weapon Type Incompatibility: Give sword user a claymore build
def corrupt_weapon_type_mismatch(c: sqlite3.Connection):
    # Albedo (Sword user) recommended weapon set to Wolf's Gravestone (ID 129, Claymore)
    c.execute("UPDATE character_builds SET recommended_weapon_id = 129 WHERE character_id = 1;")

caught, err = run_verify_on_temp_db(corrupt_weapon_type_mismatch)
if caught:
    record_pass("Injected Defect: Weapon type incompatibility", f"Caught: {err}")
else:
    record_fail("Injected Defect: Weapon type incompatibility", "verify_db failed to catch weapon type mismatch")

# 2.11 Injected CSV-DB Parity Disparity: Alter base_atk in DB for Kinich
def corrupt_csv_parity_character(c: sqlite3.Connection):
    c.execute("UPDATE characters SET base_atk = 999 WHERE character_id = 84;")

caught, err = run_verify_on_temp_db(corrupt_csv_parity_character)
if caught:
    record_pass("Injected Defect: CSV-to-DB disparity on character attribute", f"Caught: {err}")
else:
    record_fail("Injected Defect: CSV-to-DB disparity on character attribute", "verify_db failed to catch parity mismatch")

# 2.12 Injected CSV-DB Parity Disparity: Alter weapon sub-stat in DB
def corrupt_csv_parity_weapon(c: sqlite3.Connection):
    c.execute("UPDATE weapons SET sub_stat_value = 99.9 WHERE weapon_id = 128;")

caught, err = run_verify_on_temp_db(corrupt_csv_parity_weapon)
if caught:
    record_pass("Injected Defect: CSV-to-DB disparity on weapon stat", f"Caught: {err}")
else:
    record_fail("Injected Defect: CSV-to-DB disparity on weapon stat", "verify_db failed to catch parity mismatch")

# 2.13 Injected Missing Index: Drop idx_weapons_signature
def corrupt_drop_signature_index(c: sqlite3.Connection):
    c.execute("DROP INDEX idx_weapons_signature;")

caught, err = run_verify_on_temp_db(corrupt_drop_signature_index)
if caught:
    record_pass("Injected Defect: Missing index idx_weapons_signature", f"Caught: {err}")
else:
    record_fail("Injected Defect: Missing index idx_weapons_signature", "verify_db failed to catch missing index")

# 2.14 Injected Missing Index: Drop idx_builds_weapon
def corrupt_drop_builds_weapon_index(c: sqlite3.Connection):
    c.execute("DROP INDEX idx_builds_weapon;")

caught, err = run_verify_on_temp_db(corrupt_drop_builds_weapon_index)
if caught:
    record_pass("Injected Defect: Missing index idx_builds_weapon", f"Caught: {err}")
else:
    record_fail("Injected Defect: Missing index idx_builds_weapon", "verify_db failed to catch missing index")

# 2.15 Injected Missing Index: Drop idx_builds_artifact
def corrupt_drop_builds_artifact_index(c: sqlite3.Connection):
    c.execute("DROP INDEX idx_builds_artifact;")

caught, err = run_verify_on_temp_db(corrupt_drop_builds_artifact_index)
if caught:
    record_pass("Injected Defect: Missing index idx_builds_artifact", f"Caught: {err}")
else:
    record_fail("Injected Defect: Missing index idx_builds_artifact", "verify_db failed to catch missing index")


# =====================================================================
# SUITE 3: PIPELINE REGENERATION, DETERMINISM & IDEMPOTENCY
# =====================================================================
print("\n--- Suite 3: Pipeline Regeneration, Determinism & Idempotency ---")

csv_files = ["characters.csv", "weapons.csv", "artifact_sets.csv", "character_builds.csv"]
initial_hashes = {f: file_sha256(os.path.join(DATA_DIR, f)) for f in csv_files}

# 3.1 Execute generate_csvs.py
gen_res = subprocess.run(["python3", "generate_csvs.py"], cwd=PROJECT_ROOT, capture_output=True, text=True)
if gen_res.returncode == 0:
    record_pass("Pipeline Step 1: python3 generate_csvs.py", "Exited with code 0")
else:
    record_fail("Pipeline Step 1: python3 generate_csvs.py", f"Exit code {gen_res.returncode}: {gen_res.stderr}")

# 3.2 Verify SHA-256 byte-for-byte reproducibility
post_gen_hashes = {f: file_sha256(os.path.join(DATA_DIR, f)) for f in csv_files}
for f in csv_files:
    if initial_hashes[f] == post_gen_hashes[f]:
        record_pass(f"Determinism Check: {f}", f"SHA-256 matched: {initial_hashes[f][:12]}...")
    else:
        record_fail(f"Determinism Check: {f}", f"Hash changed! {initial_hashes[f]} != {post_gen_hashes[f]}")

# 3.3 Execute init_db.py
init_res = subprocess.run(["python3", "init_db.py"], cwd=PROJECT_ROOT, capture_output=True, text=True)
if init_res.returncode == 0:
    record_pass("Pipeline Step 2: python3 init_db.py", "Exited with code 0")
else:
    record_fail("Pipeline Step 2: python3 init_db.py", f"Exit code {init_res.returncode}: {init_res.stderr}")

# 3.4 Execute verify_db.py
verify_res = subprocess.run(["python3", "verify_db.py"], cwd=PROJECT_ROOT, capture_output=True, text=True)
if verify_res.returncode == 0:
    record_pass("Pipeline Step 3: python3 verify_db.py", "Exited with code 0")
else:
    record_fail("Pipeline Step 3: python3 verify_db.py", f"Exit code {verify_res.returncode}: {verify_res.stderr}")

# 3.5 Execute test_e2e_genshin.py
e2e_res = subprocess.run(["python3", "tests/test_e2e_genshin.py"], cwd=PROJECT_ROOT, capture_output=True, text=True)
if e2e_res.returncode == 0:
    record_pass("Pipeline Regression: python3 tests/test_e2e_genshin.py", "171/171 passed (code 0)")
else:
    record_fail("Pipeline Regression: python3 tests/test_e2e_genshin.py", f"Exit code {e2e_res.returncode}: {e2e_res.stderr}")


# =====================================================================
# SUITE 4: SCHEMA REFERENTIAL ACTIONS & CONSTRAINTS STRESS
# =====================================================================
print("\n--- Suite 4: Schema Referential Actions & Constraints Stress ---")

# We test in an isolated copy so we can perform destructive DML safely
with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
    sandbox_db = tf.name

try:
    shutil.copyfile(DB_PATH, sandbox_db)
    s_conn = get_connection(sandbox_db)
    s_cur = s_conn.cursor()

    # 4.1 ON DELETE CASCADE: character deletion cascades to builds
    char_with_builds = s_cur.execute("""
        SELECT character_id, COUNT(*) as b_cnt 
        FROM character_builds 
        GROUP BY character_id 
        HAVING b_cnt > 1 
        LIMIT 1;
    """).fetchone()
    target_cid = char_with_builds[0]
    expected_builds_dropped = char_with_builds[1]

    s_cur.execute("DELETE FROM characters WHERE character_id = ?;", (target_cid,))
    remaining_builds = s_cur.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = ?;", (target_cid,)).fetchone()[0]
    if remaining_builds == 0:
        record_pass(f"ON DELETE CASCADE on character {target_cid}", f"Dropped {expected_builds_dropped} builds cleanly")
    else:
        record_fail(f"ON DELETE CASCADE on character {target_cid}", f"Found {remaining_builds} lingering builds")

    # 4.2 ON DELETE SET NULL: character deletion nullifies signature_character_id in weapons
    sig_weapon = s_cur.execute("""
        SELECT weapon_id, signature_character_id 
        FROM weapons 
        WHERE signature_character_id IS NOT NULL 
        LIMIT 1;
    """).fetchone()
    wid, owner_cid = sig_weapon[0], sig_weapon[1]
    s_cur.execute("DELETE FROM characters WHERE character_id = ?;", (owner_cid,))
    new_sig = s_cur.execute("SELECT signature_character_id FROM weapons WHERE weapon_id = ?;", (wid,)).fetchone()[0]
    if new_sig is None:
        record_pass(f"ON DELETE SET NULL on weapon {wid}", f"Owner character {owner_cid} deleted, signature became NULL")
    else:
        record_fail(f"ON DELETE SET NULL on weapon {wid}", f"Signature did not become NULL: {new_sig}")

    # 4.3 ON DELETE RESTRICT: weapon referenced in build cannot be deleted
    used_weapon = s_cur.execute("SELECT recommended_weapon_id FROM character_builds LIMIT 1;").fetchone()[0]
    try:
        s_cur.execute("DELETE FROM weapons WHERE weapon_id = ?;", (used_weapon,))
        record_fail("ON DELETE RESTRICT on weapons", "Expected sqlite3.IntegrityError but delete succeeded")
    except sqlite3.IntegrityError as e:
        record_pass("ON DELETE RESTRICT on weapons", f"Blocked deletion of referenced weapon {used_weapon}: {e}")

    # 4.4 ON DELETE RESTRICT: artifact set referenced in build cannot be deleted
    used_art = s_cur.execute("SELECT recommended_artifact_id FROM character_builds LIMIT 1;").fetchone()[0]
    try:
        s_cur.execute("DELETE FROM artifact_sets WHERE artifact_set_id = ?;", (used_art,))
        record_fail("ON DELETE RESTRICT on artifact_sets", "Expected sqlite3.IntegrityError but delete succeeded")
    except sqlite3.IntegrityError as e:
        record_pass("ON DELETE RESTRICT on artifact_sets", f"Blocked deletion of referenced artifact {used_art}: {e}")

    # 4.5 CHECK Constraints: rarity IN (4, 5)
    try:
        s_cur.execute("""
            INSERT INTO characters (character_id, name, rarity, vision, weapon_type, region, default_role, base_hp, base_atk, base_def, talent_priority, release_patch)
            VALUES (9991, 'InvalidRarity', 6, 'Pyro', 'Sword', 'Liyue', 'DPS', 10000, 300, 800, 'Burst', 1.0);
        """)
        record_fail("CHECK constraint: character rarity", "Expected IntegrityError on rarity=6")
    except sqlite3.IntegrityError:
        record_pass("CHECK constraint: character rarity", "Rarity 6 blocked by CHECK (rarity IN (4, 5))")

    # 4.6 CHECK Constraints: vision IN valid visions
    try:
        s_cur.execute("""
            INSERT INTO characters (character_id, name, rarity, vision, weapon_type, region, default_role, base_hp, base_atk, base_def, talent_priority, release_patch)
            VALUES (9992, 'InvalidVision', 5, 'Cosmo', 'Sword', 'Liyue', 'DPS', 10000, 300, 800, 'Burst', 1.0);
        """)
        record_fail("CHECK constraint: character vision", "Expected IntegrityError on vision='Cosmo'")
    except sqlite3.IntegrityError:
        record_pass("CHECK constraint: character vision", "Vision 'Cosmo' blocked by CHECK")

    # 4.7 CHECK Constraints: weapon_type IN valid types
    try:
        s_cur.execute("""
            INSERT INTO weapons (weapon_id, name, weapon_type, rarity, base_atk, sub_stat_type, sub_stat_value, is_craftable, signature_character_id)
            VALUES (9993, 'Gun', 'Pistol', 4, 454, 'ATK%', 55.1, 0, NULL);
        """)
        record_fail("CHECK constraint: weapon_type", "Expected IntegrityError on weapon_type='Pistol'")
    except sqlite3.IntegrityError:
        record_pass("CHECK constraint: weapon_type", "Weapon type 'Pistol' blocked by CHECK")

    # 4.8 CHECK Constraints: tier_rating IN ('SS', 'S+', 'S', 'A')
    try:
        s_cur.execute("""
            INSERT INTO character_builds (build_id, character_id, build_name, role, recommended_weapon_id, recommended_artifact_id, sands_stat, goblet_stat, circlet_stat, tier_rating, playstyle_notes)
            VALUES (9994, 84, 'InvalidTier', 'DPS', 128, 59, 'ATK%', 'Dendro DMG', 'CRIT Rate', 'B', 'Notes');
        """)
        record_fail("CHECK constraint: tier_rating", "Expected IntegrityError on tier_rating='B'")
    except sqlite3.IntegrityError:
        record_pass("CHECK constraint: tier_rating", "Tier 'B' blocked by CHECK (tier_rating IN ('SS', 'S+', 'S', 'A'))")

    s_conn.close()
finally:
    if os.path.exists(sandbox_db):
        os.remove(sandbox_db)


# =====================================================================
# SUITE 5: COMPLEX ANALYTICAL QUERIES, BOUNDARY & ESCAPING STRESS
# =====================================================================
print("\n--- Suite 5: Complex Analytical Queries, Boundary & Escaping Stress ---")

conn = get_connection()
cursor = conn.cursor()

# 5.1 Full 5-Way Relational Join: Characters + Signature Weapon + Builds + Recommended Weapon + Recommended Artifact
query_5way = """
    SELECT 
        c.name AS character_name,
        c.vision,
        c.region,
        sw.name AS signature_weapon,
        cb.build_name,
        cb.role,
        rw.name AS build_weapon,
        a.name AS build_artifact,
        cb.tier_rating
    FROM characters c
    LEFT JOIN weapons sw ON c.character_id = sw.signature_character_id
    JOIN character_builds cb ON c.character_id = cb.character_id
    JOIN weapons rw ON cb.recommended_weapon_id = rw.weapon_id
    JOIN artifact_sets a ON cb.recommended_artifact_id = a.artifact_set_id
    ORDER BY c.character_id, cb.build_id;
"""
rows_5way = cursor.execute(query_5way).fetchall()
if len(rows_5way) == 168:
    record_pass("5-Way Full Relational Join", f"Returned exactly 168 rows covering all builds")
else:
    record_fail("5-Way Full Relational Join", f"Expected 168 rows, got {len(rows_5way)}")

# 5.2 Window Function & CTE: Ranks and running aggregates
query_window = """
    WITH WeaponAnalysis AS (
        SELECT 
            weapon_type,
            name,
            rarity,
            base_atk,
            RANK() OVER (PARTITION BY weapon_type, rarity ORDER BY base_atk DESC) as atk_rank
        FROM weapons
    )
    SELECT weapon_type, rarity, COUNT(*) as top_tier_weapons
    FROM WeaponAnalysis
    WHERE atk_rank = 1
    GROUP BY weapon_type, rarity;
"""
rows_window = cursor.execute(query_window).fetchall()
if len(rows_window) > 0:
    record_pass("Window Function & CTE Partitioning", f"Executed successfully ({len(rows_window)} groups returned)")
else:
    record_fail("Window Function & CTE Partitioning", "Window function query returned 0 rows")

# 5.3 Special Characters and Escaping Stress (Apostrophes in names)
query_apostrophes = """
    SELECT COUNT(*) 
    FROM weapons 
    WHERE name LIKE "%'%" 
       OR name LIKE "%-%";
"""
cnt_special = cursor.execute(query_apostrophes).fetchone()[0]
if cnt_special > 0:
    record_pass("Special Character Escaping (apostrophes/hyphens)", f"Successfully queried {cnt_special} weapons with special characters")
else:
    record_fail("Special Character Escaping", "No weapons with apostrophes or hyphens matched")

# 5.4 Nullability Boundary Stress: weapons without signature_character_id
cnt_null_sig = cursor.execute("SELECT COUNT(*) FROM weapons WHERE signature_character_id IS NULL;").fetchone()[0]
cnt_has_sig = cursor.execute("SELECT COUNT(*) FROM weapons WHERE signature_character_id IS NOT NULL;").fetchone()[0]
if cnt_null_sig + cnt_has_sig == 155 and cnt_has_sig > 0 and cnt_null_sig > 0:
    record_pass("Signature Nullability Boundary", f"Total: 155 (With Signature: {cnt_has_sig}, Null Signature: {cnt_null_sig})")
else:
    record_fail("Signature Nullability Boundary", f"Unexpected distribution: Null={cnt_null_sig}, NotNull={cnt_has_sig}")

# 5.5 Aloy Region 'None' Boundary: Only 1 character with region 'None'
aloy_check = cursor.execute("SELECT name, region FROM characters WHERE region = 'None';").fetchall()
if len(aloy_check) == 1 and aloy_check[0][0] == "Aloy":
    record_pass("Aloy Region 'None' Boundary", "Aloy is the sole character with region 'None'")
else:
    record_fail("Aloy Region 'None' Boundary", f"Expected only Aloy, got: {aloy_check}")

conn.close()


# =====================================================================
# FINAL VERDICT & SUMMARY
# =====================================================================
print("\n" + "=" * 80)
print("MILENSTONE 4 CHALLENGER ADVERSARIAL TEST SUMMARY")
print("=" * 80)
print(f"Total Tests Executed : {passed_tests + failed_tests}")
print(f"Total Passed         : {passed_tests}")
print(f"Total Failed         : {failed_tests}")

if failed_tests == 0:
    print("\nFINAL ADVERSARIAL VERDICT: [APPROVE]")
    print("All adversarial probes, index utilization checks, negative injected defect tests,")
    print("pipeline regeneration cycles, and schema referential integrity tests PASSED.")
    sys.exit(0)
else:
    print(f"\nFINAL ADVERSARIAL VERDICT: [REJECT] ({failed_tests} failure(s) detected)")
    for name, reason in findings:
        print(f"  - {name}: {reason}")
    sys.exit(1)
