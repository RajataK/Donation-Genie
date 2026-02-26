# Tasks: Full-Stack Project Boilerplate

**Input**: Design documents from `/specs/001-init-project-boilerplate/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/health-api.yaml, quickstart.md

**Tests**: TDD is NON-NEGOTIABLE per project constitution. Test tasks are included for every user story with production code. Tests MUST be written first and MUST fail before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: Root project files and monorepo structure

- [x] T001 Create .gitignore with Python, Node.js, Docker, .env, and IDE patterns at .gitignore
- [x] T002 [P] Create initial .env.example with placeholder variables at .env.example
- [x] T003 [P] Create Makefile skeleton with help target at Makefile

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Initialize both backend and frontend projects to a buildable state. Test frameworks configured so TDD can begin in user story phases.

**CRITICAL**: No user story work can begin until this phase is complete.

- [x] T004 Initialize Django project — create backend/manage.py, backend/config/__init__.py, backend/config/urls.py, backend/config/wsgi.py, backend/config/asgi.py
- [x] T005 Create Django split settings with django-environ — backend/config/settings/__init__.py (env selector), backend/config/settings/base.py (INSTALLED_APPS, MIDDLEWARE, DATABASES via env.db()), backend/config/settings/local.py (DEBUG=True, .env loading)
- [x] T006 [P] Create backend requirements — backend/requirements/base.txt (Django==5.2.*, djangorestframework, drf-spectacular, django-environ, gunicorn, psycopg[binary]) and backend/requirements/local.txt (pytest, pytest-django)
- [x] T007 [P] Configure pytest for backend — backend/pytest.ini (django settings module, test paths), backend/tests/__init__.py, backend/tests/conftest.py (shared fixtures)
- [x] T008 Initialize Vite React project — frontend/package.json (react, react-dom, @tanstack/react-router, @tanstack/router-devtools, typescript, vite, @vitejs/plugin-react, vitest, @testing-library/react, @testing-library/jest-dom, @testing-library/user-event, openapi-typescript, openapi-fetch), frontend/vite.config.ts (react plugin + vitest test config with jsdom + TanStack Router plugin), frontend/tsconfig.json, frontend/tsconfig.node.json, frontend/index.html, frontend/src/main.tsx (minimal render), frontend/src/App.tsx (placeholder), frontend/src/test/setup.ts (@testing-library/jest-dom import)
- [x] T009 Create backend Dockerfile at backend/Dockerfile with development target (python:3.13-slim, pip install requirements, expose 8000)
- [x] T010 [P] Create frontend Dockerfile at frontend/Dockerfile with development target (node:24-alpine, npm ci, expose 5173, CMD npm run dev -- --host 0.0.0.0)

**Checkpoint**: Both projects buildable. pytest and vitest configured. TDD can begin.

---

## Phase 3: User Story 1 — Run the Entire Stack Locally (Priority: P1) MVP

**Goal**: A developer starts all services with a single command and accesses the app through the reverse proxy.

**Independent Test**: Run `make up`, visit http://localhost, hit http://localhost/api/health/, run `make down`.

### Implementation for User Story 1

- [x] T011 [US1] Create Nginx reverse proxy configuration at nginx/default.conf — SPA fallback (try_files $uri /index.html), /api/ proxy to django:8000, /static/ alias to shared volume, gzip compression, cache headers for hashed assets
- [x] T012 [US1] Create docker-compose.yml at docker-compose.yml — 4 services: db (postgres:17-alpine with healthcheck pg_isready, named volume), django (backend Dockerfile dev target, depends_on db healthy, env_file .env, expose 8000, volume mount ./backend:/app, healthcheck curl /api/health/), frontend (frontend Dockerfile dev target, volume mount ./frontend:/app with anonymous node_modules volume, ports 5173), nginx (nginx:1.27-alpine, ports 80, depends_on django healthy and frontend started, mount nginx/default.conf and static volume)
- [x] T013 [P] [US1] Create database seed fixture at backend/fixtures/seed.json — minimal placeholder data, and add Django management command or loaddata integration for seeding
- [x] T014 [US1] Add Makefile orchestration targets at Makefile — setup (build + migrate + seed), up (docker compose up -d), down (docker compose down), teardown (docker compose down -v), logs (docker compose logs -f), shell (docker compose exec django python manage.py shell), migrate (docker compose exec django python manage.py migrate), seed (docker compose exec django python manage.py loaddata fixtures/seed.json)
- [x] T015 [US1] Verify end-to-end: run make up, confirm all 4 containers are healthy, curl http://localhost returns HTML, curl http://localhost/api/health/ returns JSON, run make down confirms clean shutdown

**Checkpoint**: Developer can run `make up` and access the full stack. US1 is independently functional.

---

## Phase 4: User Story 2 — Backend Layered Architecture (Priority: P2)

**Goal**: Backend has a health app demonstrating the layered pattern (urls → views → services → models). OpenAPI schema is generated.

**Independent Test**: Run backend tests with pytest. Hit GET /api/health/ and verify structured JSON response.

### Tests for User Story 2 (TDD — write first, verify RED)

- [x] T016 [US2] Write health endpoint test at backend/tests/health/__init__.py and backend/tests/health/test_health_endpoint.py — test GET /api/health/ returns 200 with JSON containing status, database, version, timestamp fields; test returns 503 when database unreachable. Use pytest + Django test client. Verify tests FAIL (RED) before proceeding.

### Implementation for User Story 2

- [x] T017 [US2] Create health app structure — backend/apps/__init__.py, backend/apps/health/__init__.py, backend/apps/health/apps.py (HealthConfig with name='apps.health')
- [x] T018 [US2] Implement get_health_status pure function at backend/apps/health/services.py — accepts db connection checker as argument, returns dict matching HealthStatus schema (status, database, version, timestamp). No side effects in the function itself.
- [x] T019 [US2] Implement HealthCheckView at backend/apps/health/views.py — DRF APIView, GET method calls services.get_health_status(), returns Response with appropriate status code (200 or 503)
- [x] T020 [US2] Register routes at backend/apps/health/urls.py (urlpatterns with path to HealthCheckView) and include in backend/config/urls.py with path('api/', include('apps.health.urls'))
- [x] T021 [US2] Configure DRF and drf-spectacular in backend/config/settings/base.py — add rest_framework and drf_spectacular to INSTALLED_APPS, set DEFAULT_SCHEMA_CLASS, add SPECTACULAR_SETTINGS (title, version, description), add schema URL patterns in backend/config/urls.py (SpectacularAPIView, SpectacularSwaggerView)
- [x] T022 [US2] Verify health test passes (GREEN) — run pytest, confirm all health tests pass. Verify GET /api/health/ returns correct JSON matching contracts/health-api.yaml schema.

**Checkpoint**: Backend layered architecture proven. Health endpoint works. OpenAPI schema generated. US2 independently testable.

---

## Phase 5: User Story 3 — Frontend Component Structure (Priority: P3)

**Goal**: Frontend has routing, component library structure, and API client wired to the backend via OpenAPI.

**Independent Test**: Run frontend tests with vitest. Navigate to / in browser and see HomePage. API client can call /api/health/.

### Tests for User Story 3 (TDD — write first, verify RED)

- [x] T023 [US3] Write App smoke test at frontend/tests/App.test.tsx — test that App renders without crashing, test that HomePage content is visible. Use React Testing Library. Verify tests FAIL (RED) before proceeding.

### Implementation for User Story 3

- [x] T024 [US3] Set up TanStack Router at frontend/src/router.tsx — create rootRoute and indexRoute (/) pointing to HomePage using createRouter and createRootRoute. Update frontend/src/main.tsx to use RouterProvider from @tanstack/react-router. Update frontend/src/App.tsx as root layout component with Outlet.
- [x] T025 [P] [US3] Create directory structure with .gitkeep files — frontend/src/components/ui/.gitkeep, frontend/src/hooks/.gitkeep, frontend/src/utils/.gitkeep
- [x] T026 [US3] Create HomePage component at frontend/src/pages/HomePage.tsx — functional component displaying app name and health status placeholder. Pure presentational component.
- [x] T027 [US3] Set up API client at frontend/src/api/client.ts — configure openapi-fetch createClient with base URL from import.meta.env.VITE_API_URL. Create frontend/src/types/generated/.gitkeep for generated types.
- [x] T028 [US3] Add OpenAPI TypeScript generation — add "generate:api" script in frontend/package.json using openapi-typescript pointing to backend schema URL. Add generate-api target to Makefile. Run generation and verify types are created in frontend/src/types/generated/.

**Checkpoint**: Frontend structure established. Routing works. API client configured. US3 independently testable.

---

## Phase 6: User Story 4 — Run Tests Across the Monorepo (Priority: P4)

**Goal**: Single Makefile command runs all tests. Individual package tests run in isolation.

**Independent Test**: Run `make test` and see results from both backend (pytest) and frontend (vitest).

### Implementation for User Story 4

- [x] T029 [US4] Add Makefile test targets at Makefile — test (runs test-backend then test-frontend), test-backend (docker compose exec django pytest or cd backend && pytest), test-frontend (docker compose exec frontend npm test or cd frontend && npx vitest run)
- [x] T030 [US4] Verify test isolation — run make test-backend (only backend tests execute), run make test-frontend (only frontend tests execute), confirm neither requires the other's services
- [x] T031 [US4] Verify monorepo-wide test — run make test, confirm it discovers and runs tests in both packages, output clearly identifies which package each test belongs to

**Checkpoint**: Test infrastructure complete. `make test` runs everything. Each package testable independently.

---

## Phase 7: User Story 5 — Environment Configuration (Priority: P5)

**Goal**: Environment variables documented. Settings switch between local and production via DJANGO_ENV. Cloud targets require only config changes.

**Independent Test**: Set DJANGO_ENV=production, verify production settings load. Change DATABASE_URL, verify it takes effect.

### Implementation for User Story 5

- [x] T032 [US5] Fully document .env.example at .env.example — all variables with descriptions as comments: DJANGO_SECRET_KEY, DJANGO_ENV, DATABASE_URL, DEBUG, ALLOWED_HOSTS, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, VITE_API_URL. Include sensible local defaults.
- [x] T033 [P] [US5] Create production settings stub at backend/config/settings/production.py — import from base, set DEBUG=False, SECURE_SSL_REDIRECT=True, SESSION_COOKIE_SECURE=True, CSRF_COOKIE_SECURE=True. No .env file loading (env vars injected by platform).
- [x] T034 [US5] Verify environment switching — confirm DJANGO_ENV=local loads local.py, DJANGO_ENV=production loads production.py. Confirm DATABASE_URL change in .env switches database target without code changes.

**Checkpoint**: Configuration system proven. Cloud-ready without code changes.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup across all user stories

- [x] T035 [P] Run full stack validation per specs/001-init-project-boilerplate/quickstart.md — follow every step, verify every URL and command works
- [x] T036 [P] Clean up placeholder content — verify all .gitkeep files are in empty directories only, remove any template comments from source files, ensure no TODO markers remain in production code
- [x] T037 Run complete test suite (make test) and verify all tests pass with clean output

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup (T001-T003) — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational (T004-T010) — needs buildable projects for Docker
- **US2 (Phase 4)**: Depends on Foundational (T004-T010) — needs Django project and pytest
- **US3 (Phase 5)**: Depends on Foundational (T004-T010) — needs React project and vitest
- **US4 (Phase 6)**: Depends on US2 (T022) and US3 (T028) — needs tests to exist in both packages
- **US5 (Phase 7)**: Depends on Foundational (T005) — needs Django settings to exist
- **Polish (Phase 8)**: Depends on all user stories complete

### User Story Dependencies

- **US1 (P1)**: Depends on Foundational. Can run in parallel with US2, US3, US5.
- **US2 (P2)**: Depends on Foundational. Independent of US1, US3.
- **US3 (P3)**: Depends on Foundational. Independent of US1, US2.
- **US4 (P4)**: Depends on US2 and US3 (needs test files in both packages).
- **US5 (P5)**: Depends on Foundational. Independent of US1-US4.

### Within Each User Story

- Tests MUST be written FIRST and MUST FAIL before implementation (TDD)
- App structure before business logic
- Services before views
- Routes registered last
- Story verified (GREEN) before moving to next

### Parallel Opportunities

- Setup: T002 and T003 run in parallel
- Foundational: T006+T007 in parallel, T009+T010 in parallel
- After Foundational: US1, US2, US3, and US5 can ALL start in parallel
- US1: T013 runs in parallel with T011
- US3: T025 runs in parallel with T024
- US5: T033 runs in parallel with T032
- Polish: T035 and T036 run in parallel

---

## Parallel Example: After Foundational Phase

```bash
# All four of these user stories can start simultaneously:
# Stream A: US1 — Docker orchestration (T011-T015)
# Stream B: US2 — Backend health app with TDD (T016-T022)
# Stream C: US3 — Frontend structure with TDD (T023-T028)
# Stream D: US5 — Environment config (T032-T034)

