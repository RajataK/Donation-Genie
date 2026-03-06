# Tasks: Expand Seed Fixtures

**Input**: Design documents from `/specs/005-expand-seed-fixtures/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Included — constitution mandates TDD (Red-Green-Refactor).

**Organization**: Tasks grouped by user story. Since the deliverable is a single file (`backend/fixtures/seed.json`), US1 and US2 are sequential (US2 adds wishlist items referencing US1's food banks). US3 adds related table records referencing both.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Test infrastructure for fixture validation

- [x] T001 Create fixture validation test file with helper utilities (load JSON, extract records by model, collect UUIDs, collect FK references) in `backend/tests/core/test_seed_fixtures.py`

**Checkpoint**: Test infrastructure ready — story-specific test cases can now be added.

---

## Phase 2: User Story 1 - Developer Seeds Database with Realistic UK-Wide Data (Priority: P1) 🎯 MVP

**Goal**: 40 food banks with realistic UK-wide geographic distribution

**Independent Test**: Load fixture and verify 40 food banks exist with valid UK coordinates spanning all four nations

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T002 [US1] Write test: exactly 40 `foodbanks.foodbank` records exist in `backend/fixtures/seed.json` — in `backend/tests/core/test_seed_fixtures.py`
- [x] T003 [P] [US1] Write test: all food bank UUIDs are unique — in `backend/tests/core/test_seed_fixtures.py`
- [x] T004 [P] [US1] Write test: all food bank latitudes are within UK bounds (49.9–60.8) and longitudes within (-8.2–1.8) — in `backend/tests/core/test_seed_fixtures.py`
- [x] T005 [P] [US1] Write test: food banks cover at least 10 distinct UK cities/regions (check address fields contain expected city names from England, Scotland, Wales, Northern Ireland) — in `backend/tests/core/test_seed_fixtures.py`
- [x] T006 [P] [US1] Write test: all `urgency_level` values are valid choices (urgent, active, normal) — in `backend/tests/core/test_seed_fixtures.py`
- [x] T007 [P] [US1] Write test: all `families_served_weekly` values are between 20 and 500 — in `backend/tests/core/test_seed_fixtures.py`
- [x] T008 [P] [US1] Write test: all food bank names are unique — in `backend/tests/core/test_seed_fixtures.py`

### Implementation for User Story 1

- [x] T009 [US1] Add 40 food bank records to `backend/fixtures/seed.json` with realistic names, addresses, postcodes, and coordinates distributed across UK (London ×5, Manchester ×2, Birmingham ×2, Edinburgh ×2, Glasgow ×2, Cardiff ×2, Belfast ×2, Leeds, Liverpool, Bristol, Sheffield, Newcastle, Nottingham, Leicester, Southampton, Brighton, Oxford, Cambridge, Plymouth, Norwich, York, Bath, Exeter, Coventry, Reading, Aberdeen, Swansea, Bangor, Derry/Londonderry) — replace the existing single food bank record
- [x] T010 [US1] Run tests T002–T008 and verify all pass — in `backend/tests/core/test_seed_fixtures.py`

**Checkpoint**: 40 food banks with UK-wide coverage. Fixture loads successfully with `python manage.py loaddata seed`.

---

## Phase 3: User Story 2 - Developer Has Diverse Wishlist Items for Testing (Priority: P1)

**Goal**: 120+ wishlist items across all 6 categories and 3 urgency levels with diverse product names

**Independent Test**: Load fixture and verify wishlist items span all categories and urgency levels with 30+ distinct product names

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T011 [US2] Write test: at least 120 `foodbanks.wishlistitem` records exist — in `backend/tests/core/test_seed_fixtures.py`
- [x] T012 [P] [US2] Write test: all wishlist item UUIDs are unique — in `backend/tests/core/test_seed_fixtures.py`
- [x] T013 [P] [US2] Write test: all 6 categories are represented (tinned_goods, dried_goods, fresh, dairy, baby, hygiene) — in `backend/tests/core/test_seed_fixtures.py`
- [x] T014 [P] [US2] Write test: all 3 urgency levels are represented (urgent, needed, optional) — in `backend/tests/core/test_seed_fixtures.py`
- [x] T015 [P] [US2] Write test: at least 30 distinct `item_name` values exist — in `backend/tests/core/test_seed_fixtures.py`
- [x] T016 [P] [US2] Write test: all `food_bank` FK references point to existing food bank UUIDs in the fixture — in `backend/tests/core/test_seed_fixtures.py`

### Implementation for User Story 2

- [x] T017 [US2] Add 120+ wishlist item records to `backend/fixtures/seed.json` — distribute 3–5 items per food bank, using diverse product names across all categories (tinned: baked beans, tinned tomatoes, tinned soup, tinned tuna, tinned sweetcorn, tinned fruit, tinned spaghetti, tinned chickpeas; dried: rice, pasta, cereal, porridge oats, flour, couscous, lentils, instant noodles; fresh: potatoes, onions, carrots, apples, bananas, bread, eggs; dairy: UHT milk, long-life juice, powdered milk, cheese spread; baby: baby formula, nappies size 3, nappies size 5, baby wipes, baby food pouches; hygiene: toothpaste, shampoo, soap, deodorant, washing-up liquid, laundry detergent, toilet roll, sanitary products) — replace existing wishlist items
- [x] T018 [US2] Run tests T011–T016 and verify all pass — in `backend/tests/core/test_seed_fixtures.py`

**Checkpoint**: 40 food banks + 120+ diverse wishlist items. Core seed data complete.

---

## Phase 4: User Story 3 - Developer Has Populated Related Tables for End-to-End Testing (Priority: P2)

**Goal**: Populated related tables (recipes, donations, delivery tracking, settings, supermarket preferences, QR scans) linked to food banks

**Independent Test**: Load fixture and verify all related tables have records with valid FK references

### Tests for User Story 3 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T019 [US3] Write test: at least 12 `foodbanks.generatedrecipe` records exist with valid `food_bank` FKs and non-empty `ingredients` JSON arrays — in `backend/tests/core/test_seed_fixtures.py`
- [x] T020 [P] [US3] Write test: at least 18 `donations.donation` records exist with valid `food_bank` FKs, valid `donation_type` values, and recipe_kit donations have valid `recipe` FKs — in `backend/tests/core/test_seed_fixtures.py`
- [x] T021 [P] [US3] Write test: at least 12 `donations.deliverytracking` records exist with valid `donation` FKs, valid `status` values, and received-status records have `received_confirmed=true` — in `backend/tests/core/test_seed_fixtures.py`
- [x] T022 [P] [US3] Write test: at least 25 `foodbanks.foodbanksettings` records exist with valid `food_bank` FKs and no duplicate food_bank references (one-to-one) — in `backend/tests/core/test_seed_fixtures.py`
- [x] T023 [P] [US3] Write test: at least 40 `foodbanks.foodbanksupermarketpreference` records exist with valid `food_bank` FKs, valid `supermarket` values (tesco, sainsburys, asda, waitrose), and no duplicate (food_bank, supermarket) pairs — in `backend/tests/core/test_seed_fixtures.py`
- [x] T024 [P] [US3] Write test: at least 15 `foodbanks.qrscan` records exist with valid `food_bank` FKs, valid `source` values (qr_poster, qr_sticker, qr_social), and converted scans have valid `donation` FKs — in `backend/tests/core/test_seed_fixtures.py`

### Implementation for User Story 3

- [x] T025 [US3] Add 12 generated recipe records to `backend/fixtures/seed.json` — spread across 8 food banks, with realistic recipe names, ingredient lists (matching wishlist items where possible), cook times (10–60 min), serves (2–6), costs (£2–8), and food emojis — replace existing recipe record
- [x] T026 [US3] Add 25 food bank settings records to `backend/fixtures/seed.json` — varied configurations of pepesto_enabled, accept_direct_delivery, allow_donor_collection, and delivery_notes — replace existing settings record
- [x] T027 [P] [US3] Add 40 supermarket preference records to `backend/fixtures/seed.json` — distribute across food banks with settings, covering all 4 supermarkets (tesco, sainsburys, asda, waitrose), delivery_time_days 1–5 — replace existing preference record
- [x] T028 [US3] Add 18 donation records to `backend/fixtures/seed.json` — mix of recipe_kit (linking to recipe UUIDs) and individual_items types, varied total_cost and donor postcodes, mix of completed true/false — replace existing donation record
- [x] T029 [US3] Add 12 delivery tracking records to `backend/fixtures/seed.json` — linked to donations, mix of all 4 statuses (pending, dispatched, delivered, received), with appropriate tracking numbers, estimated/actual delivery dates, and received_confirmed flags — replace existing delivery tracking record
- [x] T030 [US3] Add 15 QR scan records to `backend/fixtures/seed.json` — spread across 10 food banks, mix of all 3 sources (qr_poster, qr_sticker, qr_social), ~40% converted_to_donation with valid donation FKs — replace existing QR scan record
- [x] T031 [US3] Run tests T019–T024 and verify all pass — in `backend/tests/core/test_seed_fixtures.py`

**Checkpoint**: All tables populated with realistic data. Full end-to-end seed data complete.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation across all user stories

- [x] T032 Write cross-cutting test: all UUIDs across entire fixture are globally unique (no pk reused across models) — in `backend/tests/core/test_seed_fixtures.py`
- [x] T033 Write cross-cutting test: all FK references across entire fixture are internally consistent (every referenced UUID exists as a pk somewhere) — in `backend/tests/core/test_seed_fixtures.py`
- [x] T034 Run full test suite `pytest backend/tests/core/test_seed_fixtures.py -v` and verify all tests pass
- [x] T035 Verify fixture loads successfully: `cd backend && python manage.py loaddata seed` against a clean database
- [x] T036 Run `ruff check backend/tests/core/test_seed_fixtures.py` and fix any lint issues

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — T001 starts immediately
- **US1 (Phase 2)**: Depends on T001 (test infrastructure)
- **US2 (Phase 3)**: Depends on US1 completion (wishlist items FK to food banks)
- **US3 (Phase 4)**: Depends on US1 + US2 completion (related tables FK to food banks, recipes reference wishlist items)
- **Polish (Phase 5)**: Depends on all user stories complete

### Within Each User Story

1. Tests written FIRST and verified to FAIL (Red)
2. Implementation written to make tests PASS (Green)
3. Verification run confirms all pass

### Parallel Opportunities

Within US1 tests: T003–T008 can run in parallel (all read-only checks on food bank records)
Within US2 tests: T012–T016 can run in parallel
Within US3 tests: T020–T024 can run in parallel
Within US3 implementation: T026 and T027 can run in parallel (settings and supermarket prefs are independent)

---

## Parallel Example: User Story 1

```bash
# Launch all US1 tests together (they all read the same fixture file):
Task: T003 "test: all food bank UUIDs are unique"
Task: T004 "test: UK coordinate bounds"
Task: T005 "test: geographic coverage"
Task: T006 "test: valid urgency_level values"
Task: T007 "test: families_served_weekly range"
Task: T008 "test: unique food bank names"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Test infrastructure (T001)
2. Complete Phase 2: US1 — 40 food banks (T002–T010)
3. **STOP and VALIDATE**: `python manage.py loaddata seed` loads 40 food banks
4. Fixture is usable for map and location testing

### Incremental Delivery

1. T001 → Test infrastructure ready
2. T002–T010 → 40 food banks with UK-wide coverage (MVP)
3. T011–T018 → 120+ diverse wishlist items added
4. T019–T031 → All related tables populated
5. T032–T036 → Final validation and lint clean

---

## Notes

- All tasks modify the same fixture file (`backend/fixtures/seed.json`) and test file (`backend/tests/core/test_seed_fixtures.py`)
- Tests validate the static JSON fixture data — no database required for test execution
- UUIDs must be hardcoded (not generated) to ensure idempotent fixture loading
- Commit after each phase checkpoint for clean TDD history
