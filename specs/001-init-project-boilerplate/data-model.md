# Data Model: Full-Stack Project Boilerplate

**Date**: 2026-02-26
**Feature**: 001-init-project-boilerplate

## Overview

The boilerplate establishes the foundational data model for the
Donation Genie application. At this stage, the only runtime entity
is the health-check response. The primary "data" is the project
structure and configuration itself.

Future features will add domain entities (donations, users, etc.)
by creating new Django apps following the established layered
pattern.

## Entities

### HealthStatus

Represents the response from the backend health-check endpoint.
This is a read-only, non-persisted entity.

| Field         | Type    | Description                          |
|---------------|---------|--------------------------------------|
| status        | string  | Overall status: "healthy" or "unhealthy" |
| database      | string  | Database connectivity: "connected" or "disconnected" |
| version       | string  | Application version identifier       |
| timestamp     | string  | ISO 8601 timestamp of the check      |

**Notes**:
- Not stored in the database. Computed on each request.
- Database connectivity is checked via a lightweight query.

### Migration (Django built-in)

Django's migration framework manages schema versioning. Each
migration is a Python file with:

| Field         | Type    | Description                          |
|---------------|---------|--------------------------------------|
| app_label     | string  | Django app the migration belongs to  |
| name          | string  | Migration identifier (e.g., "0001_initial") |
| dependencies  | list    | Other migrations this depends on     |
| operations    | list    | Schema changes (CreateModel, AddField, etc.) |

**Notes**:
- Managed entirely by Django's migration framework.
- `python manage.py migrate` applies pending migrations.
- `python manage.py makemigrations` generates new migrations.

### Environment Configuration (runtime)

Not a database entity. Configuration is loaded from environment
variables at startup.

| Variable         | Default (local)                          | Description                    |
|------------------|------------------------------------------|--------------------------------|
| DJANGO_SECRET_KEY | auto-generated for local                | Django secret key              |
| DJANGO_ENV       | local                                    | Settings module selector       |
| DATABASE_URL     | postgres://genie:changeme@db:5432/donation_genie | Database connection URL |
| DEBUG            | True                                     | Django debug mode              |
| ALLOWED_HOSTS    | localhost,127.0.0.1                      | Allowed HTTP host headers      |
| VITE_API_URL     | /api                                     | API base URL for frontend      |

## Relationships

```text
HealthStatus ──checks──> Database (PostgreSQL)
Migration ──belongs_to──> Django App
Environment Configuration ──configures──> All Services
```

## Future Extension Points

When adding domain entities (e.g., Donation, User, Organization):

1. Create a new Django app: `python manage.py startapp donations`
2. Add the app to `INSTALLED_APPS` in `config/settings/base.py`
3. Define models in `apps/donations/models.py`
4. Add business logic in `apps/donations/services.py`
5. Add routes in `apps/donations/urls.py`
6. Add thin views in `apps/donations/views.py`
7. Include app URLs in `config/urls.py`
8. Generate migrations: `python manage.py makemigrations`
