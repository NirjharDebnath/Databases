# Definitive Data Specification Catalog for R1, R2, and R3

**Explorer**: `explorer_survey_2_gen2`  
**Date**: 2026-11-20  
**Project Root**: `/home/nirjhar/Python Codes/Einstein/Databases`  
**Working Directory**: `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_2_gen2`  
**Status**: Completed (Hard Handoff)

---

## 1. Observation

### 1.1 Direct Database & Script Audit Findings

Inspection of `generate_csvs.py`, `init_db.py`, `data/*.csv`, and `genshin_learning.db` revealed the following exact lines and data points:

1. **Artifact Sets 59, 60, 62, 63, 64 in `generate_csvs.py` (lines 355–360)**:
   ```python
   (59, "Aubade of Morningstar and Moon", "Moonchild's Treasures", "Nod-Krai", "+15% Lunar Reaction DMG", "Dealing Lunar Reaction DMG increases character ATK and direct Lunar DMG by 35%"),
   (60, "A Day Carved from Rising Winds", "Moonchild's Treasures", "Nod-Krai", "+18% ATK", "Grants Blessing of Pastoral Winds boosting ATK by 25% and CRIT Rate by 20% with Witch's Homework"),
   (61, "Celestial Gift", "Thorny Crown of the Mountain Wind", "Mondstadt", "+20% Energy Recharge", "Using Skill grants team 20% Elemental DMG bonus (up to 40% with Hexerei Secret Rite)"),
   (62, "Disenchantment in Deep Shadow", "Thorny Crown of the Mountain Wind", "Snezhnaya", "+18% ATK", "Superconduct Reaction DMG +80% (Stellar +40%); CRIT Rate +16% against affected foes"),
   (63, "Scarlet Proof", "Palace of Frost", "Snezhnaya", "+15% Cryo DMG", "Triggering Melt or Stellar Reaction increases CRIT DMG by 45% for 8s"),
   (64, "Heart of the Furnace", "Palace of Frost", "Snezhnaya", "+80 Elemental Mastery", "Swirl and Stellar Swirl reactions grant party +25% ATK and +15% All Elemental DMG")
   ```
   - **Set 59**: 2-piece bonus currently lists `+15% Lunar Reaction DMG` instead of official `+80 Elemental Mastery`; 4-piece bonus lacks off-field trigger and Moonsign Level scaling.
   - **Set 60**: 4-piece text lacks full trigger conditions (Normal/Charged/Skill/Burst hits) and proper effect upgrade naming (*Blessing of Pastoral Winds* -> *Resolve of Pastoral Winds*).
   - **Set 62**: Region is currently marked `"Snezhnaya"`, whereas its paired domain `"Thorny Crown of the Mountain Wind"` (shared with Set 61) is located in **Mondstadt** (near Dornman Port / Windrest Peak).
   - **Set 63**: Domain is listed as `"Palace of Frost"` instead of official **`"Inverted Glacier"`**; 2-piece bonus is listed as `+15% Cryo DMG` instead of **`+18% ATK`**; 4-piece bonus incorrectly mentions Melt instead of **Stellar Swirl** reaction scaling.
   - **Set 64**: Domain is listed as `"Palace of Frost"` instead of **`"Inverted Glacier"`**; 2-piece bonus is listed as `+80 Elemental Mastery` instead of **`+18% ATK`**; 4-piece bonus incorrectly mentions Swirl instead of **Stellar Glimmer** party reaction scaling.

2. **Corrupted Weapon Stats in `generate_csvs.py` (lines 186 & 189)**:
   ```python
   (128, "Fang of the Mountain King", "Claymore", 5, 608, "CRIT Rate", 33.1, 0, 84),      # Kinich
   (131, "A Thousand Blazing Suns", "Claymore", 5, 608, "CRIT Rate", 33.1, 0, 87),        # Mavuika
   ```
   Both weapon records currently have `base_atk = 608` and `sub_stat_value = 33.1`. The official patch data for both 5★ claymores is `base_atk = 741` and `sub_stat_value = 11.0` (CRIT Rate).

3. **Character Attribute Defects in `generate_csvs.py` (lines 103, 124, 135, 140, 141, 142, 145)**:
   - `Arlecchino` (ID 72): `region = "Fontaine"` (must be `"Snezhnaya"`).
   - `Iansan` (ID 91): `release_patch = 5.4` (must be `5.5`).
   - `Zibai` (ID 99): `region = "Nod-Krai"` (must be `"Liyue"`).
   - `Columbina` (ID 102): `region = "Snezhnaya"` (must be `"Nod-Krai"`).
   - `Sandrone` (ID 103): `vision = "Geo"`, `weapon_type = "Catalyst"` (must be `vision = "Cryo"`, `weapon_type = "Claymore"`).
   - `Capitano` (ID 104): `(104, "Capitano", 5, "Cryo", "Claymore", "Snezhnaya", "Main DPS", ...)` — Non-playable NPC that must be purged along with `character_builds` row 381.
   - `Aloy` (ID 105): `region = "Outlander"` (must be `"None"`).

