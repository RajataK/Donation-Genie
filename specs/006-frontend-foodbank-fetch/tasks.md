# Tasks: Frontend Food Bank Data Fetch

**Input**: Design documents from `/specs/006-frontend-foodbank-fetch/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Included per constitution requirement (TDD: Red-Green-Refactor).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install new dependencies and configure dev environment for frontend-backend communication

- [x] T001 Install `@tanstack/react-query` dependency in `frontend/package.json`
- [x] T002 Add Vite dev server proxy for `/api` to `http://localhost:8000` in `frontend/vite.config.ts`

---

## Phase 2: Foundational (Backend API Endpoint)

**Purpose**: Create the backend food bank list API endpoint that ALL frontend work depends on

**⚠️ CRITICAL**: No frontend user story work can begin until this phase is complete

### Tests for Backend API ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T003 Create test directory and init file at `backend/apps/foodbanks/tests/__init__.py`
- [x] T004 Write tests for `GET /api/food-banks/` endpoint in `backend/tests/foodbanks/test_views.py` covering: returns 200 with list of all food banks, response contains all required fields (id, name, postcode, latitude, longitude, address, families_served_weekly, urgency_level, last_updated), returns empty array when no food banks exist, no authentication required

### Backend Implementation

- [x] T005 [P] Create `FoodBankSerializer` (ModelSerializer with all fields from data-model.md) in `backend/apps/foodbanks/serializers.py`
- [x] T006 [P] Create `FoodBankListView` (ListAPIView, no auth, using FoodBankSerializer) in `backend/apps/foodbanks/views.py`
- [x] T007 Create URL config with `food-banks/` path in `backend/apps/foodbanks/urls.py`
- [x] T008 Register foodbanks URLs under `api/` prefix in `backend/config/urls.py` by adding `path("api/", include("apps.foodbanks.urls"))`
- [x] T009 Verify backend tests pass (run `pytest backend/apps/foodbanks/tests/`)

### Contract-First Type Generation

- [x] T010 Regenerate frontend TypeScript types from updated OpenAPI schema by running `npm run generate:api` in `frontend/` (requires backend running)

**Checkpoint**: Backend API endpoint is live at `GET /api/food-banks/` and returns seeded food bank data. Frontend has updated generated types.

---

## Phase 3: User Story 1 - Fetch and Display Food Bank Data in Console (Priority: P1) 🎯 MVP

**Goal**: Frontend fetches all food bank records from the backend on app load and logs them to the browser console

**Independent Test**: Load `http://localhost:5173` with backend running, open browser dev tools, confirm food bank data appears in Console tab

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T011 [P] [US1] Write unit test for `useFoodBanks` hook in `frontend/src/hooks/__tests__/useFoodBanks.test.ts` covering: hook returns food bank data on success, hook returns error state on fetch failure
- [x] T012 [P] [US1] Write unit test for `FoodBankLogger` component in `frontend/src/components/donor/__tests__/FoodBankLogger.test.tsx` covering: logs food bank data to console on successful fetch, logs error to console on fetch failure, handles empty food bank list without errors

### Implementation for User Story 1

- [x] T013 [US1] Create `useFoodBanks` custom hook using TanStack Query's `useQuery` with the `openapi-fetch` client to call `GET /api/food-banks/` in `frontend/src/hooks/useFoodBanks.ts`
- [x] T014 [US1] Create `FoodBankLogger` component that calls `useFoodBanks` and uses `useEffect` to `console.log` data on success and `console.error` on failure in `frontend/src/components/donor/FoodBankLogger.tsx`
- [x] T015 [US1] Wrap the app with `QueryClientProvider` in `frontend/src/App.tsx` and render `FoodBankLogger` inside the provider
- [x] T016 [US1] Verify frontend tests pass (run `npm test` in `frontend/`)

**Checkpoint**: User Story 1 is complete. Loading the app logs all food bank data to the browser console. Errors are caught and logged gracefully.

---

## Phase 4: User Story 2 - Data Caching and Refetch Behaviour (Priority: P2)

**Goal**: TanStack Query caches food bank data and avoids redundant network requests within the cache window

**Independent Test**: Open Network tab in browser dev tools, load app (1 request fires), navigate away and back (no new request within stale time)

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T017 [US2] Write unit test verifying `useFoodBanks` hook uses a `staleTime` configuration (data is not refetched within the cache period) in `frontend/src/hooks/__tests__/useFoodBanks.test.ts` (add to existing test file)

### Implementation for User Story 2

- [x] T018 [US2] Configure `staleTime` (5 minutes) in the `useQuery` options within `frontend/src/hooks/useFoodBanks.ts`
- [x] T019 [US2] Verify caching test passes (run `npm test` in `frontend/`)

**Checkpoint**: User Stories 1 AND 2 are both complete. Data is cached by TanStack Query with a 5-minute stale time.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation across both backend and frontend

- [x] T020 Run backend linting (`ruff check .` in `backend/`)
- [x] T021 Run frontend linting (`npm run lint` in `frontend/`)
- [x] T022 Run full test suite (pytest in `backend/`, `npm test` in `frontend/`)
- [x] T023 Run quickstart.md validation — follow all steps and verify console output

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) completion
- **User Story 2 (Phase 4)**: Depends on User Story 1 (Phase 3) — extends the `useFoodBanks` hook
- **Polish (Phase 5)**: Depends on all user stories being complete

### Within Each Phase

- Tests MUST be written and FAIL before implementation begins (TDD)
- Backend serializer (T005) and view (T006) can be created in parallel
- Frontend hook test (T011) and component test (T012) can be created in parallel
- Implementation follows: hook → component → App integration

### Parallel Opportunities

**Phase 1**:
- T001 and T002 touch different files — can run in parallel

**Phase 2**:
- T005 (serializer) and T006 (view) touch different files — can run in parallel
- T003 and T004 are sequential (directory then test file)

**Phase 3**:
- T011 (hook test) and T012 (component test) touch different files — can run in parallel
- T013 (hook) and T014 (component) are sequential (component depends on hook)

---

## Parallel Example: Phase 2 (Foundational)

```bash
# Write tests first:
Task: "Create test directory at backend/apps/foodbanks/tests/__init__.py"
Task: "Write endpoint tests in backend/apps/foodbanks/tests/test_views.py"

# Then launch parallel implementation:
Task: "Create FoodBankSerializer in backend/apps/foodbanks/serializers.py"
Task: "Create FoodBankListView in backend/apps/foodbanks/views.py"

# Then sequential wiring:
Task: "Create URL config in backend/apps/foodbanks/urls.py"
Task: "Register URLs in backend/config/urls.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (install deps, add proxy)
2. Complete Phase 2: Backend API endpoint (tests → implementation → type generation)
3. Complete Phase 3: User Story 1 (tests → hook → component → App integration)
4. **STOP and VALIDATE**: Open browser, check console for food bank data
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Backend API ready
2. Add User Story 1 → Data flows end-to-end, logged to console (MVP!)
3. Add User Story 2 → Caching prevents redundant requests
4. Polish → All linting and tests green

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Constitution requires TDD: all test tasks MUST be completed before their corresponding implementation tasks
- Commit after each task or logical group
- T010 (type generation) requires the backend to be running — start it before running `npm run generate:api`
- The `FoodBankLogger` component is temporary (per spec assumptions) — future features will render data in UI
