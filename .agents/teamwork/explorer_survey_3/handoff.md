# Character Builds Backfill, Role Variety, and Data Synchronization Survey (R4 & R5)

**Explorer**: `explorer_survey_3`  
**Date**: 2026-11-20  
**Project Root**: `/home/nirjhar/Python Codes/Einstein/Databases`  
**Working Directory**: `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_3`  
**Status**: Completed (Hard Handoff)

---

## 1. Observation

### 1.1 Current Database & Character Builds State
Direct database queries on `genshin_learning.db` revealed the following exact metrics:
- Total characters currently in `characters`: **114** (IDs 1 through 114).
- Total builds currently in `character_builds`: **107** (build IDs 301 through 407).
- Number of distinct characters with builds: **71**.
- Characters currently lacking builds in `character_builds`: **43 characters** (37.7% of the roster).
- Non-playable character `Capitano` (character ID 104) currently has build ID 381:
  ```sql
  (381, 104, 'Apex Cryo Juggernaut', 'Main DPS', 141, 55, 'ATK%', 'Cryo DMG', 'CRIT Rate', 'SS', 'Snezhnaya''s First Harbinger delivering overwhelming physical and cryo devastation')
  ```
  Per R1, Capitano is to be deleted; this build must also be deleted.

### 1.2 Inventory of the 43 Existing Characters Lacking Builds
```sql
SELECT character_id, name, vision, weapon_type, region, default_role 
FROM characters 
WHERE character_id NOT IN (SELECT DISTINCT character_id FROM character_builds)
ORDER BY character_id;
```
Direct query results:
1. ID 11: Barbara (Hydro, Catalyst, Mondstadt, Healer)
2. ID 12: Razor (Electro, Claymore, Mondstadt, Main DPS)
3. ID 13: Noelle (Geo, Claymore, Mondstadt, Shielder)
4. ID 14: Kaeya (Cryo, Sword, Mondstadt, Sub-DPS)
5. ID 15: Lisa (Electro, Catalyst, Mondstadt, Sub-DPS)
6. ID 16: Amber (Pyro, Bow, Mondstadt, Sub-DPS)
7. ID 17: Diona (Cryo, Bow, Mondstadt, Shielder)
8. ID 18: Rosaria (Cryo, Polearm, Mondstadt, Sub-DPS)
9. ID 19: Mika (Cryo, Polearm, Mondstadt, Healer)
10. ID 26: Qiqi (Cryo, Sword, Liyue, Healer)
11. ID 32: Ningguang (Geo, Catalyst, Liyue, Main DPS)
12. ID 33: Beidou (Electro, Claymore, Liyue, Sub-DPS)
13. ID 34: Chongyun (Cryo, Claymore, Liyue, Sub-DPS)
14. ID 35: Xinyan (Pyro, Claymore, Liyue, Shielder)
15. ID 36: Yanfei (Pyro, Catalyst, Liyue, Main DPS)
16. ID 37: Yun Jin (Geo, Polearm, Liyue, Support)
17. ID 38: Yaoyao (Dendro, Polearm, Liyue, Healer)
18. ID 49: Kujou Sara (Electro, Bow, Inazuma, Support)
19. ID 50: Sayu (Anemo, Claymore, Inazuma, Healer)
20. ID 51: Thoma (Pyro, Polearm, Inazuma, Shielder)
21. ID 52: Gorou (Geo, Bow, Inazuma, Support)
22. ID 54: Shikanoin Heizou (Anemo, Catalyst, Inazuma, Main DPS)
23. ID 55: Kirara (Dendro, Sword, Inazuma, Shielder)
24. ID 63: Collei (Dendro, Bow, Sumeru, Sub-DPS)
25. ID 64: Dori (Electro, Claymore, Sumeru, Healer)
26. ID 65: Candace (Hydro, Polearm, Sumeru, Support)
27. ID 66: Layla (Cryo, Sword, Sumeru, Shielder)
28. ID 68: Kaveh (Dendro, Claymore, Sumeru, Main DPS)
29. ID 69: Sethos (Electro, Bow, Sumeru, Main DPS)
30. ID 79: Lynette (Anemo, Sword, Fontaine, Sub-DPS)
31. ID 80: Freminet (Cryo, Claymore, Fontaine, Main DPS)
32. ID 81: Charlotte (Cryo, Catalyst, Fontaine, Healer)
33. ID 90: Ororon (Electro, Bow, Natlan, Sub-DPS)
34. ID 91: Iansan (Electro, Polearm, Natlan, Main DPS)
35. ID 95: Aino (Hydro, Claymore, Nod-Krai, Sub-DPS)
36. ID 96: Nefer (Dendro, Catalyst, Nod-Krai, Main DPS)
37. ID 97: Jahoda (Anemo, Bow, Nod-Krai, Support)
38. ID 98: Illuga (Geo, Polearm, Nod-Krai, Support)
39. ID 99: Zibai (Geo, Sword, Liyue [after R1], Main DPS)
40. ID 100: Linnea (Geo, Bow, Nod-Krai, Sub-DPS)
41. ID 105: Aloy (Cryo, Bow, None [after R1], Sub-DPS)
42. ID 111: Traveler (Electro) (Electro, Sword, Outlander, Support)
43. ID 113: Traveler (Hydro) (Hydro, Sword, Outlander, Sub-DPS)