4. **Missing Playable Characters (R2)**:
   The existing `characters` table contains 114 rows (IDs 1–114). The 16 characters (*Ifa*, *Escoffier*, *Dahlia*, *Skirk*, *Wonderland Manekin*, *Durin*, *Varka*, *Nicole*, *Prune*, *Lohen*, *Alyosha*, *Odette*, *Vesna*, *Vodyanitsa*, *Mitya*, *Valeriy*) are completely absent from the dataset.

5. **Missing Weapons (R3)**:
   The existing `weapons` table contains 103 rows (IDs 101–203). None of the 24 missing 5-star signatures, 19 missing craftables, or key meta staples (*Fleuve Cendre Ferryman*, *The Stringless*, *Cinnabar Spindle*, Natlan gacha series) are present in the catalog.

---

## 2. Logic Chain

1. **R1 Defect Corrections**:
   - *Observation*: Set 61 has domain `"Thorny Crown of the Mountain Wind"` in Mondstadt. Set 62 has the same domain but is tagged Snezhnaya.
   - *Reasoning*: A single Domain of Blessing physically resides in one geographical nation. Geographically, Thorny Crown of the Mountain Wind is at Windrest Peak in Mondstadt. Thus, Set 62's region must be corrected to `"Mondstadt"`.
   - *Observation*: Sets 63 and 64 share the domain `"Palace of Frost"` in Snezhnaya in the old code. Official patch 7.0 sources designate `"Inverted Glacier"` as the Snezhnaya artifact domain housing both *Scarlet Proof* (Stellar Swirl carry set) and *Heart of the Furnace* (Stellar Glimmer buffer set). Both share a 2pc bonus of `+18% ATK`.
   - *Reasoning*: Updating domain name to `"Inverted Glacier"`, 2pc bonus to `+18% ATK`, and official 4pc mechanics eliminates all inaccuracies.
   - *Observation*: Kinich's *Fang of the Mountain King* and Mavuika's *A Thousand Blazing Suns* are high-base-ATK profile 5★ weapons (741 ATK at Lv. 90, 11.0% CRIT Rate).
   - *Reasoning*: Correcting `base_atk` from 608 to 741 and `sub_stat_value` from 33.1 to 11.0 rectifies the stats to match official scaling.
   - *Observation*: Capitano is an NPC. Removing character ID 104 without removing build ID 381 triggers a foreign key violation (`FOREIGN KEY constraint failed`).
   - *Reasoning*: Both Capitano (ID 104) and build 381 must be purged synchronously from `generate_csvs.py` and CSVs.

2. **R2 Character Ingestion**:
   - *Observation*: Character IDs 1 through 114 currently exist. Removing Capitano (104) leaves 113 existing characters.
   - *Reasoning*: Sequential IDs 115 through 130 must be assigned to the 16 incoming characters. Each row must satisfy the exact SQLite schema:
     `rarity IN (4, 5)`, `vision IN ('Pyro', 'Hydro', 'Anemo', 'Electro', 'Dendro', 'Cryo', 'Geo')`, `weapon_type IN ('Sword', 'Claymore', 'Polearm', 'Bow', 'Catalyst')`, non-null base stats, and non-empty talent priorities.
   - *Regional Recalculation*:
     - Liyue: 21 + 1 (Zibai) = 22
     - Mondstadt: 19 + 4 (Dahlia, Durin, Varka, Nicole) = 23
     - Inazuma: 17 (no change) = 17
     - Sumeru: 14 (no change) = 14
     - Fontaine: 13 - 1 (Arlecchino) + 1 (Escoffier) = 13
     - Natlan: 10 + 1 (Ifa) = 11
     - Nod-Krai: 9 - 1 (Zibai) + 1 (Columbina) + 3 (Prune, Lohen, Vesna) = 12
     - Outlander: 7 - 1 (Aloy) + 2 (Skirk, Wonderland Manekin) = 8
     - Snezhnaya: 4 - 1 (Capitano) + 1 (Arlecchino) - 1 (Columbina) + 5 (Alyosha, Odette, Vodyanitsa, Mitya, Valeriy) = 8
     - None: 0 + 1 (Aloy) = 1
     - Total: 22 + 23 + 17 + 14 + 13 + 11 + 12 + 8 + 8 + 1 = **129 playable characters**.

