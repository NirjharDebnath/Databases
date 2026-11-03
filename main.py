#!/usr/bin/env python3
"""
main.py
Quick SQL Playground for Genshin Impact Learning Database.
Run this script to execute sample queries or enter your own custom SQL queries!
"""

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "genshin_learning.db")

SAMPLE_QUERIES = [
    ("Top 5 Characters by Base ATK", """
        SELECT name, vision, weapon_type, region, base_atk 
        FROM characters 
        ORDER BY base_atk DESC 
        LIMIT 5;
    """),
    ("Character Count & Avg Base ATK by Vision", """
        SELECT 
            vision, 
            COUNT(*) AS total_heroes, 
            ROUND(AVG(base_atk), 1) AS avg_base_atk,
            ROUND(AVG(base_hp), 0) AS avg_base_hp
        FROM characters 
        GROUP BY vision 
        ORDER BY avg_base_atk DESC;
    """),
    ("Game8 SS-Tier Build Loadouts (Multi-Table JOIN)", """
        SELECT 
            c.name AS character,
            c.vision,
            cb.build_name,
            w.name AS weapon,
            a.name AS artifact_set,
            cb.sands_stat,
            cb.goblet_stat,
            cb.circlet_stat
        FROM character_builds cb
        JOIN characters c ON cb.character_id = c.character_id
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
        JOIN artifact_sets a ON cb.recommended_artifact_id = a.artifact_set_id
        WHERE cb.tier_rating = 'SS'
        ORDER BY c.name
        LIMIT 8;
    """),
    ("Regional Character Distribution (All 8 Regions)", """
        SELECT region, COUNT(*) AS character_count
        FROM characters
        GROUP BY region
        ORDER BY character_count DESC;
    """)
]

def print_table(columns, rows):
    if not rows:
        print("(No results returned)\n")
        return
    col_widths = [len(c) for c in columns]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val) if val is not None else "NULL"))

    header = " | ".join(f"{columns[i]:<{col_widths[i]}}" for i in range(len(columns)))
    divider = "-+-".join("-" * col_widths[i] for i in range(len(columns)))
    print(header)
    print(divider)
    for row in rows:
        line = " | ".join(f"{str(row[i]) if row[i] is not None else 'NULL':<{col_widths[i]}}" for i in range(len(columns)))
        print(line)
    print(f"\n({len(rows)} row(s) returned)\n")

def execute_query(conn, sql):
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        if cursor.description:
            columns = [d[0] for d in cursor.description]
            rows = cursor.fetchall()
            print_table(columns, rows)
        else:
            conn.commit()
            print("Query executed successfully (no result set).\n")
    except Exception as e:
        print(f"SQL Error: {e}\n")

def main():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}. Run 'python3 init_db.py' first.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    print("=" * 65)
    print("  GENSHIN IMPACT SQL LEARNING PLAYGROUND ('genshin_learning.db')")
    print("=" * 65)
    print("Running initial showcase queries...\n")

    for title, query in SAMPLE_QUERIES:
        print(f"▶ Query: {title}")
        print(f"SQL:{query.strip()}\n")
        execute_query(conn, query)

    print("-" * 65)
    print("Interactive Mode:")
    print("Type any SELECT query below (or type 'exit' / 'quit' to close).\n")

    while True:
        try:
            user_input = input("SQL> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print("Goodbye! Happy querying.")
                break
            execute_query(conn, user_input)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Happy querying!")
            break

    conn.close()

if __name__ == "__main__":
    main()
