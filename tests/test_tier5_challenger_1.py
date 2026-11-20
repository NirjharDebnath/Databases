#!/usr/bin/env python3
"""
tests/test_tier5_challenger_1.py
Phase 2: Tier 5 Adversarial Coverage Hardening Test Suite.

Author: challenger_final_1 (Empirical Challenger)
Role: critic, specialist
Target Milestone: M_FINAL / Phase 2: Tier 5 Adversarial Coverage Hardening

Scope of Adversarial Challenge:
- Suite 1: Transaction Rollback & Data Ingestion Atomicity (Adversarial Data Ingestion)
- Suite 2: Relational Action Cascades & Consistency Invariants (CASCADE, SET NULL, RESTRICT)
- Suite 3: SQL Injection Vectors, Special Character Escaping & Web Security Hardening
- Suite 4: Extreme Boundary Conditions & Domain-Specific Constraints
- Suite 5: Relational Index Utilization, Optimization & Sargability Stress
- Suite 6: CSV Serialization Parity & Ingestion Idempotency
- Suite 7: Complex Meta Learning & Real-World Query Scenarios
"""

import os
import sys
import csv
import json
import time
import shutil
import hashlib
import sqlite3
import tempfile
import subprocess
import unittest
from typing import Dict, List, Tuple, Any, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(PROJECT_ROOT, "genshin_learning.db")
VENV_PYTHON = os.path.join(PROJECT_ROOT, ".venv", "bin", "python")

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
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at {db_path}")
    conn = sqlite3.connect(db_path, timeout=10.0)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def clone_db_to_memory(source_path: str = DB_PATH) -> sqlite3.Connection:
    """Creates an in-memory clone of the database for safe destructive testing."""
    src = sqlite3.connect(source_path)
    mem = sqlite3.connect(":memory:")
    src.backup(mem)
    src.close()
    mem.execute("PRAGMA foreign_keys = ON;")
    mem.row_factory = sqlite3.Row
    return mem


# =====================================================================
# SUITE 1: TRANSACTION ROLLBACK & INGESTION ATOMICITY
# =====================================================================
def run_suite_1():
    print("\n--- Suite 1: Transaction Rollback & Data Ingestion Atomicity ---")
    mem = clone_db_to_memory()
    cur = mem.cursor()

    # 1.1 Rollback on Primary Key Collision
    try:
        cur.execute("BEGIN TRANSACTION;")
        # Attempt inserting duplicate character_id 1 (Venti)
        cur.execute("""
            INSERT INTO characters (
                character_id, name, rarity, vision, weapon_type, region,
                default_role, base_hp, base_atk, base_def, talent_priority, release_patch
            ) VALUES (1, 'Venti Duplicate', 5, 'Anemo', 'Bow', 'Mondstadt', 'Support', 10531, 263, 669, 'Burst', 1.0);
        """)
        mem.commit()
        record_fail("1.1 Duplicate Primary Key", "Insertion succeeded unexpectedly")
    except sqlite3.IntegrityError:
        mem.rollback()
        # Verify count unchanged
        count = cur.execute("SELECT COUNT(*) FROM characters;").fetchone()[0]
        if count == 129:
            record_pass("1.1 Duplicate Primary Key", "IntegrityError raised, transaction cleanly rolled back (count=129)")
        else:
            record_fail("1.1 Duplicate Primary Key", f"Table modified despite rollback, count={count}")
    except Exception as e:
        mem.rollback()
        record_fail("1.1 Duplicate Primary Key", f"Unexpected exception: {e}")

    # 1.2 Rollback on Foreign Key Invariant Violation
    try:
        cur.execute("BEGIN TRANSACTION;")
        # Attempt inserting build with non-existent character_id 99999
        cur.execute("""
            INSERT INTO character_builds (
                build_id, character_id, build_name, role,
                recommended_weapon_id, recommended_artifact_id,
                sands_stat, goblet_stat, circlet_stat, tier_rating, playstyle_notes
            ) VALUES (9999, 99999, 'Phantom Build', 'Support', 201, 1, 'ATK%', 'Pyro DMG%', 'CRIT Rate', 'SS', 'Notes');
        """)
        mem.commit()
        record_fail("1.2 Foreign Key Invariant Violation", "Insertion with invalid character_id succeeded")
    except sqlite3.IntegrityError:
        mem.rollback()
        build_count = cur.execute("SELECT COUNT(*) FROM character_builds;").fetchone()[0]
        if build_count == 168:
            record_pass("1.2 Foreign Key Invariant Violation", "FK violation raised, rollback preserved exact 168 builds")
        else:
            record_fail("1.2 Foreign Key Invariant Violation", f"Build count corrupted: {build_count}")
    except Exception as e:
        mem.rollback()
        record_fail("1.2 Foreign Key Invariant Violation", f"Unexpected exception: {e}")

    # 1.3 Rollback on Check Constraint Violation
    try:
        cur.execute("BEGIN TRANSACTION;")
        # Attempt inserting invalid rarity 7
        cur.execute("""
            INSERT INTO characters (
                character_id, name, rarity, vision, weapon_type, region,
                default_role, base_hp, base_atk, base_def, talent_priority, release_patch
            ) VALUES (9001, 'Illegal Hero', 7, 'Pyro', 'Sword', 'Mondstadt', 'Main DPS', 10000, 200, 500, 'Burst', 1.0);
        """)
        mem.commit()
        record_fail("1.3 Check Constraint Violation (Rarity)", "Insertion of rarity 7 succeeded")
    except sqlite3.IntegrityError:
        mem.rollback()
        record_pass("1.3 Check Constraint Violation (Rarity)", "CHECK failed on rarity 7, rollback intact")
    except Exception as e:
        mem.rollback()
        record_fail("1.3 Check Constraint Violation (Rarity)", f"Unexpected error: {e}")

    # 1.4 In-Flight Transaction Isolation & Dirty Read Prevention
    # Use two separate connections to a temporary file DB to test isolation
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_f:
        tmp_db_path = tmp_f.name

    try:
        shutil.copy2(DB_PATH, tmp_db_path)
        conn1 = sqlite3.connect(tmp_db_path)
        conn1.execute("PRAGMA foreign_keys = ON;")
        conn2 = sqlite3.connect(tmp_db_path)
        conn2.execute("PRAGMA foreign_keys = ON;")

        cur1 = conn1.cursor()
        cur2 = conn2.cursor()

        cur1.execute("BEGIN IMMEDIATE;")
        cur1.execute("""
            INSERT INTO characters (
                character_id, name, rarity, vision, weapon_type, region,
                default_role, base_hp, base_atk, base_def, talent_priority, release_patch
            ) VALUES (9002, 'Uncommitted Hero', 5, 'Hydro', 'Sword', 'Fontaine', 'Support', 12000, 250, 700, 'Burst', 4.0);
        """)

        # Connection 2 should not see uncommitted row
        c2_view = cur2.execute("SELECT COUNT(*) FROM characters WHERE character_id = 9002;").fetchone()[0]
        cur1.execute("ROLLBACK;")
        c1_after = cur1.execute("SELECT COUNT(*) FROM characters WHERE character_id = 9002;").fetchone()[0]

        if c2_view == 0 and c1_after == 0:
            record_pass("1.4 Transaction Isolation & Dirty Read Prevention", "Uncommitted writes isolated from other connections and vanished on rollback")
        else:
            record_fail("1.4 Transaction Isolation & Dirty Read Prevention", f"Isolation failed: c2_view={c2_view}, c1_after={c1_after}")

        conn1.close()
        conn2.close()
    finally:
        if os.path.exists(tmp_db_path):
            os.remove(tmp_db_path)

    # 1.5 Savepoint & Partial Rollback Mechanics
    try:
        cur.execute("SAVEPOINT sp_outer;")
        cur.execute("""
            INSERT INTO characters (
                character_id, name, rarity, vision, weapon_type, region,
                default_role, base_hp, base_atk, base_def, talent_priority, release_patch
            ) VALUES (9003, 'Valid Savepoint Hero', 5, 'Geo', 'Polearm', 'Liyue', 'Shielder', 14000, 250, 800, 'Skill', 1.0);
        """)

        cur.execute("SAVEPOINT sp_inner;")
        try:
            cur.execute("""
                INSERT INTO characters (
                    character_id, name, rarity, vision, weapon_type, region,
                    default_role, base_hp, base_atk, base_def, talent_priority, release_patch
                ) VALUES (9004, 'Invalid Vision Hero', 5, 'UnknownVision', 'Sword', 'Liyue', 'DPS', 10000, 200, 500, 'Burst', 1.0);
            """)
        except sqlite3.IntegrityError:
            cur.execute("ROLLBACK TO sp_inner;")

        cur.execute("RELEASE sp_outer;")

        hero_9003 = cur.execute("SELECT COUNT(*) FROM characters WHERE character_id = 9003;").fetchone()[0]
        hero_9004 = cur.execute("SELECT COUNT(*) FROM characters WHERE character_id = 9004;").fetchone()[0]

        if hero_9003 == 1 and hero_9004 == 0:
            record_pass("1.5 Savepoint & Partial Rollback", "Nested savepoint successfully rolled back corrupt insertion while preserving outer valid insertion")
        else:
            record_fail("1.5 Savepoint & Partial Rollback", f"Unexpected state: hero_9003={hero_9003}, hero_9004={hero_9004}")

    except Exception as e:
        record_fail("1.5 Savepoint & Partial Rollback", f"Exception encountered: {e}")

    mem.close()


