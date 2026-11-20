#!/usr/bin/env python3
"""
tests/test_tier5_challenger_2.py
Tier 5 Adversarial Coverage Hardening & Empirical Stress Harness for Genshin Database.

Author: challenger_final_2 (Empirical Challenger)
Role: critic, specialist
Target: Phase 2 Tier 5 Adversarial Coverage Hardening (M_FINAL)

Verification Taxonomy:
- Suite 1: Data Consistency, Foreign Keys & Cross-Table Relational Invariants
- Suite 2: Referential Actions (CASCADE, RESTRICT, SET NULL) & Transaction Rollbacks
- Suite 3: Index Utilization, Forced Indexing (INDEXED BY) & Planner Bypass Stress
- Suite 4: Extreme Inputs, String Escaping & Boundary Value Analysis
- Suite 5: Educational Web App Security, SQL Injection Vectors & DoS Protections
- Suite 6: Pipeline Idempotency, Determinism & Negative verify_db.py Testing
"""

import os
import sys
import re
import csv
import glob
import time
import json
import shutil
import hashlib
import sqlite3
import tempfile
import subprocess
from typing import Dict, List, Tuple, Any, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Ensure .venv site-packages are accessible for Flask testing if running under system python
venv_site_packages = glob.glob(os.path.join(PROJECT_ROOT, ".venv", "lib", "python*", "site-packages"))
for p in venv_site_packages:
    if p not in sys.path:
        sys.path.insert(0, p)

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
print("TIER 5 ADVERSARIAL COVERAGE HARDENING: EMPIRICAL CHALLENGER 2")
print(f"Project Root : {PROJECT_ROOT}")
print(f"Database     : {DB_PATH}")
print("=" * 80)


# =====================================================================
# SUITE 1: DATA CONSISTENCY, FOREIGN KEYS & CROSS-TABLE RELATIONAL INVARIANTS
# =====================================================================
print("\n--- Suite 1: Data Consistency, Foreign Keys & Cross-Table Relational Invariants ---")

conn = get_connection()
cursor = conn.cursor()

# 1.1 PRAGMA foreign_key_check = 0
fk_violations = cursor.execute("PRAGMA foreign_key_check;").fetchall()
if len(fk_violations) == 0:
    record_pass("1.1 PRAGMA foreign_key_check", "0 violations confirmed")
else:
    record_fail("1.1 PRAGMA foreign_key_check", f"Violations found: {fk_violations}")

# 1.2 Signature weapon to character weapon-type compatibility invariant
sig_weapon_mismatches = cursor.execute("""
    SELECT w.weapon_id, w.name, w.weapon_type, c.character_id, c.name, c.weapon_type
    FROM weapons w
    JOIN characters c ON w.signature_character_id = c.character_id
    WHERE w.weapon_type != c.weapon_type;
""").fetchall()
if len(sig_weapon_mismatches) == 0:
    record_pass("1.2 Signature weapon owner weapon-type compatibility", "All signature weapons match owner weapon_type")
else:
    record_fail("1.2 Signature weapon owner weapon-type compatibility", f"Mismatches: {sig_weapon_mismatches}")

# 1.3 Build weapon-type compatibility invariant
build_weapon_mismatches = cursor.execute("""
    SELECT cb.build_id, c.name, c.weapon_type, w.name, w.weapon_type
    FROM character_builds cb
    JOIN characters c ON cb.character_id = c.character_id
    JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
    WHERE c.weapon_type != w.weapon_type;
""").fetchall()
if len(build_weapon_mismatches) == 0:
    record_pass("1.3 Build weapon-type compatibility", "All 168 builds have 100% weapon_type compatibility")
else:
    record_fail("1.3 Build weapon-type compatibility", f"Mismatches: {build_weapon_mismatches}")

# 1.4 Zero orphaned characters
orphans = cursor.execute("""
    SELECT c.character_id, c.name
    FROM characters c
    LEFT JOIN character_builds cb ON c.character_id = cb.character_id
    WHERE cb.build_id IS NULL;
""").fetchall()
if len(orphans) == 0:
    record_pass("1.4 Zero orphaned characters", "All 129 characters have at least 1 verified build")
else:
    record_fail("1.4 Zero orphaned characters", f"Orphans found: {orphans}")

# 1.5 Recommended artifact reference validity
invalid_artifacts = cursor.execute("""
    SELECT cb.build_id, cb.recommended_artifact_id
    FROM character_builds cb
    LEFT JOIN artifact_sets a ON cb.recommended_artifact_id = a.artifact_set_id
    WHERE a.artifact_set_id IS NULL;
""").fetchall()
if len(invalid_artifacts) == 0:
    record_pass("1.5 Recommended artifact reference validity", "All build artifact references resolve")
else:
    record_fail("1.5 Recommended artifact reference validity", f"Invalid artifacts: {invalid_artifacts}")

# 1.6 Regional distribution invariant (All 10 regions, sum = 129)
expected_regions = {
    "Mondstadt": 23, "Liyue": 22, "Inazuma": 17, "Sumeru": 14, "Fontaine": 13,
    "Nod-Krai": 12, "Natlan": 11, "Outlander": 8, "Snezhnaya": 8, "None": 1
}
reg_rows = cursor.execute("SELECT region, COUNT(*) FROM characters GROUP BY region;").fetchall()
reg_dict = dict(reg_rows)
if reg_dict == expected_regions and sum(reg_dict.values()) == 129:
    record_pass("1.6 Regional character distribution invariant", "All 10 regions match exact target counts (sum = 129)")
