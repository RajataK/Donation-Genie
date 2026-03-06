# Implementation Plan: Frontend Food Bank Data Fetch

**Branch**: `006-frontend-foodbank-fetch` | **Date**: 2026-03-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-frontend-foodbank-fetch/spec.md`

## Summary

Create a backend REST API endpoint to list all food banks, integrate TanStack Query on the frontend to fetch the data, and log the response to the browser console. This establishes the first end-to-end data flow between backend and frontend.

## Technical Context

**Language/Version**: Python 3.13 (backend), TypeScript 5.7 (frontend)
**Primary Dependencies**: Django 5.2 LTS, Django REST Framework 3.15, drf-spectacular (backend); React 19, Vite 6, TanStack Router 1.95, openapi-fetch 0.13, TanStack Query 5 (frontend — new dependency)
**Storage**: PostgreSQL 17 (local via Docker Compose)
**Testing**: pytest (backend), Vitest (frontend unit), Playwright (E2E)
**Target Platform**: Web browser (frontend), Linux/macOS server (backend)
**Project Type**: Web application (Django API + React SPA)
**Performance Goals**: Food bank list response within 3 seconds (spec SC-001)
**Constraints**: No authentication required for list endpoint; ~40 food bank records (no pagination needed)
**Scale/Scope**: 40 seeded food bank records, single list endpoint

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. TDD (Red-Green-Refactor) | PASS | Tests will be written before implementation for both backend endpoint and frontend query hook |
| II. Proven Solutions Over Clever Ones | PASS | Using TanStack Query (industry standard), DRF serializers/viewsets (proven Django pattern) |
| III. No Premature Optimization | PASS | No pagination, no caching layer beyond TanStack Query defaults, no abstractions |
| Accessibility (WCAG 2.1 AA) | N/A | No new UI — console logging only |
| Layered Architecture | PASS | Thin view, serializer for data shaping, model for data access |
| Contract-First API | PASS | drf-spectacular auto-generates OpenAPI schema; frontend types generated from it |
| Responsive Design | N/A | No new UI |

**Quality Gates**:
- All tests pass (pytest + Vitest + Playwright) — will verify
- Linting clean (ruff + ESLint with jsx-a11y) — will verify
- TDD evidence — test commits will precede implementation
- No [NEEDS CLARIFICATION] markers — none remain
- Accessibility audit — N/A (no UI changes)

## Project Structure

### Documentation (this feature)

```text
specs/006-frontend-foodbank-fetch/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── food-bank-list.md
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── foodbanks/
│       ├── serializers.py       # NEW: FoodBank list serializer
│       ├── views.py             # NEW: FoodBank list view
│       ├── urls.py              # NEW: foodbanks URL config
│       └── tests/
│           ├── __init__.py      # NEW
│           └── test_views.py    # NEW: API endpoint tests
└── config/
    └── urls.py                  # MODIFIED: include foodbanks URLs

frontend/
├── src/
│   ├── App.tsx                  # MODIFIED: wrap with QueryClientProvider
│   ├── hooks/
│   │   └── useFoodBanks.ts     # NEW: TanStack Query hook
│   ├── components/
│   │   └── donor/
│   │       └── FoodBankLogger.tsx  # NEW: component that fetches + logs
│   └── types/
│       └── generated/
│           └── api.d.ts         # REGENERATED: from updated OpenAPI schema
└── package.json                 # MODIFIED: add @tanstack/react-query
```

**Structure Decision**: Web application layout matching existing `backend/` + `frontend/` structure. New files follow existing conventions (app-based Django modules, feature-based frontend hooks/components).

## Complexity Tracking

No violations to justify — all changes use standard patterns within existing project structure.
