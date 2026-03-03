# Research: Full-Stack Project Boilerplate

**Date**: 2026-02-26
**Feature**: 001-init-project-boilerplate

## Decisions

### Backend Stack

- **Decision**: Python 3.13 + Django 5.2 LTS + Django REST Framework
- **Rationale**: Django 5.2 is the current LTS (supported until
  April 2028). Python 3.13 is the latest stable with JIT
  performance gains, supported by Django 5.2 and forward-compatible
  with Django 6.0.
- **Alternatives considered**:
  - Python 3.12: Shorter support window, no JIT improvements.
  - Django 4.2 LTS: End of life April 2026 — too close.

### OpenAPI Schema Generation

- **Decision**: drf-spectacular
- **Rationale**: Officially recommended by DRF. Supports OpenAPI
  3.0.3 and 3.1. drf-yasg is frozen and only supports Swagger 2.0.
  DRF's built-in schema generator is deprecated.
- **Alternatives considered**:
  - drf-yasg: OpenAPI 2.0 only, maintenance mode.
  - DRF built-in: Deprecated.

### TypeScript Type Generation from OpenAPI

- **Decision**: openapi-typescript + openapi-fetch
- **Rationale**: Lightweight, zero-runtime approach. Generates pure
  TypeScript types from the OpenAPI schema. openapi-fetch wraps
  native `fetch` with full type-safety (~6 KB). ~2.4M weekly npm
  downloads — largest adoption.
- **Alternatives considered**:
  - orval: Generates TanStack Query hooks. More opinionated, adds
    dependency on query library. Better for later when React Query
    is adopted.
  - openapi-generator: Requires Java, verbose output, more config.

### Django Project Structure

- **Decision**: HackSoft style guide pattern — Django apps with
  explicit layers: urls.py (routes), views.py (thin adapters),
  services.py (business logic as pure functions), models.py (data
  access).
- **Rationale**: Most widely adopted layered pattern for Django.
  Well-documented. Aligns with FP constitution principle — services
  are pure functions, side effects isolated in views/models.
- **Alternatives considered**:
  - Separate top-level directories (routes/, services/,
    repositories/): Fights Django conventions, confuses Django
    tooling (migrations, app discovery).
  - DRF ViewSets as the only layer: Mixes routing, validation,
    and business logic in one place.

### Django Settings & Environment

- **Decision**: django-environ with split settings
  (base.py / local.py / production.py)
- **Rationale**: Django-specific, handles DATABASE_URL parsing,
  .env file loading, type coercion. Settings split by environment
  keeps each config small and focused. DJANGO_ENV variable selects
  the active settings module.
- **Alternatives considered**:
  - python-dotenv: Lower-level, no DATABASE_URL parsing.
  - python-decouple: Similar to django-environ but less Django-
    specific tooling.

### Frontend Stack

- **Decision**: React 19 + Vite 6 + TypeScript 5
- **Rationale**: React 19 is current stable. Vite is the standard
  build tool for new React projects (fast, minimal config,
  first-class TypeScript). CRA is in maintenance mode.
- **Alternatives considered**:
  - Next.js SPA mode: Heavier, adds SSR complexity not needed.
  - Create React App: Maintenance mode, not recommended for new
    projects.

### Frontend Routing

- **Decision**: TanStack Router
- **Rationale**: Fully type-safe routing with TypeScript-first
  design. File-based route generation provides automatic route
  types. Growing ecosystem with strong community momentum. Pairs
  naturally with the TypeScript-heavy stack (openapi-typescript
  generated types flow directly into route loaders).
- **Alternatives considered**:
  - React Router v7: Larger ecosystem but weaker type safety.
    Library mode still viable but TanStack Router's DX is superior
    for TypeScript projects.
  - React Router v6: Superseded by v7.

### Frontend Testing

- **Decision**: Vitest + React Testing Library + jsdom
- **Rationale**: Vitest shares the Vite config (plugins, aliases,
  TypeScript) with zero extra setup. Jest requires Babel or ts-jest
  shims and fights Vite's ESM-first model.
- **Alternatives considered**:
  - Jest: Extra configuration needed for Vite/ESM/TypeScript.

### Backend Testing

- **Decision**: pytest + pytest-django
- **Rationale**: pytest is the standard Python testing framework.
  pytest-django provides Django-specific fixtures (client, db
  access, settings). Aligns with TDD constitution principle.
- **Alternatives considered**:
  - Django's unittest: More verbose, less feature-rich (no
    fixtures, parametrize, etc.).

### Database

- **Decision**: PostgreSQL 17
- **Rationale**: Current stable (EOL November 2029). Standard
  choice for Django projects. Alpine image for small container
  size.
- **Alternatives considered**:
  - PostgreSQL 16: Shorter support window.
  - PostgreSQL 18: Too new, less battle-tested.

### Reverse Proxy

- **Decision**: Nginx 1.27
- **Rationale**: Most common reverse proxy for Django+React.
  Simple configuration. Handles SPA fallback
  (try_files → index.html) and API proxying (/api/ → Django).
  Alpine image for small container size.
- **Alternatives considered**:
  - Traefik: More complex, auto-discovery features not needed for
    local dev.
  - Caddy: Simpler config syntax but smaller ecosystem.

### Node.js Version

- **Decision**: Node.js 24 LTS
- **Rationale**: Current Active LTS (EOL April 2028). Used in
  Docker images for frontend build and dev server.
- **Alternatives considered**:
  - Node.js 22: Maintenance LTS, shorter support.
  - Node.js 20: Near end of life (April 2026).

### Task Runner

- **Decision**: Makefile
- **Rationale**: Available on all Unix systems. No additional
  dependencies. Simple target syntax. Standard for Docker Compose
  workflows.
- **Alternatives considered**:
  - Just: Better syntax but requires installation.
  - npm scripts: Only covers frontend, not the full stack.

## Version Pin Summary

| Component        | Version         | EOL / Support  |
|------------------|-----------------|----------------|
| Python           | 3.13            | Oct 2029       |
| Django           | 5.2 LTS         | Apr 2028       |
| DRF              | 3.15.x          | Active         |
| drf-spectacular  | latest           | Active         |
| React            | 19.x            | Active         |
| TanStack Router  | latest           | Active         |
| Vite             | 6.x             | Active         |
| TypeScript       | 5.x             | Active         |
| Vitest           | 3.x             | Active         |
| Node.js          | 24 LTS          | Apr 2028       |
| PostgreSQL       | 17              | Nov 2029       |
| Nginx            | 1.27            | Active         |
| openapi-typescript | latest         | Active         |
| openapi-fetch    | latest           | Active         |
| django-environ   | latest           | Active         |
