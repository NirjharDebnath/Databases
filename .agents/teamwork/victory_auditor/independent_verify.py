#!/usr/bin/env python3
"""
independent_verify.py
Independent Victory Auditor Verification Script.
Exhaustively tests all R1-R5 requirements and acceptance criteria from ORIGINAL_REQUEST.md.
"""

import os
import sys
import csv
import sqlite3

PROJECT_ROOT = "/home/nirjhar/Python Codes/Einstein/Databases"
DB_PATH = os.path.join(PROJECT_ROOT, "genshin_learning.db")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

def run_audit():
    print("=" * 80)
    print("INDEPENDENT VICTORY AUDITOR VERIFICATION SUITE")
    print(f"Target DB: {DB_PATH}")
    print("=" * 80)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    failures = []

    def check(condition, desc, error_detail=""):
        if condition:
            print(f"  [PASS] {desc}")
        else:
            print(f"  [FAIL] {desc} -> {error_detail}")
            failures.append(f"{desc}: {error_detail}")

    # =========================================================================
    # R1: Database Defect Remediation
    # =========================================================================
    print("\n--- Auditing Requirement R1: Database Defect Remediation ---")

    # 1.1 Artifact Sets 59, 60, 62, 63, 64
    sets_data = {r[0]: r for r in cursor.execute("SELECT artifact_set_id, name, domain_name, region, two_piece_bonus, four_piece_bonus FROM artifact_sets WHERE artifact_set_id IN (59, 60, 62, 63, 64);").fetchall()}

    s59 = sets_data.get(59)
    check(s59 and s59[1] == "Aubade of Morningstar and Moon" and s59[2] == "Moonchild's Treasures" and s59[3] == "Nod-Krai" and "+80" in s59[4] and "Moonsign" in s59[5],
          "Artifact Set 59 (Aubade of Morningstar and Moon): Nod-Krai, Moonchild's Treasures, +80 EM, Moonsign scaling", str(s59))

    s60 = sets_data.get(60)
    check(s60 and s60[1] == "A Day Carved from Rising Winds" and s60[2] == "Moonchild's Treasures" and s60[3] == "Nod-Krai" and "+18% ATK" in s60[4] and "Pastoral Winds" in s60[5],
          "Artifact Set 60 (A Day Carved from Rising Winds): Nod-Krai, Moonchild's Treasures, +18% ATK, Pastoral Winds scaling", str(s60))

    s62 = sets_data.get(62)
    check(s62 and s62[1] == "Disenchantment in Deep Shadow" and s62[2] == "Thorny Crown of the Mountain Wind" and s62[3] == "Mondstadt" and "+18% ATK" in s62[4] and "Stellar-Conduct" in s62[5],
          "Artifact Set 62 (Disenchantment in Deep Shadow): Mondstadt, Thorny Crown, +18% ATK, Stellar-Conduct scaling", str(s62))

    s63 = sets_data.get(63)
    check(s63 and s63[1] == "Scarlet Proof" and s63[2] == "Inverted Glacier" and s63[3] == "Snezhnaya" and "+18% ATK" in s63[4] and "Stellar Swirl" in s63[5],
          "Artifact Set 63 (Scarlet Proof): Snezhnaya, Inverted Glacier, +18% ATK, Stellar Swirl scaling", str(s63))

    s64 = sets_data.get(64)
    check(s64 and s64[1] == "Heart of the Furnace" and s64[2] == "Inverted Glacier" and s64[3] == "Snezhnaya" and "+18% ATK" in s64[4] and "Stellar Glimmer" in s64[5],
          "Artifact Set 64 (Heart of the Furnace): Snezhnaya, Inverted Glacier, +18% ATK, Stellar Glimmer scaling", str(s64))

    # 1.2 Weapons 128 & 131 Stats
    w128 = cursor.execute("SELECT weapon_id, name, base_atk, sub_stat_type, sub_stat_value FROM weapons WHERE weapon_id = 128;").fetchone()
    check(w128 and w128[1] == "Fang of the Mountain King" and w128[2] == 741 and w128[3] == "CRIT Rate" and abs(w128[4] - 11.0) < 0.01,
          "Weapon 128 (Fang of the Mountain King): Base ATK 741, Sub-stat 11.0% CRIT Rate", str(w128))

    w131 = cursor.execute("SELECT weapon_id, name, base_atk, sub_stat_type, sub_stat_value FROM weapons WHERE weapon_id = 131;").fetchone()
    check(w131 and w131[1] == "A Thousand Blazing Suns" and w131[2] == 741 and w131[3] == "CRIT Rate" and abs(w131[4] - 11.0) < 0.01,
          "Weapon 131 (A Thousand Blazing Suns): Base ATK 741, Sub-stat 11.0% CRIT Rate", str(w131))

    # 1.3 Character Attributes
    chars_by_name = {r[1]: r for r in cursor.execute("SELECT character_id, name, region, vision, weapon_type, release_patch FROM characters;").fetchall()}

    arl = chars_by_name.get("Arlecchino")
    check(arl and arl[2] == "Snezhnaya", "Arlecchino: Region Snezhnaya", str(arl))

    zib = chars_by_name.get("Zibai")
    check(zib and zib[2] == "Liyue", "Zibai: Region Liyue", str(zib))

    col = chars_by_name.get("Columbina")
    check(col and col[2] == "Nod-Krai", "Columbina: Region Nod-Krai", str(col))

    san = chars_by_name.get("Sandrone")
    check(san and san[3] == "Cryo" and san[4] == "Claymore", "Sandrone: Vision Cryo, Weapon Claymore", str(san))

    ian = chars_by_name.get("Iansan")
    check(ian and abs(ian[5] - 5.5) < 0.01, "Iansan: Release Patch 5.5", str(ian))

    aly = chars_by_name.get("Aloy")
    check(aly and aly[2] == "None", "Aloy: Region None", str(aly))

    # 1.4 Capitano Removal
    cap_c = cursor.execute("SELECT COUNT(*) FROM characters WHERE name LIKE '%Capitano%' OR character_id = 104;").fetchone()[0]
    cap_b = cursor.execute("SELECT COUNT(*) FROM character_builds WHERE build_id = 381 OR character_id = 104;").fetchone()[0]
    cap_w = cursor.execute("SELECT COUNT(*) FROM weapons WHERE signature_character_id = 104;").fetchone()[0]
    check(cap_c == 0 and cap_b == 0 and cap_w == 0, "Capitano ID 104 and Build 381 purged completely from DB", f"chars={cap_c}, builds={cap_b}, weapons={cap_w}")

    # =========================================================================
    # R2: Missing Playable Characters Ingestion
    # =========================================================================
    print("\n--- Auditing Requirement R2: Missing Playable Characters Ingestion ---")
    new_chars = [
        "Ifa", "Escoffier", "Dahlia", "Skirk", "Wonderland Manekin", "Durin", "Varka",
        "Nicole", "Prune", "Lohen", "Alyosha", "Odette", "Vesna", "Vodyanitsa", "Mitya", "Valeriy"
    ]
    total_chars = cursor.execute("SELECT COUNT(*) FROM characters;").fetchone()[0]
    check(total_chars == 129, f"Total characters count is 129 (actual: {total_chars})")

    for nc in new_chars:
        row = chars_by_name.get(nc)
        check(row is not None, f"New character '{nc}' exists in database", str(row))

    # Check stats for all 16 new characters
    stats_valid = cursor.execute("""
        SELECT COUNT(*) FROM characters 
        WHERE name IN ({})
          AND base_hp > 0 AND base_atk > 0 AND base_def > 0 AND release_patch >= 5.5;
    """.format(",".join(f"'{c}'" for c in new_chars))).fetchone()[0]
    check(stats_valid == 16, f"All 16 new characters have valid positive stats and release_patch >= 5.5 (valid: {stats_valid}/16)")

    # =========================================================================
    # R3: Weapons Catalog Expansion
    # =========================================================================
    print("\n--- Auditing Requirement R3: Weapons Catalog Expansion ---")
    total_weapons = cursor.execute("SELECT COUNT(*) FROM weapons;").fetchone()[0]
    check(total_weapons == 155, f"Total weapons count is 155 (actual: {total_weapons})")

    # 24 5-star signatures (IDs 204 to 227)
    sig_count = cursor.execute("""
        SELECT COUNT(*) FROM weapons 
        WHERE weapon_id BETWEEN 204 AND 227 
          AND rarity = 5 AND is_craftable = 0 AND signature_character_id IS NOT NULL;
    """).fetchone()[0]
    check(sig_count == 24, f"All 24 missing 5-star signatures exist (IDs 204-227) with valid attributes (found: {sig_count}/24)")

    # Check named signatures
    for req_sig in ["Calamity Queller", "Everlasting Moonglow", "Sunny Morning Sleep-In", "Vivid Notions", "Azurelight"]:
        found_sig = cursor.execute("SELECT weapon_id, name, rarity, signature_character_id FROM weapons WHERE name = ?;", (req_sig,)).fetchone()
        check(found_sig is not None and found_sig[2] == 5, f"5-star signature '{req_sig}' present in weapons catalog", str(found_sig))

    # 19 missing craftables (IDs 228 to 246)
    craftable_count = cursor.execute("""
        SELECT COUNT(*) FROM weapons 
        WHERE weapon_id BETWEEN 228 AND 246 
          AND rarity = 4 AND is_craftable = 1 AND signature_character_id IS NULL;
    """).fetchone()[0]
    check(craftable_count == 19, f"All 19 missing craftable weapons exist (IDs 228-246) with is_craftable = 1 (found: {craftable_count}/19)")

    # Key meta staples
    ferryman = cursor.execute("SELECT weapon_id, name, base_atk, sub_stat_type, sub_stat_value FROM weapons WHERE weapon_id = 247;").fetchone()
    check(ferryman and ferryman[1] == "Fleuve Cendre Ferryman" and ferryman[2] == 510 and ferryman[3] == "Energy Recharge",
          "Meta staple: Fleuve Cendre Ferryman (ID 247) verified", str(ferryman))

    stringless = cursor.execute("SELECT weapon_id, name, base_atk, sub_stat_type, sub_stat_value FROM weapons WHERE weapon_id = 248;").fetchone()
    check(stringless and stringless[1] == "The Stringless" and stringless[2] == 510 and stringless[3] == "Elemental Mastery",
          "Meta staple: The Stringless (ID 248) verified", str(stringless))

    cinnabar = cursor.execute("SELECT weapon_id, name, base_atk, sub_stat_type, sub_stat_value, signature_character_id FROM weapons WHERE weapon_id = 249;").fetchone()
    check(cinnabar and cinnabar[1] == "Cinnabar Spindle" and cinnabar[2] == 454 and cinnabar[3] == "DEF%" and cinnabar[5] == 6,
          "Meta staple: Cinnabar Spindle (ID 249, signature of Albedo ID 6) verified", str(cinnabar))

    natlan_series = cursor.execute("SELECT COUNT(*) FROM weapons WHERE weapon_id BETWEEN 250 AND 255 AND rarity = 4 AND is_craftable = 0;").fetchone()[0]
    check(natlan_series == 6, f"Natlan event/gacha series (IDs 250-255) verified (found: {natlan_series}/6)")

    # =========================================================================
    # R4: Character Builds Backfill & Role Variety
    # =========================================================================
    print("\n--- Auditing Requirement R4: Character Builds Backfill & Role Variety ---")
    total_builds = cursor.execute("SELECT COUNT(*) FROM character_builds;").fetchone()[0]
    check(total_builds == 168, f"Total character builds count is 168 (actual: {total_builds})")

    # 100% build coverage: 0 orphan characters
    orphaned = cursor.execute("""
        SELECT c.character_id, c.name 
        FROM characters c 
        LEFT JOIN character_builds cb ON c.character_id = cb.character_id 
        WHERE cb.build_id IS NULL;
    """).fetchall()
    check(len(orphaned) == 0, "100% playable character build coverage (0 orphan characters)", f"orphaned: {orphaned}")

    # Backfill builds (IDs 408 to 450)
    backfill_count = cursor.execute("SELECT COUNT(*) FROM character_builds WHERE build_id BETWEEN 408 AND 450;").fetchone()[0]
    check(backfill_count == 43, f"All 43 backfill builds present (IDs 408-450) (found: {backfill_count}/43)")

    for char_name in ["Barbara", "Noelle", "Beidou", "Rosaria", "Ororon", "Yaoyao", "Diona", "Qiqi"]:
        b_cnt = cursor.execute("""
            SELECT COUNT(*) FROM character_builds cb 
            JOIN characters c ON cb.character_id = c.character_id 
            WHERE c.name = ?;
        """, (char_name,)).fetchone()[0]
        check(b_cnt >= 1, f"Character '{char_name}' has at least 1 verified meta build (found: {b_cnt})")

    # Alternative meta roles (IDs 467, 468, 469)
    mavuika_alt = cursor.execute("""
        SELECT cb.build_id, c.name, cb.build_name, cb.role, cb.recommended_artifact_id, a.name 
        FROM character_builds cb 
        JOIN characters c ON cb.character_id = c.character_id 
        JOIN artifact_sets a ON cb.recommended_artifact_id = a.artifact_set_id 
        WHERE cb.build_id = 467;
    """).fetchone()
    check(mavuika_alt and mavuika_alt[1] == "Mavuika" and "Cinder City" in mavuika_alt[5],
          "Mavuika Alt Role (Build 467): Scroll of the Hero of Cinder City Support", str(mavuika_alt))

    citlali_alt = cursor.execute("""
        SELECT cb.build_id, c.name, cb.build_name, w.name, cb.tier_rating 
        FROM character_builds cb 
        JOIN characters c ON cb.character_id = c.character_id 
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id 
        WHERE cb.build_id = 468;
    """).fetchone()
    check(citlali_alt and citlali_alt[1] == "Citlali" and citlali_alt[3] == "Sacrificial Fragments",
          "Citlali F2P Alt Role (Build 468): Sacrificial Fragments", str(citlali_alt))

    chasca_alt = cursor.execute("""
        SELECT cb.build_id, c.name, cb.build_name, w.name, cb.tier_rating 
        FROM character_builds cb 
        JOIN characters c ON cb.character_id = c.character_id 
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id 
        WHERE cb.build_id = 469;
    """).fetchone()
    check(chasca_alt and chasca_alt[1] == "Chasca" and chasca_alt[3] == "Chain Breaker",
          "Chasca F2P Alt Role (Build 469): Chain Breaker", str(chasca_alt))

    # Re-linked builds: Furina, Albedo, Shenhe
    furina_build = cursor.execute("SELECT cb.build_id, c.name, cb.recommended_weapon_id, w.name FROM character_builds cb JOIN characters c ON cb.character_id = c.character_id JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id WHERE cb.build_id = 305;").fetchone()
    check(furina_build and furina_build[1] == "Furina" and furina_build[2] == 247,
          "Furina (Build 305) re-linked to Fleuve Cendre Ferryman (ID 247)", str(furina_build))

    albedo_build = cursor.execute("SELECT cb.build_id, c.name, cb.recommended_weapon_id, w.name FROM character_builds cb JOIN characters c ON cb.character_id = c.character_id JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id WHERE cb.build_id = 387;").fetchone()
    check(albedo_build and albedo_build[1] == "Albedo" and albedo_build[2] == 249,
          "Albedo (Build 387) re-linked to Cinnabar Spindle (ID 249)", str(albedo_build))

    shenhe_build = cursor.execute("SELECT cb.build_id, c.name, cb.recommended_weapon_id, w.name FROM character_builds cb JOIN characters c ON cb.character_id = c.character_id JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id WHERE cb.build_id = 392;").fetchone()
    check(shenhe_build and shenhe_build[1] == "Shenhe" and shenhe_build[2] == 204,
          "Shenhe (Build 392) re-linked to Calamity Queller (ID 204)", str(shenhe_build))

    # Weapon type compatibility
    mismatches = cursor.execute("""
        SELECT cb.build_id, c.name, c.weapon_type, w.name, w.weapon_type 
        FROM character_builds cb 
        JOIN characters c ON cb.character_id = c.character_id 
        JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id 
        WHERE c.weapon_type != w.weapon_type;
    """).fetchall()
    check(len(mismatches) == 0, "100% weapon type compatibility across all 168 builds", f"mismatches: {mismatches}")

    # =========================================================================
    # R5: Data Synchronization & Automated Verification
    # =========================================================================
    print("\n--- Auditing Requirement R5: Data Synchronization & Automated Verification ---")
    # PRAGMA foreign_key_check
    fk_violations = cursor.execute("PRAGMA foreign_key_check;").fetchall()
    check(len(fk_violations) == 0, "PRAGMA foreign_key_check returns 0 violations", f"violations: {fk_violations}")

    # Check 8 indexes
    db_indexes = {r[0] for r in cursor.execute("SELECT name FROM sqlite_master WHERE type = 'index';").fetchall()}
    expected_indexes = [
        "idx_characters_region", "idx_characters_vision",
        "idx_weapons_type", "idx_weapons_signature",
        "idx_builds_character", "idx_builds_tier",
        "idx_builds_weapon", "idx_builds_artifact"
    ]
    for idx in expected_indexes:
        check(idx in db_indexes, f"Relational index '{idx}' exists in sqlite_master")

    # CSV 1:1 Parity
    for table_name, csv_file, count in [
        ("characters", "characters.csv", 129),
        ("weapons", "weapons.csv", 155),
        ("artifact_sets", "artifact_sets.csv", 64),
        ("character_builds", "character_builds.csv", 168),
    ]:
        csv_path = os.path.join(DATA_DIR, csv_file)
        check(os.path.exists(csv_path), f"CSV file '{csv_file}' exists")
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = list(csv.reader(f))
            header = reader[0]
            rows = reader[1:]
        check(len(rows) == count, f"CSV '{csv_file}' row count matches expected ({len(rows)}/{count})")

    conn.close()

    print("\n" + "=" * 80)
    if failures:
        print(f"AUDIT FAILED WITH {len(failures)} DISCREPANCIES:")
        for f in failures:
            print(f"  - {f}")
        return False
    else:
        print("INDEPENDENT AUDIT PASSED 100%! ALL R1-R5 REQUIREMENTS AND ACCEPTANCE CRITERIA MET.")
        return True

if __name__ == "__main__":
    success = run_audit()
    sys.exit(0 if success else 1)