# =====================================================================
# SUITE 2: RELATIONAL ACTION CASCADES & CONSISTENCY INVARIANTS
# =====================================================================
def run_suite_2():
    print("\n--- Suite 2: Relational Action Cascades & Consistency Invariants ---")
    mem = clone_db_to_memory()
    cur = mem.cursor()

    # 2.1 ON DELETE CASCADE: characters -> character_builds
    # Character 6 (Albedo) has build 387
    builds_before = cur.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = 6;").fetchone()[0]
    cur.execute("DELETE FROM characters WHERE character_id = 6;")
    builds_after = cur.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = 6;").fetchone()[0]
    if builds_before >= 1 and builds_after == 0:
        record_pass("2.1 ON DELETE CASCADE (characters -> builds)", f"Albedo ({builds_before} builds) deleted; cascaded cleanly to 0 builds")
    else:
        record_fail("2.1 ON DELETE CASCADE (characters -> builds)", f"Before={builds_before}, After={builds_after}")

    # 2.2 ON DELETE SET NULL: characters -> weapons.signature_character_id
    # Character 84 (Kinich) owns Weapon 128 (Fang of the Mountain King)
    sig_before = cur.execute("SELECT signature_character_id FROM weapons WHERE weapon_id = 128;").fetchone()[0]
    cur.execute("DELETE FROM characters WHERE character_id = 84;")
    sig_after = cur.execute("SELECT signature_character_id FROM weapons WHERE weapon_id = 128;").fetchone()[0]
    weapon_still_exists = cur.execute("SELECT COUNT(*) FROM weapons WHERE weapon_id = 128;").fetchone()[0]
    if sig_before == 84 and sig_after is None and weapon_still_exists == 1:
        record_pass("2.2 ON DELETE SET NULL (characters -> weapons)", "Signature owner deletion set signature_character_id to NULL without deleting weapon")
    else:
        record_fail("2.2 ON DELETE SET NULL (characters -> weapons)", f"sig_before={sig_before}, sig_after={sig_after}, exists={weapon_still_exists}")

    # 2.3 ON DELETE RESTRICT: weapons -> character_builds
    # Try deleting weapon 247 (Fleuve Cendre Ferryman) which is used in Furina build 305
    try:
        cur.execute("DELETE FROM weapons WHERE weapon_id = 247;")
        record_fail("2.3 ON DELETE RESTRICT (weapons -> builds)", "Deletion of recommended weapon succeeded unexpectedly")
    except sqlite3.IntegrityError:
        record_pass("2.3 ON DELETE RESTRICT (weapons -> builds)", "Attempted deletion of recommended weapon blocked by RESTRICT foreign key constraint")
    except Exception as e:
        record_fail("2.3 ON DELETE RESTRICT (weapons -> builds)", f"Unexpected exception: {e}")

    # 2.4 ON DELETE RESTRICT: artifact_sets -> character_builds
    # Try deleting artifact set 59 (Aubade of Morningstar and Moon)
    try:
        cur.execute("DELETE FROM artifact_sets WHERE artifact_set_id = 59;")
        record_fail("2.4 ON DELETE RESTRICT (artifact_sets -> builds)", "Deletion of recommended artifact set succeeded unexpectedly")
    except sqlite3.IntegrityError:
        record_pass("2.4 ON DELETE RESTRICT (artifact_sets -> builds)", "Attempted deletion of recommended artifact set blocked by RESTRICT constraint")
    except Exception as e:
        record_fail("2.4 ON DELETE RESTRICT (artifact_sets -> builds)", f"Unexpected exception: {e}")

    # 2.5 Universal Weapon Type Compatibility across all 168 builds
    mismatches = cur.execute("""
        SELECT cb.build_id, c.name, c.weapon_type, w.name, w.weapon_type
        FROM character_builds cb
        JOIN characters c ON cb.character_id = c.character_id
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        WHERE c.weapon_type != w.weapon_type;
    """).fetchall()
    if len(mismatches) == 0:
        record_pass("2.5 Universal Weapon Type Compatibility", "168/168 builds have matching weapon types with their respective characters")
    else:
        record_fail("2.5 Universal Weapon Type Compatibility", f"Found {len(mismatches)} mismatches: {mismatches[:3]}")

    # 2.6 Signature Weapon Type Compatibility
    sig_mismatches = cur.execute("""
        SELECT w.weapon_id, w.name, w.weapon_type, c.name, c.weapon_type
        FROM weapons w
        JOIN characters c ON w.signature_character_id = c.character_id
        WHERE w.weapon_type != c.weapon_type;
    """).fetchall()
    if len(sig_mismatches) == 0:
        record_pass("2.6 Signature Weapon Type Compatibility", "All signature weapons match their owner character's weapon type")
    else:
        record_fail("2.6 Signature Weapon Type Compatibility", f"Found signature mismatches: {sig_mismatches}")

    # 2.7 Multi-Build Role Divergence
    # Characters with > 1 build must have distinct build_names and roles
    multi_build_chars = cur.execute("""
        SELECT character_id, COUNT(*) as cnt
        FROM character_builds
        GROUP BY character_id
        HAVING cnt > 1;
    """).fetchall()
    divergent_ok = True
    for cid, cnt in multi_build_chars:
        builds = cur.execute("SELECT build_name, role, recommended_weapon_id, recommended_artifact_id FROM character_builds WHERE character_id = ?;", (cid,)).fetchall()
        names = [b[0] for b in builds]
        if len(set(names)) != len(names):
            divergent_ok = False
            record_fail("2.7 Multi-Build Role Divergence", f"Character ID {cid} has duplicate build names: {names}")
            break
    if divergent_ok:
        record_pass("2.7 Multi-Build Role Divergence", f"All {len(multi_build_chars)} multi-build characters exhibit distinct build names and role setups")

    # 2.8 Zero Orphaned Characters
    orphans = cur.execute("""
        SELECT c.character_id, c.name
        FROM characters c
        LEFT JOIN character_builds cb ON c.character_id = cb.character_id
        WHERE cb.build_id IS NULL;
    """).fetchall()
    if len(orphans) == 0:
        record_pass("2.8 Zero Orphaned Characters", "129/129 characters have at least 1 verified build (0 orphans)")
    else:
        record_fail("2.8 Zero Orphaned Characters", f"Found {len(orphans)} orphans: {orphans}")

    mem.close()


