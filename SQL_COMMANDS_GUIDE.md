# Master Guide: SQL Read Queries with SQLite

Welcome to your hands-on guide for mastering SQL queries! This guide uses your local `genshin_learning.db` SQLite database, containing **105 characters across all 8 regions**, **69 weapons**, **34 artifact sets**, and **97 Game8 meta builds**.

---

## 1. Database Schema Quick Reference

```
+---------------------------------------------------------------------------------+
|                                   CHARACTERS                                    |
+---------------------------------------------------------------------------------+
| character_id (PK) | name | rarity | vision | weapon_type | region | default_role|
| base_hp | base_atk | base_def | talent_priority | release_patch                 |
+---------------------------------------------------------------------------------+
        ^                                                   ^
        | (1-to-many)                                       | (1-to-1 optional)
        |                                                   |
+---------------------------------------------------+       |
|                 CHARACTER_BUILDS                  |       |
+---------------------------------------------------+       |
| build_id (PK)                                     |       |
| character_id (FK -> characters)                   |       |
| build_name                                        |       |
| role                                              |       |
| recommended_weapon_id (FK -> weapons)             |       |
| recommended_artifact_id (FK -> artifact_sets)     |       |
| sands_stat | goblet_stat | circlet_stat           |       |
| tier_rating | playstyle_notes                     |       |
+---------------------------------------------------+       |
        |                                 |                 |
        | (FK)                            | (FK)            |
        v                                 v                 |
+-------------------------------+   +-----------------------------+
|            WEAPONS            |   |        ARTIFACT_SETS        |
+-------------------------------+   +-----------------------------+
| weapon_id (PK)                |   | artifact_set_id (PK)        |
| name                          |   | name                        |
| weapon_type                   |   | domain_name                 |
| rarity                        |   | region                      |
| base_atk                      |   | two_piece_bonus             |
| sub_stat_type, sub_stat_value |   | four_piece_bonus            |
| is_craftable                  |   +-----------------------------+
| signature_character_id (FK) --+---------------------------+
+-------------------------------+
```

---

## 2. How to Run Queries

You can execute queries in your terminal right away using the built-in `sqlite3` CLI:

```bash
# Open interactive mode with nice table formatting:
sqlite3 genshin_learning.db
sqlite> .mode table
sqlite> .headers on
sqlite> SELECT name, vision, region FROM characters LIMIT 5;
```

Or execute directly from your shell:
```bash
sqlite3 -header -table genshin_learning.db "SELECT name, vision, base_atk FROM characters ORDER BY base_atk DESC LIMIT 5;"
```

---

## 3. Core SQL Concepts & Commands

### Phase 1: Basic Retrieval, Filtering & Ordering

#### 1.1 `SELECT` specific columns and Aliasing (`AS`)
Select columns to inspect, compute custom expressions, and give them readable names:
```sql
SELECT 
    name, 
    vision, 
    base_atk, 
    base_atk * 1.25 AS boosted_atk
FROM characters;
```

#### 1.2 `WHERE` with Comparison Operators
Filter rows using `=`, `!=` (or `<>`), `<`, `>`, `<=`, `>=`:
```sql
-- Find 5-star characters with base ATK greater than 330
SELECT name, vision, region, base_atk
FROM characters
WHERE rarity = 5 AND base_atk > 330;
```

#### 1.3 Logical Operators (`AND`, `OR`, `NOT`)
Combine multiple conditions. Use parentheses to control precedence:
```sql
-- Find characters from Fontaine or Natlan who are Bow or Catalyst users
SELECT name, region, weapon_type, vision
FROM characters
WHERE (region = 'Fontaine' OR region = 'Natlan')
  AND (weapon_type = 'Bow' OR weapon_type = 'Catalyst');
```

#### 1.4 Sorting with `ORDER BY`
Sort ascending (`ASC`, default) or descending (`DESC`). Multiple sort columns can be chained:
```sql
-- Order characters by rarity descending, then by base HP descending
SELECT name, rarity, region, base_hp
FROM characters
ORDER BY rarity DESC, base_hp DESC
LIMIT 10;
```

#### 1.5 Pagination with `LIMIT` & `OFFSET`
Get the top records or paginate through a result set:
```sql
-- Get page 2 of highest base ATK characters (rows 6 to 10)
SELECT name, vision, base_atk
FROM characters
ORDER BY base_atk DESC
LIMIT 5 OFFSET 5;
```

---

### Phase 2: Ranges, Sets, Patterns & NULLs

#### 2.1 `BETWEEN ... AND ...`
Check if a numeric or date value lies within an inclusive range:
```sql
-- Weapons with base ATK between 540 and 610
SELECT name, weapon_type, rarity, base_atk
FROM weapons
WHERE base_atk BETWEEN 540 AND 610
ORDER BY base_atk DESC;
```