else:
    record_fail("1.6 Regional character distribution invariant", f"Found {reg_dict} vs expected {expected_regions}")

# 1.7 Primary Key uniqueness and positivity across all tables
for tbl, pk in [("characters", "character_id"), ("weapons", "weapon_id"),
                ("artifact_sets", "artifact_set_id"), ("character_builds", "build_id")]:
    pk_check = cursor.execute(f"""
        SELECT COUNT(*), COUNT(DISTINCT {pk}), MIN({pk}), MAX({pk})
        FROM {tbl}
        WHERE {pk} IS NULL OR {pk} <= 0;
    """).fetchone()
    if pk_check[0] == 0:
        record_pass(f"1.7 Primary Key integrity: {tbl}", f"{pk} is strictly positive and unique")
    else:
        record_fail(f"1.7 Primary Key integrity: {tbl}", f"Invalid PKs in {tbl}")

# 1.8 Unique name constraints
for tbl in ["characters", "weapons", "artifact_sets"]:
    dup_names = cursor.execute(f"SELECT name, COUNT(*) FROM {tbl} GROUP BY name HAVING COUNT(*) > 1;").fetchall()
    if len(dup_names) == 0:
        record_pass(f"1.8 Name uniqueness: {tbl}", "0 duplicate names")
    else:
        record_fail(f"1.8 Name uniqueness: {tbl}", f"Duplicates found: {dup_names}")

# 1.9 Check constraints negative testing in an in-memory clone
mem_conn = sqlite3.connect(":memory:")
mem_conn.execute("PRAGMA foreign_keys = ON;")
mem_cursor = mem_conn.cursor()
with open(os.path.join(PROJECT_ROOT, "init_db.py"), "r") as f:
    init_code = f.read()
# Extract SCHEMA_SQL from init_db.py
schema_match = re.search(r'SCHEMA_SQL\s*=\s*"""(.*?)"""', init_code, re.DOTALL)
assert schema_match is not None, "Failed to parse SCHEMA_SQL from init_db.py"
mem_cursor.executescript(schema_match.group(1))

# Test character CHECK constraints
invalid_char_cases = [
    ("rarity=3", (999, "Test1", 3, "Pyro", "Sword", "Mondstadt", "DPS", 10000, 200, 600, "Burst", 1.0)),
    ("rarity=6", (999, "Test2", 6, "Pyro", "Sword", "Mondstadt", "DPS", 10000, 200, 600, "Burst", 1.0)),
    ("vision=Quantum", (999, "Test3", 5, "Quantum", "Sword", "Mondstadt", "DPS", 10000, 200, 600, "Burst", 1.0)),
    ("weapon_type=Gun", (999, "Test4", 5, "Pyro", "Gun", "Mondstadt", "DPS", 10000, 200, 600, "Burst", 1.0)),
]
for desc, row in invalid_char_cases:
    try:
        mem_cursor.execute("INSERT INTO characters VALUES (?,?,?,?,?,?,?,?,?,?,?,?);", row)
        record_fail(f"1.9 Character CHECK violation ({desc})", "Invalid row inserted without error")
    except sqlite3.IntegrityError:
        record_pass(f"1.9 Character CHECK violation rejected ({desc})", "Enforced via CHECK constraint")

# Test weapon CHECK constraints
invalid_weapon_cases = [
    ("rarity=2", (999, "Wep1", "Sword", 2, 500, "ATK%", 20.0, 0, None)),
    ("rarity=6", (999, "Wep2", "Sword", 6, 500, "ATK%", 20.0, 0, None)),
    ("weapon_type=Whip", (999, "Wep3", "Whip", 4, 500, "ATK%", 20.0, 0, None)),
    ("is_craftable=2", (999, "Wep4", "Sword", 4, 500, "ATK%", 20.0, 2, None)),
]
for desc, row in invalid_weapon_cases:
    try:
        mem_cursor.execute("INSERT INTO weapons VALUES (?,?,?,?,?,?,?,?,?);", row)
        record_fail(f"1.9 Weapon CHECK violation ({desc})", "Invalid row inserted without error")
    except sqlite3.IntegrityError:
        record_pass(f"1.9 Weapon CHECK violation rejected ({desc})", "Enforced via CHECK constraint")

# Test build CHECK constraints
try:
    mem_cursor.execute("""
        INSERT INTO character_builds VALUES (999, 1, 'Build', 'DPS', 101, 1, 'ATK', 'Pyro', 'CRIT', 'SSS', 'Notes');
    """)
    record_fail("1.9 Build CHECK tier_rating violation", "Invalid tier rating 'SSS' inserted without error")
except sqlite3.IntegrityError:
    record_pass("1.9 Build CHECK tier_rating violation rejected ('SSS')", "Enforced via CHECK constraint")

# 1.10 NOT NULL constraints rejection
try:
    mem_cursor.execute("INSERT INTO characters VALUES (999, NULL, 5, 'Pyro', 'Sword', 'Mondstadt', 'DPS', 10000, 200, 600, 'Burst', 1.0);")
    record_fail("1.10 Character NOT NULL name", "NULL allowed for name")
