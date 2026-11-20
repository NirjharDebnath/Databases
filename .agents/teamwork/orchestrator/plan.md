# Master Execution Plan

## 1. Overview
The goal is to fix all database defects, ingest missing characters and weapons, backfill missing character builds and role variants, synchronize CSVs and generator scripts, and achieve 100% green verification in `verify_db.py` without foreign key or integrity violations.

## 2. Phase 0: Survey (3 Parallel Explorers)
- **Explorer 1**: Explore codebase structure, SQLite database (`genshin_learning.db`), table schemas, `init_db.py`, `generate_csvs.py`, `verify_db.py`, and `data/*.csv`.
- **Explorer 2**: Detail R1 & R2 & R3 specs: exact artifact set values (59, 60, 62, 63, 64), weapon stats (128, 131), character attribute corrections (Arlecchino, Zibai, Columbina, Sandrone, Iansan, Aloy), Capitano (104) removal, list of 16 missing characters and 24 signature + 19 craftables + staples.
- **Explorer 3**: Detail R4 & R5 specs: 43 missing character builds, Mavuika/Citlali/Chasca alt roles, Furina/Albedo/Shenhe relinking, and verification checks.

## 3. Phase 1: Synthesis & Decomposition (`PROJECT.md`)
- Aggregate Explorer findings into `PROJECT.md § Feature Inventory`.
- Define Milestones:
  - M_E2E: E2E Test Suite Track (Tiers 1-4, `TEST_READY.md`)
  - M1: R1 Defect Remediation & Schema Cleanup
  - M2: R2 Characters Ingestion
  - M3: R3 Weapons Catalog Expansion
  - M4: R4 Character Builds Backfill & Role Variety
  - M5: R5 Data Synchronization (`generate_csvs.py`, `init_db.py`, CSV regeneration)
  - M_FINAL: E2E Verification & Adversarial Hardening (Tier 5)

## 4. Phase 2: Parallel Tracks Execution
- Dispatch E2E Testing Orchestrator.
- Dispatch Implementation Sub-Orchestrators according to milestone dependencies.
- Enforce strict iteration loops (Explorer -> Worker -> Reviewer -> Challenger -> Auditor) with binary auditor veto.

## 5. Phase 3: Final Acceptance & Reporting
- 100% E2E test pass across all tiers.
- 0 foreign key violations, 0 orphaned records, verified CSV-DB synchronization.
- Full verification handoff to parent.