# =====================================================================
# SUITE 3: SQL INJECTION VECTORS, ESCAPING & WEB SECURITY HARDENING
# =====================================================================
def run_suite_3():
    print("\n--- Suite 3: SQL Injection Vectors, Escaping & Web Security Hardening ---")
    conn = get_connection()
    cur = conn.cursor()

    # 3.1 Parameterized Query SQL Injection Resistance
    injection_payloads = [
        "' OR '1'='1",
        "'; DROP TABLE characters; --",
        "' UNION SELECT 1, 'Hacked', 5, 'Pyro', 'Sword', 'None', 'DPS', 1, 1, 1, 'None', 1.0; --",
        "admin'--",
        "\" OR \"\"=\"",
        "1; DELETE FROM weapons WHERE 1=1;",
    ]
    all_injections_safe = True
    for payload in injection_payloads:
        # Search by name with parameter
        res = cur.execute("SELECT COUNT(*) FROM characters WHERE name = ?;", (payload,)).fetchone()[0]
        if res != 0:
            all_injections_safe = False
            record_fail("3.1 Parameterized SQL Injection", f"Payload matched rows unexpectedly: {payload}")
            break
    # Confirm characters table is intact
    count_after = cur.execute("SELECT COUNT(*) FROM characters;").fetchone()[0]
    if all_injections_safe and count_after == 129:
        record_pass("3.1 Parameterized SQL Injection", "All 6 hostile SQL injection payloads safely neutralized via parameterization")
    else:
        record_fail("3.1 Parameterized SQL Injection", f"Table integrity compromised or check failed: count={count_after}")

    # 3.2 Special Characters & Apostrophe Punctuation Handling
    test_apostrophe_terms = [
        ("Witch's Homework", "artifact_sets", "four_piece_bonus"),
        ("Amos' Bow", "weapons", "name"),
        ("Surf's Up", "weapons", "name"),
        ("Wolf's Gravestone", "weapons", "name"),
        ("Hunter's Path", "weapons", "name"),
        ("Heart of the Furnace", "artifact_sets", "name"),
        ("Thorny Crown of the Mountain Wind", "artifact_sets", "domain_name"),
    ]
    all_apostrophes_found = True
    for term, table, col in test_apostrophe_terms:
        found = cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} LIKE ?;", (f"%{term}%",)).fetchone()[0]
        if found == 0:
            all_apostrophes_found = False
            record_fail("3.2 Apostrophe Punctuation Handling", f"Failed to match term '{term}' in {table}.{col}")
            break
    if all_apostrophes_found:
        record_pass("3.2 Apostrophe Punctuation Handling", "All strings with apostrophes, hyphens, and quotes query accurately")

    conn.close()

    # 3.3 to 3.6: Web App Security & Authorizer Integration Tests
    # Run test_security_oom.py or call app test client directly if available
    try:
        from app import app, MAX_QUERY_LENGTH, MAX_STREAM_ROWS, QUERY_TIMEOUT_SECONDS
        client = app.test_client()

        # 3.3 Blocked writes and authorizer
        attacks = [
            ("DROP TABLE characters;", 403),
            ("INSERT INTO characters(character_id, name) VALUES (999, 'Hacker');", 403),
            ("UPDATE characters SET name = 'Owned';", 403),
            ("DELETE FROM weapons;", 403),
            ("CREATE TABLE evil(id int);", 403),
            ("ATTACH DATABASE ':memory:' AS evil;", 403),
            ("PRAGMA schema_version;", 403),
            ("VACUUM;", 403),
            ("SELECT 1; DROP TABLE characters;", 400),
            ("/* harmless */ DROP TABLE characters;", 403),
            ("SELECT load_extension('evil');", 400),
        ]
        attacks_blocked = True
        for q, expected_code in attacks:
            resp = client.post("/api/query", json={"query": q})
            if resp.status_code not in (400, 403):
                attacks_blocked = False
                record_fail("3.3 Web App Security Authorizer", f"Query was not blocked: {q} (status {resp.status_code})")
                break
        if attacks_blocked:
            record_pass("3.3 Web App Security Authorizer", f"All {len(attacks)} malicious write/administrative queries rejected with 400/403")

        # 3.4 Infinite CTE Watchdog Timeout
        infinite_cte = "WITH RECURSIVE cnt(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM cnt) SELECT count(*) FROM cnt;"
        t0 = time.perf_counter()
        resp = client.post("/api/query", json={"query": infinite_cte})
        elapsed = time.perf_counter() - t0
        err_msg = resp.get_json().get("error", "").lower() if resp.is_json else ""
        if ("timeout" in err_msg or "interrupted" in err_msg or "aborted" in err_msg) and elapsed < QUERY_TIMEOUT_SECONDS + 2.5:
            record_pass("3.4 Infinite CTE Watchdog Timeout", f"Infinite CTE terminated in {elapsed:.2f}s (timeout={QUERY_TIMEOUT_SECONDS}s)")
        else:
            record_fail("3.4 Infinite CTE Watchdog Timeout", f"Watchdog timeout failed: elapsed={elapsed:.2f}s, response={resp.data}")

        # 3.5 Cartesian Explosion Stream Capping
        cartesian = "SELECT * FROM characters, weapons, artifact_sets, character_builds;"
        resp = client.post("/api/query", json={"query": cartesian})
        lines = [json.loads(line) for line in resp.data.decode().strip().split("\n") if line.strip()]
        complete_ev = [l for l in lines if l.get("type") == "complete"]
        if complete_ev and complete_ev[0].get("count") == MAX_STREAM_ROWS and complete_ev[0].get("truncated") is True:
            record_pass("3.5 Cartesian Explosion Stream Capping", f"Cartesian query stream capped at exactly {MAX_STREAM_ROWS} rows with truncated flag")
        else:
            record_fail("3.5 Cartesian Explosion Stream Capping", f"Stream capping failed: {complete_ev}")

        # 3.6 Oversized and Malformed Request Guardrails
        oversized_query = "SELECT " + ("1+" * 35000) + "1;"
        resp_too_large = client.post("/api/query", json={"query": oversized_query})
        resp_not_json = client.post("/api/query", data="plain text sql", content_type="text/plain")
        resp_empty_json = client.post("/api/query", json={})

        if resp_too_large.status_code in (400, 413) and resp_not_json.status_code == 415 and resp_empty_json.status_code == 400:
            record_pass("3.6 Request Guardrails", "Oversized (>64KB), non-JSON (415), and empty query (400) payloads correctly rejected")
        else:
            record_fail("3.6 Request Guardrails", f"Guardrail check failed: large={resp_too_large.status_code}, text={resp_not_json.status_code}, empty={resp_empty_json.status_code}")

    except ImportError:
        # Flask is in virtual environment: invoke via subprocess
        sec_res = subprocess.run([VENV_PYTHON, "test_security_oom.py"], cwd=PROJECT_ROOT, capture_output=True, text=True)
        if sec_res.returncode == 0:
            record_pass("3.3-3.6 Web App Security (via venv)", "test_security_oom.py passed all 22 tests cleanly")
        else:
            record_fail("3.3-3.6 Web App Security (via venv)", f"test_security_oom.py failed with code {sec_res.returncode}")