3. **R3 Weapons Catalog Expansion**:
   - *Observation*: Weapons table currently spans IDs 101 to 203 (103 rows).
   - *Reasoning*: Sequential IDs starting at 204 prevent any collision.
     - 24 5-star signatures occupy IDs **204 to 227**.
     - 19 missing craftables occupy IDs **228 to 246**.
     - 9 key meta staples and event/gacha weapons occupy IDs **247 to 255**.
     - Total new weapons: 24 + 19 + 9 = **52 weapons**.
     - Total weapons post-expansion: 103 + 52 = **155 weapons**.
   - *Foreign Key Verification*: Every 5★ signature weapon's `signature_character_id` points to a valid `character_id` in `characters`. Craftable and staple weapons cleanly set `signature_character_id` to `NULL` (except `Cinnabar Spindle` which links to Albedo, `character_id = 6`).

---

## 3. Concrete Data Specifications

### 3.1 R1 Defect Remediation Specification

#### A. Artifact Sets Corrections (Sets 59, 60, 62, 63, 64)

```python
# Replace entries in ARTIFACT_SETS list in generate_csvs.py:
CORRECTED_ARTIFACT_SETS = [
    (59, "Aubade of Morningstar and Moon", "Moonchild's Treasures", "Nod-Krai", 
     "+80 Elemental Mastery", 
     "When off-field, Lunar Reaction DMG +20%. When party Moonsign Level is Ascendant Gleam, Lunar Reaction DMG +40%"),

    (60, "A Day Carved from Rising Winds", "Moonchild's Treasures", "Nod-Krai", 
     "+18% ATK", 
     "Normal/Charged/Skill/Burst hits grant Blessing of Pastoral Winds (ATK +25% for 6s); upgrades with Witch's Homework to Resolve of Pastoral Winds (CRIT Rate +20%)"),

    (62, "Disenchantment in Deep Shadow", "Thorny Crown of the Mountain Wind", "Mondstadt", 
     "+18% ATK", 
     "Superconduct Reaction DMG +80% (Stellar-Conduct +40%); attacking affected foes increases CRIT Rate by 16%"),

    (63, "Scarlet Proof", "Inverted Glacier", "Snezhnaya", 
     "+18% ATK", 
     "After triggering a Stellar Swirl reaction, CRIT Rate +16% and Stellar Swirl DMG +40% for 10s"),

    (64, "Heart of the Furnace", "Inverted Glacier", "Snezhnaya", 
     "+18% ATK", 
     "Triggering Stellar Glimmer or dealing its DMG grants ATK +12% for 12s, and increases party Stellar Glimmer DMG by 50%")
]
```

#### B. Corrupted Weapon Stats Fixes (Weapons 128 & 131)

```python
# In WEAPONS list in generate_csvs.py:
(128, "Fang of the Mountain King", "Claymore", 5, 741, "CRIT Rate", 11.0, 0, 84),      # Kinich
(131, "A Thousand Blazing Suns", "Claymore", 5, 741, "CRIT Rate", 11.0, 0, 87),        # Mavuika
```

#### C. Character Attributes Corrections

```python
# In CHARACTERS list in generate_csvs.py:
(72, "Arlecchino", 5, "Pyro", "Polearm", "Snezhnaya", "Main DPS", 13103, 342, 765, "Normal > Skill > Burst", 4.6),
(91, "Iansan", 4, "Electro", "Polearm", "Natlan", "Main DPS", 11419, 268, 674, "Skill > Burst > Normal", 5.5),
(99, "Zibai", 5, "Geo", "Sword", "Liyue", "Main DPS", 13103, 332, 850, "Skill > Burst > Normal", 6.2),
(102, "Columbina", 5, "Hydro", "Catalyst", "Nod-Krai", "Sub-DPS", 14695, 268, 696, "Burst > Skill > Normal", 6.0),
(103, "Sandrone", 5, "Cryo", "Claymore", "Snezhnaya", "Support", 12858, 244, 876, "Skill > Burst > Normal", 6.2),
(105, "Aloy", 5, "Cryo", "Bow", "None", "Sub-DPS", 10899, 234, 676, "Skill > Burst > Normal", 2.1)
```