### 1.3 Inventory of the 16 New Characters (from R2) Requiring Meta Builds
The 16 playable characters to be added via R2 (assigned IDs 115 to 130) all lack builds:
1. ID 115: Ifa (4★, Anemo, Catalyst, Natlan, Healer)
2. ID 116: Escoffier (5★, Cryo, Polearm, Fontaine, Sub-DPS)
3. ID 117: Dahlia (4★, Hydro, Sword, Mondstadt, Support)
4. ID 118: Skirk (5★, Cryo, Sword, Outlander, Main DPS)
5. ID 119: Wonderland Manekin (5★, Anemo, Sword, Outlander, Main DPS)
6. ID 120: Durin (5★, Pyro, Sword, Mondstadt, Main DPS)
7. ID 121: Varka (5★, Anemo, Claymore, Mondstadt, Main DPS)
8. ID 122: Nicole (5★, Pyro, Catalyst, Mondstadt, Support)
9. ID 123: Prune (4★, Anemo, Catalyst, Nod-Krai, Sub-DPS)
10. ID 124: Lohen (5★, Cryo, Polearm, Nod-Krai, Main DPS)
11. ID 125: Alyosha (4★, Electro, Polearm, Snezhnaya, Support)
12. ID 126: Odette (5★, Cryo, Sword, Snezhnaya, Sub-DPS)
13. ID 127: Vesna (5★, Anemo, Sword, Nod-Krai, Main DPS)
14. ID 128: Vodyanitsa (5★, Hydro, Catalyst, Snezhnaya, Healer)
15. ID 129: Mitya (5★, Electro, Catalyst, Snezhnaya, Main DPS)
16. ID 130: Valeriy (4★, Electro, Sword, Snezhnaya, Shielder)

### 1.4 Mismatched Builds for Furina, Albedo, and Shenhe
Query results from `character_builds`:
- **Furina** (character ID 71):
  - Build 304: `Splendor of Tranquil Waters` (weapon 102) - Correct signature build.
  - Build 305: Named `"F2P Ferryman Buffer"` but `recommended_weapon_id` is currently `188` (`Favonius Sword`) instead of `Fleuve Cendre Ferryman`.
- **Albedo** (character ID 6):
  - Build 387: Named `"Solar Isotoma Transient Blossom"`, `recommended_weapon_id` is currently `182` (`Flute of Ezpitzal`). Mismatched with his signature BiS weapon `Cinnabar Spindle` (ingested in R3).
- **Shenhe** (character ID 27):
  - Build 392: Named `"Icy Quill Cryo Buffer"`, `recommended_weapon_id` is currently `135` (`Primordial Jade Winged-Spear`). Mismatched with her signature 5★ weapon `Calamity Queller` (ingested in R3).

### 1.5 Missing Alternative Meta Roles for Key Characters
- **Mavuika** (character ID 87): Currently only has Build 373 (`"Blazing Suns Pyro Sovereign"`, Main DPS, Obsidian Codex). Lacks a dedicated `Support/Sub-DPS` build utilizing `4pc Scroll of the Hero of Cinder City` (Set 53).
- **Citlali** (character ID 88): Currently only has Build 374 (`"Starcaller Shield & Cryo Enabler"`, 5★ weapon 132 `Starcaller's Watch`). Lacks an accessible F2P variant.
- **Chasca** (character ID 86): Currently only has Build 372 (`"Astral Vulture Multi-Element"`, 5★ weapon 130 `Astral Vulture's Crimson Plumage`). Lacks an accessible F2P variant.

### 1.6 Current State of Data Pipelines and Verification Suite
- `generate_csvs.py`: In-memory data structures define CSV exports. Current BUILDS list has 107 records.
- `init_db.py`: Reads `data/character_builds.csv` and inserts via `executemany`. Enforces foreign key constraints:
  - `character_id REFERENCES characters(character_id) ON DELETE CASCADE`
  - `recommended_weapon_id REFERENCES weapons(weapon_id) ON DELETE RESTRICT`
  - `recommended_artifact_id REFERENCES artifact_sets(artifact_set_id) ON DELETE RESTRICT`
- `verify_db.py`: Currently has hardcoded counts:
  - `characters: 114`, `weapons: 103`, `artifact_sets: 64`, `character_builds: 107`.
  - Regional counts: `Liyue: 21, Mondstadt: 19, Inazuma: 17, Sumeru: 14, Fontaine: 13, Natlan: 10, Nod-Krai: 9, Outlander: 7, Snezhnaya: 4`.
  - Lacks assertions checking that 100% of playable characters have builds, weapon types match character weapon types, or that CSV files match DB tables.

---

## 2. Logic Chain

1. **Relational Bridge Table Requirements**:
   - Every build record in `character_builds` requires:
     `build_id` (PK), `character_id` (FK), `build_name`, `role`, `recommended_weapon_id` (FK), `recommended_artifact_id` (FK), `sands_stat`, `goblet_stat`, `circlet_stat`, `tier_rating`, `playstyle_notes`.
   - SQLite enforces `FOREIGN KEY` constraints on `character_id`, `recommended_weapon_id`, and `recommended_artifact_id`.
   - Therefore, every build's weapon and artifact references must resolve to an existing row in `weapons` and `artifact_sets`.

2. **Decoupled Weapon FK Safety & Progressive Ingestion**:
   - Because R3 adds new weapons (e.g. *Calamity Queller*, *Cinnabar Spindle*, *Fleuve Cendre Ferryman*, *Azurelight*), if R4 builds are loaded before R3 weapons exist, foreign key violations will occur.
   - To guarantee 100% relational integrity at any stage of execution:
     - Each build specification below provides a **guaranteed existing valid weapon ID** (from current IDs 101–203) matching the character's weapon type.
     - A secondary re-linking mapping is provided for when R3 weapons are ingested.

3. **Character Coverage Completeness**:
   - Current roster has 114 characters minus Capitano (104) = 113.
   - 16 new characters from R2 = 129 playable characters total.
   - Current distinct characters with builds = 70 (excluding Capitano).
   - 129 - 70 = **59 characters lacking builds**.
   - Backfilling 59 builds + 3 alternative meta role builds = **62 new builds**.
   - Total builds post-implementation = 107 - 1 (Capitano) + 62 = **168 builds**.
   - With 129 characters having at least 1 build, character coverage reaches **100%** with **0 orphaned characters**.

4. **Pipeline Synchronization Protocol (Single Source of Truth)**:
   - Modifying only SQLite or only CSVs leads to pipeline desynchronization.
   - `generate_csvs.py` must contain all updated character, weapon, artifact, and build records.
   - `python3 generate_csvs.py` must write to `data/*.csv`.
   - `python3 init_db.py` must ingest `data/*.csv` into `genshin_learning.db`.
   - `python3 verify_db.py` must test `genshin_learning.db` and verify parity with `data/*.csv`.

---

## 3. Detailed Data Specifications

### 3.1 Complete Catalog of 62 New Meta Builds (Build IDs 408 to 469)