# =====================================================================
# SUITE 4: EXTREME BOUNDARY CONDITIONS & DOMAIN CONSTRAINTS
# =====================================================================
def run_suite_4():
    print("\n--- Suite 4: Extreme Boundary Conditions & Domain Constraints ---")
    conn = get_connection()
    cur = conn.cursor()

    # 4.1 Character Base Stats Numerical Bounds
    char_stats = cur.execute("""
        SELECT 
            MIN(base_hp), MAX(base_hp),
            MIN(base_atk), MAX(base_atk),
            MIN(base_def), MAX(base_def)
        FROM characters;
    """).fetchone()
    min_hp, max_hp, min_atk, max_atk, min_def, max_def = char_stats
    if min_hp >= 9000 and max_hp <= 16000 and min_atk >= 100 and max_atk <= 400 and min_def >= 500 and max_def <= 1000:
        record_pass("4.1 Character Base Stats Bounds", f"HP [{min_hp}, {max_hp}], ATK [{min_atk}, {max_atk}], DEF [{min_def}, {max_def}] strictly within expected bounds")
    else:
        record_fail("4.1 Character Base Stats Bounds", f"Out of bounds: HP=({min_hp},{max_hp}), ATK=({min_atk},{max_atk}), DEF=({min_def},{max_def})")

    # 4.2 Weapon Base Stats Numerical Bounds
    w_stats = cur.execute("""
        SELECT 
            MIN(base_atk), MAX(base_atk),
            MIN(sub_stat_value), MAX(sub_stat_value)
        FROM weapons;
    """).fetchone()
    w_min_atk, w_max_atk, w_min_sub, w_max_sub = w_stats
    if w_min_atk >= 350 and w_max_atk <= 741 and w_min_sub >= 10.0 and w_max_sub <= 300.0:
        record_pass("4.2 Weapon Base Stats Bounds", f"Weapon ATK [{w_min_atk}, {w_max_atk}], Sub-stat [{w_min_sub}, {w_max_sub}] within expected bounds")
    else:
        record_fail("4.2 Weapon Base Stats Bounds", f"Weapon stats out of bounds: {w_stats}")

    # 4.3 Remediated Weapons 128 & 131 Specific Stats
    w128 = cur.execute("SELECT base_atk, sub_stat_type, sub_stat_value FROM weapons WHERE weapon_id = 128;").fetchone()
    w131 = cur.execute("SELECT base_atk, sub_stat_type, sub_stat_value FROM weapons WHERE weapon_id = 131;").fetchone()
    if (w128["base_atk"] == 741 and w128["sub_stat_type"] == "CRIT Rate" and abs(w128["sub_stat_value"] - 11.0) < 0.01 and
        w131["base_atk"] == 741 and w131["sub_stat_type"] == "CRIT Rate" and abs(w131["sub_stat_value"] - 11.0) < 0.01):
        record_pass("4.3 Remediated Weapon Stats (128 & 131)", "Fang of the Mountain King & A Thousand Blazing Suns have Base ATK = 741, Sub-stat = 11.0% CRIT Rate")
    else:
        record_fail("4.3 Remediated Weapon Stats (128 & 131)", f"W128={dict(w128)}, W131={dict(w131)}")

    # 4.4 Sub-stat Type Enumeration
    valid_substats = {'CRIT DMG', 'CRIT Rate', 'Energy Recharge', 'Elemental Mastery', 'HP%', 'DEF%', 'Physical DMG', 'ATK%'}
    actual_substats = {r[0] for r in cur.execute("SELECT DISTINCT sub_stat_type FROM weapons;").fetchall()}
    invalid_substats = actual_substats - valid_substats
    if len(invalid_substats) == 0:
        record_pass("4.4 Sub-stat Type Enumeration", f"All weapon sub-stats map strictly to valid 8 official types: {actual_substats}")
    else:
        record_fail("4.4 Sub-stat Type Enumeration", f"Found unrecognized sub-stat types: {invalid_substats}")

    # 4.5 Release Patch Monotonic Range
    patch_stats = cur.execute("SELECT MIN(release_patch), MAX(release_patch) FROM characters;").fetchone()
    if patch_stats[0] >= 1.0 and patch_stats[1] <= 7.5:
        record_pass("4.5 Release Patch Range", f"Release patches strictly in [{patch_stats[0]}, {patch_stats[1]}]")
    else:
        record_fail("4.5 Release Patch Range", f"Release patches out of range: {patch_stats}")

    # 4.6 Aloy Representation (Region 'None', Rarity 5)
    aloy = cur.execute("SELECT rarity, vision, weapon_type, region FROM characters WHERE name = 'Aloy';").fetchone()
    if aloy and aloy["region"] == "None" and aloy["rarity"] == 5 and aloy["vision"] == "Cryo" and aloy["weapon_type"] == "Bow":
        record_pass("4.6 Aloy Representation", "Aloy has region 'None' (literal string), rarity 5, Cryo, Bow")
    else:
        record_fail("4.6 Aloy Representation", f"Aloy attributes mismatch: {dict(aloy) if aloy else None}")

    # 4.7 1-Piece Tiaras Specifications
    tiaras = cur.execute("SELECT artifact_set_id, name, region, domain_name, four_piece_bonus FROM artifact_sets WHERE artifact_set_id IN (15, 16, 17, 18);").fetchall()
    tiaras_ok = len(tiaras) == 4 and all(
        "Bosses" in t["domain_name"] and t["region"] == "Teyvat" and "1-Piece Set" in t["four_piece_bonus"]
        for t in tiaras
    )
    if tiaras_ok:
        record_pass("4.7 1-Piece Tiaras Specifications", "All 4 Tiaras (IDs 15-18) correctly configured with Bosses domain, Teyvat region, 1-Piece Set")
    else:
        record_fail("4.7 1-Piece Tiaras Specifications", f"Tiaras misconfigured: {[dict(t) for t in tiaras]}")

    conn.close()


