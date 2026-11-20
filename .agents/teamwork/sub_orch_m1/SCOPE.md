# Scope: Milestone 1 (M1) — Database Defect Remediation

## Architecture & Code Boundaries
- **Owned Source Files**: `generate_csvs.py`, `data/*.csv`, `genshin_learning.db`
- **Execution Script**: `python3 generate_csvs.py` then `python3 init_db.py`

## Feature Inventory Assignment
- F1: Artifact sets 59/60/62/63/64 remediation
- F2: Weapon stats 128 & 131 correction (741 ATK, 11.0% CRIT Rate)
- F3: Character attributes correction (Arlecchino, Zibai, Columbina, Sandrone, Iansan, Aloy)
- F4: Capitano (104) and Build 381 absolute purge

## Iteration Loop Plan
- Explorer: Confirm exact code diffs in `generate_csvs.py` and downstream impact
- Worker: Implement edits in `generate_csvs.py`, run `generate_csvs.py` and `init_db.py`
- Reviewer: Verify diffs, schema validity, and FK integrity
- Challenger: Test edge cases and data correctness
- Forensic Auditor: Verify authentic execution and 0 integrity violations
- Gate: Approve M1 and update project status