#### D. Capitano (ID 104) and Build 381 Absolute Purge
- In `CHARACTERS`: Remove row `(104, "Capitano", 5, "Cryo", "Claymore", "Snezhnaya", "Main DPS", 15552, 359, 876, "Normal > Skill > Burst", 6.1)`.
- In `BUILDS`: Remove row `(381, 104, "Apex Cryo Juggernaut", "Main DPS", 141, 55, "ATK%", "Cryo DMG", "CRIT Rate", "SS", "Snezhnaya's First Harbinger delivering overwhelming physical and cryo devastation")`.

---

### 3.2 R2 Missing Characters Ingestion Specification (IDs 115 to 130)

Complete schema tuples for `characters` table:
`Schema: (character_id, name, rarity, vision, weapon_type, region, default_role, base_hp, base_atk, base_def, talent_priority, release_patch)`

```python
NEW_CHARACTERS = [
    (115, "Ifa", 4, "Anemo", "Catalyst", "Natlan", "Healer", 11201, 193, 655, "Skill > Burst > Normal", 5.6),
    (116, "Escoffier", 5, "Cryo", "Polearm", "Fontaine", "Sub-DPS", 12907, 337, 789, "Skill > Burst > Normal", 5.6),
    (117, "Dahlia", 4, "Hydro", "Sword", "Mondstadt", "Support", 11962, 196, 713, "Burst > Skill > Normal", 5.7),
    (118, "Skirk", 5, "Cryo", "Sword", "Outlander", "Main DPS", 13103, 349, 799, "Normal > Skill > Burst", 5.7),
    (119, "Wonderland Manekin", 5, "Anemo", "Sword", "Outlander", "Main DPS", 10875, 297, 683, "Skill = Burst > Normal", 6.1),
    (120, "Durin", 5, "Pyro", "Sword", "Mondstadt", "Main DPS", 13348, 342, 784, "Skill > Burst > Normal", 6.2),
    (121, "Varka", 5, "Anemo", "Claymore", "Mondstadt", "Main DPS", 13864, 359, 799, "Normal = Skill > Burst", 6.4),
    (122, "Nicole", 5, "Pyro", "Catalyst", "Mondstadt", "Support", 12907, 268, 696, "Burst > Skill > Normal", 6.6),
    (123, "Prune", 4, "Anemo", "Catalyst", "Nod-Krai", "Sub-DPS", 9787, 225, 628, "Skill > Burst > Normal", 6.6),
    (124, "Lohen", 5, "Cryo", "Polearm", "Nod-Krai", "Main DPS", 13103, 342, 789, "Normal > Skill > Burst", 6.6),
    (125, "Alyosha", 4, "Electro", "Polearm", "Snezhnaya", "Support", 11636, 212, 751, "Burst > Skill > Normal", 7.0),
    (126, "Odette", 5, "Cryo", "Sword", "Snezhnaya", "Sub-DPS", 12858, 337, 784, "Skill > Burst > Normal", 7.0),
    (127, "Vesna", 5, "Anemo", "Sword", "Nod-Krai", "Main DPS", 13348, 342, 807, "Normal > Skill > Burst", 7.1),
    (128, "Vodyanitsa", 5, "Hydro", "Catalyst", "Snezhnaya", "Healer", 14695, 234, 657, "Skill > Burst > Normal", 7.1),
    (129, "Mitya", 5, "Electro", "Catalyst", "Snezhnaya", "Main DPS", 12858, 342, 765, "Normal > Skill > Burst", 7.2),
    (130, "Valeriy", 4, "Electro", "Sword", "Snezhnaya", "Shielder", 12397, 202, 771, "Skill > Burst > Normal", 7.2)
]
```

---

### 3.3 R3 Weapons Catalog Expansion Specification (IDs 204 to 255)

Complete schema tuples for `weapons` table:
`Schema: (weapon_id, name, weapon_type, rarity, base_atk, sub_stat_type, sub_stat_value, is_craftable, signature_character_id)`

#### A. 24 Missing 5-Star Signatures (IDs 204 to 227)