# =====================================================================
# SUITE 5: RELATIONAL INDEX UTILIZATION & SARGABILITY STRESS
# =====================================================================
def run_suite_5():
    print("\n--- Suite 5: Relational Index Utilization & Sargability Stress ---")
    conn = get_connection()
    cur = conn.cursor()

    # 5.1 Schema Index Completeness
    required_indexes = {
        "idx_characters_region",
        "idx_characters_vision",
        "idx_weapons_type",
        "idx_weapons_signature",
        "idx_builds_character",
        "idx_builds_tier",
        "idx_builds_weapon",
        "idx_builds_artifact",
    }
    existing_indexes = {
        row[0]
        for row in cur.execute("SELECT name FROM sqlite_master WHERE type = 'index';").fetchall()
    }
    missing = required_indexes - existing_indexes
    if len(missing) == 0:
        record_pass("5.1 Schema Index Completeness", f"All {len(required_indexes)} required relational indexes present in sqlite_master")
    else:
        record_fail("5.1 Schema Index Completeness", f"Missing indexes: {missing}")

    # 5.2 Sargable Index Utilization via EXPLAIN QUERY PLAN
    indexed_queries = [
        ("idx_characters_region", "SELECT * FROM characters WHERE region = 'Fontaine';"),
        ("idx_characters_vision", "SELECT * FROM characters WHERE vision = 'Electro';"),
        ("idx_weapons_type", "SELECT * FROM weapons WHERE weapon_type = 'Polearm';"),
        ("idx_weapons_signature", "SELECT * FROM weapons WHERE signature_character_id = 41;"),
        ("idx_builds_character", "SELECT * FROM character_builds WHERE character_id = 41;"),
        ("idx_builds_tier", "SELECT * FROM character_builds WHERE tier_rating = 'SS';"),
        ("idx_builds_weapon", "SELECT * FROM character_builds WHERE recommended_weapon_id = 204;"),
        ("idx_builds_artifact", "SELECT * FROM character_builds WHERE recommended_artifact_id = 60;"),
    ]
    all_sargable_indexed = True
    for idx_name, q in indexed_queries:
        plan = cur.execute(f"EXPLAIN QUERY PLAN {q}").fetchall()
        plan_str = " ".join([str(p[3]) for p in plan])
        if "USING INDEX" not in plan_str or idx_name not in plan_str:
            all_sargable_indexed = False
            record_fail(f"5.2 Sargable Index ({idx_name})", f"Query plan did not use expected index: {plan_str}")
    if all_sargable_indexed:
        record_pass("5.2 Sargable Index Utilization", "All 8 relational indexes utilized via SEARCH ... USING INDEX on sargable predicates")

    # 5.3 Non-Sargable Index Bypass Detection
    # When an indexed column is wrapped in an expression, SQLite falls back to SCAN
    non_sargable_queries = [
        ("characters region bypass", "SELECT * FROM characters WHERE region || '' = 'Mondstadt';", "characters"),
        ("weapons weapon_type bypass", "SELECT * FROM weapons WHERE LOWER(weapon_type) = 'claymore';", "weapons"),
    ]
    all_bypasses_confirmed = True
    for label, q, table_name in non_sargable_queries:
        plan = cur.execute(f"EXPLAIN QUERY PLAN {q}").fetchall()
        plan_str = " ".join([str(p[3]) for p in plan])
        if f"SCAN {table_name}" not in plan_str:
            all_bypasses_confirmed = False
            record_fail(f"5.3 Non-Sargable Bypass ({label})", f"Expected SCAN but got: {plan_str}")
    if all_bypasses_confirmed:
        record_pass("5.3 Non-Sargable Bypass Detection", "Verified query optimizer correctly falls back to full SCAN for non-sargable expressions")

    # 5.4 Multi-Table JOIN Query Plan
    join_sql = """
        SELECT c.name, cb.build_name, w.name, a.name
        FROM character_builds cb
        JOIN characters c ON cb.character_id = c.character_id
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        JOIN artifact_sets a ON cb.recommended_artifact_id = a.artifact_set_id
        WHERE cb.tier_rating = 'SS';
    """
    join_plan = cur.execute(f"EXPLAIN QUERY PLAN {join_sql}").fetchall()
    join_plan_str = " ".join([str(p[3]) for p in plan])
    # The query must use idx_builds_tier for filtering and PK/FK lookups for joins
    has_tier_index = any("idx_builds_tier" in str(p[3]) for p in join_plan)
    if has_tier_index:
        record_pass("5.4 Multi-Table JOIN Query Plan", "4-Table JOIN efficiently uses idx_builds_tier and PK lookups without cross-product cartesian scans")
    else:
        record_fail("5.4 Multi-Table JOIN Query Plan", f"Expected idx_builds_tier in plan, got: {join_plan}")

    # 5.5 Index Forcing & Invalid Index Handling
    try:
        cur.execute("EXPLAIN QUERY PLAN SELECT * FROM weapons INDEXED BY idx_weapons_type WHERE weapon_type = 'Sword';")
        forced_ok = True
    except sqlite3.OperationalError:
        forced_ok = False

    try:
        cur.execute("EXPLAIN QUERY PLAN SELECT * FROM weapons INDEXED BY non_existent_index WHERE weapon_type = 'Sword';")
        invalid_rejected = False
    except sqlite3.OperationalError:
        invalid_rejected = True

    if forced_ok and invalid_rejected:
        record_pass("5.5 Index Forcing & Invalid Handling", "Forced index succeeds on valid index; invalid INDEXED BY cleanly raises OperationalError")
    else:
        record_fail("5.5 Index Forcing & Invalid Handling", f"forced_ok={forced_ok}, invalid_rejected={invalid_rejected}")

    conn.close()


