# Implementation Plan: Initialize PostgreSQL Schema

**Branch**: `004-init-postgres-schema` | **Date**: 2026-03-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-init-postgres-schema/spec.md`

## Summary

Replace the existing 9-model schema with a redesigned 9-entity schema using UUID primary keys across all models. The new schema reflects the full Donation Genie domain: Food Bank, Wish List Item, Generated Recipe, Donation, Food Bank Admin, QR Scan, Food Bank Settings, Food Bank Supermarket Preference, and Delivery Tracking. Key changes include JSON fields for recipe ingredients and donation items, enum-based categories, UUID PKs, and new entities for admin auth, analytics, settings, and delivery tracking.

## Technical Context

**Language/Version**: Python 3.13
**Primary Dependencies**: Django 5.2 LTS, Django REST Framework 3.15, psycopg (PostgreSQL adapter)
**Storage**: PostgreSQL 17 (local via Docker, production via AWS RDS)
**Testing**: pytest + pytest-django
**Target Platform**: Linux server (Docker container)
**Project Type**: Web service (backend API)
**Performance Goals**: Standard web application — no specific throughput targets for schema layer
**Constraints**: PostgreSQL-specific features (JSONField relies on PostgreSQL's native JSON type)
**Scale/Scope**: ~10 entities, single database, UK food bank domain

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. TDD (Red-Green-Refactor) | PASS | Tests written before model implementation |
| II. Proven Solutions | PASS | Django ORM, UUIDField, JSONField — all standard Django patterns |
| III. No Premature Optimization | PASS | No custom abstractions beyond TimestampMixin; JSON fields avoid unnecessary join tables where appropriate |
| Accessibility | N/A | Backend schema — no UI |
| Layered Architecture | PASS | Models handle data access only |
| Contract-first API | N/A | Schema feature — API contracts come in a later feature |

**Deviations from user-provided schema (justified):**

1. **FoodBankAdmin.password_hash**: Django provides built-in password hashing via `AbstractBaseUser` or `make_password`/`check_password`. Instead of a raw `password_hash` TextField, we use Django's `AbstractBaseUser` which stores the hash in a `password` field with proper hashing utilities. This is the proven Django pattern and avoids rolling custom auth. The user schema's intent (hashed password storage) is preserved.

## Project Structure

### Documentation (this feature)

```text
specs/004-init-postgres-schema/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   ├── core/
│   │   └── models.py          # TimestampMixin abstract base
│   ├── foodbanks/
│   │   ├── models.py          # FoodBank, WishListItem, GeneratedRecipe,
│   │   │                      # FoodBankSettings, FoodBankSupermarketPreference,
│   │   │                      # QRScan
│   │   └── migrations/
│   ├── donations/
│   │   ├── models.py          # Donation, DeliveryTracking
│   │   └── migrations/
│   └── accounts/
│       ├── models.py          # FoodBankAdmin (extends AbstractBaseUser)
│       └── migrations/
├── tests/
│   ├── foodbanks/
│   │   └── test_models.py
│   ├── donations/
│   │   └── test_models.py
│   └── accounts/
│       └── test_models.py
└── fixtures/
    └── seed.json
```

**Structure Decision**: Three domain apps — `foodbanks` (food bank entity and configuration), `donations` (donation events and delivery), `accounts` (food bank admin auth). Shared `core` app provides TimestampMixin. FoodBankAdmin gets its own app because Django custom user models must be in a dedicated app and set as `AUTH_USER_MODEL`.

## Complexity Tracking

| Deviation | Why Needed | User Schema Difference |
|-----------|------------|------------------------|
| `AbstractBaseUser` for FoodBankAdmin | Django's auth framework requires it; provides password hashing, session support, admin integration out of the box | User specified raw `password_hash` field — intent preserved, implementation uses Django's battle-tested auth |
| `accounts` app | Django's `AUTH_USER_MODEL` must be set before first migration; custom user models should be in their own app per Django docs | User didn't specify app organization — this is an implementation detail |