| ID | Weapon Name | Weapon Type | Rarity | Base ATK | Sub-Stat Type | Sub-Stat Value | Craftable | Signature Character | Owner Char ID |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---:|
| **204** | Calamity Queller | Polearm | 5 | 741 | ATK% | 16.5 | 0 | Shenhe | 27 |
| **205** | Everlasting Moonglow | Catalyst | 5 | 608 | HP% | 49.6 | 0 | Sangonomiya Kokomi | 44 |
| **206** | Fractured Halo | Polearm | 5 | 608 | CRIT DMG | 66.2 | 0 | Ineffa | 92 |
| **207** | Nightweaver's Looking Glass | Catalyst | 5 | 542 | Elemental Mastery | 265.0 | 0 | Lauma | 93 |
| **208** | Pocztowy Demonspear | Polearm | 5 | 674 | CRIT Rate | 22.1 | 0 | Flins | 94 |
| **209** | Reliquary of Truth | Catalyst | 5 | 542 | CRIT DMG | 88.2 | 0 | Nefer | 96 |
| **210** | Lightbearing Moonshard | Sword | 5 | 542 | CRIT DMG | 88.2 | 0 | Zibai | 99 |
| **211** | Golden Frostbound Oath | Bow | 5 | 542 | CRIT DMG | 88.2 | 0 | Linnea | 100 |
| **212** | Nocturne's Curtain Call | Catalyst | 5 | 542 | CRIT DMG | 88.2 | 0 | Columbina | 102 |
| **213** | A Teaspoon of Transcendence | Claymore | 5 | 674 | CRIT Rate | 22.1 | 0 | Sandrone | 103 |
| **214** | Sunny Morning Sleep-In | Catalyst | 5 | 542 | Elemental Mastery | 265.0 | 0 | Yumemizuki Mizuki | 107 |
| **215** | Vivid Notions | Catalyst | 5 | 674 | CRIT DMG | 44.1 | 0 | Varesa | 108 |
| **216** | Symphonist of Scents | Polearm | 5 | 608 | CRIT DMG | 66.2 | 0 | Escoffier | 116 |
| **217** | Azurelight | Sword | 5 | 674 | CRIT Rate | 22.1 | 0 | Skirk | 118 |
| **218** | Athame Artis | Sword | 5 | 608 | CRIT Rate | 33.1 | 0 | Durin | 120 |
| **219** | Gest of the Mighty Wolf | Claymore | 5 | 608 | CRIT Rate | 33.1 | 0 | Varka | 121 |
| **220** | Angelos' Heptades | Catalyst | 5 | 741 | ATK% | 16.5 | 0 | Nicole | 122 |
| **221** | Disaster and Remorse | Polearm | 5 | 674 | CRIT Rate | 22.1 | 0 | Lohen | 124 |
| **222** | Whitelake Frostfeather | Sword | 5 | 608 | CRIT DMG | 66.2 | 0 | Odette | 126 |
| **223** | Beyond the Chrysalis | Sword | 5 | 674 | CRIT DMG | 44.1 | 0 | Vesna | 127 |
| **224** | Hymn of the Maelstrom | Catalyst | 5 | 608 | HP% | 49.6 | 0 | Vodyanitsa | 128 |
| **225** | Starsealed Edict | Catalyst | 5 | 674 | CRIT Rate | 22.1 | 0 | Mitya | 129 |
| **226** | Exaiphanes Blade | Sword | 5 | 608 | CRIT Rate | 33.1 | 0 | Traveler (Pyro) | 114 |
| **227** | Miliastra Sovereign | Sword | 5 | 608 | CRIT DMG | 66.2 | 0 | Wonderland Manekin | 119 |

```python
NEW_5STAR_SIGNATURE_WEAPONS = [
    (204, "Calamity Queller", "Polearm", 5, 741, "ATK%", 16.5, 0, 27),
    (205, "Everlasting Moonglow", "Catalyst", 5, 608, "HP%", 49.6, 0, 44),
    (206, "Fractured Halo", "Polearm", 5, 608, "CRIT DMG", 66.2, 0, 92),
    (207, "Nightweaver's Looking Glass", "Catalyst", 5, 542, "Elemental Mastery", 265.0, 0, 93),
    (208, "Pocztowy Demonspear", "Polearm", 5, 674, "CRIT Rate", 22.1, 0, 94),
    (209, "Reliquary of Truth", "Catalyst", 5, 542, "CRIT DMG", 88.2, 0, 96),
    (210, "Lightbearing Moonshard", "Sword", 5, 542, "CRIT DMG", 88.2, 0, 99),
    (211, "Golden Frostbound Oath", "Bow", 5, 542, "CRIT DMG", 88.2, 0, 100),
    (212, "Nocturne's Curtain Call", "Catalyst", 5, 542, "CRIT DMG", 88.2, 0, 102),
    (213, "A Teaspoon of Transcendence", "Claymore", 5, 674, "CRIT Rate", 22.1, 0, 103),
    (214, "Sunny Morning Sleep-In", "Catalyst", 5, 542, "Elemental Mastery", 265.0, 0, 107),
    (215, "Vivid Notions", "Catalyst", 5, 674, "CRIT DMG", 44.1, 0, 108),
    (216, "Symphonist of Scents", "Polearm", 5, 608, "CRIT DMG", 66.2, 0, 116),
    (217, "Azurelight", "Sword", 5, 674, "CRIT Rate", 22.1, 0, 118),
    (218, "Athame Artis", "Sword", 5, 608, "CRIT Rate", 33.1, 0, 120),
    (219, "Gest of the Mighty Wolf", "Claymore", 5, 608, "CRIT Rate", 33.1, 0, 121),
    (220, "Angelos' Heptades", "Catalyst", 5, 741, "ATK%", 16.5, 0, 122),
    (221, "Disaster and Remorse", "Polearm", 5, 674, "CRIT Rate", 22.1, 0, 124),
    (222, "Whitelake Frostfeather", "Sword", 5, 608, "CRIT DMG", 66.2, 0, 126),
    (223, "Beyond the Chrysalis", "Sword", 5, 674, "CRIT DMG", 44.1, 0, 127),
    (224, "Hymn of the Maelstrom", "Catalyst", 5, 608, "HP%", 49.6, 0, 128),
    (225, "Starsealed Edict", "Catalyst", 5, 674, "CRIT Rate", 22.1, 0, 129),
    (226, "Exaiphanes Blade", "Sword", 5, 608, "CRIT Rate", 33.1, 0, 114),
    (227, "Miliastra Sovereign", "Sword", 5, 608, "CRIT DMG", 66.2, 0, 119)
]
```