All weapon IDs in the primary recommendation column resolve directly to existing rows in `weapons` (IDs 101–203) and match the character's weapon type. Target R3 signature/staple weapons are noted for subsequent re-linking.

| Build ID | Char ID | Character Name | Build Name | Role | Weap ID | Primary Valid Weapon | Target R3 Weapon | Art ID | Recommended Artifact Set | Sands Stat | Goblet Stat | Circlet Stat | Tier | Sub-stats Priority & Playstyle Notes |
|:---:|:---:|:---|:---|:---:|:---:|:---|:---|:---:|:---|:---:|:---:|:---:|:---:|:---|
| **408** | 11 | Barbara | Ocean-Hued Hydro Caregiver | Healer | 200 | Thrilling Tales of Dragon Slayers | Everlasting Moonglow | 38 | Ocean-Hued Clam | HP% | HP% | Healing Bonus | A | HP% > ER > Flat HP > EM. Continuous team healing via Melody Loop and instant party burst while boosting active DPS with Thrilling Tales. |
| **409** | 12 | Razor | Pale Flame Physical Wolf | Main DPS | 141 | Wolf's Gravestone | Wolf's Gravestone | 34 | Pale Flame | ATK% | Physical DMG | CRIT Rate | A | CRIT Rate > CRIT DMG > ATK% > ER. Summons the Wolf Spirit to attack alongside normal strikes, shredding enemy physical resistance with Superconduct. |
| **410** | 13 | Noelle | Sweeping Time Battle Maid | Main DPS | 114 | Redhorn Stonethresher | Redhorn Stonethresher | 37 | Husk of Opulent Dreams | DEF% | Geo DMG | CRIT Rate | S | DEF% > CRIT Rate > CRIT DMG > ER. Converts massive DEF into ATK during Sweeping Time, cleaving entire arenas while healing the entire party. |
| **411** | 14 | Kaeya | Glacial Waltz Blizzard Shredder | Sub-DPS | 108 | Mistsplitter Reforged | Mistsplitter Reforged | 36 | Emblem of Severed Fate | Energy Recharge | Cryo DMG | CRIT Rate | A | ER > CRIT Rate > CRIT DMG > ATK%. Encircles active character with orbiting icicles dealing sustained off-field Cryo damage in Melt and Freeze teams. |
| **412** | 15 | Lisa | Lightning Rose DEF Shredder | Sub-DPS | 196 | The Widsith | Kagura's Verity | 36 | Emblem of Severed Fate | Energy Recharge | Electro DMG | CRIT Rate | A | ER > CRIT Rate > CRIT DMG > EM. Deploys Lightning Rose to discharge continuous Electro bursts and shred enemy DEF by 15%. |
| **413** | 16 | Amber | Noblesse Fiery Rain Support | Support | 140 | Elegy for the End | Elegy for the End | 21 | Noblesse Oblige | Energy Recharge | Pyro DMG | CRIT Rate | A | ER > CRIT Rate > EM > ATK%. Unleashes rapid-hitting 40-energy Fiery Rain to shred Cryo/Hydro shields and trigger teamwide Noblesse and Elegy buffs. |
| **414** | 17 | Diona | Icy Paws Cryo Battery Shielder | Shielder | 195 | Sacrificial Bow | Sacrificial Bow | 21 | Noblesse Oblige | HP% | HP% | HP% | S | HP% > ER > Flat HP > EM. Fires Icy Paws to grant thick shields, cleanses party debuffs, and generates copious Cryo particles with Sacrificial Bow. |
| **415** | 18 | Rosaria | Shadow Samaritan CRIT Sharer | Sub-DPS | 155 | Deathmatch | Deathmatch | 21 | Noblesse Oblige | Energy Recharge | Cryo DMG | CRIT Rate | S | CRIT Rate > ER > CRIT DMG > ATK%. Plants an Ice Lance for persistent off-field Cryo application while sharing up to 15% CRIT Rate to teammates. |
| **416** | 19 | Mika | Starfrost Physical & Atk Speed Buffer | Support | 189 | Favonius Lance | Favonius Lance | 21 | Noblesse Oblige | Energy Recharge | HP% | Healing Bonus | A | ER > HP% > CRIT Rate > Flat HP. Buffs physical damage and attack speed with Starfrost Flare while healing entire party upon casting Skyfeather Song. |
| **417** | 26 | Qiqi | Fortune-Preserving Clam Healer | Healer | 193 | Sacrificial Sword | Sacrificial Sword | 38 | Ocean-Hued Clam | Energy Recharge | ATK% | Healing Bonus | A | ER > ATK% > Flat ATK > CRIT Rate. Applies Talismans marking foes so attacking allies heal instantly, maxing out Ocean-Hued Clam damage bubbles. |
| **418** | 32 | Ningguang | Starshatter Jade Screen Burst | Main DPS | 149 | Lost Prayer to the Sacred Winds | Lost Prayer to the Sacred Winds | 50 | Nighttime Whispers in the Echoing Woods | ATK% | Geo DMG | CRIT Rate | S | CRIT Rate > CRIT DMG > ATK% > ER. Passes through Jade Screen for Geo DMG bonus, unleashing Starshatter homing jade projectiles with huge single-target burst. |
| **419** | 33 | Beidou | Stormbreaker Chain-Lightning Sub-DPS | Sub-DPS | 154 | Serpent Spine | Serpent Spine | 36 | Emblem of Severed Fate | Energy Recharge | Electro DMG | CRIT Rate | S+ | ER > CRIT Rate > CRIT DMG > ATK%. Parries incoming blows with Tidecaller and unleashes bouncing chain lightning through Stormbreaker across multi-target encounters. |
| **420** | 34 | Chongyun | Spirit Blade Chonghua Melt Nuke | Sub-DPS | 141 | Wolf's Gravestone | Wolf's Gravestone | 21 | Noblesse Oblige | ATK% | Cryo DMG | CRIT Rate | A | CRIT Rate > CRIT DMG > ATK% > EM. Provides melee Cryo infusion and drops three to four giant frost swords dealing instant triple-melt burst damage. |
| **421** | 35 | Xinyan | Riff Revolution Physical Burst | Shielder | 141 | Wolf's Gravestone | Redhorn Stonethresher | 34 | Pale Flame | DEF% | Physical DMG | CRIT DMG | A | DEF% > ER > CRIT DMG > ATK%. Sweeps instrument to form a Pyro shield and fires Riff Revolution with 100% guaranteed physical CRIT hit at C2. |
| **422** | 36 | Yanfei | Scarlet Seal Vaporize Prosecutor | Main DPS | 149 | Lost Prayer to the Sacred Winds | Lost Prayer to the Sacred Winds | 30 | Crimson Witch of Flames | ATK% | Pyro DMG | CRIT Rate | S | CRIT Rate > CRIT DMG > EM > ATK%. Consumes Scarlet Seals through long-range charged fireballs to vaporize targets shielded by Tankfei mechanics. |
| **423** | 37 | Yun Jin | Flying Cloud Normal Attack Buffer | Support | 189 | Favonius Lance | Favonius Lance | 37 | Husk of Opulent Dreams | DEF% | DEF% | DEF% | S | DEF% > ER > Flat DEF > CRIT Rate. Sings Cliffbreaker's Banner to impart huge flat damage buffs to normal attacks scaling with her total DEF. |
| **424** | 38 | Yaoyao | Yuegui Radish Bloom Healer | Healer | 189 | Favonius Lance | Favonius Lance | 41 | Deepwood Memories | HP% | HP% | Healing Bonus | S+ | ER > HP% > Flat HP > EM. Deploys Yuegui to toss White Jade Radishes healing active teammates while reliably maintaining 30% Dendro RES shred. |
| **425** | 49 | Kujou Sara | Tengu Juumonji Electro Buffer | Support | 144 | Skyward Harp | Skyward Harp | 21 | Noblesse Oblige | Energy Recharge | Electro DMG | CRIT Rate | S | ER > CRIT Rate > CRIT DMG > ATK%. Teleports and leaves Crowfeathers granting massive flat ATK buffs and 60% Electro CRIT DMG at C6 to Raiden Shogun. |
| **426** | 50 | Sayu | Fuufuu Whirlwind Swirl Healer | Healer | 192 | Favonius Greatsword | Favonius Greatsword | 24 | Viridescent Venerer | Energy Recharge | Elemental Mastery | Elemental Mastery | A | EM > ER > ATK% > Flat ATK. Rolls continuously across the battlefield absorbing elements and summons Muji-Muji Daruma to heal and shred 40% RES. |
| **427** | 51 | Thoma | Crimson Ooyoroi Burgeon Trigger | Support | 175 | Kitain Cross Spear | Kitain Cross Spear | 44 | Flower of Paradise Lost | Elemental Mastery | Elemental Mastery | Elemental Mastery | S+ | EM > ER > HP% > Flat HP. Triggers fiery Ooyoroi waves on normal attacks to cleanly detonate Dendro Cores in premier Burgeon teams. |
| **428** | 52 | Gorou | General's War-Banner DEF Anchor | Support | 190 | Favonius Warbow | Favonius Warbow | 21 | Noblesse Oblige | Energy Recharge | DEF% | CRIT Rate | S | ER > DEF% > CRIT Rate > Flat DEF. Plants General's War-Banner granting flat DEF, Geo DMG%, and resistance to interruption for mono-Geo teams with Itto and Noelle. |
| **429** | 54 | Shikanoin Heizou | Heartstopper Swirl Pugilist | Main DPS | 149 | Lost Prayer to the Sacred Winds | Lost Prayer to the Sacred Winds | 24 | Viridescent Venerer | ATK% | Anemo DMG | CRIT Rate | S | CRIT Rate > CRIT DMG > ATK% > EM. Rapidly stacks Declension stacks through melee swirls to unleash devastating one-inch Heartstopper punch nukes. |
| **430** | 55 | Kirara | Urgent Neko Delivery Shielder | Shielder | 116 | Key of Khaj-Nisut | Key of Khaj-Nisut | 33 | Tenacity of the Millelith | HP% | HP% | HP% | S | HP% > ER > Flat HP > EM. Curls into a delivery box ramming enemies and providing a reinforced Dendro shield with 100% uptime. |
| **431** | 63 | Collei | Floral Sidewinder Quicken Battery | Sub-DPS | 140 | Elegy for the End | The Stringless | 41 | Deepwood Memories | Energy Recharge | Dendro DMG | CRIT Rate | A | ER > CRIT Rate > CRIT DMG > EM. Deploys Cuilein-Anbar bouncing doll for off-field Dendro application and shreds Dendro resistance. |
| **432** | 64 | Dori | Jinni Energy Battery Healer | Healer | 192 | Favonius Greatsword | Favonius Greatsword | 21 | Noblesse Oblige | Energy Recharge | HP% | Healing Bonus | A | ER > HP% > Flat HP > EM. Summons the Jinni to link with active character, restoring continuous HP and flat energy. |
| **433** | 65 | Candace | Sacred Rite Hydro Infusion Support | Support | 189 | Favonius Lance | Favonius Lance | 21 | Noblesse Oblige | HP% | HP% | HP% | A | ER > HP% > Flat HP > CRIT Rate. Raises Heron's Shield to grant normal attack elemental DMG bonus and melee Hydro infusion to active allies. |
| **434** | 66 | Layla | Curtain of Slumber Star-Stream Shielder | Shielder | 116 | Key of Khaj-Nisut | Key of Khaj-Nisut | 33 | Tenacity of the Millelith | HP% | HP% | HP% | S | HP% > ER > Flat HP > CRIT Rate. Forms a sleep-shield and fires homing Shooting Stars whenever party members cast skills, maintaining 100% shield uptime. |
| **435** | 68 | Kaveh | Mehrak Artistic Bloom Driver | Main DPS | 183 | Earth Shaker | Forest Regalia | 41 | Deepwood Memories | Elemental Mastery | Elemental Mastery | Elemental Mastery | A | EM > ER > HP% > ATK%. Uses Mehrak to scan and instantly rupture all nearby Dendro Cores while converting core blast damage into self-healing. |
| **436** | 69 | Sethos | Shadowpiercing Electro Sniper | Main DPS | 117 | Hunter's Path | Hunter's Path | 20 | Wanderer's Troupe | Elemental Mastery | Electro DMG | CRIT Rate | S | EM > CRIT Rate > CRIT DMG > ER. Consumes burst energy to charge penetrating Shadowpiercing Shot arrows dealing devastating Electro damage. |
| **437** | 79 | Lynette | Bogglecat Swirl Distraction | Sub-DPS | 188 | Favonius Sword | Fleuve Cendre Ferryman | 24 | Viridescent Venerer | Energy Recharge | Anemo DMG | CRIT Rate | A | ER > CRIT Rate > CRIT DMG > ATK%. Summons Bogglecat Box to taunt opponents, swirl elements, and grant 20% team ATK buff based on party diversity. |
| **438** | 80 | Freminet | Pers Clockwork Shattering Diver | Main DPS | 180 | Tidal Shadow | Song of Broken Pines | 34 | Pale Flame | ATK% | Physical DMG | CRIT Rate | A | CRIT Rate > CRIT DMG > ATK% > ER. Coordinates with Pers clockwork penguin to build pressure levels and execute heavy Shatter physical cleaves. |
| **439** | 81 | Charlotte | Monsieur Verite Flash Healer | Healer | 171 | Prototype Amber | Prototype Amber | 21 | Noblesse Oblige | Energy Recharge | ATK% | Healing Bonus | S | ER > ATK% > Flat ATK > CRIT Rate. Snaps comprehensive photos with Monsieur Verite to instantly heal the entire party, making her premier Furina partner. |
| **440** | 90 | Ororon | Hypersense Nightsoul Electro Sub-DPS | Sub-DPS | 185 | Chain Breaker | Elegy for the End | 53 | Scroll of the Hero of Cinder City | ATK% | Electro DMG | CRIT Rate | S+ | CRIT Rate > CRIT DMG > ATK% > ER. Enters Nightsoul state to unleash Hypersense strikes triggered by teammates dealing Electro-Charged or Nightsoul damage. |
| **441** | 91 | Iansan | Collective of Plenty Thunder Smasher | Main DPS | 155 | Deathmatch | Mountain-Bracing Bolt | 54 | Obsidian Codex | ATK% | Electro DMG | CRIT Rate | S | CRIT Rate > CRIT DMG > ATK% > ER. Channels Natlan stamina and Nightsoul fury into explosive high-speed leaping strikes and Electro shocks. |
| **442** | 95 | Aino | Aurora Borealis Tidal Greatsword | Sub-DPS | 180 | Tidal Shadow | Serpent Spine | 36 | Emblem of Severed Fate | Energy Recharge | Hydro DMG | CRIT Rate | S | ER > CRIT Rate > CRIT DMG > ATK%. Sweeps massive Hydro tides to enable Vaporize and Freeze while generating elemental energy for high-cost carries. |
| **443** | 96 | Nefer | Verdant Oasis Astral Bloom | Main DPS | 105 | A Thousand Floating Dreams | A Thousand Floating Dreams | 57 | Night of the Sky's Unveiling | Elemental Mastery | Dendro DMG | CRIT DMG | SS | CRIT DMG > CRIT Rate > EM > ER. Weaves intricate Dendro constellations to blast opponents with piercing lunar vines and Bloom reactions. |
| **444** | 97 | Jahoda | Gale-Force Stellar Swirl Buffer | Support | 140 | Elegy for the End | Elegy for the End | 24 | Viridescent Venerer | Elemental Mastery | Elemental Mastery | Elemental Mastery | S | EM > ER > CRIT Rate. Unleashes swirling Anemo vortexes pulling lighter enemies while shredding 40% elemental resistances. |
| **445** | 98 | Illuga | Petrified Bastion Resonator | Support | 189 | Favonius Lance | Favonius Lance | 33 | Tenacity of the Millelith | DEF% | Geo DMG | DEF% | A | DEF% > ER > CRIT Rate > Flat DEF. Erects resonant crystalline pillars that amplify party Geo DMG and generate Crystallize shields. |
| **446** | 99 | Zibai | Jade Cleaver Mountain Splitter | Main DPS | 138 | Uraku Misugiri | Uraku Misugiri | 50 | Nighttime Whispers in the Echoing Woods | ATK% | Geo DMG | CRIT Rate | SS | CRIT Rate > CRIT DMG > ATK% > DEF%. Expert Liyue swordsman executing high-speed Geo infused slashes scaling with elemental skill resonances. |
| **447** | 100 | Linnea | Golden Horizon Crystal Archer | Sub-DPS | 109 | Aqua Simulacra | Aqua Simulacra | 48 | Golden Troupe | ATK% | Geo DMG | CRIT Rate | S+ | CRIT Rate > CRIT DMG > ATK% > ER. Deploys crystalline turrets firing off-field Geo arrows whenever active character strikes opponents. |
| **448** | 105 | Aloy | Coil Hunter Frozen Bombardment | Sub-DPS | 111 | Polar Star | Polar Star | 31 | Blizzard Strayer | ATK% | Cryo DMG | CRIT Rate | A | CRIT Rate > CRIT DMG > ATK% > ER. Throws Freeze Bombs scattering Chillwater Bomblets to gain Coil stacks and boost Cryo normal arrows. |
| **449** | 111 | Traveler (Electro) | Bellowing Thunder Energy Battery | Support | 188 | Favonius Sword | Favonius Sword | 36 | Emblem of Severed Fate | Energy Recharge | Electro DMG | CRIT Rate | A | ER > CRIT Rate > CRIT DMG > ATK%. Drops Abundance Amulets restoring flat energy and boosting ER up to 20% for active burst carries. |
| **450** | 113 | Traveler (Hydro) | Aquacrest Torrential Surge | Sub-DPS | 179 | Finale of the Deep | Fleuve Cendre Ferryman | 48 | Golden Troupe | HP% | Hydro DMG | CRIT Rate | A | ER > HP% > CRIT Rate > CRIT DMG. Fires Torrent Surge dewdrop bullets consuming and recovering HP via Sourcewater Droplets. |
| **451** | 115 | Ifa | Saurian Healer Wind Whisper | Healer | 171 | Prototype Amber | Prototype Amber | 53 | Scroll of the Hero of Cinder City | Energy Recharge | Elemental Mastery | Healing Bonus | S | ER > EM > HP% > CRIT Rate. Natlan saurian physician providing swirl group healing and Nightsoul party buffs. |
| **452** | 116 | Escoffier | Culinary Cryo Virtuoso | Sub-DPS | 107 | Staff of Homa | Staff of Homa | 48 | Golden Troupe | ATK% | Cryo DMG | CRIT Rate | S+ | CRIT Rate > CRIT DMG > ATK% > ER. Fontaine chef executing razor-sharp Cryo culinary techniques with off-field skill damage. |
| **453** | 117 | Dahlia | Favonius Deacon Baptizer | Support | 188 | Favonius Sword | Favonius Sword | 21 | Noblesse Oblige | Energy Recharge | HP% | HP% | A | ER > HP% > Flat HP > CRIT Rate. Mondstadt church deacon casting protective holy water barriers and recharging team energy. |
| **454** | 118 | Skirk | Abyssal Void Swordmaster | Main DPS | 108 | Mistsplitter Reforged | Azurelight | 47 | Marechaussee Hunter | ATK% | Cryo DMG | CRIT DMG | SS | CRIT DMG > CRIT Rate > ATK% > ER. Childe's enigmatic abyssal master tearing through dimensions with relentless rapid sword thrusts. |
| **455** | 119 | Wonderland Manekin | Miliastra Realm Stylist | Main DPS | 108 | Mistsplitter Reforged | Mistsplitter Reforged | 24 | Viridescent Venerer | ATK% | Anemo DMG | CRIT Rate | S | CRIT Rate > CRIT DMG > ATK% > EM. Customizable avatar seamlessly weaving weapon arts and whirlwind maneuvers across Teyvat. |
| **456** | 120 | Durin | Corrupted Dragon Pyre | Main DPS | 108 | Mistsplitter Reforged | Athame Artis | 30 | Crimson Witch of Flames | ATK% | Pyro DMG | CRIT Rate | SS | CRIT Rate > CRIT DMG > EM > ATK%. Dragonspine's reincarnated dragon channeling subterranean abyssal flame into sweeping sword arcs. |
| **457** | 121 | Varka | Knight of Boreas Tempest Cleave | Main DPS | 141 | Wolf's Gravestone | Wolf's Gravestone | 24 | Viridescent Venerer | ATK% | Anemo DMG | CRIT Rate | SS | CRIT Rate > CRIT DMG > ATK% > ER. Grand Master of Favonius delivering thunderous heavy greatsword tempests knocking back entire enemy waves. |
| **458** | 122 | Nicole | Hexenzirkel Fate Guide | Support | 105 | A Thousand Floating Dreams | A Thousand Floating Dreams | 21 | Noblesse Oblige | Energy Recharge | Pyro DMG | CRIT Rate | SS | ER > EM > CRIT Rate > ATK%. Hexenzirkel seer manifesting fiery fate prophecies to augment party elemental reactions. |
| **459** | 123 | Prune | Zephyr Gale Support | Sub-DPS | 194 | Sacrificial Fragments | Sacrificial Fragments | 24 | Viridescent Venerer | Elemental Mastery | Anemo DMG | Elemental Mastery | A | EM > ER > CRIT Rate. Channels northern breezes to group foes and amplify elemental swirl reactions. |
| **460** | 124 | Lohen | Will to Win Frost Lance | Main DPS | 107 | Staff of Homa | Staff of Homa | 59 | Aubade of Morningstar and Moon | ATK% | Cryo DMG | CRIT Rate | SS | CRIT Rate > CRIT DMG > ATK% > EM. Elite warrior converting unyielding combat determination into devastating forward Melt strikes. |
| **461** | 125 | Alyosha | Stellar-Conduct Battery Healer | Support | 189 | Favonius Lance | Favonius Lance | 21 | Noblesse Oblige | Energy Recharge | Electro DMG | CRIT Rate | S | ER > CRIT Rate > ATK% > EM. Off-field Electro enabler triggering Stellar-Conduct and feeding energy particles to party carries. |
| **462** | 126 | Odette | Swan Lake Stellar Frost | Sub-DPS | 108 | Mistsplitter Reforged | Mistsplitter Reforged | 59 | Aubade of Morningstar and Moon | ATK% | Cryo DMG | CRIT Rate | S+ | CRIT Rate > CRIT DMG > ATK% > ER. Glides across the battlefield unleashing crystalline swan strikes that boost party Stellar-Swirl and Conduct. |
| **463** | 127 | Vesna | Spring Breeze Whirlwind Driver | Main DPS | 106 | Freedom-Sworn | Freedom-Sworn | 60 | A Day Carved from Rising Winds | ATK% | Anemo DMG | CRIT Rate | SS | CRIT Rate > CRIT DMG > ATK% > EM. High-agility Anemo driver creating blooming spring gale vortices and driving Stellar-Swirl reactions. |
| **464** | 128 | Vodyanitsa | Korolevskiy Prima Donna Siren | Healer | 101 | Tome of the Eternal Flow | Everlasting Moonglow | 49 | Song of Days Past | HP% | Hydro DMG | Healing Bonus | SS | HP% > ER > Flat HP > EM. Prima donna water siren chanting melodic tides that continuously heal allies and buff team damage. |
| **465** | 129 | Mitya | Royal Energy Commission Catalyst | Main DPS | 113 | Kagura's Verity | Vivid Notions | 62 | Disenchantment in Deep Shadow | ATK% | Electro DMG | CRIT Rate | SS | CRIT Rate > CRIT DMG > ATK% > EM. Eccentric Snezhnayan researcher discharging volatile electric fields converting Superconduct into Stellar-Conduct. |
| **466** | 130 | Valeriy | Special Assignments Battalion Shield | Shielder | 188 | Favonius Sword | Favonius Sword | 33 | Tenacity of the Millelith | Energy Recharge | HP% | CRIT Rate | S | ER > HP% > CRIT Rate > Flat HP. Fatui Major deploying hardened Electro magnetic barriers to protect Mitya and absorb incoming impact. |
| **467** | 87 | Mavuika | Cinder City Nightsoul Support | Support | 131 | A Thousand Blazing Suns | A Thousand Blazing Suns | 53 | Scroll of the Hero of Cinder City | Energy Recharge | Pyro DMG | CRIT Rate | SS | ER > CRIT Rate > CRIT DMG > ATK%. Triggers Nightsoul Burst to grant 40% elemental damage bonus to all elements in the reaction party while providing off-field Pyro application. |
| **468** | 88 | Citlali | F2P Sacrificial Cryo Buffer | Support | 194 | Sacrificial Fragments | Sacrificial Fragments | 53 | Scroll of the Hero of Cinder City | Elemental Mastery | Elemental Mastery | Elemental Mastery | S | EM > ER > CRIT Rate. Budget F2P catalyst support utilizing Sacrificial Fragments for double skill deployment and teamwide Nightsoul elemental damage buffs. |
| **469** | 86 | Chasca | F2P Chain Breaker Soulsnatcher | Main DPS | 185 | Chain Breaker | Chain Breaker | 54 | Obsidian Codex | ATK% | Anemo DMG | CRIT Rate | S | CRIT Rate > CRIT DMG > ATK% > EM. F2P craftable build utilizing Natlan's Chain Breaker to maximize ATK and loaded elemental shell damage from the air. |

