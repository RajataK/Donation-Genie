# Implementation Plan: Expand Seed Fixtures

**Branch**: `005-expand-seed-fixtures` | **Date**: 2026-03-05 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-expand-seed-fixtures/spec.md`

## Summary

Expand the existing `backend/fixtures/seed.json` from a single food bank with minimal related data to 40 food banks with realistic UK-wide geographic distribution, 120+ diverse wishlist items across all categories, and proportionally populated related tables (recipes, donations, delivery tracking, settings, supermarket preferences, QR scans). This is a data-only change — no code, models, or schema modifications.

## Technical Context

**Language/Version**: Python 3.13 (backend), Django 5.2 LTS
**Primary Dependencies**: Django `loaddata` management command (built-in)
**Storage**: PostgreSQL 17 (local via Docker Compose)
**Testing**: pytest with pytest-django — fixture validation tests
**Target Platform**: Local development environment
**Project Type**: Web application (data seed file)
**Performance Goals**: N/A (seed data, loaded once during setup)
**Constraints**: Fixture must be valid JSON loadable by Django's `loaddata`; all UUIDs hardcoded for idempotency
**Scale/Scope**: ~300+ total fixture records across 8 model types

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. TDD (Red-Green-Refactor) | PASS | Tests will validate fixture integrity (record counts, FK consistency, enum values, geographic distribution) before the fixture data is written |
| II. Proven Solutions | PASS | Using Django's built-in `loaddata` fixture format — no custom tooling |
| III. No Premature Optimization | PASS | Straightforward JSON data file, no abstractions or generated code |
| Accessibility | N/A | No UI changes |
| Layered Architecture | N/A | No code changes |
| Contract-First (API) | N/A | No API changes |
| Responsive Design | N/A | No UI changes |

**Quality Gates**:
- All tests pass: pytest fixture validation tests
- Linting clean: ruff on any new test files
- TDD evidence: Test commits before fixture data commit
- No [NEEDS CLARIFICATION]: All resolved in spec

**Gate result**: PASS — no violations.

## Project Structure

### Documentation (this feature)

```text
specs/005-expand-seed-fixtures/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (via /speckit.tasks)
```

### Source Code (repository root)

```text
backend/
├── fixtures/
│   └── seed.json            # Updated: expanded from ~10 to ~300+ records
└── tests/
    └── core/
        └── test_seed_fixtures.py  # New: fixture validation tests
```

**Structure Decision**: No new directories needed. The fixture file already exists at `backend/fixtures/seed.json`. A single new test file validates fixture integrity.