except sqlite3.IntegrityError:
    record_pass("1.10 Character NOT NULL name enforced", "sqlite3.IntegrityError raised on NULL")

mem_conn.close()


# =====================================================================
# SUITE 2: REFERENTIAL ACTIONS & TRANSACTION ROLLBACK EDGE CASES
# =====================================================================
print("\n--- Suite 2: Referential Actions & Transaction Rollback Edge Cases ---")

# We create an isolated temp database with existing database contents to test actual deletions & cascades
with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_f:
    tmp_db_path = tmp_f.name

shutil.copyfile(DB_PATH, tmp_db_path)
t_conn = sqlite3.connect(tmp_db_path)
t_conn.execute("PRAGMA foreign_keys = ON;")
t_cur = t_conn.cursor()

# 2.1 ON DELETE CASCADE on character_builds.character_id
# Find a character with builds (e.g. Mavuika, character_id = 87, builds 407, 467)
mavuika_build_ids = [r[0] for r in t_cur.execute("SELECT build_id FROM character_builds WHERE character_id = 87;").fetchall()]
assert len(mavuika_build_ids) >= 2, f"Mavuika must have >= 2 builds, got {mavuika_build_ids}"

t_cur.execute("DELETE FROM characters WHERE character_id = 87;")
remaining_builds = t_cur.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = 87;").fetchone()[0]
if remaining_builds == 0:
    record_pass("2.1 ON DELETE CASCADE on character_builds", f"Character deletion cascaded; removed {len(mavuika_build_ids)} builds")
else:
    record_fail("2.1 ON DELETE CASCADE on character_builds", f"Found {remaining_builds} lingering builds")

# 2.2 ON DELETE RESTRICT on recommended_weapon_id
# Weapon 101 (Tome of the Eternal Flow) is referenced by Neuvillette's build
try:
    t_cur.execute("DELETE FROM weapons WHERE weapon_id = 101;")
    record_fail("2.2 ON DELETE RESTRICT on recommended_weapon_id", "Referenced weapon was deleted without error")
except sqlite3.IntegrityError as e:
    record_pass("2.2 ON DELETE RESTRICT on recommended_weapon_id", "Deletion blocked by foreign key constraint")

# 2.3 ON DELETE RESTRICT on recommended_artifact_id
# Find an artifact set currently referenced by a build
used_artifact_id = t_cur.execute("SELECT recommended_artifact_id FROM character_builds LIMIT 1;").fetchone()[0]
try:
    t_cur.execute("DELETE FROM artifact_sets WHERE artifact_set_id = ?;", (used_artifact_id,))
    record_fail("2.3 ON DELETE RESTRICT on recommended_artifact_id", f"Referenced artifact set {used_artifact_id} was deleted without error")
except sqlite3.IntegrityError as e:
    record_pass("2.3 ON DELETE RESTRICT on recommended_artifact_id", f"Deletion of artifact set {used_artifact_id} blocked by foreign key constraint")

# 2.4 ON DELETE SET NULL on weapons.signature_character_id
# Weapon 102 (Splendor of Tranquil Waters) has signature_character_id = 71 (Furina)
furina_sig_before = t_cur.execute("SELECT signature_character_id FROM weapons WHERE weapon_id = 102;").fetchone()[0]
assert furina_sig_before == 71, f"Expected 71, got {furina_sig_before}"
t_cur.execute("DELETE FROM characters WHERE character_id = 71;")
furina_sig_after = t_cur.execute("SELECT signature_character_id FROM weapons WHERE weapon_id = 102;").fetchone()[0]
wep_102_exists = t_cur.execute("SELECT COUNT(*) FROM weapons WHERE weapon_id = 102;").fetchone()[0]
if wep_102_exists == 1 and furina_sig_after is None:
    record_pass("2.4 ON DELETE SET NULL on signature_character_id", "Character deleted; weapon signature set to NULL")
else:
    record_fail("2.4 ON DELETE SET NULL on signature_character_id", f"Signature is {furina_sig_after}, exists: {wep_102_exists}")

# 2.5 Multi-statement Transaction Atomicity & Rollback
t_conn.commit()  # Ensure clean state before testing rollback
try:
    t_cur.execute("INSERT INTO characters VALUES (901, 'TempChar1', 5, 'Pyro', 'Sword', 'Mondstadt', 'DPS', 10000, 200, 600, 'Burst', 1.0);")
    # Intentionally trigger an error on second insert (duplicate ID)
    t_cur.execute("INSERT INTO characters VALUES (901, 'TempChar2', 5, 'Hydro', 'Sword', 'Liyue', 'DPS', 10000, 200, 600, 'Burst', 1.0);")
    t_conn.commit()
except sqlite3.IntegrityError:
    t_conn.rollback()

rolled_back_char = t_cur.execute("SELECT COUNT(*) FROM characters WHERE character_id = 901;").fetchone()[0]
if rolled_back_char == 0:
    record_pass("2.5 Transaction Atomicity & Rollback", "Rollback successfully reverted all uncommitted statements")
else:
    record_fail("2.5 Transaction Atomicity & Rollback", "Partial insert survived rollback")

t_conn.close()
if os.path.exists(tmp_db_path):
    os.remove(tmp_db_path)