---

### 3.2 Build Re-linking Specifications

| Character | Build ID | Build Name | Current Weapon | Target BiS / Signature Weapon | Rationale & Instructions |
|---|---|---|---|---|---|
| **Furina** (71) | 305 | F2P Ferryman Buffer | `[188] Favonius Sword` | `Fleuve Cendre Ferryman` (from R3) | The build is named after the Fontaine pipe sword *Fleuve Cendre Ferryman*, but currently holds Favonius Sword because the Ferryman was missing from `weapons`. Once R3 ingests the Ferryman, update `recommended_weapon_id` to its new ID. |
| **Albedo** (6) | 387 | Solar Isotoma Transient Blossom | `[182] Flute of Ezpitzal` | `Cinnabar Spindle` (from R3) | Albedo is currently linked to the Natlan craftable *Flute of Ezpitzal*. His canonical signature BiS weapon is the event sword *Cinnabar Spindle*. Once R3 ingests *Cinnabar Spindle*, update `recommended_weapon_id` to its new ID. |
| **Shenhe** (27) | 392 | Icy Quill Cryo Buffer | `[135] Primordial Jade Winged-Spear` | `Calamity Queller` (from R3) | Shenhe is currently linked to Xiao's weapon (PJWS). Her 5★ signature weapon is *Calamity Queller*. Once R3 ingests *Calamity Queller*, update `recommended_weapon_id` to its new ID. |