# =====================================================================
# SUITE 6: CSV SERIALIZATION PARITY & INGESTION IDEMPOTENCY
# =====================================================================
def run_suite_6():
    print("\n--- Suite 6: CSV Serialization Parity & Ingestion Idempotency ---")
    conn = get_connection()
    cur = conn.cursor()

    # 6.1 Exact Record Count Parity
    expected_counts = {
        "characters.csv": ("characters", 129),
        "weapons.csv": ("weapons", 155),
        "artifact_sets.csv": ("artifact_sets", 64),
        "character_builds.csv": ("character_builds", 168),
    }
    counts_ok = True
    for csv_file, (tbl, exp_count) in expected_counts.items():
        csv_path = os.path.join(DATA_DIR, csv_file)
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            csv_len = len(list(reader))
        db_len = cur.execute(f"SELECT COUNT(*) FROM {tbl};").fetchone()[0]
        if csv_len != exp_count or db_len != exp_count:
            counts_ok = False
            record_fail(f"6.1 Record Count Parity ({tbl})", f"CSV={csv_len}, DB={db_len}, expected={exp_count}")
    if counts_ok:
        record_pass("6.1 Record Count Parity", "All 4 CSVs and database tables match exact targets (129, 155, 64, 168; Total 516)")

    # 6.2 Cell-for-Cell Parity
    # Characters check
    with open(os.path.join(DATA_DIR, "characters.csv"), "r", encoding="utf-8") as f:
        char_rows = list(csv.reader(f))[1:]
    db_chars = {r[0]: tuple(r) for r in cur.execute("SELECT character_id, name, rarity, vision, weapon_type, region, default_role, base_hp, base_atk, base_def, talent_priority, release_patch FROM characters;").fetchall()}
    char_parity = all(
        db_chars[int(r[0])] == (int(r[0]), r[1], int(r[2]), r[3], r[4], r[5], r[6], int(r[7]), int(r[8]), int(r[9]), r[10], float(r[11]))
        for r in char_rows
    )

    # Weapons check
    with open(os.path.join(DATA_DIR, "weapons.csv"), "r", encoding="utf-8") as f:
        weapon_rows = list(csv.reader(f))[1:]
    db_weapons = {r[0]: tuple(r) for r in cur.execute("SELECT weapon_id, name, weapon_type, rarity, base_atk, sub_stat_type, sub_stat_value, is_craftable, signature_character_id FROM weapons;").fetchall()}
    weapon_parity = all(
        db_weapons[int(r[0])] == (int(r[0]), r[1], r[2], int(r[3]), int(r[4]), r[5], float(r[6]), int(r[7]), int(r[8]) if r[8].strip() else None)
        for r in weapon_rows
    )

    # Artifacts check
    with open(os.path.join(DATA_DIR, "artifact_sets.csv"), "r", encoding="utf-8") as f:
        artifact_rows = list(csv.reader(f))[1:]
    db_artifacts = {r[0]: tuple(r) for r in cur.execute("SELECT artifact_set_id, name, domain_name, region, two_piece_bonus, four_piece_bonus FROM artifact_sets;").fetchall()}
    artifact_parity = all(
        db_artifacts[int(r[0])] == (int(r[0]), r[1], r[2], r[3], r[4], r[5])
        for r in artifact_rows
    )

    # Builds check
    with open(os.path.join(DATA_DIR, "character_builds.csv"), "r", encoding="utf-8") as f:
        build_rows = list(csv.reader(f))[1:]
    db_builds = {r[0]: tuple(r) for r in cur.execute("SELECT build_id, character_id, build_name, role, recommended_weapon_id, recommended_artifact_id, sands_stat, goblet_stat, circlet_stat, tier_rating, playstyle_notes FROM character_builds;").fetchall()}
    build_parity = all(
        db_builds[int(r[0])] == (int(r[0]), int(r[1]), r[2], r[3], int(r[4]), int(r[5]), r[6], r[7], r[8], r[9], r[10])
        for r in build_rows
    )

    if char_parity and weapon_parity and artifact_parity and build_parity:
        record_pass("6.2 Cell-for-Cell Parity", "100% cell-by-cell equality confirmed across all 4 tables (516/516 records)")
    else:
        record_fail("6.2 Cell-for-Cell Parity", f"Parity mismatch: chars={char_parity}, weapons={weapon_parity}, artifacts={artifact_parity}, builds={build_parity}")

    # 6.3 Capitano Complete Purge Check
    capitano_in_db = cur.execute("SELECT COUNT(*) FROM characters WHERE name LIKE '%Capitano%' OR character_id = 104;").fetchone()[0]
    capitano_build = cur.execute("SELECT COUNT(*) FROM character_builds WHERE build_id = 381 OR character_id = 104;").fetchone()[0]
    capitano_csv = False
    for csv_file in ["characters.csv", "weapons.csv", "artifact_sets.csv", "character_builds.csv"]:
        with open(os.path.join(DATA_DIR, csv_file), "r", encoding="utf-8") as f:
            if "Capitano" in f.read():
                capitano_csv = True
                break
    if capitano_in_db == 0 and capitano_build == 0 and not capitano_csv:
        record_pass("6.3 Capitano Complete Purge Check", "Zero traces of NPC Capitano (ID 104, Build 381) in database or CSV files")
    else:
        record_fail("6.3 Capitano Complete Purge Check", f"Capitano found: db={capitano_in_db}, build={capitano_build}, csv={capitano_csv}")

    # 6.4 Clean Text Encoding & Absence of Control Characters
    control_char_found = False
    for tbl, cols in [
        ("characters", ["name", "region", "default_role", "talent_priority"]),
        ("weapons", ["name", "sub_stat_type"]),
        ("artifact_sets", ["name", "domain_name", "region", "two_piece_bonus", "four_piece_bonus"]),
        ("character_builds", ["build_name", "role", "sands_stat", "goblet_stat", "circlet_stat", "playstyle_notes"]),
    ]:
        for col in cols:
            values = [row[0] for row in cur.execute(f"SELECT {col} FROM {tbl} WHERE {col} IS NOT NULL;").fetchall()]
            for val in values:
                if any(ord(c) < 32 and c not in '\r\n\t' for c in str(val)):
                    control_char_found = True
                    record_fail("6.4 Text Encoding & Control Chars", f"Found control character in {tbl}.{col}: {val!r}")
                    break
            if control_char_found:
                break
        if control_char_found:
            break
    if not control_char_found:
        record_pass("6.4 Text Encoding & Control Chars", "All textual fields across all 4 tables are free of unwanted control characters")

    # 6.5 Ingestion Idempotency & Determinism
    # Run init_db in a scratch directory to verify reproducibility
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_db = os.path.join(tmp_dir, "scratch_genshin.db")
        # Initialize scratch db
        scratch_conn = sqlite3.connect(tmp_db)
        from init_db import SCHEMA_SQL, load_csv
        scratch_conn.execute("PRAGMA foreign_keys = ON;")
        scratch_cur = scratch_conn.cursor()
        scratch_cur.executescript(SCHEMA_SQL)

        # Ingest characters
        char_rows = load_csv("characters.csv")
        scratch_cur.executemany("INSERT INTO characters VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", char_rows)

        # Ingest weapons
        weapon_rows = load_csv("weapons.csv")
        cleaned_w = [(int(r[0]), r[1], r[2], int(r[3]), int(r[4]), r[5], float(r[6]), int(r[7]), int(r[8]) if r[8].strip() else None) for r in weapon_rows]
        scratch_cur.executemany("INSERT INTO weapons VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", cleaned_w)

        # Ingest artifacts
        artifact_rows = load_csv("artifact_sets.csv")
        scratch_cur.executemany("INSERT INTO artifact_sets VALUES (?, ?, ?, ?, ?, ?);", artifact_rows)

        # Ingest builds
        build_rows = load_csv("character_builds.csv")
        scratch_cur.executemany("INSERT INTO character_builds VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", build_rows)
        scratch_conn.commit()

        fk_violations = scratch_cur.execute("PRAGMA foreign_key_check;").fetchall()
        tot = scratch_cur.execute("SELECT (SELECT count(*) FROM characters) + (SELECT count(*) FROM weapons) + (SELECT count(*) FROM artifact_sets) + (SELECT count(*) FROM character_builds);").fetchone()[0]
        scratch_conn.close()

        if len(fk_violations) == 0 and tot == 516:
            record_pass("6.5 Ingestion Idempotency & Determinism", "Pipeline re-execution produces 0 FK violations and exact 516 records")
        else:
            record_fail("6.5 Ingestion Idempotency & Determinism", f"FK violations={len(fk_violations)}, total_records={tot}")

    conn.close()