# Then once US2 + US3 complete:
# Stream E: US4 — Test infrastructure (T029-T031)

# Finally:
# Stream F: Polish (T035-T037)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T010)
3. Complete Phase 3: US1 — Docker Stack (T011-T015)
4. **STOP and VALIDATE**: `make up` works, all containers healthy
5. Deploy/demo if ready — basic stack runs

### Incremental Delivery

1. Setup + Foundational → Both projects buildable
2. US1 → Docker stack works → Demo: `make up` starts everything
3. US2 → Backend proven → Demo: health endpoint with TDD
4. US3 → Frontend proven → Demo: SPA with routing and API client
5. US4 → Tests unified → Demo: `make test` runs all
6. US5 → Config documented → Demo: environment switching
7. Polish → Production-ready boilerplate

### Sequential (Single Developer)

Recommended order for solo work:

1. Phase 1: Setup (T001-T003)
2. Phase 2: Foundational (T004-T010)
3. Phase 4: US2 — Backend first (T016-T022) — establishes TDD pattern
4. Phase 5: US3 — Frontend next (T023-T028) — consumes backend API
5. Phase 3: US1 — Docker orchestration (T011-T015) — wires everything together
6. Phase 6: US4 — Test infrastructure (T029-T031)
7. Phase 7: US5 — Environment config (T032-T034)
8. Phase 8: Polish (T035-T037)

**Rationale**: Building backend then frontend before Docker means each piece is verified independently before orchestration. This reduces debugging Docker issues vs application issues.

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- TDD is mandatory: write test → verify RED → implement → verify GREEN
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Total: 37 tasks across 8 phases