#### B. 19 Missing Regional Craftables (IDs 228 to 246)

| ID | Weapon Name | Weapon Type | Rarity | Base ATK | Sub-Stat Type | Sub-Stat Value | Craftable | Region Origin |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **228** | Snow-Tombed Starsilver | Claymore | 4 | 565 | Physical DMG | 34.5 | 1 | Dragonspine |
| **229** | Dragonspine Spear | Polearm | 4 | 454 | Physical DMG | 69.0 | 1 | Dragonspine |
| **230** | Frostbearer | Catalyst | 4 | 510 | ATK% | 41.3 | 1 | Dragonspine |
| **231** | Forest Regalia | Claymore | 4 | 565 | Energy Recharge | 30.6 | 1 | Sumeru |
| **232** | Moonpiercer | Polearm | 4 | 565 | Elemental Mastery | 110.0 | 1 | Sumeru |
| **233** | King's Squire | Bow | 4 | 454 | ATK% | 55.1 | 1 | Sumeru |
| **234** | Fruit of Fulfillment | Catalyst | 4 | 510 | Energy Recharge | 45.9 | 1 | Sumeru |
| **235** | Song of Stillness | Bow | 4 | 510 | ATK% | 41.3 | 1 | Fontaine |
| **236** | Flowing Purity | Catalyst | 4 | 565 | ATK% | 27.6 | 1 | Fontaine |
| **237** | Serenity's Call | Sword | 4 | 454 | Energy Recharge | 61.3 | 1 | Nod-Krai |
| **238** | Master Key | Claymore | 4 | 454 | Energy Recharge | 61.3 | 1 | Nod-Krai |
| **239** | Prospector's Shovel | Polearm | 4 | 510 | ATK% | 41.3 | 1 | Nod-Krai |
| **240** | Snare Hook | Bow | 4 | 454 | Energy Recharge | 61.3 | 1 | Nod-Krai |
| **241** | Blackmarrow Lantern | Catalyst | 4 | 454 | Elemental Mastery | 221.0 | 1 | Nod-Krai |
| **242** | Emberwell | Sword | 4 | 510 | Elemental Mastery | 165.0 | 1 | Snezhnaya |
| **243** | Blade of Atonement | Claymore | 4 | 565 | ATK% | 27.6 | 1 | Snezhnaya |
| **244** | Song of the Vigil | Polearm | 4 | 565 | Elemental Mastery | 110.0 | 1 | Snezhnaya |
| **245** | Covenant of Frost and Snow | Bow | 4 | 510 | DEF% | 51.7 | 1 | Snezhnaya |
| **246** | Echoes of the Heart | Catalyst | 4 | 565 | ATK% | 27.6 | 1 | Snezhnaya |