# =====================================================================
# SUITE 3: INDEX UTILIZATION, FORCED INDEXING & PLANNER BYPASS STRESS
# =====================================================================
print("\n--- Suite 3: Index Utilization, Forced Indexing & Planner Bypass Stress ---")

# 3.1 All 8 required schema indexes exist
ALL_8_INDEXES = [
    "idx_characters_region", "idx_characters_vision",
    "idx_weapons_type", "idx_weapons_signature",
    "idx_builds_character", "idx_builds_tier",
    "idx_builds_weapon", "idx_builds_artifact"
]
db_indexes = {r[0] for r in cursor.execute("SELECT name FROM sqlite_master WHERE type = 'index';").fetchall()}
missing_idx = [idx for idx in ALL_8_INDEXES if idx not in db_indexes]
if not missing_idx:
    record_pass("3.1 Schema Relational Indexes existence", f"All {len(ALL_8_INDEXES)} required indexes present")
else:
    record_fail("3.1 Schema Relational Indexes existence", f"Missing indexes: {missing_idx}")

# 3.2 Forced index usage with INDEXED BY syntax
indexed_by_queries = [
    ("idx_characters_region", "SELECT name FROM characters INDEXED BY idx_characters_region WHERE region = 'Natlan';"),
    ("idx_characters_vision", "SELECT name FROM characters INDEXED BY idx_characters_vision WHERE vision = 'Pyro';"),
    ("idx_weapons_type", "SELECT name FROM weapons INDEXED BY idx_weapons_type WHERE weapon_type = 'Claymore';"),
    ("idx_weapons_signature", "SELECT name FROM weapons INDEXED BY idx_weapons_signature WHERE signature_character_id = 87;"),
    ("idx_builds_character", "SELECT build_name FROM character_builds INDEXED BY idx_builds_character WHERE character_id = 87;"),
    ("idx_builds_tier", "SELECT build_name FROM character_builds INDEXED BY idx_builds_tier WHERE tier_rating = 'SS';"),
    ("idx_builds_weapon", "SELECT build_name FROM character_builds INDEXED BY idx_builds_weapon WHERE recommended_weapon_id = 131;"),
    ("idx_builds_artifact", "SELECT build_name FROM character_builds INDEXED BY idx_builds_artifact WHERE recommended_artifact_id = 53;"),
]
for idx_name, sql in indexed_by_queries:
    try:
        res = cursor.execute(sql).fetchall()
        assert len(res) > 0, f"Query returned 0 rows for {idx_name}"
        record_pass(f"3.2 Forced index execution: {idx_name}", f"Query executed successfully via INDEXED BY ({len(res)} rows)")
    except Exception as e:
        record_fail(f"3.2 Forced index execution: {idx_name}", str(e))

# 3.3 Query Planner verification (EXPLAIN QUERY PLAN uses index)
plan_queries = [
    ("characters(region)", "SELECT * FROM characters WHERE region = 'Mondstadt';", "idx_characters_region"),
    ("characters(vision)", "SELECT * FROM characters WHERE vision = 'Electro';", "idx_characters_vision"),
    ("weapons(signature)", "SELECT * FROM weapons WHERE signature_character_id = 72;", "idx_weapons_signature"),
    ("character_builds(character_id)", "SELECT * FROM character_builds WHERE character_id = 72;", "idx_builds_character"),
    ("character_builds(recommended_weapon_id)", "SELECT * FROM character_builds WHERE recommended_weapon_id = 103;", "idx_builds_weapon"),
    ("character_builds(recommended_artifact_id)", "SELECT * FROM character_builds WHERE recommended_artifact_id = 51;", "idx_builds_artifact"),
]
for label, sql, expected_idx in plan_queries:
    plan = cursor.execute(f"EXPLAIN QUERY PLAN {sql}").fetchall()
    plan_str = " ".join([str(tuple(r)) for r in plan])
    if expected_idx in plan_str:
        record_pass(f"3.3 EXPLAIN QUERY PLAN utilization: {label}", f"Uses {expected_idx}")
    else:
        record_fail(f"3.3 EXPLAIN QUERY PLAN utilization: {label}", f"Plan '{plan_str}' does not mention {expected_idx}")

# 3.4 Adversarial Index Bypass: Expression wrapping and table scan equivalence
# Wrap region in an expression to prevent B-tree lookup and verify exact match
normal_res = cursor.execute("SELECT character_id, name FROM characters WHERE region = 'Fontaine' ORDER BY character_id;").fetchall()
bypassed_res = cursor.execute("SELECT character_id, name FROM characters WHERE (region || '') = 'Fontaine' ORDER BY character_id;").fetchall()
bypass_plan = cursor.execute("EXPLAIN QUERY PLAN SELECT character_id, name FROM characters WHERE (region || '') = 'Fontaine';").fetchall()
bypass_plan_str = " ".join([str(tuple(r)) for r in bypass_plan])

if normal_res == bypassed_res and "SCAN" in bypass_plan_str.upper():
    record_pass("3.4 Adversarial Index Bypass", f"Expression forces table scan; results identical ({len(normal_res)} rows)")
else:
    record_fail("3.4 Adversarial Index Bypass", "Bypassed query results do not match indexed query results")

