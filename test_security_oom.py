#!/usr/bin/env python3
"""
test_security_oom.py
Comprehensive test suite verifying:
1. Security: Blocked writes, schema alterations, ATTACH, PRAGMA.
2. OOM & DoS: Infinite recursive CTE aborts cleanly via timeout watchdog.
3. OOM & Cartesian Join: Stream capping at MAX_STREAM_ROWS without memory explosion.
4. Correctness: Standard SELECT, JOIN, GROUP BY, and CTE queries succeed.
5. Endpoints: /api/schema and /api/samples function properly.
"""

import time
import json
from app import app, MAX_STREAM_ROWS, QUERY_TIMEOUT_SECONDS

def run_tests():
    client = app.test_client()
    passed = 0
    failed = 0

    def assert_true(cond, name, details=""):
        nonlocal passed, failed
        if cond:
            print(f"  ✅ PASS: {name}")
            passed += 1
        else:
            print(f"  ❌ FAIL: {name} - {details}")
            failed += 1

    print("=" * 60)
    print("RUNNING SECURITY & OOM MITIGATION TESTS")
    print("=" * 60)

    # 1. Normal Queries
    print("\n--- 1. Testing Standard Read Queries ---")
    res = client.post("/api/query", json={"query": "SELECT name, vision, region FROM characters LIMIT 5;"})
    assert_true(res.status_code == 200, "Standard SELECT returns HTTP 200")
    lines = [json.loads(line) for line in res.data.decode().strip().split("\n") if line.strip()]
    assert_true(lines[0]["type"] == "start" and len(lines[0]["columns"]) == 3, "Start event has correct columns")
    complete_ev = [l for l in lines if l["type"] == "complete"][0]
    assert_true(complete_ev["count"] == 5, "Row count is exactly 5")

    # 2. Aggregations & Joins
    print("\n--- 2. Testing Joins & Aggregations ---")
    query_join = """
    SELECT c.name, w.name AS weapon, cb.build_name, cb.tier_rating
    FROM character_builds cb
    JOIN characters c ON cb.character_id = c.character_id
    JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
    LIMIT 10;
    """
    res = client.post("/api/query", json={"query": query_join})
    assert_true(res.status_code == 200, "JOIN query returns HTTP 200")
    lines = [json.loads(line) for line in res.data.decode().strip().split("\n") if line.strip()]
    complete_ev = [l for l in lines if l["type"] == "complete"][0]
    assert_true(complete_ev["count"] == 10, "JOIN row count matches LIMIT 10")

    # 3. Security Hardening (Blocked operations)
    print("\n--- 3. Testing Security Protection & Authorizer ---")
    attacks = [
        ("DROP TABLE characters;", 403),
        ("INSERT INTO characters(character_id, name) VALUES (999, 'Hacker');", 403),
        ("UPDATE characters SET name = 'Owned';", 403),
        ("DELETE FROM weapons;", 403),
        ("CREATE TABLE evil(id int);", 403),
        ("ATTACH DATABASE ':memory:' AS evil;", 403),
        ("PRAGMA schema_version;", 403),
        ("VACUUM;", 403),
    ]
    for q, expected_code in attacks:
        res = client.post("/api/query", json={"query": q})
        assert_true(res.status_code in (400, 403), f"Blocked unauthorized query: {q[:30]}")

    # 4. Infinite Recursive CTE (Timeout Safeguard)
    print(f"\n--- 4. Testing Watchdog Timeout on Infinite CTE (Timeout = {QUERY_TIMEOUT_SECONDS}s) ---")
    infinite_cte = "WITH RECURSIVE cnt(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM cnt) SELECT count(*) FROM cnt;"
    t0 = time.perf_counter()
    res = client.post("/api/query", json={"query": infinite_cte})
    elapsed = time.perf_counter() - t0
    data = res.get_json() if res.is_json else {}
    err_text = data.get("error", "")
    assert_true(
        "timeout" in err_text.lower() or "aborted" in err_text.lower() or "interrupted" in err_text.lower(),
        "Infinite CTE aborted by watchdog timer",
        f"Response: {data}"
    )
    assert_true(elapsed < QUERY_TIMEOUT_SECONDS + 2.0, f"Aborted promptly ({elapsed:.2f}s)")

    # 5. Cartesian Explosion & Row Capping
    print(f"\n--- 5. Testing Cartesian Join Stream Capping (Cap = {MAX_STREAM_ROWS}) ---")
    cartesian = "SELECT * FROM characters, weapons, artifact_sets, character_builds;"
    t0 = time.perf_counter()
    res = client.post("/api/query", json={"query": cartesian})
    lines = [json.loads(line) for line in res.data.decode().strip().split("\n") if line.strip()]
    complete_ev = [l for l in lines if l["type"] == "complete"][0]
    assert_true(complete_ev["count"] == MAX_STREAM_ROWS, f"Cartesian explosion capped at exactly {MAX_STREAM_ROWS} rows")
    assert_true(complete_ev.get("truncated") is True, "Completion event flagged as truncated")
    assert_true(bool(complete_ev.get("warning")), "Warning message present in completion event")

    # 6. Schema metadata endpoint
    print("\n--- 6. Testing Schema & Preview Endpoints ---")
    res = client.get("/api/schema")
    assert_true(res.status_code == 200, "Schema endpoint returns HTTP 200")
    schema = res.get_json()
    assert_true("characters" in schema and "weapons" in schema, "Schema includes core tables")

    res = client.get("/api/table/characters/preview")
    assert_true(res.status_code == 200, "Preview endpoint returns HTTP 200")
    preview = res.get_json()
    assert_true(len(preview["rows"]) == 10, "Preview returns 10 rows")

    print("\n" + "=" * 60)
    print(f"TEST SUMMARY: {passed} PASSED, {failed} FAILED")
    print("=" * 60)
    return failed == 0

if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
