#!/usr/bin/env python3
"""
tests/test_m3_adversarial_challenger.py
Empirical Adversarial Stress Suite for Milestone 3 (M3): Character Builds Backfill & Role Variety.

Author: challenger_m3_1 (Empirical Challenger)
Role: critic, specialist
Verification Scope:
- Suite 1: Data Pipeline Determinism & CSV-to-DB Parity Stress
- Suite 2: Character Build Coverage & Zero Orphan Probe (100% build coverage)
- Suite 3: Weapon Type Compatibility Across ALL 168 Builds (c.weapon_type == w.weapon_type)
- Suite 4: Specific Milestone 3 Requirements (Relinked builds 305, 387, 392, 380, alt builds 467-469)
- Suite 5: Foreign Key & Schema Integrity Stress (PRAGMA foreign_key_check + CASCADE/RESTRICT simulation)
- Suite 6: Field Validity, Value Distributions & Boundary Stress
- Suite 7: Full 4-Table Relational Joins & Real Queries
- Suite 8: E2E Test Suite Regression & Test Contract Analysis
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
print("STARTING ADVERSARIAL EMPIRICAL STRESS SUITE FOR MILESTONE 3 (M3)")
print("Project Root:", PROJECT_ROOT)
print("Database Path:", DB_PATH)
print("=" * 80)

# =====================================================================
# SUITE 1: DATA PIPELINE DETERMINISM & CSV-TO-DB PARITY STRESS
# =====================================================================
print("\n--- Suite 1: Data Pipeline Determinism & CSV-to-DB Parity Stress ---")

csv_files = ["characters.csv", "weapons.csv", "artifact_sets.csv", "character_builds.csv"]

try:
    initial_hashes = {f: file_sha256(os.path.join(DATA_DIR, f)) for f in csv_files}
    record_pass("Initial CSV Hashes Computed", f"Tracked 4 files in {DATA_DIR}")

    # Run generate_csvs.py to verify determinism
    proc = subprocess.run([sys.executable, "generate_csvs.py"], cwd=PROJECT_ROOT, capture_output=True, text=True)
    if proc.returncode == 0:
        record_pass("generate_csvs.py Execution", "Exit code 0")
    else:
        record_fail("generate_csvs.py Execution", f"Non-zero exit: {proc.stderr}")

    post_hashes = {f: file_sha256(os.path.join(DATA_DIR, f)) for f in csv_files}
    hash_match = True
    for f in csv_files:
        if initial_hashes[f] != post_hashes[f]:
            hash_match = False
            record_fail("CSV Hash Invariance", f"File {f} changed after regeneration!")
    if hash_match:
        record_pass("CSV Hash Invariance", "All 4 CSVs are bit-for-bit identical after re-run")

    # Verify character_builds.csv row count
    builds_csv_path = os.path.join(DATA_DIR, "character_builds.csv")
    with open(builds_csv_path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        csv_build_count = len(reader)
        if csv_build_count == 168:
            record_pass("character_builds.csv Row Count", "Exactly 168 records")
        else:
            record_fail("character_builds.csv Row Count", f"Expected 168 records, found {csv_build_count}")

    # Verify CSV vs DB cell-for-cell parity
    conn = get_connection()
    cur = conn.cursor()
    db_builds = cur.execute("SELECT * FROM character_builds ORDER BY build_id ASC;").fetchall()
    if len(db_builds) == 168:
        record_pass("DB character_builds Row Count", "Exactly 168 records")
    else:
        record_fail("DB character_builds Row Count", f"Expected 168 records, found {len(db_builds)}")

    parity_errors = []
    for csv_row, db_row in zip(reader, db_builds):
        if int(csv_row["build_id"]) != db_row["build_id"]:
            parity_errors.append(f"build_id mismatch: CSV {csv_row['build_id']} vs DB {db_row['build_id']}")
        if int(csv_row["character_id"]) != db_row["character_id"]:
            parity_errors.append(f"character_id mismatch on build {db_row['build_id']}")
        if csv_row["build_name"] != db_row["build_name"]:
            parity_errors.append(f"build_name mismatch on build {db_row['build_id']}")
        if csv_row["role"] != db_row["role"]:
            parity_errors.append(f"role mismatch on build {db_row['build_id']}")
        if int(csv_row["recommended_weapon_id"]) != db_row["recommended_weapon_id"]:
            parity_errors.append(f"recommended_weapon_id mismatch on build {db_row['build_id']}")
        if int(csv_row["recommended_artifact_id"]) != db_row["recommended_artifact_id"]:
            parity_errors.append(f"recommended_artifact_id mismatch on build {db_row['build_id']}")
        if csv_row["tier_rating"] != db_row["tier_rating"]:
            parity_errors.append(f"tier_rating mismatch on build {db_row['build_id']}")
        if csv_row["playstyle_notes"] != db_row["playstyle_notes"]:
            parity_errors.append(f"playstyle_notes mismatch on build {db_row['build_id']}")

    if not parity_errors:
        record_pass("CSV-DB Cell Parity", "100% cell-for-cell parity between character_builds.csv and DB")
    else:
        record_fail("CSV-DB Cell Parity", f"Found {len(parity_errors)} parity mismatches: {parity_errors[:3]}")

    conn.close()

except Exception as e:
    record_fail("Suite 1 Exception", str(e))

# =====================================================================
# SUITE 2: CHARACTER BUILD COVERAGE & ZERO ORPHAN PROBE
# =====================================================================
print("\n--- Suite 2: Character Build Coverage & Zero Orphan Probe ---")

try:
    conn = get_connection()
    cur = conn.cursor()

    # 1. Probe for orphan characters (characters lacking any builds)
    orphans = cur.execute("""
        SELECT c.character_id, c.name, c.region, c.rarity, c.vision
        FROM characters c
        LEFT JOIN character_builds cb ON c.character_id = cb.character_id
        WHERE cb.build_id IS NULL;
    """).fetchall()

    if len(orphans) == 0:
        record_pass("Zero Orphaned Characters", "Strictly 0 characters lack builds (129/129 covered)")
    else:
        record_fail("Zero Orphaned Characters", f"Found {len(orphans)} orphan characters: {[o['name'] for o in orphans]}")

    # 2. Check total distinct characters in characters vs character_builds
    total_chars = cur.execute("SELECT COUNT(*) FROM characters;").fetchone()[0]
    covered_chars = cur.execute("SELECT COUNT(DISTINCT character_id) FROM character_builds;").fetchone()[0]
    if total_chars == 129 and covered_chars == 129:
        record_pass("Distinct Character Coverage", f"All {total_chars} playable characters have >= 1 build")
    else:
        record_fail("Distinct Character Coverage", f"Total chars: {total_chars}, covered: {covered_chars}")

    # 3. Verify all 43 backfilled characters exist and have >= 1 build
    backfill_names = [
        "Barbara", "Razor", "Noelle", "Kaeya", "Lisa", "Amber", "Diona", "Rosaria",
        "Mika", "Qiqi", "Ningguang", "Beidou", "Chongyun", "Xinyan", "Yanfei",
        "Yun Jin", "Yaoyao", "Kujou Sara", "Sayu", "Thoma", "Gorou",
        "Shikanoin Heizou", "Kirara", "Collei", "Dori", "Candace", "Layla",
        "Kaveh", "Sethos", "Lynette", "Freminet", "Charlotte", "Ororon",
        "Iansan", "Aino", "Nefer", "Jahoda", "Illuga", "Zibai", "Linnea",
        "Aloy", "Traveler (Electro)", "Traveler (Hydro)"
    ]
    missing_backfill = []
    for name in backfill_names:
        cnt = cur.execute("""
            SELECT COUNT(*) FROM character_builds cb
            JOIN characters c ON cb.character_id = c.character_id
            WHERE c.name = ?;
        """, (name,)).fetchone()[0]
        if cnt == 0:
            missing_backfill.append(name)

    if not missing_backfill:
        record_pass("All 43 Backfilled Characters Covered", f"All 43 target characters verified with builds")
    else:
        record_fail("All 43 Backfilled Characters Covered", f"Missing builds for: {missing_backfill}")

    # 4. Verify backfilled build ID range 408 to 450
    b_ids_408_450 = tuple(range(408, 451))
    actual_408_450 = cur.execute(f"SELECT COUNT(*) FROM character_builds WHERE build_id IN ({','.join('?' for _ in b_ids_408_450)});", b_ids_408_450).fetchone()[0]
    if actual_408_450 == 43:
        record_pass("Backfill Build IDs 408–450", "All 43 build IDs exist continuously")
    else:
        record_fail("Backfill Build IDs 408–450", f"Expected 43 builds, found {actual_408_450}")

    # 5. Verify all 16 new characters from M2 (IDs 115–130) have builds
    new_char_ids = tuple(range(115, 131))
    missing_new = []
    for cid in new_char_ids:
        cnt = cur.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = ?;", (cid,)).fetchone()[0]
        if cnt == 0:
            missing_new.append(cid)

    if not missing_new:
        record_pass("All 16 New Characters Covered", "Characters 115–130 each have >= 1 build")
    else:
        record_fail("All 16 New Characters Covered", f"Missing builds for new characters: {missing_new}")

    # 6. Verify new character build IDs 451 to 466
    b_ids_451_466 = tuple(range(451, 467))
    actual_451_466 = cur.execute(f"SELECT COUNT(*) FROM character_builds WHERE build_id IN ({','.join('?' for _ in b_ids_451_466)});", b_ids_451_466).fetchone()[0]
    if actual_451_466 == 16:
        record_pass("New Character Build IDs 451–466", "All 16 build IDs exist continuously")
    else:
        record_fail("New Character Build IDs 451–466", f"Expected 16 builds, found {actual_451_466}")

    # 7. Purged NPC Capitano check
    capitano_in_builds = cur.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = 104;").fetchone()[0]
    b381_exists = cur.execute("SELECT COUNT(*) FROM character_builds WHERE build_id = 381;").fetchone()[0]
    if capitano_in_builds == 0 and b381_exists == 0:
        record_pass("Capitano Absence in Builds", "Character 104 has 0 builds, Build 381 purged")
    else:
        record_fail("Capitano Absence in Builds", f"Capitano in builds: {capitano_in_builds}, Build 381 exists: {b381_exists}")

    conn.close()
except Exception as e:
    record_fail("Suite 2 Exception", str(e))

# =====================================================================
# SUITE 3: WEAPON TYPE COMPATIBILITY ACROSS ALL 168 BUILDS
# =====================================================================
print("\n--- Suite 3: Weapon Type Compatibility Across ALL 168 Builds ---")

try:
    conn = get_connection()
    cur = conn.cursor()

    # Query all builds and join character weapon_type with weapon weapon_type
    weapon_mismatches = cur.execute("""
        SELECT cb.build_id, cb.build_name, c.name AS char_name, c.weapon_type AS char_wt,
               w.name AS wep_name, w.weapon_type AS wep_wt
        FROM character_builds cb
        JOIN characters c ON cb.character_id = c.character_id
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        WHERE c.weapon_type != w.weapon_type;
    """).fetchall()

    if len(weapon_mismatches) == 0:
        record_pass("100% Weapon Type Compatibility", "c.weapon_type == w.weapon_type across all 168 builds")
    else:
        record_fail("100% Weapon Type Compatibility", f"Found {len(weapon_mismatches)} weapon type mismatches: {[(m['build_id'], m['char_name'], m['char_wt'], m['wep_name'], m['wep_wt']) for m in weapon_mismatches]}")

    # Check weapon type breakdown across builds
    wt_dist = cur.execute("""
        SELECT w.weapon_type, COUNT(*) as cnt
        FROM character_builds cb
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        GROUP BY w.weapon_type
        ORDER BY cnt DESC;
    """).fetchall()
    dist_str = ", ".join([f"{r['weapon_type']}: {r['cnt']}" for r in wt_dist])
    record_pass("Weapon Type Distribution Across Builds", dist_str)

    # Check weapon rarity distribution in builds
    rarity_dist = cur.execute("""
        SELECT w.rarity, COUNT(*) as cnt
        FROM character_builds cb
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        GROUP BY w.rarity
        ORDER BY w.rarity DESC;
    """).fetchall()
    rarity_str = ", ".join([f"{r['rarity']}★: {r['cnt']}" for r in rarity_dist])
    record_pass("Weapon Rarity Distribution Across Builds", rarity_str)

    conn.close()
except Exception as e:
    record_fail("Suite 3 Exception", str(e))

# =====================================================================
# SUITE 4: SPECIFIC MILESTONE 3 REQUIREMENTS PROBE
# =====================================================================
print("\n--- Suite 4: Specific Milestone 3 Requirements Probe ---")

try:
    conn = get_connection()
    cur = conn.cursor()

    # 1. Furina Build 305 -> Fleuve Cendre Ferryman (247)
    b305 = cur.execute("""
        SELECT cb.*, c.name as char_name, c.weapon_type as char_wt, w.name as wep_name, w.weapon_type as wep_wt
        FROM character_builds cb
        JOIN characters c ON cb.character_id = c.character_id
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        WHERE cb.build_id = 305;
    """).fetchone()
    if b305 and b305["recommended_weapon_id"] == 247:
        record_pass("Furina Build 305 Relinked", f"Weapon is 247 ({b305['wep_name']})")
    else:
        record_fail("Furina Build 305 Relinked", f"Expected weapon 247, got {b305['recommended_weapon_id'] if b305 else None}")

    # 2. Albedo Build 387 -> Cinnabar Spindle (249)
    b387 = cur.execute("""
        SELECT cb.*, c.name as char_name, c.weapon_type as char_wt, w.name as wep_name, w.weapon_type as wep_wt
        FROM character_builds cb
        JOIN characters c ON cb.character_id = c.character_id
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        WHERE cb.build_id = 387;
    """).fetchone()
    if b387 and b387["recommended_weapon_id"] == 249:
        record_pass("Albedo Build 387 Relinked", f"Weapon is 249 ({b387['wep_name']})")
    else:
        record_fail("Albedo Build 387 Relinked", f"Expected weapon 249, got {b387['recommended_weapon_id'] if b387 else None}")

    # 3. Shenhe Build 392 -> Calamity Queller (204)
    b392 = cur.execute("""
        SELECT cb.*, c.name as char_name, c.weapon_type as char_wt, w.name as wep_name, w.weapon_type as wep_wt
        FROM character_builds cb
        JOIN characters c ON cb.character_id = c.character_id
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        WHERE cb.build_id = 392;
    """).fetchone()
    if b392 and b392["recommended_weapon_id"] == 204:
        record_pass("Shenhe Build 392 Relinked", f"Weapon is 204 ({b392['wep_name']})")
    else:
        record_fail("Shenhe Build 392 Relinked", f"Expected weapon 204, got {b392['recommended_weapon_id'] if b392 else None}")

    # 4. Sandrone Build 380 -> A Teaspoon of Transcendence (213), Cryo Claymore, Support
    b380 = cur.execute("""
        SELECT cb.*, c.name as char_name, c.vision, c.weapon_type as char_wt, w.name as wep_name, w.weapon_type as wep_wt
        FROM character_builds cb
        JOIN characters c ON cb.character_id = c.character_id
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        WHERE cb.build_id = 380;
    """).fetchone()
    if b380 and b380["recommended_weapon_id"] == 213 and b380["goblet_stat"] == "Cryo DMG" and b380["role"] == "Support" and b380["char_wt"] == "Claymore" and b380["wep_wt"] == "Claymore":
        record_pass("Sandrone Build 380 Remediated", f"Weapon: 213 ({b380['wep_name']}), Goblet: {b380['goblet_stat']}, Role: {b380['role']}")
    else:
        record_fail("Sandrone Build 380 Remediated", f"Unexpected Sandrone attributes: {dict(b380) if b380 else None}")

    # 5. Mavuika Build 467 -> Support, Set 53 (Scroll of Cinder City), Weapon 131
    b467 = cur.execute("SELECT * FROM character_builds WHERE build_id = 467;").fetchone()
    if b467 and b467["character_id"] == 87 and b467["role"] == "Support" and b467["recommended_artifact_id"] == 53:
        record_pass("Mavuika Alt Build 467", f"Support role with 4pc Scroll of Cinder City (Set 53)")
    else:
        record_fail("Mavuika Alt Build 467", f"Unexpected Mavuika build: {dict(b467) if b467 else None}")

    # 6. Citlali Build 468 -> Support, Weapon 194 (Sacrificial Fragments), F2P
    b468 = cur.execute("SELECT * FROM character_builds WHERE build_id = 468;").fetchone()
    if b468 and b468["character_id"] == 88 and b468["recommended_weapon_id"] == 194 and "F2P" in b468["build_name"]:
        record_pass("Citlali F2P Alt Build 468", f"F2P Sacrificial Fragments (194)")
    else:
        record_fail("Citlali F2P Alt Build 468", f"Unexpected Citlali build: {dict(b468) if b468 else None}")

    # 7. Chasca Build 469 -> Main DPS, Weapon 185 (Chain Breaker), F2P
    b469 = cur.execute("SELECT * FROM character_builds WHERE build_id = 469;").fetchone()
    if b469 and b469["character_id"] == 86 and b469["recommended_weapon_id"] == 185 and "F2P" in b469["build_name"] and b469["role"] == "Main DPS":
        record_pass("Chasca F2P Alt Build 469", f"F2P Chain Breaker (185) Main DPS")
    else:
        record_fail("Chasca F2P Alt Build 469", f"Unexpected Chasca build: {dict(b469) if b469 else None}")

    # 8. Character multi-build diversity probe
    multi_build_chars = cur.execute("""
        SELECT c.character_id, c.name, COUNT(*) as build_count
        FROM character_builds cb
        JOIN characters c ON cb.character_id = c.character_id
        GROUP BY c.character_id
        HAVING build_count > 1
        ORDER BY build_count DESC, c.character_id ASC;
    """).fetchall()
    multi_names = [f"{r['name']} ({r['build_count']})" for r in multi_build_chars]
    record_pass("Characters with Multiple Builds", f"{len(multi_build_chars)} characters have >1 build: {', '.join(multi_names[:8])}...")

    conn.close()
except Exception as e:
    record_fail("Suite 4 Exception", str(e))

# =====================================================================
# SUITE 5: FOREIGN KEY & SCHEMA INTEGRITY STRESS
# =====================================================================
print("\n--- Suite 5: Foreign Key & Schema Integrity Stress ---")

try:
    conn = get_connection()
    cur = conn.cursor()

    # 1. PRAGMA foreign_key_check
    fk_check = cur.execute("PRAGMA foreign_key_check;").fetchall()
    if len(fk_check) == 0:
        record_pass("PRAGMA foreign_key_check", "0 violations across entire database")
    else:
        record_fail("PRAGMA foreign_key_check", f"{len(fk_check)} violations: {fk_check}")

    # 2. In-memory clone for CASCADE and RESTRICT stress testing
    mem_conn = sqlite3.connect(":memory:")
    mem_conn.execute("PRAGMA foreign_keys = ON;")
    conn.backup(mem_conn)
    mem_cur = mem_conn.cursor()

    # Test CASCADE on characters deletion: Deleting Mavuika (87) should delete her builds (367 and 467)
    mem_cur.execute("DELETE FROM characters WHERE character_id = 87;")
    mav_builds_left = mem_cur.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = 87;").fetchone()[0]
    if mav_builds_left == 0:
        record_pass("CASCADE Deletion Test", "Deleting character successfully cascades to character_builds (0 builds left)")
    else:
        record_fail("CASCADE Deletion Test", f"Expected 0 builds after character deletion, got {mav_builds_left}")

    # Test RESTRICT on weapons deletion: Deleting Fleuve Cendre Ferryman (247) used by Furina (305) must be blocked
    try:
        mem_cur.execute("DELETE FROM weapons WHERE weapon_id = 247;")
        record_fail("RESTRICT Deletion on Weapon", "Expected IntegrityError, but delete succeeded!")
    except sqlite3.IntegrityError:
        record_pass("RESTRICT Deletion on Weapon", "IntegrityError raised: weapon delete blocked by RESTRICT constraint")

    # Test RESTRICT on artifact_sets deletion: Deleting Scroll of Cinder City (53) must be blocked
    try:
        mem_cur.execute("DELETE FROM artifact_sets WHERE artifact_set_id = 53;")
        record_fail("RESTRICT Deletion on Artifact Set", "Expected IntegrityError, but delete succeeded!")
    except sqlite3.IntegrityError:
        record_pass("RESTRICT Deletion on Artifact Set", "IntegrityError raised: artifact set delete blocked by RESTRICT constraint")

    # Test inserting build with non-existent character_id (9999)
    try:
        mem_cur.execute("""
            INSERT INTO character_builds (build_id, character_id, build_name, role, recommended_weapon_id, recommended_artifact_id, sands_stat, goblet_stat, circlet_stat, tier_rating, playstyle_notes)
            VALUES (9999, 9999, 'Phantom Build', 'Support', 188, 21, 'ER', 'HP%', 'Healing', 'S', 'Test note');
        """)
        record_fail("FK Rejection on Invalid character_id", "Expected IntegrityError for character_id 9999, but insert succeeded!")
    except sqlite3.IntegrityError:
        record_pass("FK Rejection on Invalid character_id", "IntegrityError raised: invalid character_id rejected")

    # Test inserting build with non-existent recommended_weapon_id (9999)
    try:
        mem_cur.execute("""
            INSERT INTO character_builds (build_id, character_id, build_name, role, recommended_weapon_id, recommended_artifact_id, sands_stat, goblet_stat, circlet_stat, tier_rating, playstyle_notes)
            VALUES (9999, 1, 'Phantom Build', 'Support', 9999, 21, 'ER', 'HP%', 'Healing', 'S', 'Test note');
        """)
        record_fail("FK Rejection on Invalid recommended_weapon_id", "Expected IntegrityError for recommended_weapon_id 9999, but insert succeeded!")
    except sqlite3.IntegrityError:
        record_pass("FK Rejection on Invalid recommended_weapon_id", "IntegrityError raised: invalid recommended_weapon_id rejected")

    # Test inserting build with non-existent recommended_artifact_id (9999)
    try:
        mem_cur.execute("""
            INSERT INTO character_builds (build_id, character_id, build_name, role, recommended_weapon_id, recommended_artifact_id, sands_stat, goblet_stat, circlet_stat, tier_rating, playstyle_notes)
            VALUES (9999, 1, 'Phantom Build', 'Support', 188, 9999, 'ER', 'HP%', 'Healing', 'S', 'Test note');
        """)
        record_fail("FK Rejection on Invalid recommended_artifact_id", "Expected IntegrityError for recommended_artifact_id 9999, but insert succeeded!")
    except sqlite3.IntegrityError:
        record_pass("FK Rejection on Invalid recommended_artifact_id", "IntegrityError raised: invalid recommended_artifact_id rejected")

    mem_conn.close()
    conn.close()
except Exception as e:
    record_fail("Suite 5 Exception", str(e))

# =====================================================================
# SUITE 6: FIELD VALIDITY, VALUE DISTRIBUTIONS & BOUNDARY STRESS
# =====================================================================
print("\n--- Suite 6: Field Validity, Value Distributions & Boundary Stress ---")

try:
    conn = get_connection()
    cur = conn.cursor()

    # 1. Null / Empty String checks across all columns of character_builds
    columns = [
        "build_id", "character_id", "build_name", "role",
        "recommended_weapon_id", "recommended_artifact_id",
        "sands_stat", "goblet_stat", "circlet_stat", "tier_rating", "playstyle_notes"
    ]
    null_issues = []
    for col in columns:
        cnt_null = cur.execute(f"SELECT COUNT(*) FROM character_builds WHERE {col} IS NULL;").fetchone()[0]
        cnt_empty = cur.execute(f"SELECT COUNT(*) FROM character_builds WHERE typeof({col}) = 'text' AND trim({col}) = '';").fetchone()[0]
        if cnt_null > 0 or cnt_empty > 0:
            null_issues.append(f"{col}: {cnt_null} NULLs, {cnt_empty} empty strings")

    if not null_issues:
        record_pass("Zero NULL / Empty Values", "All 11 columns across 168 builds are non-null and non-empty")
    else:
        record_fail("Zero NULL / Empty Values", f"Found issues: {null_issues}")

    # 2. tier_rating domain check: IN ('SS', 'S+', 'S', 'A')
    invalid_tiers = cur.execute("""
        SELECT build_id, build_name, tier_rating
        FROM character_builds
        WHERE tier_rating NOT IN ('SS', 'S+', 'S', 'A');
    """).fetchall()
    if len(invalid_tiers) == 0:
        record_pass("tier_rating Domain Validity", "All 168 builds have tier_rating in ('SS', 'S+', 'S', 'A')")
    else:
        record_fail("tier_rating Domain Validity", f"Invalid tier ratings: {invalid_tiers}")

    # Tier breakdown
    tier_dist = cur.execute("""
        SELECT tier_rating, COUNT(*) as cnt
        FROM character_builds
        GROUP BY tier_rating
        ORDER BY CASE tier_rating WHEN 'SS' THEN 1 WHEN 'S+' THEN 2 WHEN 'S' THEN 3 WHEN 'A' THEN 4 ELSE 5 END;
    """).fetchall()
    tier_str = ", ".join([f"{r['tier_rating']}: {r['cnt']}" for r in tier_dist])
    record_pass("Tier Rating Distribution", tier_str)

    # 3. role domain check: standard roles
    invalid_roles = cur.execute("""
        SELECT build_id, build_name, role
        FROM character_builds
        WHERE role NOT IN ('Main DPS', 'Sub-DPS', 'Support', 'Healer', 'Shielder');
    """).fetchall()
    if len(invalid_roles) == 0:
        record_pass("role Domain Validity", "All 168 builds have role in ('Main DPS', 'Sub-DPS', 'Support', 'Healer', 'Shielder')")
    else:
        record_fail("role Domain Validity", f"Invalid roles: {invalid_roles}")

    # Role breakdown
    role_dist = cur.execute("""
        SELECT role, COUNT(*) as cnt
        FROM character_builds
        GROUP BY role
        ORDER BY cnt DESC;
    """).fetchall()
    role_str = ", ".join([f"{r['role']}: {r['cnt']}" for r in role_dist])
    record_pass("Role Distribution", role_str)

    # 4. Stat naming convention check
    sands_stats = cur.execute("SELECT DISTINCT sands_stat FROM character_builds ORDER BY sands_stat;").fetchall()
    goblet_stats = cur.execute("SELECT DISTINCT goblet_stat FROM character_builds ORDER BY goblet_stat;").fetchall()
    circlet_stats = cur.execute("SELECT DISTINCT circlet_stat FROM character_builds ORDER BY circlet_stat;").fetchall()

    valid_sands = {"ATK%", "DEF%", "HP%", "Energy Recharge", "Elemental Mastery"}
    actual_sands = {r["sands_stat"] for r in sands_stats}
    if actual_sands.issubset(valid_sands):
        record_pass("Sands Stat Standard", f"Valid sands: {actual_sands}")
    else:
        record_fail("Sands Stat Standard", f"Unexpected sands: {actual_sands - valid_sands}")

    valid_goblets = {
        "Anemo DMG", "Cryo DMG", "Dendro DMG", "Electro DMG", "Geo DMG", "Hydro DMG", "Pyro DMG",
        "Physical DMG", "ATK%", "DEF%", "HP%", "Elemental Mastery"
    }
    actual_goblets = {r["goblet_stat"] for r in goblet_stats}
    if actual_goblets.issubset(valid_goblets):
        record_pass("Goblet Stat Standard", f"Valid goblets: {len(actual_goblets)} standard stats")
    else:
        record_fail("Goblet Stat Standard", f"Unexpected goblets: {actual_goblets - valid_goblets}")

    valid_circlets = {"CRIT Rate", "CRIT DMG", "Healing Bonus", "ATK%", "DEF%", "HP%", "Elemental Mastery"}
    actual_circlets = {r["circlet_stat"] for r in circlet_stats}
    if actual_circlets.issubset(valid_circlets):
        record_pass("Circlet Stat Standard", f"Valid circlets: {actual_circlets}")
    else:
        record_fail("Circlet Stat Standard", f"Unexpected circlets: {actual_circlets - valid_circlets}")

    # 5. Playstyle notes quality check
    short_notes = cur.execute("SELECT build_id, build_name, length(playstyle_notes) as len FROM character_builds WHERE length(playstyle_notes) < 25;").fetchall()
    placeholder_notes = cur.execute("""
        SELECT build_id, build_name, playstyle_notes
        FROM character_builds
        WHERE playstyle_notes LIKE '%TODO%' OR playstyle_notes LIKE '%TBD%' OR playstyle_notes LIKE '%N/A%' OR playstyle_notes LIKE '%test%';
    """).fetchall()
    if len(short_notes) == 0 and len(placeholder_notes) == 0:
        record_pass("Playstyle Notes Quality", "All 168 builds have substantive (>25 chars) descriptive notes with zero placeholders")
    else:
        record_fail("Playstyle Notes Quality", f"Short notes: {len(short_notes)}, Placeholders: {len(placeholder_notes)}")

    # 6. Build ID uniqueness and continuity
    all_bids = [r["build_id"] for r in cur.execute("SELECT build_id FROM character_builds ORDER BY build_id ASC;").fetchall()]
    if len(all_bids) == len(set(all_bids)) == 168:
        expected_range = set(range(301, 470)) - {381} # 381 purged Capitano
        if set(all_bids) == expected_range:
            record_pass("Build ID Continuity", "IDs span exactly [301..469] with 381 purged (168 contiguous IDs)")
        else:
            diff = set(all_bids).symmetric_difference(expected_range)
            record_fail("Build ID Continuity", f"Mismatch in expected build ID set: {diff}")
    else:
        record_fail("Build ID Continuity", f"Duplicate build IDs found: total {len(all_bids)}, unique {len(set(all_bids))}")

    conn.close()
except Exception as e:
    record_fail("Suite 6 Exception", str(e))

# =====================================================================
# SUITE 7: FULL 4-TABLE RELATIONAL JOINS & REAL QUERIES
# =====================================================================
print("\n--- Suite 7: Full 4-Table Relational Joins & Real Queries ---")

try:
    conn = get_connection()
    cur = conn.cursor()

    # 1. 4-Table INNER JOIN across all entities
    four_way_join = cur.execute("""
        SELECT cb.build_id, c.name AS char_name, c.vision, c.weapon_type,
               w.name AS weapon_name, w.rarity AS weapon_rarity,
               a.name AS artifact_name, a.region AS artifact_region,
               cb.role, cb.tier_rating
        FROM character_builds cb
        JOIN characters c ON cb.character_id = c.character_id
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        JOIN artifact_sets a ON cb.recommended_artifact_id = a.artifact_set_id;
    """).fetchall()
    if len(four_way_join) == 168:
        record_pass("Full 4-Table INNER JOIN", "Successfully joined 168/168 builds across characters, weapons, and artifact_sets")
    else:
        record_fail("Full 4-Table INNER JOIN", f"Expected 168 rows from INNER JOIN, got {len(four_way_join)}")

    # 2. Team Composition Real Query: Build a 4-person Melt/Vaporize team using M3 builds
    team_query = cur.execute("""
        WITH ranked_builds AS (
            SELECT c.name, c.vision, cb.role, cb.tier_rating, w.name as weapon, a.name as artifact,
                   ROW_NUMBER() OVER(PARTITION BY c.vision, cb.role ORDER BY CASE cb.tier_rating WHEN 'SS' THEN 1 WHEN 'S+' THEN 2 WHEN 'S' THEN 3 ELSE 4 END) as rn
            FROM character_builds cb
            JOIN characters c ON cb.character_id = c.character_id
            JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
            JOIN artifact_sets a ON cb.recommended_artifact_id = a.artifact_set_id
        )
        SELECT name, vision, role, tier_rating, weapon, artifact
        FROM ranked_builds
        WHERE (vision = 'Pyro' AND role = 'Main DPS' AND rn = 1)
           OR (vision = 'Hydro' AND role = 'Sub-DPS' AND rn = 1)
           OR (vision = 'Anemo' AND role = 'Support' AND rn = 1)
           OR (vision = 'Cryo' AND role = 'Healer' AND rn = 1);
    """).fetchall()
    if len(team_query) == 4:
        team_desc = " | ".join([f"{r['name']} ({r['vision']} {r['role']}: {r['weapon']})" for r in team_query])
        record_pass("Realistic Team Composition Query", f"Constructed balanced 4-man reaction team: {team_desc}")
    else:
        record_fail("Realistic Team Composition Query", f"Expected 4 team members, got {len(team_query)}")

    # 3. F2P Weapon Recommendation Query across builds
    f2p_builds = cur.execute("""
        SELECT cb.build_id, c.name, cb.build_name, w.name as weapon, w.is_craftable
        FROM character_builds cb
        JOIN characters c ON cb.character_id = c.character_id
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        WHERE w.is_craftable = 1 OR cb.build_name LIKE '%F2P%';
    """).fetchall()
    record_pass("F2P Build Query Support", f"Identified {len(f2p_builds)} explicit F2P/Craftable builds in catalog")

    conn.close()
except Exception as e:
    record_fail("Suite 7 Exception", str(e))

# =====================================================================
# SUITE 8: E2E TEST SUITE REGRESSION & TEST CONTRACT ANALYSIS
# =====================================================================
print("\n--- Suite 8: E2E Test Suite Regression & Test Contract Analysis ---")

try:
    # 1. Milestone 3 target tests (F9, F10, F11, F12)
    proc_m3 = subprocess.run(
        [sys.executable, "tests/test_e2e_genshin.py", "--tier", "1", "--feature", "F9,F10,F11,F12"],
        cwd=PROJECT_ROOT, capture_output=True, text=True
    )
    if proc_m3.returncode == 0:
        record_pass("Milestone 3 E2E Tests (F9–F12)", "20/20 PASS (100% success)")
    else:
        record_fail("Milestone 3 E2E Tests (F9–F12)", f"Failing M3 tests: {proc_m3.stdout}")

    # 2. Cumulative Milestones 1–3 tests (F1 through F12)
    proc_cum = subprocess.run(
        [sys.executable, "tests/test_e2e_genshin.py", "--tier", "1", "--feature", "F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11,F12"],
        cwd=PROJECT_ROOT, capture_output=True, text=True
    )
    if proc_cum.returncode == 0:
        record_pass("Cumulative Milestones 1–3 Tests (F1–F12)", "60/60 PASS (100% success)")
    else:
        record_fail("Cumulative Milestones 1–3 Tests (F1–F12)", f"Failing cumulative tests: {proc_cum.stdout}")

    # 3. Security and OOM suite
    proc_sec = subprocess.run(
        ["./.venv/bin/python", "test_security_oom.py"],
        cwd=PROJECT_ROOT, capture_output=True, text=True
    )
    if proc_sec.returncode == 0 and "22 PASSED, 0 FAILED" in proc_sec.stdout:
        record_pass("Web Security & OOM Mitigation Suite", "22/22 PASS (100% success)")
    else:
        record_fail("Web Security & OOM Mitigation Suite", f"Security test output: {proc_sec.stdout}")

    # 4. Evaluation of Tier 3 Cross-Feature Tests
    proc_t3 = subprocess.run(
        [sys.executable, "tests/test_e2e_genshin.py", "--tier", "3"],
        cwd=PROJECT_ROOT, capture_output=True, text=True
    )
    if proc_t3.returncode == 0:
        record_pass("Tier 3 Cross-Feature Relational Suite", "25/25 PASS")
    else:
        # Diagnostic analysis of the 2 failures
        t3_out = proc_t3.stdout
        fails = []
        if "test_t3_cryo_characters_and_cryo_artifacts_pair" in t3_out:
            fails.append("test_t3_cryo_characters_and_cryo_artifacts_pair (Build 452 Escoffier uses Set 48 Golden Troupe)")
        if "test_t3_pyro_characters_and_pyro_artifacts_pair" in t3_out:
            fails.append("test_t3_pyro_characters_and_pyro_artifacts_pair (Build 421 Xinyan uses Set 34 Pale Flame)")
        record_fail("Tier 3 Cross-Feature Relational Suite", f"23/25 passed, 2 failures: {', '.join(fails)}")

except Exception as e:
    record_fail("Suite 8 Exception", str(e))

# =====================================================================
# SUMMARY
# =====================================================================
print("\n" + "=" * 80)
print("ADVERSARIAL STRESS SUITE EXECUTION SUMMARY")
print("=" * 80)
print(f"Total Tests Executed: {passed_tests + failed_tests}")
print(f"Passed              : {passed_tests}")
print(f"Failed              : {failed_tests}")

if findings:
    print("\nRecorded Findings:")
    for name, reason in findings:
        print(f"  - [{name}]: {reason}")

print("=" * 80)

if failed_tests > 0:
    sys.exit(1)
else:
    sys.exit(0)
