#!/usr/bin/env python3
"""
init_db.py
Initializes the SQLite database 'genshin_learning.db' by reading curated CSVs
from the data/ directory, enforcing foreign key relationships, constraints,
indexes, and verifying relational integrity.
"""

import os
import csv
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "genshin_learning.db")

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS character_builds;
DROP TABLE IF EXISTS weapons;
DROP TABLE IF EXISTS artifact_sets;
DROP TABLE IF EXISTS characters;

-- 1. Characters Dimension Table
CREATE TABLE characters (
    character_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    rarity INTEGER NOT NULL CHECK (rarity IN (4, 5)),
    vision TEXT NOT NULL CHECK (vision IN ('Pyro', 'Hydro', 'Anemo', 'Electro', 'Dendro', 'Cryo', 'Geo')),
    weapon_type TEXT NOT NULL CHECK (weapon_type IN ('Sword', 'Claymore', 'Polearm', 'Bow', 'Catalyst')),
    region TEXT NOT NULL,
    default_role TEXT NOT NULL,
    base_hp INTEGER NOT NULL,
    base_atk INTEGER NOT NULL,
    base_def INTEGER NOT NULL,
    talent_priority TEXT NOT NULL,
    release_patch REAL NOT NULL
);

-- 2. Weapons Dimension Table
CREATE TABLE weapons (
    weapon_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    weapon_type TEXT NOT NULL CHECK (weapon_type IN ('Sword', 'Claymore', 'Polearm', 'Bow', 'Catalyst')),
    rarity INTEGER NOT NULL CHECK (rarity IN (3, 4, 5)),
    base_atk INTEGER NOT NULL,
    sub_stat_type TEXT NOT NULL,
    sub_stat_value REAL NOT NULL,
    is_craftable INTEGER NOT NULL CHECK (is_craftable IN (0, 1)),
    signature_character_id INTEGER REFERENCES characters(character_id) ON DELETE SET NULL
);

-- 3. Artifact Sets Dimension Table
CREATE TABLE artifact_sets (
    artifact_set_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    domain_name TEXT NOT NULL,
    region TEXT NOT NULL,
    two_piece_bonus TEXT NOT NULL,
    four_piece_bonus TEXT NOT NULL
);

-- 4. Character Builds Relational Bridge Table (Game8 Meta Builds)
CREATE TABLE character_builds (
    build_id INTEGER PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters(character_id) ON DELETE CASCADE,
    build_name TEXT NOT NULL,
    role TEXT NOT NULL,
    recommended_weapon_id INTEGER NOT NULL REFERENCES weapons(weapon_id) ON DELETE RESTRICT,
    recommended_artifact_id INTEGER NOT NULL REFERENCES artifact_sets(artifact_set_id) ON DELETE RESTRICT,
    sands_stat TEXT NOT NULL,
    goblet_stat TEXT NOT NULL,
    circlet_stat TEXT NOT NULL,
    tier_rating TEXT NOT NULL CHECK (tier_rating IN ('SS', 'S+', 'S', 'A')),
    playstyle_notes TEXT
);

-- Indexes for performance and learning query plans (EXPLAIN QUERY PLAN)
CREATE INDEX idx_characters_region ON characters(region);
CREATE INDEX idx_characters_vision ON characters(vision);
CREATE INDEX idx_weapons_type ON weapons(weapon_type);
CREATE INDEX idx_builds_character ON character_builds(character_id);
CREATE INDEX idx_builds_tier ON character_builds(tier_rating);
"""

def load_csv(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    return rows

def main():
    print(f"Connecting to database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    print("Creating tables and indexes...")
    cursor.executescript(SCHEMA_SQL)

    # 1. Populate characters
    print("Loading characters.csv...")
    char_rows = load_csv("characters.csv")
    cursor.executemany(
        """
        INSERT INTO characters (
            character_id, name, rarity, vision, weapon_type, region,
            default_role, base_hp, base_atk, base_def, talent_priority, release_patch
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        char_rows
    )

    # 2. Populate weapons
    print("Loading weapons.csv...")
    weapon_rows = load_csv("weapons.csv")
    cleaned_weapons = []
    for r in weapon_rows:
        # If signature_character_id is empty, insert None (SQL NULL)
        sig_id = int(r[8]) if r[8].strip() else None
        cleaned_weapons.append((
            int(r[0]), r[1], r[2], int(r[3]), int(r[4]), r[5], float(r[6]), int(r[7]), sig_id
        ))
    cursor.executemany(
        """
        INSERT INTO weapons (
            weapon_id, name, weapon_type, rarity, base_atk,
            sub_stat_type, sub_stat_value, is_craftable, signature_character_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        cleaned_weapons
    )

    # 3. Populate artifact_sets
    print("Loading artifact_sets.csv...")
    artifact_rows = load_csv("artifact_sets.csv")
    cursor.executemany(
        """
        INSERT INTO artifact_sets (
            artifact_set_id, name, domain_name, region,
            two_piece_bonus, four_piece_bonus
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        artifact_rows
    )

    # 4. Populate character_builds
    print("Loading character_builds.csv...")
    build_rows = load_csv("character_builds.csv")
    cursor.executemany(
        """
        INSERT INTO character_builds (
            build_id, character_id, build_name, role,
            recommended_weapon_id, recommended_artifact_id,
            sands_stat, goblet_stat, circlet_stat, tier_rating, playstyle_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        build_rows
    )

    conn.commit()

    # Integrity Check
    print("\nRunning relational integrity check (PRAGMA foreign_key_check)...")
    fk_violations = cursor.execute("PRAGMA foreign_key_check;").fetchall()
    if fk_violations:
        print(f"WARNING: Found {len(fk_violations)} foreign key violation(s): {fk_violations}")
    else:
        print("PASS: 0 Foreign Key violations! Schema integrity confirmed.")

    # Table Row Summary
    print("\n" + "="*50)
    print("DATABASE POPULATION SUMMARY")
    print("="*50)
    for table in ["characters", "weapons", "artifact_sets", "character_builds"]:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]
        print(f"Table '{table:18}': {count:3} rows")

    total_rows = cursor.execute("""
        SELECT 
            (SELECT COUNT(*) FROM characters) +
            (SELECT COUNT(*) FROM weapons) +
            (SELECT COUNT(*) FROM artifact_sets) +
            (SELECT COUNT(*) FROM character_builds);
    """).fetchone()[0]
    print(f"\nTotal rows across database: {total_rows}")

    # Regional Character Breakdown
    print("\n" + "-"*50)
    print("CHARACTERS PER REGION")
    print("-" * 50)
    regional_counts = cursor.execute("""
        SELECT region, COUNT(*) as count 
        FROM characters 
        GROUP BY region 
        ORDER BY count DESC, region ASC;
    """).fetchall()
    for reg, c in regional_counts:
        print(f"Region '{reg:12}': {c:2} characters")

    conn.close()
    print("\nDatabase initialization complete! Ready for SQL learning.")

if __name__ == "__main__":
    main()