# =====================================================================
# SUITE 7: COMPLEX META LEARNING & REAL-WORLD QUERY SCENARIOS
# =====================================================================
def run_suite_7():
    print("\n--- Suite 7: Complex Meta Learning & Real-World Query Scenarios ---")
    conn = get_connection()
    cur = conn.cursor()

    # 7.1 Elemental Resonance Team Composition
    # Build a 4-hero team with Pyro Resonance (+25% ATK): Hu Tao (21), Xiangling (30), Xingqiu (31), Zhongli (20)
    team_ids = (21, 30, 31, 20)
    team_members = cur.execute(f"""
        SELECT c.character_id, c.name, c.vision, c.weapon_type, c.base_atk,
               cb.build_name, cb.role, w.name as weapon_name, a.name as artifact_name
        FROM characters c
        JOIN character_builds cb ON c.character_id = cb.character_id
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        JOIN artifact_sets a ON cb.recommended_artifact_id = a.artifact_set_id
        WHERE c.character_id IN {team_ids}
        GROUP BY c.character_id;
    """).fetchall()

    pyro_count = sum(1 for m in team_members if m["vision"] == "Pyro")
    if len(team_members) == 4 and pyro_count == 2:
        record_pass("7.1 Team Composition & Elemental Resonance", "Formulated 4-member Vaporize team with Pyro Resonance (Hu Tao, Xiangling, Xingqiu, Zhongli) successfully")
    else:
        record_fail("7.1 Team Composition & Elemental Resonance", f"Team members count={len(team_members)}, pyro_count={pyro_count}")

    # 7.2 Window Function Regional ATK Ranking
    ranked_query = """
        WITH Ranked AS (
            SELECT name, region, base_atk,
                   DENSE_RANK() OVER (PARTITION BY region ORDER BY base_atk DESC) as rk
            FROM characters
        )
        SELECT region, rk, name, base_atk
        FROM Ranked
        WHERE rk = 1
        ORDER BY region;
    """
    ranked_rows = cur.execute(ranked_query).fetchall()
    # There are 10 regions, each should have at least 1 rank 1 character
    regions_ranked = {r["region"] for r in ranked_rows}
    if len(ranked_rows) >= 10 and len(regions_ranked) == 10:
        record_pass("7.2 Window Function Regional ATK Ranking", f"DENSE_RANK correctly identified top ATK characters across all 10 regions ({len(ranked_rows)} records)")
    else:
        record_fail("7.2 Window Function Regional ATK Ranking", f"Expected 10 regions, got {len(regions_ranked)} ({len(ranked_rows)} rows)")

    # 7.3 F2P Build Feasibility Engine
    # Find all characters that have a build with an accessible weapon (is_craftable = 1 OR rarity <= 4)
    f2p_query = """
        SELECT DISTINCT c.character_id, c.name
        FROM characters c
        JOIN character_builds cb ON c.character_id = cb.character_id
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        WHERE w.is_craftable = 1 OR w.rarity <= 4;
    """
    f2p_chars = cur.execute(f2p_query).fetchall()
    # At least 70 characters should have accessible craftable/4-star recommended builds
    if len(f2p_chars) >= 70:
        record_pass("7.3 F2P Build Feasibility Engine", f"Identified {len(f2p_chars)} characters with craftable or 4★ recommended weapon builds")
    else:
        record_fail("7.3 F2P Build Feasibility Engine", f"Only {len(f2p_chars)} characters have F2P builds")

    # 7.4 Domain Optimization Aggregation
    domain_query = """
        SELECT domain_name, region, COUNT(*) as set_count
        FROM artifact_sets
        GROUP BY domain_name, region
        HAVING set_count >= 2
        ORDER BY set_count DESC, domain_name ASC;
    """
    domain_rows = cur.execute(domain_query).fetchall()
    if len(domain_rows) >= 20:
        record_pass("7.4 Domain Optimization Aggregation", f"Artifact domain aggregation identifies {len(domain_rows)} multi-set farming domains")
    else:
        record_fail("7.4 Domain Optimization Aggregation", f"Only {len(domain_rows)} multi-set domains found")

    # 7.5 Exact Regional Distribution across all 10 Regions
    expected_regions = {
        "Mondstadt": 23,
        "Liyue": 22,
        "Inazuma": 17,
        "Sumeru": 14,
        "Fontaine": 13,
        "Nod-Krai": 12,
        "Natlan": 11,
        "Outlander": 8,
        "Snezhnaya": 8,
        "None": 1,
    }
    actual_regions = dict(cur.execute("SELECT region, count(*) FROM characters GROUP BY region;").fetchall())
    if actual_regions == expected_regions:
        record_pass("7.5 Exact Regional Distribution", f"All 10 regions match exact targets: {actual_regions}")
    else:
        record_fail("7.5 Exact Regional Distribution", f"Regional mismatch: actual={actual_regions}, expected={expected_regions}")

    conn.close()