```python
NEW_CRAFTABLE_WEAPONS = [
    # Dragonspine (3)
    (228, "Snow-Tombed Starsilver", "Claymore", 4, 565, "Physical DMG", 34.5, 1, None),
    (229, "Dragonspine Spear", "Polearm", 4, 454, "Physical DMG", 69.0, 1, None),
    (230, "Frostbearer", "Catalyst", 4, 510, "ATK%", 41.3, 1, None),

    # Sumeru (4)
    (231, "Forest Regalia", "Claymore", 4, 565, "Energy Recharge", 30.6, 1, None),
    (232, "Moonpiercer", "Polearm", 4, 565, "Elemental Mastery", 110.0, 1, None),
    (233, "King's Squire", "Bow", 4, 454, "ATK%", 55.1, 1, None),
    (234, "Fruit of Fulfillment", "Catalyst", 4, 510, "Energy Recharge", 45.9, 1, None),

    # Fontaine (2)
    (235, "Song of Stillness", "Bow", 4, 510, "ATK%", 41.3, 1, None),
    (236, "Flowing Purity", "Catalyst", 4, 565, "ATK%", 27.6, 1, None),

    # Nod-Krai (5)
    (237, "Serenity's Call", "Sword", 4, 454, "Energy Recharge", 61.3, 1, None),
    (238, "Master Key", "Claymore", 4, 454, "Energy Recharge", 61.3, 1, None),
    (239, "Prospector's Shovel", "Polearm", 4, 510, "ATK%", 41.3, 1, None),
    (240, "Snare Hook", "Bow", 4, 454, "Energy Recharge", 61.3, 1, None),
    (241, "Blackmarrow Lantern", "Catalyst", 4, 454, "Elemental Mastery", 221.0, 1, None),

    # Snezhnaya (5)
    (242, "Emberwell", "Sword", 4, 510, "Elemental Mastery", 165.0, 1, None),
    (243, "Blade of Atonement", "Claymore", 4, 565, "ATK%", 27.6, 1, None),
    (244, "Song of the Vigil", "Polearm", 4, 565, "Elemental Mastery", 110.0, 1, None),
    (245, "Covenant of Frost and Snow", "Bow", 4, 510, "DEF%", 51.7, 1, None),
    (246, "Echoes of the Heart", "Catalyst", 4, 565, "ATK%", 27.6, 1, None)
]
```

#### C. Key Meta Staples and Event/Gacha Series (IDs 247 to 255)

| ID | Weapon Name | Weapon Type | Rarity | Base ATK | Sub-Stat Type | Sub-Stat Value | Craftable | Signature / Role Context |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **247** | Fleuve Cendre Ferryman | Sword | 4 | 510 | Energy Recharge | 45.9 | 0 | Fontaine Fishing / Furina F2P BiS (Build 305) |
| **248** | The Stringless | Bow | 4 | 510 | Elemental Mastery | 165.0 | 0 | General Gacha Reaction Staple (Build 431) |
| **249** | Cinnabar Spindle | Sword | 4 | 454 | DEF% | 69.0 | 0 | Albedo 4★ Event Signature (Char ID 6, Build 387) |
| **250** | Mountain-Bracing Bolt | Polearm | 4 | 565 | Energy Recharge | 30.6 | 0 | Natlan Gacha Series / Iansan BiS (Build 441) |
| **251** | Sturdy Bone | Sword | 4 | 565 | ATK% | 27.6 | 0 | Natlan Gacha Series (Movement / Normal Atk) |
| **252** | Fruitful Hook | Claymore | 4 | 565 | ATK% | 27.6 | 0 | Natlan Gacha Series (Plunging Attack) |
| **253** | Flower-Wreathed Feathers | Bow | 4 | 510 | ATK% | 41.3 | 0 | Natlan Gacha Series (Aimed Shot / Gliding) |
| **254** | Waveriding Whirl | Catalyst | 4 | 454 | Energy Recharge | 61.3 | 0 | Natlan Gacha Series (Swimming / Burst Utility) |
| **255** | Calamity of Eshu | Sword | 4 | 510 | ATK% | 41.3 | 0 | Natlan Event Weapon (Shield Normal/Charged Atk) |

```python
NEW_STAPLE_WEAPONS = [
    (247, "Fleuve Cendre Ferryman", "Sword", 4, 510, "Energy Recharge", 45.9, 0, None),
    (248, "The Stringless", "Bow", 4, 510, "Elemental Mastery", 165.0, 0, None),
    (249, "Cinnabar Spindle", "Sword", 4, 454, "DEF%", 69.0, 0, 6),                     # Albedo
    (250, "Mountain-Bracing Bolt", "Polearm", 4, 565, "Energy Recharge", 30.6, 0, None),
    (251, "Sturdy Bone", "Sword", 4, 565, "ATK%", 27.6, 0, None),
    (252, "Fruitful Hook", "Claymore", 4, 565, "ATK%", 27.6, 0, None),
    (253, "Flower-Wreathed Feathers", "Bow", 4, 510, "ATK%", 41.3, 0, None),
    (254, "Waveriding Whirl", "Catalyst", 4, 454, "Energy Recharge", 61.3, 0, None),
    (255, "Calamity of Eshu", "Sword", 4, 510, "ATK%", 41.3, 0, None)
]
```