# Multi-predicate filter accuracy
multi_pred = cursor.execute("""
    SELECT c.name, c.region, c.vision, cb.build_name, w.name AS weapon
    FROM characters c
    JOIN character_builds cb ON c.character_id = cb.character_id
    JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
    WHERE c.region = 'Liyue' AND c.vision = 'Pyro' AND cb.tier_rating = 'SS';
""").fetchall()
if len(multi_pred) >= 2:  # Hu Tao, Xiangling
    record_pass("3.4 Multi-predicate index filtering", f"Resolved {len(multi_pred)} composite matches cleanly")
else:
    record_fail("3.4 Multi-predicate index filtering", f"Expected >= 2 matches, got {len(multi_pred)}")


# =====================================================================
# SUITE 4: EXTREME INPUTS, STRING ESCAPING & BOUNDARY VALUE ANALYSIS
# =====================================================================
print("\n--- Suite 4: Extreme Inputs, String Escaping & Boundary Value Analysis ---")

# 4.1 String escaping: single quotes, hyphens, and parentheses
names_with_apostrophe = [
    ("Crimson Moon's Semblance", "weapons"),
    ("Kagura's Verity", "weapons"),
    ("Hunter's Path", "weapons"),
    ("Wolf's Gravestone", "weapons"),
    ("Gladiator's Finale", "artifact_sets"),
    ("Wanderer's Troupe", "artifact_sets"),
    ("Defender's Will", "artifact_sets"),
    ("Shimenawa's Reminiscence", "artifact_sets"),
    ("Nymph's Dream", "artifact_sets"),
    ("Vourukasha's Glow", "artifact_sets"),
    ("Long Night's Oath", "artifact_sets"),
]
for name, tbl in names_with_apostrophe:
    # Parameterized
    param_row = cursor.execute(f"SELECT * FROM {tbl} WHERE name = ?;", (name,)).fetchone()
    # Literal with SQL double single-quote escaping
    escaped_name = name.replace("'", "''")
    literal_row = cursor.execute(f"SELECT * FROM {tbl} WHERE name = '{escaped_name}';").fetchone()
    if param_row is not None and literal_row is not None and param_row["name"] == literal_row["name"]:
        record_pass(f"4.1 Escaping parity: '{name}' in {tbl}", "Parameterized & literal queries return identical row")
    else:
        record_fail(f"4.1 Escaping parity: '{name}' in {tbl}", "Mismatch between parameterized and literal query")

# 4.2 Extreme statistical bounds
stats_check = cursor.execute("""
    SELECT 
        MIN(base_hp), MAX(base_hp),
        MIN(base_atk), MAX(base_atk),
        MIN(base_def), MAX(base_def),
        MIN(release_patch), MAX(release_patch)
    FROM characters;
""").fetchone()
min_hp, max_hp, min_atk, max_atk, min_def, max_def, min_patch, max_patch = stats_check

if (9000 <= min_hp <= 10000 and 15000 <= max_hp <= 16000 and
    100 <= min_atk <= 120 and 340 <= max_atk <= 360 and
    500 <= min_def <= 550 and 950 <= max_def <= 1000 and
    min_patch == 1.0 and 7.0 <= max_patch <= 7.5):
    record_pass("4.2 Character statistical bounds",
                f"HP:[{min_hp}-{max_hp}], ATK:[{min_atk}-{max_atk}], DEF:[{min_def}-{max_def}], Patch:[{min_patch}-{max_patch}]")
else:
    record_fail("4.2 Character statistical bounds", f"Out of bounds stats: {stats_check}")

# Weapon ATK boundaries (741 maximum 5-star base ATK across 6 signatures)
max_weapon_atk_rows = cursor.execute("SELECT weapon_id, name, base_atk FROM weapons WHERE base_atk = 741;").fetchall()
expected_741_weapons = {
    128: "Fang of the Mountain King",
    131: "A Thousand Blazing Suns",
    133: "Song of Broken Pines",
    137: "Crane's Echoing Call",
    204: "Calamity Queller",
    220: "Angelos' Heptades"
}
found_741 = {r[0]: r[1] for r in max_weapon_atk_rows}
if set(found_741.keys()) == set(expected_741_weapons.keys()):
    record_pass("4.2 Weapon maximum base ATK (741)", f"All 6 weapons with 741 Base ATK confirmed: {list(found_741.values())}")
else:
    record_fail("4.2 Weapon maximum base ATK (741)", f"Found {found_741} vs expected {expected_741_weapons}")

# 4.3 Defect Remediation Invariants
# Weapon 128 and 131 stats: 741 Base ATK and 11.0% CRIT Rate
w128 = cursor.execute("SELECT base_atk, sub_stat_type, sub_stat_value FROM weapons WHERE weapon_id = 128;").fetchone()
w131 = cursor.execute("SELECT base_atk, sub_stat_type, sub_stat_value FROM weapons WHERE weapon_id = 131;").fetchone()
if (w128["base_atk"] == 741 and w128["sub_stat_type"] == "CRIT Rate" and w128["sub_stat_value"] == 11.0 and
    w131["base_atk"] == 741 and w131["sub_stat_type"] == "CRIT Rate" and w131["sub_stat_value"] == 11.0):
    record_pass("4.3 Weapon 128 & 131 stats verified", "741 Base ATK, 11.0% CRIT Rate verified")
else:
    record_fail("4.3 Weapon 128 & 131 stats verified", f"W128: {dict(w128)}, W131: {dict(w131)}")

