#!/usr/bin/env python3
"""
verify_db.py
Verifies the integrity, row counts, regional character distributions,
artifact sets count (must be exactly 64), and tests sample queries against genshin_learning.db.
"""

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "genshin_learning.db")

def test_database():
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # 1. Foreign Key Verification
    fk_violations = cursor.execute("PRAGMA foreign_key_check;").fetchall()
    assert len(fk_violations) == 0, f"Found foreign key violations: {fk_violations}"
    print("✓ Foreign Key Integrity: PASSED (0 violations)")

    # 2. Row Counts Verification
    expected_tables = {
        "characters": 114,
        "weapons": 103,
        "artifact_sets": 64,
        "character_builds": 107
    }
    for table, exp_count in expected_tables.items():
        count = cursor.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]
        assert count == exp_count, f"Table {table} has {count} rows, expected {exp_count}"
        print(f"✓ Table '{table}' row count: {count} rows (PASSED)")

    # 3. Exact 64 Artifact Sets Check
    artifact_count = cursor.execute("SELECT COUNT(*) FROM artifact_sets;").fetchone()[0]
    assert artifact_count == 64, f"Expected exactly 64 artifact sets, found {artifact_count}"
    print("✓ Exact 64 Artifact Sets: CONFIRMED (PASSED)")

    # 4. Regional Character Verification
    expected_regions = {
        "Liyue": 21,
        "Mondstadt": 19,
        "Inazuma": 17,
        "Sumeru": 14,
        "Fontaine": 13,
        "Natlan": 10,
        "Nod-Krai": 9,
        "Outlander": 7,
        "Snezhnaya": 4
    }
    region_rows = cursor.execute("SELECT region, COUNT(*) FROM characters GROUP BY region;").fetchall()
    found_regions = dict(region_rows)
    for reg, exp_count in expected_regions.items():
        actual = found_regions.get(reg, 0)
        assert actual == exp_count, f"Region {reg} expected {exp_count} characters, got {actual}"
        print(f"✓ Region '{reg}': {actual} characters confirmed (PASSED)")

    # 5. Sample Query Executions
    queries = [
        ("Multi-table INNER JOIN", """
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
        """)
    ]

    print("\nTesting Core SQL Learning Queries on Expanded Dataset:")
    for label, sql in queries:
        res = cursor.execute(sql).fetchall()
        assert len(res) > 0, f"Query '{label}' returned 0 rows"
        print(f"✓ Query '{label}': executed successfully ({len(res)} rows returned)")

    conn.close()
    print("\nALL EXPANDED DATABASE TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_database()