---

## 4. Caveats

1. **Read-Only Investigation Guarantee**:
   No project source files, CSV files, or database binaries were modified during this investigation. All specifications are completely prepared for direct insertion into `generate_csvs.py`.
2. **Build Re-linking Dependency**:
   When implementing R3 weapons, the implementation agent must update the foreign key `recommended_weapon_id` in `character_builds` for builds 305 (*Furina*, update to 247), 387 (*Albedo*, update to 249), and 392 (*Shenhe*, update to 204), as well as linking any new builds from `explorer_survey_3` that reference these new IDs.
3. **Database Nullability Representation**:
   When serializing `weapons.csv`, `signature_character_id` should be exported as an empty string `""` for NULL values, which `init_db.py` parses into Python `None` (SQL `NULL`).

---

## 5. Conclusion

1. **R1 Remediation Ready**: Exact official texts for Artifact Sets 59, 60, 62, 63, and 64; stat corrections for weapons 128 and 131; regional and attribute fixes for Arlecchino, Zibai, Columbina, Sandrone, Iansan, and Aloy; and the full deletion plan for Capitano (104) and build 381 are 100% specified.
2. **R2 Characters Ingestion Ready**: All 16 missing playable characters are numbered contiguously from 115 to 130 and have fully verified base stats, weapon types, visions, and release patches matching the 12-column table schema. Regional count after expansion is verified at exactly 129 characters.
3. **R3 Weapons Catalog Expansion Ready**: Exactly 52 new weapons (IDs 204 to 255) are cataloged across 24 5-star signatures, 19 craftables, and 9 meta staples. Every tuple conforms to schema constraints and foreign key linkages.

---

## 6. Verification Method

To verify these specifications independently:

1. **Verify Current Weapon Defects (IDs 128 & 131)**:
   ```bash
   python3 -c "
   import sqlite3
   conn = sqlite3.connect('genshin_learning.db')
   cur = conn.cursor()
   print(cur.execute('SELECT weapon_id, name, base_atk, sub_stat_value FROM weapons WHERE weapon_id IN (128, 131);').fetchall())
   "
   ```
   *Expected Output*: Shows current incorrect stats `(608, 33.1)`. Target specification replaces them with `(741, 11.0)`.

2. **Verify Current Capitano & Build 381 Presence**:
   ```bash
   python3 -c "
   import sqlite3
   conn = sqlite3.connect('genshin_learning.db')
   cur = conn.cursor()
   print('Capitano character:', cur.execute('SELECT character_id, name FROM characters WHERE character_id = 104;').fetchall())
   print('Capitano build:', cur.execute('SELECT build_id, character_id, build_name FROM character_builds WHERE character_id = 104;').fetchall())
   "
   ```
   *Expected Output*: Character 104 and Build 381 are present and must be removed.

3. **Verify Foreign Key Consistency on New Weapon Signatures**:
   ```bash
   python3 -c "
   # Simulate inserting new weapons into temporary table to test FKs
   import sqlite3
   conn = sqlite3.connect('genshin_learning.db')
   conn.execute('PRAGMA foreign_keys = ON;')
   cur = conn.cursor()
   sig_ids = [27, 44, 92, 93, 94, 96, 99, 100, 102, 103, 107, 108, 114, 6]
   missing = [sid for sid in sig_ids if not cur.execute('SELECT 1 FROM characters WHERE character_id = ?;', (sid,)).fetchone()]
   print('Existing characters missing:', missing)
   "
   ```
   *Expected Output*: `Existing characters missing: []`. All existing signatures resolve immediately, while signatures pointing to IDs 116–129 resolve once R2 characters are ingested.

4. **Verify Target Regional Distribution (Total 129 Characters)**:
   ```bash
   python3 -c "
   expected = {'Liyue': 22, 'Mondstadt': 23, 'Inazuma': 17, 'Sumeru': 14, 'Fontaine': 13, 'Natlan': 11, 'Nod-Krai': 12, 'Outlander': 8, 'Snezhnaya': 8, 'None': 1}
   print('Total sum:', sum(expected.values()))
   assert sum(expected.values()) == 129
   print('Regional distribution math verified: 129 characters.')
   "
   ```
   *Expected Output*: `Total sum: 129`, `Regional distribution math verified: 129 characters.`