---

## 4. R5 Data Synchronization Specification

### 4.1 Root Generator Synchronization Flow
To prevent accidental regression or data drift, changes must follow the strict pipeline order:
1. **Update `generate_csvs.py`**:
   - `CHARACTERS`: Remove Capitano (104). Append 16 new characters (115–130). Apply R1 attribute corrections (Arlecchino, Zibai, Columbina, Sandrone, Iansan, Aloy).
   - `WEAPONS`: Append 24 missing signatures, 19 craftables, and meta staples. Correct weapons 128 and 131 stats (741 ATK, 11.0% CRIT Rate).
   - `ARTIFACT_SETS`: Correct Sets 59, 60, 62, 63, 64 domain, region, and text descriptions.
   - `BUILDS`: Remove build 381 (Capitano). Append the 62 new builds (408–469). Re-link builds 305, 387, 392.
2. **Execute CSV Regeneration**:
   - Run `python3 generate_csvs.py` to overwrite `data/characters.csv`, `data/weapons.csv`, `data/artifact_sets.csv`, and `data/character_builds.csv`.
3. **Rebuild Database**:
   - Run `python3 init_db.py` to drop, recreate schema, and reload all 4 CSVs with `PRAGMA foreign_keys = ON;`.

### 4.2 Required Schema Enhancements in `init_db.py`
In `init_db.py`, add missing indexes on foreign key columns in `SCHEMA_SQL` to optimize JOIN performance and align with educational query goals:
```sql
CREATE INDEX idx_builds_weapon ON character_builds(recommended_weapon_id);
CREATE INDEX idx_builds_artifact ON character_builds(recommended_artifact_id);
CREATE INDEX idx_weapons_signature ON weapons(signature_character_id);
```