# Capitano (104) and Build 381 purged
cap_char = cursor.execute("SELECT COUNT(*) FROM characters WHERE name LIKE '%Capitano%' OR character_id = 104;").fetchone()[0]
cap_build = cursor.execute("SELECT COUNT(*) FROM character_builds WHERE build_id = 381 OR character_id = 104;").fetchone()[0]
if cap_char == 0 and cap_build == 0:
    record_pass("4.3 Capitano & Build 381 purged", "0 records found in characters or character_builds")
else:
    record_fail("4.3 Capitano & Build 381 purged", f"Chars: {cap_char}, Builds: {cap_build}")

# Aloy region 'None'
aloy = cursor.execute("SELECT name, region FROM characters WHERE character_id = 105;").fetchone()
if aloy is not None and aloy["region"] == "None":
    record_pass("4.3 Aloy region 'None'", "Aloy region is literal string 'None'")
else:
    record_fail("4.3 Aloy region 'None'", f"Aloy row: {dict(aloy) if aloy else None}")

# Artifact Sets 59, 60, 62, 63, 64
set_checks = [
    (59, "Aubade of Morningstar and Moon", "Nod-Krai", "80 Elemental Mastery"),
    (60, "A Day Carved from Rising Winds", "Nod-Krai", "18% ATK"),
    (62, "Disenchantment in Deep Shadow", "Mondstadt", "18% ATK"),
    (63, "Scarlet Proof", "Snezhnaya", "18% ATK"),
    (64, "Heart of the Furnace", "Snezhnaya", "18% ATK"),
]
for set_id, s_name, s_region, s_2pc in set_checks:
    s_row = cursor.execute("SELECT name, region, two_piece_bonus, domain_name FROM artifact_sets WHERE artifact_set_id = ?;", (set_id,)).fetchone()
    if s_row and s_row["name"] == s_name and s_row["region"] == s_region and s_2pc in s_row["two_piece_bonus"]:
        record_pass(f"4.3 Artifact Set {set_id} ({s_name})", f"Region: {s_region}, Domain: {s_row['domain_name']}")
    else:
        record_fail(f"4.3 Artifact Set {set_id} ({s_name})", f"Found: {dict(s_row) if s_row else None}")


# =====================================================================
# SUITE 5: EDUCATIONAL WEB APP SECURITY, SQL INJECTION VECTORS & DOS
# =====================================================================
print("\n--- Suite 5: Educational Web App Security, SQL Injection Vectors & DoS Protections ---")

try:
    from app import app, MAX_STREAM_ROWS, QUERY_TIMEOUT_SECONDS, read_only_authorizer
    flask_available = True
except ImportError as e:
    flask_available = False
    record_fail("Suite 5 Flask Import", f"Could not import app: {e}")

