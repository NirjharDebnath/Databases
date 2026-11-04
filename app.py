#!/usr/bin/env python3
"""
app.py
Kaedehara Kazuha Themed Web Server for SQL Learning.
Interactive query console, visual ER model, schema explorer,
and client-side IntelliSense-style SQL autocomplete.
"""

import os
import time
import sqlite3
import re
from flask import Flask, render_template, request, jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "genshin_learning.db")

app = Flask(__name__)

@app.errorhandler(404)
def handle_not_found(error):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "API endpoint not found."}), 404
    return error

@app.errorhandler(405)
def handle_method_not_allowed(error):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "HTTP method is not allowed for this API endpoint."}), 405
    return error

# Sample queries curated for learning
SAMPLE_QUERIES = [
    {
        "category": "Basic Selection",
        "title": "5★ Characters Ordered by Base ATK",
        "description": "Demonstrates SELECT, WHERE, ORDER BY, and LIMIT",
        "query": """SELECT name, vision, weapon_type, region, base_atk, base_hp
FROM characters
WHERE rarity = 5
ORDER BY base_atk DESC
LIMIT 8;"""
    },
    {
        "category": "String & Null Logic",
        "title": "Weapons with CRIT Sub-stats & Signatures",
        "description": "Demonstrates LIKE, IS NOT NULL, and INNER JOIN",
        "query": """SELECT 
    w.name AS weapon_name,
    w.weapon_type,
    w.base_atk,
    w.sub_stat_type,
    w.sub_stat_value,
    c.name AS signature_owner
FROM weapons w
INNER JOIN characters c ON w.signature_character_id = c.character_id
WHERE w.sub_stat_type LIKE 'CRIT%'
ORDER BY w.base_atk DESC;"""
    },
    {
        "category": "Multi-Table JOIN",
        "title": "Kazuha's Game8 SS-Tier Build Loadouts",
        "description": "Joins 4 interconnected tables (Characters, Builds, Weapons, Artifacts)",
        "query": """SELECT 
    c.name AS character,
    c.vision,
    c.region,
    cb.build_name,
    cb.role,
    w.name AS recommended_weapon,
    w.sub_stat_type AS weapon_substat,
    a.name AS recommended_artifact,
    cb.sands_stat,
    cb.goblet_stat,
    cb.circlet_stat
FROM character_builds cb
JOIN characters c ON cb.character_id = c.character_id
JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
JOIN artifact_sets a ON cb.recommended_artifact_id = a.artifact_set_id
WHERE cb.tier_rating = 'SS'
ORDER BY c.region, c.name
LIMIT 12;"""
    },
    {
        "category": "Aggregation & HAVING",
        "title": "Average Stats & Hero Count by Vision",
        "description": "Demonstrates GROUP BY, COUNT, AVG, ROUND, and HAVING",
        "query": """SELECT 
    vision,
    COUNT(*) AS hero_count,
    ROUND(AVG(base_atk), 1) AS avg_base_atk,
    ROUND(AVG(base_hp), 0) AS avg_base_hp,
    ROUND(AVG(base_def), 0) AS avg_base_def
FROM characters
GROUP BY vision
HAVING COUNT(*) >= 10
ORDER BY avg_base_atk DESC;"""
    },
    {
        "category": "Common Table Expression (CTE)",
        "title": "Characters Above Their Regional ATK Average",
        "description": "Demonstrates WITH ... AS modular CTEs and Subqueries",
        "query": """WITH RegionalStats AS (
    SELECT 
        region,
        ROUND(AVG(base_atk), 1) AS avg_reg_atk
    FROM characters
    GROUP BY region
)
SELECT 
    c.name,
    c.region,
    c.vision,
    c.base_atk,
    r.avg_reg_atk,
    (c.base_atk - r.avg_reg_atk) AS atk_above_average
FROM characters c
JOIN RegionalStats r ON c.region = r.region
WHERE c.base_atk > r.avg_reg_atk
ORDER BY atk_above_average DESC
LIMIT 10;"""
    },
    {
        "category": "Window Functions",
        "title": "Top 2 Highest Base ATK per Region (DENSE_RANK)",
        "description": "Demonstrates PARTITION BY, OVER, and DENSE_RANK()",
        "query": """WITH RankedHeroes AS (
    SELECT 
        name,
        region,
        vision,
        weapon_type,
        base_atk,
        DENSE_RANK() OVER (PARTITION BY region ORDER BY base_atk DESC) AS regional_rank
    FROM characters
)
SELECT region, regional_rank, name, vision, weapon_type, base_atk
FROM RankedHeroes
WHERE regional_rank <= 2
ORDER BY region, regional_rank;"""
    }
]

