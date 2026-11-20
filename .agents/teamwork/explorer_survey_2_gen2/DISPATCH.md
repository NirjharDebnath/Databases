## 2026-11-20T16:37:58Z
You are explorer_survey_2_gen2, an exploration agent replacing a predecessor that timed out.
Working directory: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_2_gen2
Project root: /home/nirjhar/Python Codes/Einstein/Databases
Mandatory reference: /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/ORIGINAL_REQUEST.md
Supporting context:
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_1/handoff.md
- /home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_3/handoff.md

Task:
Produce the definitive, concrete data specification catalog for R1, R2, and R3:
1. R1 Defect Remediation:
   - Provide exact target text for Artifact sets 59, 60, 62, 63, 64 (name, domain_name, region, two_piece_bonus, four_piece_bonus). Ensure official casing and descriptions.
   - Confirm weapon IDs 128 (Fang of the Mountain King) and 131 (A Thousand Blazing Suns): base_atk = 741, sub_stat_type = 'CRIT Rate', sub_stat_value = 11.0.
   - Character attributes for Arlecchino (region: Snezhnaya), Zibai (region: Liyue), Columbina (region: Nod-Krai), Sandrone (vision: Cryo, weapon_type: Claymore), Iansan (release_patch: 5.5), Aloy (region: None).
   - Capitano (character_id: 104) removal details (and associated build 381).
2. R2 Missing Characters Ingestion (16 characters):
   - Characters: Ifa, Escoffier, Dahlia, Skirk, Wonderland Manekin, Durin, Varka, Nicole, Prune, Lohen, Alyosha, Odette, Vesna, Vodyanitsa, Mitya, Valeriy.
   - Number them sequentially starting at ID 115 through 130.
   - For every character, provide the complete tuple matching characters table schema:
     (character_id, name, rarity, vision, weapon_type, region, default_role, base_hp, base_atk, base_def, talent_priority, release_patch).
3. R3 Weapons Catalog Expansion:
   - 24 missing 5-star signatures (Calamity Queller, Everlasting Moonglow, Sunny Morning Sleep-In, Vivid Notions, Azurelight, etc.).
   - 19 missing craftables across Dragonspine, Sumeru, Fontaine, and Post-Natlan.
   - Key meta staples (Fleuve Cendre Ferryman, The Stringless, Cinnabar Spindle, and Natlan event/gacha series).
   - Number them sequentially starting at ID 204.
   - For every weapon, provide the complete tuple matching weapons table schema:
     (weapon_id, name, weapon_type, rarity, base_atk, sub_stat_type, sub_stat_value, is_craftable, signature_character_id).
   - Ensure signature_character_id correctly links to the owner character's ID (or NULL if non-signature).

Constraints:
- You are read-only. DO NOT modify any code, database, or CSV files.
- Periodically update progress.md in your working directory with `Last visited: [timestamp]`.
- Write your comprehensive, structured report to `/home/nirjhar/Python Codes/Einstein/Databases/.agents/teamwork/explorer_survey_2_gen2/handoff.md`.
- When finished, send a completion message to parent with summary and path to handoff.md.