#### 2.2 `IN` and `NOT IN`
Match against a specific list of values:
```sql
-- Characters released in the borderlands/outer regions
SELECT name, region, default_role
FROM characters
WHERE region IN ('Nod-Krai', 'Snezhnaya', 'Natlan')
ORDER BY region, name;
```

#### 2.3 Pattern Matching with `LIKE`
Wildcards:
- `%` matches 0 or more characters
- `_` matches exactly 1 character
```sql
-- Find all weapons with CRIT stats
SELECT name, weapon_type, sub_stat_type, sub_stat_value
FROM weapons
WHERE sub_stat_type LIKE 'CRIT%'
ORDER BY sub_stat_value DESC;
```

#### 2.4 Handling Missing Data: `IS NULL`, `IS NOT NULL`, and `COALESCE()`
`NULL` represents missing or unassigned data. You must use `IS NULL` (never `= NULL`):
```sql
-- Find all generalist 5-star weapons that are NOT signatures of any character
SELECT name, weapon_type, base_atk, sub_stat_type
FROM weapons
WHERE rarity = 5 AND signature_character_id IS NULL;
```

Using `COALESCE(val, fallback)` to replace `NULL` with friendly text:
```sql
SELECT 
    w.name AS weapon_name,
    COALESCE(c.name, 'Generalist / No Signature Owner') AS signature_character
FROM weapons w
LEFT JOIN characters c ON w.signature_character_id = c.character_id
WHERE w.rarity = 5;
```

---

### Phase 3: Multi-Table Joins (Relational Power)

#### 3.1 `INNER JOIN`: Matching rows from two tables
Only returns rows that have matching values in both tables:
```sql
-- Show each weapon and its signature owner
SELECT 
    w.name AS weapon, 
    w.weapon_type, 
    c.name AS signature_owner, 
    c.vision
FROM weapons w
INNER JOIN characters c ON w.signature_character_id = c.character_id;
```

#### 3.2 4-Table `INNER JOIN`: Complete Build Sheets
Connect `characters`, `character_builds`, `weapons`, and `artifact_sets` in a single query:
```sql
SELECT 
    c.name AS character,
    c.vision,
    cb.build_name,
    cb.role,
    w.name AS recommended_weapon,
    w.sub_stat_type AS weapon_stat,
    a.name AS recommended_artifact,
    cb.sands_stat,
    cb.goblet_stat,
    cb.circlet_stat,
    cb.tier_rating
FROM character_builds cb
INNER JOIN characters c ON cb.character_id = c.character_id
INNER JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
INNER JOIN artifact_sets a ON cb.recommended_artifact_id = a.artifact_set_id
WHERE cb.tier_rating = 'SS'
ORDER BY c.name;
```

#### 3.3 `LEFT JOIN`: Preserving rows with no match
Finds items in the left table even if they have zero corresponding rows in the right table:
```sql
-- Find weapons that are NEVER recommended in any Game8 build
SELECT 
    w.name AS unused_weapon, 
    w.weapon_type, 
    w.rarity
FROM weapons w
LEFT JOIN character_builds cb ON w.weapon_id = cb.recommended_weapon_id
WHERE cb.build_id IS NULL;
```

---

### Phase 4: Aggregation & Grouping

#### 4.1 Summary Aggregates (`COUNT`, `AVG`, `MIN`, `MAX`, `SUM`)
```sql
SELECT 
    COUNT(*) AS total_characters,
    ROUND(AVG(base_atk), 1) AS avg_base_atk,
    MAX(base_atk) AS max_base_atk,
    MIN(base_hp) AS min_base_hp
FROM characters
WHERE rarity = 5;
```

#### 4.2 `GROUP BY`: Breaking down by dimensions
```sql
-- Average base stats and count by Element/Vision
SELECT 
    vision, 
    COUNT(*) AS total_heroes,
    ROUND(AVG(base_hp), 0) AS avg_hp,
    ROUND(AVG(base_atk), 0) AS avg_atk,
    ROUND(AVG(base_def), 0) AS avg_def
FROM characters
GROUP BY vision
ORDER BY avg_atk DESC;
```

#### 4.3 Multi-Column `GROUP BY`
```sql
-- Count of characters per region and rarity
SELECT 
    region, 
    rarity, 
    COUNT(*) AS total
FROM characters
GROUP BY region, rarity
ORDER BY region, rarity DESC;
```

#### 4.4 `HAVING` vs `WHERE`
- `WHERE` filters rows **before** aggregation.
- `HAVING` filters aggregated groups **after** calculation.
```sql
-- Find artifact sets recommended in 4 or more different builds
SELECT 
    a.name AS artifact_set,
    COUNT(cb.build_id) AS build_count
FROM artifact_sets a
INNER JOIN character_builds cb ON a.artifact_set_id = cb.recommended_artifact_id
GROUP BY a.name
HAVING COUNT(cb.build_id) >= 4
ORDER BY build_count DESC;
```

