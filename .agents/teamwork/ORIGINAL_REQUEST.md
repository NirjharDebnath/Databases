# Original User Request

## 2026-11-20T16:15:39Z

# Teamwork Project Prompt

Fix all identified data defects, attribute inconsistencies, missing playable characters, weapons, artifact set descriptions, and character builds across `genshin_learning.db` to align completely with the latest Genshin Impact patch data.

Working directory: `/home/nirjhar/Python Codes/Einstein/Databases`
Integrity mode: development

## Requirements

### R1. Database Defect Remediation
Apply all factual and attribute corrections:
- Update artifact set regions, domains, casing, and bonus descriptions for Sets 59, 60, 62, 63, and 64 to match official scaling and domain locations.
- Correct corrupted 5★ weapon stats for *Fang of the Mountain King* (ID 128) and *A Thousand Blazing Suns* (ID 131) to 741 Base ATK and 11.0% CRIT Rate.
- Correct character attributes: Arlecchino (Region: Snezhnaya), Zibai (Region: Liyue), Columbina (Region: Nod-Krai), Sandrone (Vision: Cryo, Weapon: Claymore), Iansan (Release Patch: 5.5), and Aloy (Region: None).
- Remove non-playable NPC *Capitano* (ID 104) and any associated build entries.

### R2. Missing Playable Characters Ingestion
Add all 16 missing playable characters from Version 5.x through recent releases (*Ifa*, *Escoffier*, *Dahlia*, *Skirk*, *Wonderland Manekin*, *Durin*, *Varka*, *Nicole*, *Prune*, *Lohen*, *Alyosha*, *Odette*, *Vesna*, *Vodyanitsa*, *Mitya*, *Valeriy*) with accurate element, weapon type, region, rarity, base stats, and release versions.

### R3. Weapons Catalog Expansion
Ingest missing weapons to support character signatures and F2P builds:
- All 24 missing 5-star signature weapons (including *Calamity Queller*, *Everlasting Moonglow*, *Sunny Morning Sleep-In*, *Vivid Notions*, *Azurelight*, etc.).
- 19 missing craftables across Dragonspine, Sumeru, Fontaine, and Post-Natlan.
- Key meta staples (*Fleuve Cendre Ferryman*, *The Stringless*, *Cinnabar Spindle*, and Natlan event/gacha series).

### R4. Character Builds Backfill & Role Variety
- Provide verified meta builds for all 43 characters currently missing builds (e.g. *Barbara*, *Noelle*, *Beidou*, *Rosaria*, *Ororon*, *Yaoyao*, *Diona*, *Qiqi*, etc.).
- Add alternative meta roles for key characters (e.g. *Mavuika* Support/Sub-DPS with 4pc Scroll of the Hero of Cinder City, F2P variants for *Citlali* and *Chasca*).
- Re-link mismatched builds (*Furina*, *Albedo*, *Shenhe*) to their proper signature and BiS weapons.

### R5. Data Synchronization & Automated Verification
- Regenerate all CSV files in `data/` (`characters.csv`, `weapons.csv`, `artifact_sets.csv`, `character_builds.csv`).
- Update database generation scripts (`generate_csvs.py`, `init_db.py`) to ensure 100% reproducibility.
- Run `verify_db.py` to prove 0 foreign key violations, 0 orphaned records, and complete schema integrity.

## Acceptance Criteria

### Data Correctness & Integrity
- [ ] Artifact sets 59, 60, 62, 63, and 64 have verified accurate names, regions, domains, and 2pc/4pc bonus texts.
- [ ] *Fang of the Mountain King* and *A Thousand Blazing Suns* have Base ATK = 741 and Sub-stat = 11.0% CRIT Rate.
- [ ] Non-playable NPC *Capitano* is completely removed from `characters` and `character_builds`.
- [ ] All 16 missing playable characters are populated in `characters` with valid base stats.
- [ ] All 24 missing 5-star signature weapons and key craftables/staples are inserted into `weapons`.
- [ ] 100% of playable characters in `characters` have at least 1 verified meta build in `character_builds`.
- [ ] All foreign key references (`character_id`, `recommended_weapon_id`, `recommended_artifact_id`) resolve cleanly with 0 violations.
- [ ] All 4 CSV files in `data/` match database tables exactly.
- [ ] Automated verification script `verify_db.py` passes with all tests green.
