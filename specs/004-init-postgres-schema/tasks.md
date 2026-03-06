# Tasks: Initialize PostgreSQL Schema (Updated)

**Input**: Design documents from `/specs/004-init-postgres-schema/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Included per constitution (TDD Red-Green-Refactor required).

**Organization**: Tasks grouped by user story. Existing models and migrations are replaced with the new schema.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Clean up existing schema, update shared infrastructure, register new app

- [x] T001 Remove existing foodbanks migrations in backend/apps/foodbanks/migrations/ (keep __init__.py)
- [x] T002 Remove existing donations migrations in backend/apps/donations/migrations/ (keep __init__.py)
- [x] T003 Remove existing foodbanks model tests in backend/tests/foodbanks/test_models.py
- [x] T004 Remove existing donations model tests in backend/tests/donations/test_models.py
- [x] T005 Update TimestampMixin in backend/apps/core/models.py to provide only `created_at` (remove `updated_at` — models add it explicitly where needed)
- [x] T006 Create accounts app: backend/apps/accounts/__init__.py, backend/apps/accounts/apps.py (AccountsConfig, name="apps.accounts")
- [x] T007 Create empty backend/apps/accounts/models.py with placeholder comment
- [x] T008 Create backend/apps/accounts/migrations/__init__.py
- [x] T009 Add "apps.accounts" to INSTALLED_APPS and set AUTH_USER_MODEL = "accounts.FoodBankAdmin" in backend/config/settings/base.py
- [x] T010 Create backend/tests/accounts/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: FoodBank model must exist before any other entity can reference it

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T011 Write FoodBank model tests (CRUD, urgency_level enum, UUID PK, field validations, __str__) in backend/tests/foodbanks/test_models.py — tests MUST FAIL
- [x] T012 Rewrite FoodBank model in backend/apps/foodbanks/models.py with UUID PK, fields: name, postcode, latitude, longitude, address, families_served_weekly, urgency_level (urgent/active/normal), last_updated (auto_now), created_at (auto_now_add)
- [x] T013 Generate and apply FoodBank migration via `python manage.py makemigrations foodbanks`
- [x] T014 Run FoodBank tests to verify they pass

**Checkpoint**: FoodBank model exists — user story implementation can begin

---

## Phase 3: User Story 1 — Store and Retrieve Food Bank Information (Priority: P1)

**Goal**: Food bank records can be created, retrieved, filtered by urgency, and updated

**Independent Test**: Create a food bank, retrieve it, verify all fields. Filter by urgency_level. Update families_served_weekly.

> Note: FoodBank model was created in Phase 2 (foundational). This phase verifies the full story acceptance criteria are covered by the tests written in T011.

- [x] T015 [US1] Verify FoodBank tests cover all US1 acceptance scenarios (filter by urgency_level, update fields) in backend/tests/foodbanks/test_models.py — add any missing test cases

**Checkpoint**: User Story 1 fully functional and tested

---

## Phase 4: User Story 2 — Manage Wish List Items for a Food Bank (Priority: P1)

**Goal**: Wish list items can be created, associated with food banks, filtered, updated, and cascade-deleted

**Independent Test**: Create a food bank, add wish list items with category enum and urgency enum, verify association. Delete food bank and confirm items are removed.

### Tests for User Story 2

- [x] T016 [US2] Write WishListItem model tests (CRUD, category enum, urgency enum, UUID PK, FK to FoodBank, cascade delete, quantity_needed, unit, notes) in backend/tests/foodbanks/test_models.py — tests MUST FAIL

### Implementation for User Story 2

- [x] T017 [US2] Implement WishListItem model in backend/apps/foodbanks/models.py with UUID PK, fields: food_bank (FK CASCADE), item_name, category (tinned_goods/dried_goods/fresh/dairy/baby/hygiene), urgency (urgent/needed/optional), quantity_needed, unit, notes (blank), created_at
- [x] T018 [US2] Generate WishListItem migration via `python manage.py makemigrations foodbanks`
- [x] T019 [US2] Run WishListItem tests to verify they pass

**Checkpoint**: User Stories 1 and 2 independently functional

---

## Phase 5: User Story 3 — Record Donations and Track Delivery (Priority: P2)

**Goal**: Donations can be recorded with JSON items, linked to food banks and optional recipes. Delivery tracking records fulfilment status.

**Independent Test**: Create a food bank, record a donation with JSON items, verify fields. Create delivery tracking record, verify status transitions.

### Tests for User Story 3

- [x] T020 [P] [US3] Write Donation model tests (CRUD, donation_type enum, UUID PK, FK to FoodBank CASCADE, JSON items, total_cost, postcode, completed flag, recipe FK SET_NULL) in backend/tests/donations/test_models.py — tests MUST FAIL
- [x] T021 [P] [US3] Write DeliveryTracking model tests (CRUD, status enum, FK to Donation CASCADE, tracking_number, estimated/actual delivery, received_confirmed, notes) in backend/tests/donations/test_models.py — tests MUST FAIL

### Implementation for User Story 3

- [x] T022 [US3] Implement Donation model in backend/apps/donations/models.py with UUID PK, fields: food_bank (FK CASCADE), donation_type (recipe_kit/individual_items), recipe (FK GeneratedRecipe SET_NULL null blank), items (JSONField), total_cost, postcode, completed (default False), created_at
- [x] T023 [US3] Implement DeliveryTracking model in backend/apps/donations/models.py with UUID PK, fields: donation (FK CASCADE), supermarket, status (pending/dispatched/delivered/received), tracking_number (blank), estimated_delivery (null blank), actual_delivery (null blank), received_confirmed (default False), notes (blank), created_at, updated_at (auto_now)
- [x] T024 [US3] Generate donations migrations via `python manage.py makemigrations donations`
- [x] T025 [US3] Run Donation and DeliveryTracking tests to verify they pass

**Checkpoint**: Donation recording and delivery tracking functional

---

## Phase 6: User Story 4 — Store AI-Generated Recipes (Priority: P2)

**Goal**: AI-generated recipes can be stored with JSON ingredients, linked to food banks, with cache expiry

**Independent Test**: Create a food bank, store a generated recipe with JSON ingredients, verify all fields including generated_at and expires_at. Delete food bank and confirm recipe is removed.

### Tests for User Story 4

- [x] T026 [US4] Write GeneratedRecipe model tests (CRUD, UUID PK, FK to FoodBank CASCADE, JSON ingredients, serves, cook_time_minutes, estimated_cost, emoji, generated_at auto, expires_at, __str__) in backend/tests/foodbanks/test_models.py — tests MUST FAIL

### Implementation for User Story 4

- [x] T027 [US4] Implement GeneratedRecipe model in backend/apps/foodbanks/models.py with UUID PK, fields: food_bank (FK CASCADE), recipe_name, description, serves, cook_time_minutes, ingredients (JSONField), instructions, emoji, estimated_cost, generated_at (auto_now_add), expires_at
- [x] T028 [US4] Generate GeneratedRecipe migration via `python manage.py makemigrations foodbanks`
- [x] T029 [US4] Run GeneratedRecipe tests to verify they pass
- [x] T030 [US4] Update Donation model recipe FK to reference GeneratedRecipe (if not already set in T022), regenerate donations migration if needed

**Checkpoint**: Recipe storage and donation-recipe linking functional

---

## Phase 7: User Story 5 — Configure Admin, Settings, Supermarkets, and QR Analytics (Priority: P3)

**Goal**: Food bank admins can authenticate, configure settings and supermarket preferences. QR scan analytics are recorded.

**Independent Test**: Create a food bank, create an admin with email/password, verify auth. Create settings (OneToOne), supermarket preferences (unique constraint), and QR scans.

### Tests for User Story 5

- [x] T031 [P] [US5] Write FoodBankAdmin model tests (create with email/password, UUID PK, FK to FoodBank CASCADE, email unique, password hashing via AbstractBaseUser) in backend/tests/accounts/test_models.py — tests MUST FAIL
- [x] T032 [P] [US5] Write FoodBankSettings model tests (CRUD, UUID PK, OneToOne FoodBank CASCADE, boolean fields, delivery_notes blank, created_at, updated_at) in backend/tests/foodbanks/test_models.py — tests MUST FAIL
- [x] T033 [P] [US5] Write FoodBankSupermarketPreference model tests (CRUD, UUID PK, FK FoodBank CASCADE, supermarket enum, enabled, delivery_time_days, unique constraint on food_bank+supermarket) in backend/tests/foodbanks/test_models.py — tests MUST FAIL
- [x] T034 [P] [US5] Write QRScan model tests (CRUD, UUID PK, FK FoodBank CASCADE, source enum, scanned_at auto, converted_to_donation, donation FK SET_NULL) in backend/tests/foodbanks/test_models.py — tests MUST FAIL

### Implementation for User Story 5

- [x] T035 [US5] Implement FoodBankAdmin model in backend/apps/accounts/models.py extending AbstractBaseUser with UUID PK, fields: food_bank (FK CASCADE), email (unique), password (via AbstractBaseUser), created_at; USERNAME_FIELD="email", custom manager
- [x] T036 [US5] Generate accounts migration via `python manage.py makemigrations accounts`
- [x] T037 [US5] Run FoodBankAdmin tests to verify they pass
- [x] T038 [P] [US5] Implement FoodBankSettings model in backend/apps/foodbanks/models.py with UUID PK, fields: food_bank (OneToOne CASCADE), pepesto_enabled (default False), accept_direct_delivery (default True), allow_donor_collection (default False), delivery_notes (blank), created_at, updated_at (auto_now)
- [x] T039 [P] [US5] Implement FoodBankSupermarketPreference model in backend/apps/foodbanks/models.py with UUID PK, fields: food_bank (FK CASCADE), supermarket enum (tesco/sainsburys/asda/waitrose), enabled (default True), delivery_time_days (default 1), created_at; UniqueConstraint on (food_bank, supermarket)
- [x] T040 [P] [US5] Implement QRScan model in backend/apps/foodbanks/models.py with UUID PK, fields: food_bank (FK CASCADE), source enum (qr_poster/qr_sticker/qr_social), scanned_at (auto_now_add), converted_to_donation (default False), donation (FK Donation SET_NULL null blank)
- [x] T041 [US5] Generate foodbanks migrations for Settings, SupermarketPreference, QRScan via `python manage.py makemigrations foodbanks`
- [x] T042 [US5] Run all US5 tests to verify they pass

**Checkpoint**: All entities implemented and tested

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Seed data, full migration verification, final validation

- [x] T043 Update seed fixture in backend/fixtures/seed.json with sample data for all 9 entities (FoodBank, WishListItem, GeneratedRecipe, Donation, DeliveryTracking, FoodBankSettings, FoodBankSupermarketPreference, QRScan — skip FoodBankAdmin as it requires password hashing)
- [x] T044 Verify all migrations apply cleanly from scratch against empty database
- [x] T045 Verify seed fixture loads successfully via `python manage.py loaddata fixtures/seed.json`
- [x] T046 Run full test suite (`pytest`) and confirm all tests pass
- [x] T047 Run quickstart.md validation steps end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — clean up existing code
- **Foundational (Phase 2)**: Depends on Setup — creates FoodBank model that all stories need
- **US1 (Phase 3)**: Depends on Foundational — verifies FoodBank acceptance criteria
- **US2 (Phase 4)**: Depends on Foundational — WishListItem references FoodBank
- **US3 (Phase 5)**: Depends on Foundational — Donation references FoodBank; recipe FK added after US4
- **US4 (Phase 6)**: Depends on Foundational — GeneratedRecipe references FoodBank
- **US5 (Phase 7)**: Depends on Foundational + US3 (QRScan references Donation)
- **Polish (Phase 8)**: Depends on all user stories complete

### User Story Dependencies

- **US1 (P1)**: Independent after Foundational
- **US2 (P1)**: Independent after Foundational (parallel with US1)
- **US3 (P2)**: Independent after Foundational; recipe FK resolved after US4
- **US4 (P2)**: Independent after Foundational (parallel with US3)
- **US5 (P3)**: Depends on US3 (QRScan FK to Donation)

### Within Each User Story

- Tests MUST be written and FAIL before implementation (Red)
- Models implemented to make tests pass (Green)
- Migrations generated after models
- Tests re-run to confirm pass

### Parallel Opportunities

- T001-T004: Cleanup tasks can run in parallel
- T020-T021: Donation and DeliveryTracking tests in parallel
- T031-T034: All US5 test tasks in parallel
- T038-T040: Settings, SupermarketPreference, QRScan models in parallel
- US1 and US2 can run in parallel after Foundational
- US3 and US4 can run in parallel (recipe FK resolved at end of US4)

---

## Parallel Example: User Story 5

```bash
# Launch all US5 tests together (they target different models):
Task T031: "FoodBankAdmin tests in backend/tests/accounts/test_models.py"
Task T032: "FoodBankSettings tests in backend/tests/foodbanks/test_models.py"
Task T033: "FoodBankSupermarketPreference tests in backend/tests/foodbanks/test_models.py"
Task T034: "QRScan tests in backend/tests/foodbanks/test_models.py"