---

### Phase 5: Conditional Logic with `CASE WHEN`

Categorize data dynamically and create custom labels or pivot tables:

```sql
SELECT 
    name,
    vision,
    base_hp,
    base_atk,
    CASE 
        WHEN base_atk >= 330 THEN 'Glass Cannon (High ATK)'
        WHEN base_hp >= 14000 THEN 'Tank / HP Scaler'
        ELSE 'Balanced / Supportive'
    END AS combat_archetype
FROM characters
WHERE rarity = 5
ORDER BY base_atk DESC;
```

#### Pivot Count per Region:
```sql
-- Count 4-star and 5-star characters side-by-side per region
SELECT 
    region,
    COUNT(CASE WHEN rarity = 5 THEN 1 END) AS five_stars,
    COUNT(CASE WHEN rarity = 4 THEN 1 END) AS four_stars,
    COUNT(*) AS total
FROM characters
GROUP BY region
ORDER BY total DESC;
```

---

### Phase 6: Subqueries & Common Table Expressions (CTEs)

#### 6.1 Scalar Subquery in `WHERE`
Compare an individual row to a computed aggregate:
```sql
-- Find characters whose base ATK is higher than the overall 5-star average
SELECT name, vision, region, base_atk
FROM characters
WHERE rarity = 5 
  AND base_atk > (SELECT AVG(base_atk) FROM characters WHERE rarity = 5)
ORDER BY base_atk DESC;
```

#### 6.2 Correlated Subquery with `EXISTS`
Check if related rows exist in another table:
```sql
-- Find characters that have at least one SS-tier build
SELECT c.name, c.vision, c.region
FROM characters c
WHERE EXISTS (
    SELECT 1 
    FROM character_builds cb 
    WHERE cb.character_id = c.character_id 
      AND cb.tier_rating = 'SS'
);
```

#### 6.3 Common Table Expressions (`WITH ... AS`)
CTEs make complex SQL easy to read, test, and maintain by defining named temporary result sets:
```sql
WITH RegionAverages AS (
    SELECT 
        region, 
        ROUND(AVG(base_atk), 1) AS avg_regional_atk
    FROM characters
    GROUP BY region
)
SELECT 
    c.name,
    c.region,
    c.base_atk,
    ra.avg_regional_atk,
    (c.base_atk - ra.avg_regional_atk) AS atk_diff_from_region_avg
FROM characters c
JOIN RegionAverages ra ON c.region = ra.region
WHERE c.base_atk > ra.avg_regional_atk
ORDER BY c.region, atk_diff_from_region_avg DESC;
```

---

### Phase 7: Window Functions (`OVER`, `PARTITION BY`, `RANK`)

Window functions perform calculations across related rows **without collapsing rows like `GROUP BY` does**.

#### 7.1 `ROW_NUMBER()` vs `RANK()` vs `DENSE_RANK()`
Rank characters by base ATK within each Vision:
```sql
SELECT 
    name,
    vision,
    base_atk,
    ROW_NUMBER() OVER (PARTITION BY vision ORDER BY base_atk DESC) AS row_num,
    RANK()       OVER (PARTITION BY vision ORDER BY base_atk DESC) AS rank_pos,
    DENSE_RANK() OVER (PARTITION BY vision ORDER BY base_atk DESC) AS dense_rank_pos
FROM characters
WHERE rarity = 5
ORDER BY vision, base_atk DESC;
```

#### 7.2 Top-N per Group Pattern (e.g. Top 2 ATK characters per Region)
Combine a CTE with `DENSE_RANK()`:
```sql
WITH RankedCharacters AS (
    SELECT 
        name,
        region,
        vision,
        base_atk,
        DENSE_RANK() OVER (PARTITION BY region ORDER BY base_atk DESC) as regional_rank
    FROM characters
)
SELECT region, regional_rank, name, vision, base_atk
FROM RankedCharacters
WHERE regional_rank <= 2
ORDER BY region, regional_rank;
```

---

## 4. Quick SQL Practice Checklist

Try answering these questions by writing your own SQL queries against `genshin_learning.db`:

1. [ ] Which characters use a `Catalyst` and have `HP%` as their recommended Sands stat?
2. [ ] How many characters originate from each of the 8 regions?
3. [ ] What is the average base ATK of craftable weapons vs non-craftable weapons?
4. [ ] List the names of all 5★ weapons that give `CRIT Rate` or `CRIT DMG` above 40%.
5. [ ] Find characters whose talent priority upgrades `Normal Attack` first (`Normal > ...`).
6. [ ] Which artifact sets are farmed in domains located in Fontaine?
7. [ ] Find all characters who have both a Signature Weapon and an `SS` tier build.
8. [ ] List the top 3 highest base DEF characters in each weapon type.