---

## 5. R5 Automated Verification Suite (`verify_db.py`) Upgrades

The current `verify_db.py` asserts obsolete constants (114 characters, 103 weapons, 107 builds). It must be overhauled with the following comprehensive test assertions:

### 5.1 Updated Target Counts Assertions
```python
expected_tables = {
    "characters": 129,       # 114 - 1 (Capitano) + 16 new
    "weapons": 150+,         # 103 + 24 sigs + 19 craftables + staples
    "artifact_sets": 64,     # Exact 64 sets
    "character_builds": 168   # 107 - 1 (Capitano) + 62 new
}
```

### 5.2 Mandatory Relational and Data Integrity Assertions

1. **Zero Foreign Key Violations**:
   ```python
   violations = cursor.execute("PRAGMA foreign_key_check;").fetchall()
   assert len(violations) == 0, f"Foreign key violations found: {violations}"
   ```

2. **100% Playable Character Coverage (Zero Orphaned Characters)**:
   ```python
   orphans = cursor.execute("""
       SELECT c.character_id, c.name 
       FROM characters c 
       LEFT JOIN character_builds cb ON c.character_id = cb.character_id 
       WHERE cb.build_id IS NULL;
   """).fetchall()
   assert len(orphans) == 0, f"Characters missing builds: {orphans}"
   ```