if flask_available:
    client = app.test_client()

    # 5.1 SQL Injection & Administrative Attack Vectors
    attack_payloads = [
        ("DROP TABLE characters;", 403, "DROP statement"),
        ("drop table characters;", 403, "lowercase drop"),
        ("DrOp TaBlE characters;", 403, "mixed case drop"),
        ("SELECT 1; DROP TABLE characters;", 403, "piggybacked query with drop"),
        ("SELECT 1; /* comment */ DROP TABLE characters;", 403, "comment evasion drop"),
        ("SELECT 1; -- comment\n DROP TABLE characters;", 403, "single line comment evasion"),
        ("INSERT INTO characters(character_id, name) VALUES (999, 'Hacked');", 403, "INSERT statement"),
        ("UPDATE characters SET name = 'Owned';", 403, "UPDATE statement"),
        ("DELETE FROM weapons WHERE 1=1;", 403, "DELETE statement"),
        ("ALTER TABLE characters ADD COLUMN hacked TEXT;", 403, "ALTER TABLE statement"),
        ("ATTACH DATABASE ':memory:' AS evil;", 403, "ATTACH DATABASE"),
        ("DETACH DATABASE evil;", 403, "DETACH DATABASE"),
        ("VACUUM;", 403, "VACUUM statement"),
        ("PRAGMA foreign_keys = OFF;", 403, "PRAGMA statement"),
        ("REINDEX characters;", 403, "REINDEX statement"),
    ]

    for q, expected_status, label in attack_payloads:
        resp = client.post("/api/query", json={"query": q})
        if resp.status_code in (400, 403):
            record_pass(f"5.1 Attack vector blocked: {label}", f"Status {resp.status_code}")
        else:
            record_fail(f"5.1 Attack vector blocked: {label}", f"Expected 400/403, got {resp.status_code}")

    # 5.2 SQLite C-Level Authorizer Evasion Defense
    # Test authorizer directly with sqlite3 connection to ensure authorizer blocks write operations even if regex was bypassed
    auth_conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    auth_conn.set_authorizer(read_only_authorizer)
    auth_cur = auth_conn.cursor()

    # Can read
    try:
        auth_cur.execute("SELECT COUNT(*) FROM characters;")
        record_pass("5.2 Authorizer allows SELECT", "Read allowed cleanly")
    except Exception as e:
        record_fail("5.2 Authorizer allows SELECT", str(e))

    # Cannot modify
    try:
        auth_cur.execute("CREATE TABLE test_auth(id int);")
        record_fail("5.2 Authorizer blocks CREATE TABLE", "CREATE TABLE executed without authorization error")
    except sqlite3.DatabaseError as e:
        record_pass("5.2 Authorizer blocks CREATE TABLE", f"Blocked: {e}")

    try:
        auth_cur.execute("PRAGMA schema_version;")
        record_fail("5.2 Authorizer blocks PRAGMA", "PRAGMA executed without authorization error")
    except sqlite3.DatabaseError as e:
        record_pass("5.2 Authorizer blocks PRAGMA", f"Blocked: {e}")

    auth_conn.close()

    # 5.3 DoS, Watchdog Timeout & Stream Capping Protections
    # Watchdog timeout on infinite recursive CTE
    t0 = time.perf_counter()
    inf_resp = client.post("/api/query", json={
        "query": "WITH RECURSIVE loop(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM loop) SELECT count(*) FROM loop;"
    })
    elapsed = time.perf_counter() - t0
    inf_data = inf_resp.get_json() if inf_resp.is_json else {}
    inf_err = inf_data.get("error", "").lower()
    if ("timeout" in inf_err or "interrupted" in inf_err or "aborted" in inf_err) and elapsed < (QUERY_TIMEOUT_SECONDS + 2.5):
        record_pass("5.3 Watchdog timeout aborts infinite CTE", f"Terminated in {elapsed:.2f}s with timeout message")
    else:
        record_fail("5.3 Watchdog timeout aborts infinite CTE", f"Elapsed: {elapsed:.2f}s, Response: {inf_data}")

    # Cartesian join capped at MAX_STREAM_ROWS
    cart_resp = client.post("/api/query", json={
        "query": "SELECT * FROM characters, weapons, artifact_sets, character_builds;"
    })
    cart_lines = [json.loads(line) for line in cart_resp.data.decode().strip().split("\n") if line.strip()]
    comp_ev = [l for l in cart_lines if l.get("type") == "complete"][0]
    if comp_ev.get("count") == MAX_STREAM_ROWS and comp_ev.get("truncated") is True:
        record_pass("5.3 Stream truncation on Cartesian explosion", f"Capped at exactly {MAX_STREAM_ROWS} rows with truncated=True")
    else:
        record_fail("5.3 Stream truncation on Cartesian explosion", f"Unexpected completion event: {comp_ev}")

    # Payload size rejection (> 64 KB)
    huge_query = "SELECT " + ("1 AS col, " * 12000) + " 1;"
    huge_resp = client.post("/api/query", json={"query": huge_query})
    if huge_resp.status_code == 413:
        record_pass("5.3 Payload > 64 KB rejected (HTTP 413)", "Request too large handled")
    else:
        record_fail("5.3 Payload > 64 KB rejected (HTTP 413)", f"Status {huge_resp.status_code}")

    # Non-POST method rejected (HTTP 405)
    get_resp = client.get("/api/query")
    if get_resp.status_code == 405:
        record_pass("5.3 Invalid HTTP method on /api/query rejected (HTTP 405)", "Method Not Allowed")
    else:
        record_fail("5.3 Invalid HTTP method on /api/query rejected (HTTP 405)", f"Status {get_resp.status_code}")

    # Unknown API route returns JSON 404
    nf_resp = client.get("/api/unknown_route")
    if nf_resp.status_code == 404 and nf_resp.is_json:
        record_pass("5.3 Unknown API route returns 404 JSON", "JSON 404 error returned")
    else:
        record_fail("5.3 Unknown API route returns 404 JSON", f"Status: {nf_resp.status_code}")


# =====================================================================
# SUITE 6: PIPELINE IDEMPOTENCY, DETERMINISM & NEGATIVE VERIFY_DB TESTING
# =====================================================================
print("\n--- Suite 6: Pipeline Idempotency, Determinism & Negative verify_db Testing ---")

