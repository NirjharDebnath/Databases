# Scope: E2E Testing Track (M_E2E)

## Architecture
- Opaque-box requirement-driven testing track operating independently of implementation details.
- Validates database state, SQLite schema, foreign keys, CSVs, and API responses against user requirements.

## Feature Inventory Coverage
- F1: Artifact sets 59/60/62/63/64 verified
- F2: Weapons 128 & 131 stats (741 ATK, 11.0% CRIT Rate) verified
- F3: Character attributes (Arlecchino, Zibai, Columbina, Sandrone, Iansan, Aloy) verified
- F4: Capitano (104) and Build 381 purged completely
- F5: 16 missing playable characters present with valid base stats & attributes
- F6: 24 missing 5★ signature weapons present with valid stats & signature FKs
- F7: 19 missing craftables present across all regions
- F8: 9 meta staples & event weapons present
- F9: 43 missing character builds backfilled (0 orphaned characters)
- F10: 16 new character builds backfilled
- F11: Alternative meta roles present (Mavuika Cinder City support, Citlali F2P, Chasca F2P)
- F12: Build re-linking verified (Furina, Albedo, Shenhe)
- F13: Data synchronization & CSV-DB 1:1 parity verified
- F14: `verify_db.py` integrity verified

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| E2E-1 | Test Infra & Harness | Design runner and test framework, publish TEST_INFRA.md | none | IN_PROGRESS |
| E2E-2 | Tier 1 & Tier 2 Tests | Implement Feature Coverage & Boundary/Corner Tests | E2E-1 | PLANNED |
| E2E-3 | Tier 3 & Tier 4 Tests | Implement Cross-Feature & Real-World Application Tests | E2E-2 | PLANNED |
| E2E-4 | Publish TEST_READY.md | Validate runner, generate summary report | E2E-3 | PLANNED |