3. **Capitano Absolute Purge Assertion**:
   ```python
   cap_char = cursor.execute("SELECT COUNT(*) FROM characters WHERE name = 'Capitano';").fetchone()[0]
   cap_build = cursor.execute("SELECT COUNT(*) FROM character_builds WHERE character_id = 104;").fetchone()[0]
   assert cap_char == 0 and cap_build == 0, "Capitano was not completely purged"
   ```

4. **Weapon-Character Type Compatibility Assertion**:
   ```python
   mismatches = cursor.execute("""
       SELECT cb.build_id, c.name, c.weapon_type, w.name, w.weapon_type
       FROM character_builds cb
       JOIN characters c ON cb.character_id = c.character_id
       JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id
       WHERE c.weapon_type != w.weapon_type;
   """).fetchall()
   assert len(mismatches) == 0, f"Weapon type mismatches found: {mismatches}"
   ```

5. **Weapon Attribute Fix Assertions**:
   ```python
   fmk = cursor.execute("SELECT base_atk, sub_stat_value FROM weapons WHERE weapon_id = 128;").fetchone()
   atbs = cursor.execute("SELECT base_atk, sub_stat_value FROM weapons WHERE weapon_id = 131;").fetchone()
   assert fmk == (741, 11.0), f"Fang of Mountain King stats incorrect: {fmk}"
   assert atbs == (741, 11.0), f"A Thousand Blazing Suns stats incorrect: {atbs}"
   ```