def get_db_connection():
    """Connect to SQLite database in read-only mode for safety."""
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/query", methods=["POST"])
def execute_query():
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Request must use Content-Type: application/json."
        }), 415

    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify({"success": False, "error": "Request body must be a JSON object."}), 400

    raw_query = data.get("query", "")
    if not isinstance(raw_query, str):
        return jsonify({"success": False, "error": "The query must be a string."}), 400
    raw_query = raw_query.strip()

    if not raw_query:
        return jsonify({"success": False, "error": "Query cannot be empty."}), 400

    # Safety check: enforce read-only SELECT or EXPLAIN queries
    clean_query = re.sub(r"--.*$", "", raw_query, flags=re.MULTILINE)  # Strip comments
    clean_query = re.sub(r"/\*.*?\*/", "", clean_query, flags=re.DOTALL).strip()

    forbidden_patterns = [
        r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|REPLACE|ATTACH|DETACH|VACUUM|REINDEX|PRAGMA)\b"
    ]
    for pattern in forbidden_patterns:
        if re.search(pattern, clean_query, re.IGNORECASE):
            return jsonify({
                "success": False,
                "error": "Security Restriction: Only read-only queries (SELECT, WITH, EXPLAIN) are permitted."
            }), 403

    start_time = time.perf_counter()
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(raw_query)
        
        columns = [d[0] for d in cursor.description] if cursor.description else []
        rows = [list(row) for row in cursor.fetchall()]
        execution_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return jsonify({
            "success": True,
            "columns": columns,
            "rows": rows,
            "count": len(rows),
            "execution_time_ms": execution_time_ms
        })

    except sqlite3.Error as e:
        execution_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return jsonify({
            "success": False,
            "error": str(e),
            "execution_time_ms": execution_time_ms
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Internal Error: {str(e)}"
        }), 500
    finally:
        if conn is not None:
            conn.close()

@app.route("/api/schema", methods=["GET"])
def get_schema():
    """Returns database schema metadata for tables, columns, PK, FK, and row counts."""
    conn = get_db_connection()
    cursor = conn.cursor()

    tables = ["characters", "weapons", "artifact_sets", "character_builds"]
    schema_data = {}

    for table in tables:
        # Get row count
        count = cursor.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]

        # Get column info: cid, name, type, notnull, dflt_value, pk
        cols = cursor.execute(f"PRAGMA table_info({table});").fetchall()
        columns = []
        for c in cols:
            columns.append({
                "name": c["name"],
                "type": c["type"],
                "notnull": bool(c["notnull"]),
                "is_pk": bool(c["pk"])
            })

        # Get foreign keys: id, seq, table, from, to, on_update, on_delete, match
        fks = cursor.execute(f"PRAGMA foreign_key_list({table});").fetchall()
        foreign_keys = []
        for fk in fks:
            foreign_keys.append({
                "from": fk["from"],
                "to_table": fk["table"],
                "to_column": fk["to"]
            })

        schema_data[table] = {
            "row_count": count,
            "columns": columns,
            "foreign_keys": foreign_keys
        }

    conn.close()
    return jsonify(schema_data)

@app.route("/api/samples", methods=["GET"])
def get_samples():
    return jsonify(SAMPLE_QUERIES)

@app.route("/api/table/<table_name>/preview", methods=["GET"])
def preview_table(table_name):
    allowed = ["characters", "weapons", "artifact_sets", "character_builds"]
    if table_name not in allowed:
        return jsonify({"error": "Invalid table name"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
    columns = [d[0] for d in cursor.description]
    rows = [list(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify({"columns": columns, "rows": rows})

if __name__ == "__main__":
    port = 12000
    print(f"\n🍁 Kaedehara Kazuha SQL Sanctuary is starting on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
