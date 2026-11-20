#!/usr/bin/env python3
"""
verify_db.py
Comprehensive verification suite for genshin_learning.db per ORIGINAL_REQUEST.md § R5:
1. Foreign key integrity enforcement (PRAGMA foreign_key_check == 0).
2. Exact table row counts (characters: 129, weapons: 155, artifact_sets: 64, character_builds: 168).
3. Zero orphaned characters without builds (100% build coverage).
4. Regional distribution across all 10 regions (Total 129 characters).
5. Weapon type compatibility (100% match between character and recommended weapon).
6. 1:1 CSV-to-DB record parity across all 4 tables.
7. Schema relational indexes verification (all 8 required indexes present).
8. Core SQL learning queries execution (joins, aggregations, tiaras, window functions).
"""

import os
import csv
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "genshin_learning.db")

def test_database():
    print("=" * 70)
    print("GENSHIN IMPACT DATABASE VERIFICATION SUITE (R5)")
    print(f"Target Database : {DB_PATH}")
    print("=" * 70)

    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # -------------------------------------------------------------
    # 1. Foreign Key Verification & PRAGMA Status
    # -------------------------------------------------------------
    print("\n--- 1. Foreign Key Integrity Check ---")
    fk_status = cursor.execute("PRAGMA foreign_keys;").fetchone()[0]
    assert fk_status == 1, "PRAGMA foreign_keys must be enabled"

    fk_violations = cursor.execute("PRAGMA foreign_key_check;").fetchall()
    assert len(fk_violations) == 0, f"Found foreign key violations: {fk_violations}"
    print("✓ Foreign Key Integrity: PASSED (0 violations, PRAGMA foreign_keys = ON)")

    # -------------------------------------------------------------
    # 2. Exact Table Row Counts Verification
    # -------------------------------------------------------------
    print("\n--- 2. Exact Table Row Counts Check ---")
    expected_tables = {
        "characters": 129,
        "weapons": 155,
        "artifact_sets": 64,
        "character_builds": 168,
    }
    total_rows = 0
    for table, exp_count in expected_tables.items():
        count = cursor.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]
        assert count == exp_count, f"Table '{table}' has {count} rows, expected {exp_count}"
        total_rows += count
        print(f"✓ Table '{table:<18}': {count:3} rows (matches expected {exp_count})")
    assert total_rows == 516, f"Expected 516 total database rows, found {total_rows}"
    print(f"✓ Total Database Records: {total_rows} rows confirmed")

    # -------------------------------------------------------------
    # 3. Zero Orphaned Characters Check
    # -------------------------------------------------------------
    print("\n--- 3. Orphaned Characters Verification ---")
    orphaned = cursor.execute("""
        SELECT c.character_id, c.name
        FROM characters c
        LEFT JOIN character_builds cb ON c.character_id = cb.character_id
        WHERE cb.build_id IS NULL;
    """).fetchall()
    assert len(orphaned) == 0, f"Found {len(orphaned)} orphaned character(s) without builds: {orphaned}"
    print("✓ Zero Orphaned Characters: CONFIRMED (129/129 characters have >= 1 build)")

    # -------------------------------------------------------------
    # 4. Regional Character Distribution (All 10 Regions)
    # -------------------------------------------------------------
    print("\n--- 4. Regional Character Distribution Check ---")
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
    region_rows = cursor.execute("""
        SELECT region, COUNT(*) 
        FROM characters 
        GROUP BY region 
        ORDER BY COUNT(*) DESC, region ASC;
    """).fetchall()
    found_regions = dict(region_rows)

    assert set(found_regions.keys()) == set(expected_regions.keys()), (
        f"Region set mismatch: found {set(found_regions.keys())}, expected {set(expected_regions.keys())}"
    )

    for reg, exp_count in expected_regions.items():
        actual = found_regions.get(reg, 0)
        assert actual == exp_count, f"Region '{reg}' expected {exp_count} characters, got {actual}"
        print(f"✓ Region '{reg:<12}': {actual:2} characters confirmed (PASSED)")

    assert sum(found_regions.values()) == 129, f"Sum of regional characters is {sum(found_regions.values())}, expected 129"
    print("✓ Regional Distribution: ALL 10 REGIONS MATCH EXACT SPECIFICATION (129 total)")

    # -------------------------------------------------------------
    # 5. Weapon Type Compatibility Verification
    # -------------------------------------------------------------
    print("\n--- 5. Build Weapon Type Compatibility Check ---")
    weapon_mismatches = cursor.execute("""
        SELECT cb.build_id, c.name, c.weapon_type, w.name, w.weapon_type
        FROM character_builds cb
        JOIN characters c ON cb.character_id = c.character_id
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        WHERE c.weapon_type != w.weapon_type;
    """).fetchall()
    assert len(weapon_mismatches) == 0, f"Found {len(weapon_mismatches)} weapon type mismatch(es): {weapon_mismatches}"
    print(f"✓ Weapon Type Matching: PASSED (168/168 builds have 100% weapon type compatibility)")

    # -------------------------------------------------------------
    # 6. 1:1 CSV-to-DB Record Parity Verification
    # -------------------------------------------------------------
    print("\n--- 6. 1:1 CSV-to-DB Record Parity Check ---")

    # 6.1 characters.csv parity
    chars_csv_path = os.path.join(DATA_DIR, "characters.csv")
    assert os.path.exists(chars_csv_path), "characters.csv missing"
    with open(chars_csv_path, "r", encoding="utf-8") as f:
        char_csv_rows = list(csv.reader(f))[1:]
    assert len(char_csv_rows) == 129, f"characters.csv row count mismatch: {len(char_csv_rows)}"
    db_chars = cursor.execute("""
        SELECT character_id, name, rarity, vision, weapon_type, region,
               default_role, base_hp, base_atk, base_def, talent_priority, release_patch
        FROM characters;
    """).fetchall()
    db_chars_map = {r[0]: r for r in db_chars}
    for r in char_csv_rows:
        cid = int(r[0])
        expected = (
            cid, r[1], int(r[2]), r[3], r[4], r[5],
            r[6], int(r[7]), int(r[8]), int(r[9]), r[10], float(r[11])
        )
        assert cid in db_chars_map, f"Character ID {cid} missing from DB"
        assert db_chars_map[cid] == expected, f"Character parity mismatch on ID {cid}: {expected} != {db_chars_map[cid]}"
    print("✓ Parity 'characters.csv'     ➔ 'characters' table     : 129 records verified")

    # 6.2 weapons.csv parity
    weapons_csv_path = os.path.join(DATA_DIR, "weapons.csv")
    assert os.path.exists(weapons_csv_path), "weapons.csv missing"
    with open(weapons_csv_path, "r", encoding="utf-8") as f:
        weapon_csv_rows = list(csv.reader(f))[1:]
    assert len(weapon_csv_rows) == 155, f"weapons.csv row count mismatch: {len(weapon_csv_rows)}"
    db_weapons = cursor.execute("""
        SELECT weapon_id, name, weapon_type, rarity, base_atk,
               sub_stat_type, sub_stat_value, is_craftable, signature_character_id
        FROM weapons;
    """).fetchall()
    db_weapons_map = {r[0]: r for r in db_weapons}
    for r in weapon_csv_rows:
        wid = int(r[0])
        sig_id = int(r[8]) if r[8].strip() else None
        expected = (
            wid, r[1], r[2], int(r[3]), int(r[4]),
            r[5], float(r[6]), int(r[7]), sig_id
        )
        assert wid in db_weapons_map, f"Weapon ID {wid} missing from DB"
        assert db_weapons_map[wid] == expected, f"Weapon parity mismatch on ID {wid}: {expected} != {db_weapons_map[wid]}"
    print("✓ Parity 'weapons.csv'        ➔ 'weapons' table        : 155 records verified")

    # 6.3 artifact_sets.csv parity
    artifacts_csv_path = os.path.join(DATA_DIR, "artifact_sets.csv")
    assert os.path.exists(artifacts_csv_path), "artifact_sets.csv missing"
    with open(artifacts_csv_path, "r", encoding="utf-8") as f:
        artifact_csv_rows = list(csv.reader(f))[1:]
    assert len(artifact_csv_rows) == 64, f"artifact_sets.csv row count mismatch: {len(artifact_csv_rows)}"
    db_artifacts = cursor.execute("""
        SELECT artifact_set_id, name, domain_name, region, two_piece_bonus, four_piece_bonus
        FROM artifact_sets;
    """).fetchall()
    db_artifacts_map = {r[0]: r for r in db_artifacts}
    for r in artifact_csv_rows:
        aid = int(r[0])
        expected = (aid, r[1], r[2], r[3], r[4], r[5])
        assert aid in db_artifacts_map, f"Artifact set ID {aid} missing from DB"
        assert db_artifacts_map[aid] == expected, f"Artifact parity mismatch on ID {aid}: {expected} != {db_artifacts_map[aid]}"
    print("✓ Parity 'artifact_sets.csv'  ➔ 'artifact_sets' table  :  64 records verified")

    # 6.4 character_builds.csv parity
    builds_csv_path = os.path.join(DATA_DIR, "character_builds.csv")
    assert os.path.exists(builds_csv_path), "character_builds.csv missing"
    with open(builds_csv_path, "r", encoding="utf-8") as f:
        build_csv_rows = list(csv.reader(f))[1:]
    assert len(build_csv_rows) == 168, f"character_builds.csv row count mismatch: {len(build_csv_rows)}"
    db_builds = cursor.execute("""
        SELECT build_id, character_id, build_name, role,
               recommended_weapon_id, recommended_artifact_id,
               sands_stat, goblet_stat, circlet_stat, tier_rating, playstyle_notes
        FROM character_builds;
    """).fetchall()
    db_builds_map = {r[0]: r for r in db_builds}
    for r in build_csv_rows:
        bid = int(r[0])
        expected = (
            bid, int(r[1]), r[2], r[3],
            int(r[4]), int(r[5]), r[6], r[7], r[8], r[9], r[10]
        )
        assert bid in db_builds_map, f"Build ID {bid} missing from DB"
        assert db_builds_map[bid] == expected, f"Build parity mismatch on ID {bid}: {expected} != {db_builds_map[bid]}"
    print("✓ Parity 'character_builds.csv' ➔ 'character_builds': 168 records verified")
    print("✓ 1:1 CSV-to-DB Parity: 100% CELL-FOR-CELL PARITY CONFIRMED")

    # -------------------------------------------------------------
    # 7. Relational Schema Indexes Verification
    # -------------------------------------------------------------
    print("\n--- 7. Relational Schema Indexes Check ---")
    required_indexes = [
        "idx_characters_region",
        "idx_characters_vision",
        "idx_weapons_type",
        "idx_weapons_signature",
        "idx_builds_character",
        "idx_builds_tier",
        "idx_builds_weapon",
        "idx_builds_artifact",
    ]
    existing_indexes = {
        row[0]
        for row in cursor.execute("SELECT name FROM sqlite_master WHERE type = 'index';").fetchall()
    }
    for idx in required_indexes:
        assert idx in existing_indexes, f"Missing required index: {idx}"
        print(f"✓ Index '{idx}': verified")
    print(f"✓ Schema Relational Indexes: ALL {len(required_indexes)} INDEXES PRESENT")

    # -------------------------------------------------------------
    # 8. Core SQL Learning Queries Execution
    # -------------------------------------------------------------
    print("\n--- 8. Core SQL Learning Queries Check ---")
    queries = [
        ("Multi-table INNER JOIN (EXPLAIN QUERY PLAN)", """
            SELECT c.name, cb.build_name, w.name, a.name, cb.tier_rating
            FROM character_builds cb
            JOIN characters c ON cb.character_id = c.character_id
            JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
            JOIN artifact_sets a ON cb.recommended_artifact_id = a.artifact_set_id
            WHERE cb.tier_rating = 'SS'
            LIMIT 5;
        """),
        ("Craftable vs Non-Craftable Weapons Aggregation", """
            SELECT 
                is_craftable, 
                COUNT(*) as count, 
                ROUND(AVG(base_atk), 1) as avg_atk
            FROM weapons
            GROUP BY is_craftable;
        """),
        ("1-Piece Tiaras Query", """
            SELECT name, domain_name, two_piece_bonus, four_piece_bonus
            FROM artifact_sets
            WHERE name LIKE 'Prayers%';
        """),
        ("CTE with DENSE_RANK Window Function", """
            WITH Ranked AS (
                SELECT name, region, base_atk,
                       DENSE_RANK() OVER (PARTITION BY region ORDER BY base_atk DESC) as rk
                FROM characters
            )
            SELECT region, rk, name, base_atk
            FROM Ranked
            WHERE rk = 1
            ORDER BY region;
        """),
    ]

    for label, sql in queries:
        # Verify query plan execution
        plan = cursor.execute(f"EXPLAIN QUERY PLAN {sql}").fetchall()
        assert len(plan) > 0, f"Query plan generation failed for '{label}'"
        res = cursor.execute(sql).fetchall()
        assert len(res) > 0, f"Query '{label}' returned 0 rows"
        print(f"✓ Query '{label}': executed successfully ({len(res)} rows returned)")

    conn.close()
    print("\n" + "=" * 70)
    print("ALL EXPANDED DATABASE VERIFICATION CHECKS PASSED (EXIT CODE 0)!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        test_database()
    except Exception as exc:
        print(f"\n❌ VERIFICATION FAILURE: {exc}", file=sys.stderr)
        sys.exit(1)
