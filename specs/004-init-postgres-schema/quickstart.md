# Quickstart: Initialize PostgreSQL Schema

**Feature**: 004-init-postgres-schema
**Date**: 2026-03-05

## Prerequisites

- Docker and Docker Compose running (for PostgreSQL)
- Python 3.13 virtual environment activated (`backend/.venv`)
- Backend dependencies installed (`pip install -r backend/requirements/local.txt`)

## Setup Steps

### 1. Start the database

```bash
docker compose up -d db
```

### 2. Apply migrations

```bash
cd backend
DATABASE_URL=postgres://genie:genie@localhost:5432/donation_genie python manage.py migrate
```

This creates all tables for the `foodbanks`, `donations`, and `accounts` apps.

### 3. Verify schema

```bash
DATABASE_URL=postgres://genie:genie@localhost:5432/donation_genie python manage.py showmigrations foodbanks donations accounts
```

Expected output shows all migrations as applied (`[X]`).

### 4. Load seed data (optional)

```bash
DATABASE_URL=postgres://genie:genie@localhost:5432/donation_genie python manage.py loaddata fixtures/seed.json
```

## Development Workflow

### Creating new models

1. Edit `backend/apps/foodbanks/models.py`, `backend/apps/donations/models.py`, or `backend/apps/accounts/models.py`
2. Generate migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Write/update tests in `backend/tests/foodbanks/`, `backend/tests/donations/`, or `backend/tests/accounts/`

### Running tests

```bash
# All backend tests (requires PostgreSQL)
cd backend
DATABASE_URL=postgres://genie:genie@localhost:5432/donation_genie pytest

# Only model tests for this feature
DATABASE_URL=postgres://genie:genie@localhost:5432/donation_genie pytest tests/foodbanks/ tests/donations/ tests/accounts/
```

### Resetting the database

```bash
docker compose down -v   # Removes the database volume
docker compose up -d db  # Recreates empty database
cd backend
DATABASE_URL=postgres://genie:genie@localhost:5432/donation_genie python manage.py migrate
```

## Key Files

| File | Purpose |
|------|---------|
| `backend/apps/core/models.py` | TimestampMixin abstract base |
| `backend/apps/foodbanks/models.py` | FoodBank, WishListItem, GeneratedRecipe, FoodBankSettings, FoodBankSupermarketPreference, QRScan |
| `backend/apps/donations/models.py` | Donation, DeliveryTracking |
| `backend/apps/accounts/models.py` | FoodBankAdmin (custom auth user) |
| `backend/config/settings/base.py` | INSTALLED_APPS and AUTH_USER_MODEL |
| `backend/tests/foodbanks/test_models.py` | Food bank model tests |
| `backend/tests/donations/test_models.py` | Donation model tests |
| `backend/tests/accounts/test_models.py` | Account model tests |