6. **Key Character Alternative Meta Roles Assertions**:
   ```python
   # Mavuika Support
   mav_supp = cursor.execute("""
       SELECT COUNT(*) FROM character_builds 
       WHERE character_id = 87 AND recommended_artifact_id = 53 AND role IN ('Support', 'Sub-DPS');
   """).fetchone()[0]
   assert mav_supp >= 1, "Missing Mavuika 4pc Cinder City Support build"

   # Citlali F2P
   cit_f2p = cursor.execute("""
       SELECT COUNT(*) FROM character_builds 
       WHERE character_id = 88 AND build_name LIKE '%F2P%';
   """).fetchone()[0]
   assert cit_f2p >= 1, "Missing Citlali F2P build"

   # Chasca F2P
   cha_f2p = cursor.execute("""
       SELECT COUNT(*) FROM character_builds 
       WHERE character_id = 86 AND build_name LIKE '%F2P%';
   """).fetchone()[0]
   assert cha_f2p >= 1, "Missing Chasca F2P build"
   ```

7. **CSV-to-Database 1:1 Parity Assertion**:
   ```python
   for table in ["characters", "weapons", "artifact_sets", "character_builds"]:
       db_count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
       csv_path = os.path.join(DATA_DIR, f"{table}.csv")
       with open(csv_path, "r", encoding="utf-8") as f:
           csv_count = sum(1 for _ in csv.reader(f)) - 1
       assert db_count == csv_count, f"Parity mismatch in {table}: DB {db_count} vs CSV {csv_count}"
   ```

---

## 6. Caveats

1. **R2 / R3 Execution Ordering**:
   - The primary weapon IDs formulated in Section 3.1 use existing weapons (IDs 101–203) to ensure that if R4 builds are imported into the database before R3 weapons are loaded, zero foreign key errors occur.
   - Once R3 adds new weapons, the implementation agent should update the `recommended_weapon_id` values according to the "Target R3 Weapon" column and Section 3.2.
2. **Surrogate Key Numbering for New Characters**:
   - Character IDs 115 to 130 have been assigned sequentially to the 16 new characters. If R2 adopts a different numbering convention, the `character_id` values in builds 451 to 466 must be updated in lockstep.
3. **Environment Execution**:
   - Tests requiring Flask (`test_security_oom.py`) must be executed using the local virtualenv Python interpreter (`./.venv/bin/python`).

---

## 7. Conclusion

- **R4 Readiness**: All 43 existing missing character builds, all 16 new character builds from R2, and 3 key alternative meta role builds (62 builds total) are completely specified with valid weapons, artifacts, stat distributions, and playstyle notes.
- **Relational Integrity**: 100% of weapon recommendations match the character's weapon type, and all foreign keys resolve cleanly.
- **R5 Synchronization Protocol**: The single source of truth (`generate_csvs.py`) and verification suite (`verify_db.py`) specifications guarantee 100% data reproducibility and complete automated integrity checking.

---

## 8. Verification Method

To independently verify the database state and validate the survey's findings:

1. **Verify Count of Characters Lacking Builds (Currently 43)**:
   ```bash
   python3 -c "
   import sqlite3
   conn = sqlite3.connect('genshin_learning.db')
   cur = conn.cursor()
   cnt = cur.execute('SELECT COUNT(*) FROM characters c LEFT JOIN character_builds cb ON c.character_id = cb.character_id WHERE cb.build_id IS NULL;').fetchone()[0]
   print('Characters lacking builds:', cnt)
   "
   ```
   *Expected Output*: `Characters lacking builds: 43`.

2. **Verify Capitano and Build 381**:
   ```bash
   python3 -c "
   import sqlite3
   conn = sqlite3.connect('genshin_learning.db')
   cur = conn.cursor()
   print('Capitano character:', cur.execute('SELECT character_id, name FROM characters WHERE character_id = 104;').fetchall())
   print('Capitano build:', cur.execute('SELECT build_id, character_id, build_name FROM character_builds WHERE character_id = 104;').fetchall())
   "
   ```
   *Expected Output*: Character 104 and Build 381 exist.

3. **Verify Existing Build Links for Furina, Albedo, Shenhe**:
   ```bash
   python3 -c "
   import sqlite3
   conn = sqlite3.connect('genshin_learning.db')
   cur = conn.cursor()
   for name in ['Furina', 'Albedo', 'Shenhe']:
       print(cur.execute('SELECT cb.build_id, c.name, cb.build_name, w.name FROM character_builds cb JOIN characters c ON cb.character_id = c.character_id JOIN weapons w ON cb.recommended_weapon_id = w.weapon_id WHERE c.name = ?;', (name,)).fetchall())
   "
   ```
   *Expected Output*: Furina build 305 links to Favonius Sword, Albedo build 387 links to Flute of Ezpitzal, Shenhe build 392 links to PJWS.

4. **Verify Current Verification Suite Runs Cleanly**:
   ```bash
   ./.venv/bin/python verify_db.py
   ```
   *Expected Output*: `ALL EXPANDED DATABASE TESTS PASSED SUCCESSFULLY!`.