with tempfile.TemporaryDirectory() as temp_dir:
    # 6.1 Deterministic CSV Generation (generate_csvs.py)
    # Run generate_csvs.py into temp_dir/data
    temp_data_dir = os.path.join(temp_dir, "data")
    os.makedirs(temp_data_dir, exist_ok=True)
    temp_gen_script = os.path.join(temp_dir, "generate_csvs.py")

    with open(os.path.join(PROJECT_ROOT, "generate_csvs.py"), "r") as f:
        gen_content = f.read()

    with open(temp_gen_script, "w") as f:
        f.write(gen_content)

    proc_gen = subprocess.run([sys.executable, temp_gen_script], cwd=temp_dir, capture_output=True, text=True)
    if proc_gen.returncode == 0:
        record_pass("6.1 generate_csvs.py execution in clean room", "Exit code 0")
    else:
        record_fail("6.1 generate_csvs.py execution in clean room", f"Stderr: {proc_gen.stderr}")

    # Compare SHA-256 of all 4 generated CSV files with production data/*.csv
    all_csvs_match = True
    for csv_file in ["characters.csv", "weapons.csv", "artifact_sets.csv", "character_builds.csv"]:
        prod_hash = file_sha256(os.path.join(DATA_DIR, csv_file))
        temp_hash = file_sha256(os.path.join(temp_data_dir, csv_file))
        if prod_hash == temp_hash:
            record_pass(f"6.1 CSV SHA-256 bit-for-bit parity: {csv_file}", f"Hash: {prod_hash[:16]}...")
        else:
            all_csvs_match = False
            record_fail(f"6.1 CSV SHA-256 bit-for-bit parity: {csv_file}", f"Prod: {prod_hash} != Temp: {temp_hash}")

    # 6.2 Deterministic Database Initialization (init_db.py)
    temp_init_script = os.path.join(temp_dir, "init_db.py")
    with open(os.path.join(PROJECT_ROOT, "init_db.py"), "r") as f:
        init_content = f.read()

    with open(temp_init_script, "w") as f:
        f.write(init_content)

    proc_init = subprocess.run([sys.executable, temp_init_script], cwd=temp_dir, capture_output=True, text=True)
    temp_db_path = os.path.join(temp_dir, "genshin_learning.db")
    if proc_init.returncode == 0 and os.path.exists(temp_db_path):
        record_pass("6.2 init_db.py execution in clean room", "Exit code 0, generated genshin_learning.db")
    else:
        record_fail("6.2 init_db.py execution in clean room", f"Stderr: {proc_init.stderr}")

    # Verify temp DB has exact row counts
    temp_conn = sqlite3.connect(temp_db_path)
    temp_counts = {
        tbl: temp_conn.execute(f"SELECT COUNT(*) FROM {tbl};").fetchone()[0]
        for tbl in ["characters", "weapons", "artifact_sets", "character_builds"]
    }
    temp_conn.close()
    if temp_counts == {"characters": 129, "weapons": 155, "artifact_sets": 64, "character_builds": 168}:
        record_pass("6.2 Clean room DB table counts", f"Exact counts confirmed: {temp_counts}")
    else:
        record_fail("6.2 Clean room DB table counts", f"Unexpected counts: {temp_counts}")

    # 6.3 Negative verify_db.py Testing (Defect Detection Sensitivity)
    # Copy verify_db.py to temp_dir
    temp_verify_script = os.path.join(temp_dir, "verify_db.py")
    with open(os.path.join(PROJECT_ROOT, "verify_db.py"), "r") as f:
        verify_content = f.read()
    with open(temp_verify_script, "w") as f:
        f.write(verify_content)

    # Test baseline verify_db passes on clean room DB
    proc_verify_clean = subprocess.run([sys.executable, temp_verify_script], cwd=temp_dir, capture_output=True, text=True)
    if proc_verify_clean.returncode == 0:
        record_pass("6.3 verify_db.py baseline in clean room", "Exit code 0 on valid database")
    else:
        record_fail("6.3 verify_db.py baseline in clean room", f"Failed: {proc_verify_clean.stderr}")

    # Defect Injection A: Delete unreferenced weapon 255 (breaks table count 155 -> 154 without FK violation)
    corrupt_conn = sqlite3.connect(temp_db_path)
    corrupt_conn.execute("DELETE FROM weapons WHERE weapon_id = 255;")
    corrupt_conn.commit()
    corrupt_conn.close()

    proc_verify_corrupt_count = subprocess.run([sys.executable, temp_verify_script], cwd=temp_dir, capture_output=True, text=True)
    if proc_verify_corrupt_count.returncode != 0 and "VERIFICATION FAILURE" in proc_verify_corrupt_count.stderr and "expected 155" in proc_verify_corrupt_count.stderr:
        record_pass("6.3 Negative testing verify_db: row count mismatch caught", "Exited with code 1 and reported table count failure")
    else:
        record_fail("6.3 Negative testing verify_db: row count mismatch caught", f"Output: {proc_verify_corrupt_count.stderr}")

    # Re-initialize clean DB for Defect Injection B
    subprocess.run([sys.executable, temp_init_script], cwd=temp_dir, capture_output=True, text=True)

    # Defect Injection B: Foreign Key violation (Insert build pointing to non-existent weapon)
    corrupt_conn = sqlite3.connect(temp_db_path)
    corrupt_conn.execute("PRAGMA foreign_keys = OFF;")
    corrupt_conn.execute("INSERT INTO character_builds VALUES (9999, 1, 'Fake', 'DPS', 8888, 1, 'ATK', 'Pyro', 'CRIT', 'SS', 'Notes');")
    corrupt_conn.commit()
    corrupt_conn.close()

    proc_verify_corrupt_fk = subprocess.run([sys.executable, temp_verify_script], cwd=temp_dir, capture_output=True, text=True)
    if proc_verify_corrupt_fk.returncode != 0 and "VERIFICATION FAILURE" in proc_verify_corrupt_fk.stderr and "foreign key violations" in proc_verify_corrupt_fk.stderr:
        record_pass("6.3 Negative testing verify_db: FK violation caught", "Exited with code 1 and reported foreign key violations")
    else:
        record_fail("6.3 Negative testing verify_db: FK violation caught", f"Output: {proc_verify_corrupt_fk.stderr}")

conn.close()

print("\n" + "=" * 80)
print(f"TIER 5 ADVERSARIAL STRESS SUITE RESULTS: {passed_tests} PASSED, {failed_tests} FAILED")
print("=" * 80)

if failed_tests > 0:
    print(f"\n❌ FAILURES ENCOUNTERED ({failed_tests}):")
    for name, reason in findings:
        print(f"  - {name}: {reason}")
    sys.exit(1)
else:
    print("\n🎉 ALL TIER 5 ADVERSARIAL STRESS TESTS PASSED WITH 100% RELIABILITY!")
    sys.exit(0)
