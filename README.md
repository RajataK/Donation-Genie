# Donation Genie

AI-powered donation companion app.

## Tech Stack

| Layer    | Technology                                         |
| -------- | -------------------------------------------------- |
| Frontend | React 19, TypeScript, Vite, TanStack Router        |
| Backend  | Django 5.2, Django REST Framework, drf-spectacular |
| Database | PostgreSQL 17                                      |
| Proxy    | Nginx 1.27                                         |
| Infra    | Docker Compose                                     |

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose v2
- Git
- (Optional) Node.js 24 and Python 3.13 for running tests outside containers

## Getting Started

```bash
# 1. Clone the repo
git clone <repository-url>
cd Donation-Genie

# 2. Create your environment file
cp .env.example .env

# 3. Build and start everything
make setup
```

Once running, open your browser:

| URL                                     | What you see             |
| --------------------------------------- | ------------------------ |
| http://localhost                        | Frontend app (via Nginx) |
| http://localhost/api/health/            | Backend health check     |
| http://localhost/api/schema/swagger-ui/ | API docs (Swagger)       |
| http://localhost:5173                   | Vite dev server (direct) |

## Makefile Commands

```
make help          Show all available commands
make setup         First-time setup (build + migrate + seed)
make up            Start all services
make down          Stop all services
make teardown      Stop all services and remove volumes
make logs          Tail logs from all services
make shell         Open Django shell
make migrate       Run Django migrations
make seed          Load seed data
make test          Run all tests (backend + frontend)
make test-backend  Run backend tests (pytest)
make test-frontend Run frontend tests (vitest)
make generate-api  Regenerate TypeScript types from OpenAPI schema
```

## Running Tests

```bash
# Run everything
make test

# Backend only (pytest)
make test-backend

# Frontend only (vitest)
make test-frontend
```

## Project Structure

```
Donation-Genie/
├── backend/                # Django API (Python 3.13)
│   ├── config/             # Settings, URLs, WSGI/ASGI
│   │   └── settings/       # Split settings: base, local, production
│   ├── apps/               # Django apps (layered architecture)
│   │   └── health/         # Health check endpoint
│   ├── tests/              # pytest test suite
│   ├── requirements/       # pip requirements (base, local)
│   ├── fixtures/           # Seed data
│   └── Dockerfile
├── frontend/               # React SPA (TypeScript)
│   ├── src/
│   │   ├── pages/          # Route page components
│   │   ├── components/ui/  # Reusable UI components
│   │   ├── api/            # API client (openapi-fetch)
│   │   ├── types/generated/# TypeScript types from OpenAPI
│   │   ├── hooks/          # Custom React hooks
│   │   ├── utils/          # Pure utility functions
│   │   ├── router.tsx      # TanStack Router config
│   │   └── main.tsx        # Entry point
│   ├── tests/              # vitest test suite
│   └── Dockerfile
├── nginx/                  # Reverse proxy
│   └── default.conf
├── docker-compose.yml      # Full stack orchestration (4 services)
├── Makefile                # Task runner
└── .env.example            # Environment variable template
```

## Architecture

### Backend (Django)

The backend follows a layered architecture:

- **urls.py** — Route registration
- **views.py** — Thin HTTP adapters (no business logic)
- **services.py** — Pure functions with business logic
- **models.py** — Data access layer

### Frontend (React)

- **TanStack Router** for type-safe routing
- **openapi-fetch** for type-safe API calls generated from the backend OpenAPI schema
- Run `make generate-api` after backend API changes to regenerate TypeScript types

### Shared Contracts

The backend generates an OpenAPI schema via drf-spectacular. The frontend consumes it:

```bash
# Regenerate frontend types from backend schema
make generate-api
```

## Environment Configuration

All configuration is via environment variables defined in `.env`. See `.env.example` for the full list with descriptions.

Key variables:

| Variable            | Purpose                                | Default                                            |
| ------------------- | -------------------------------------- | -------------------------------------------------- |
| `DJANGO_ENV`        | Settings module (`local`/`production`) | `local`                                            |
| `DATABASE_URL`      | PostgreSQL connection string           | `postgres://genie:changeme@db:5432/donation_genie` |
| `DJANGO_SECRET_KEY` | Cryptographic signing key              | `change-me-to-a-real-secret-key`                   |
| `VITE_API_URL`      | Frontend API base URL                  | `/api`                                             |

To switch to production settings:

```bash
DJANGO_ENV=production
DEBUG=False
```

## License

Private
