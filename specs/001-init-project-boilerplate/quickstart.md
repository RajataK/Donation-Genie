# Quickstart: Donation Genie

## Prerequisites

- Docker and Docker Compose (v2) installed
- Git installed
- (Optional) Node.js 24 and Python 3.13 for local development
  outside containers

## 1. Clone and Setup

```bash
git clone <repository-url>
cd Donation-Genie
cp .env.example .env
```

## 2. Start All Services

```bash
make up
```

This starts PostgreSQL, runs Django migrations, seeds the database,
starts the Django dev server, the Vite dev server, and the Nginx
reverse proxy.

## 3. Verify

Open your browser:

| URL                          | Service                  |
|------------------------------|--------------------------|
| http://localhost              | Frontend (via Nginx)     |
| http://localhost/api/health/  | Backend health check     |
| http://localhost:5173         | Vite dev server (direct) |

Run the health check from the terminal:

```bash
curl http://localhost/api/health/
```

Expected response:

```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0",
  "timestamp": "2026-02-26T12:00:00Z"
}
```

## 4. Run Tests

```bash
# All tests (frontend + backend)
make test

# Backend only
make test-backend

# Frontend only
make test-frontend
```

## 5. Stop Services

```bash
make down
```

## 6. Other Commands

```bash
make help          # List all available commands
make setup         # First-time setup (build + migrate + seed)
make migrate       # Run Django migrations
make seed          # Load seed data
make logs          # Tail all service logs
make shell         # Open Django shell
make generate-api  # Regenerate TypeScript types from OpenAPI
```

## Project Layout

```text
Donation-Genie/
├── backend/               # Django project (Python 3.13)
│   ├── config/            # Django settings, URLs, WSGI
│   │   └── settings/      # Split: base.py, local.py
│   ├── apps/              # Django apps (layered: urls, views,
│   │   └── health/        #   services, models)
│   ├── tests/             # pytest tests
│   ├── requirements/      # Pip requirements (base, local)
│   ├── manage.py
│   └── Dockerfile
├── frontend/              # React + Vite (TypeScript)
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   │   └── ui/        # Base component library
│   │   ├── pages/         # Route page components
│   │   ├── api/           # API client (generated from OpenAPI)
│   │   ├── types/         # TypeScript types (generated/)
│   │   ├── hooks/         # Custom React hooks
│   │   ├── utils/         # Pure utility functions
│   │   ├── test/          # Test setup
│   │   ├── router.tsx     # TanStack Router config
│   │   └── main.tsx       # Entry point
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── nginx/                 # Reverse proxy config
│   └── default.conf
├── docker-compose.yml     # Full stack orchestration
├── Makefile               # Task runner
├── .env.example           # Environment variable template
└── specs/                 # Feature specifications
```

## Adding a New Backend Endpoint

1. Create a Django app or add to an existing one
2. Define the model in `models.py`
3. Write business logic in `services.py` (pure functions)
4. Create a serializer in `serializers.py`
5. Add a thin view in `views.py` that calls the service
6. Register URL patterns in `urls.py`
7. Include the app URLs in `config/urls.py`
8. Regenerate TypeScript types: `make generate-api`

## Adding a New Frontend Page

1. Create a page component in `frontend/src/pages/`
2. Add the route to the route tree in `frontend/src/router.tsx`
3. Import generated API types from `frontend/src/types/generated/`
4. Use the API client from `frontend/src/api/client.ts`