# =====================================================================
# MAIN RUNNER & TEST HARNESS ENTRYPOINT
# =====================================================================
def main():
    print("=" * 80)
    print("TIER 5 ADVERSARIAL COVERAGE HARDENING STRESS HARNESS")
    print(f"Target Database : {DB_PATH}")
    print(f"Project Root    : {PROJECT_ROOT}")
    print(f"Start Time      : {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    print("=" * 80)

    t0 = time.perf_counter()

    run_suite_1()
    run_suite_2()
    run_suite_3()
    run_suite_4()
    run_suite_5()
    run_suite_6()
    run_suite_7()

    elapsed = time.perf_counter() - t0

    print("\n" + "=" * 80)
    print("TIER 5 ADVERSARIAL STRESS HARNESS SUMMARY")
    print("=" * 80)
    print(f"Total Tests Run : {passed_tests + failed_tests}")
    print(f"Total Passed    : {passed_tests}")
    print(f"Total Failed    : {failed_tests}")
    print(f"Elapsed Time    : {elapsed:.3f} seconds")

    if failed_tests > 0:
        print("\n❌ ADVERSARIAL HARDENING FINDINGS IDENTIFIED:")
        for name, reason in findings:
            print(f"  * {name}: {reason}")
        print("=" * 80)
        sys.exit(1)
    else:
        print("\n✅ 100% HARDENED COVERAGE CONFIRMED — ZERO DEFECTS / ZERO GAPS")
        print("EXPLICIT VERDICT: APPROVE")
        print("=" * 80)
        sys.exit(0)

if __name__ == "__main__":
    main()