# After tests fail, launch parallel model implementations:
Task T038: "FoodBankSettings in backend/apps/foodbanks/models.py"
Task T039: "FoodBankSupermarketPreference in backend/apps/foodbanks/models.py"
Task T040: "QRScan in backend/apps/foodbanks/models.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup (cleanup)
2. Complete Phase 2: Foundational (FoodBank model)
3. Complete Phase 3: US1 (food bank CRUD verified)
4. Complete Phase 4: US2 (wish list items)
5. **STOP and VALIDATE**: Food banks and wish lists work independently
6. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → FoodBank exists
2. US1 + US2 → Core data model working (MVP)
3. US3 + US4 → Donations and recipes
4. US5 → Admin, settings, analytics, delivery tracking
5. Polish → Seed data, full validation

---

## Notes

- All models use UUID primary keys (UUIDField with default=uuid4)
- TimestampMixin provides only `created_at`; `updated_at`/`last_updated` added per-model
- JSON fields (ingredients, items) use Django's JSONField backed by PostgreSQL jsonb
- FoodBankAdmin uses AbstractBaseUser for Django's password hashing
- FoodBankSettings uses OneToOneField to enforce one-settings-per-food-bank
- Tests require PostgreSQL: prefix commands with `DATABASE_URL=postgres://genie:genie@localhost:5432/donation_genie`
