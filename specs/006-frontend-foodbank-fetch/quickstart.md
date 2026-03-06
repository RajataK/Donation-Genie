# Quickstart: Frontend Food Bank Data Fetch

## Prerequisites

- Docker & Docker Compose (for PostgreSQL)
- Python 3.13+ with backend virtualenv activated
- Node.js 24 LTS with frontend dependencies installed

## Setup

### 1. Start the database

```bash
docker compose up -d db
```

### 2. Run backend migrations and seed data

```bash
cd backend
python manage.py migrate
python manage.py loaddata apps/foodbanks/fixtures/*.json
```

### 3. Start the backend

```bash
cd backend
python manage.py runserver
```

### 4. Install frontend dependencies (includes new TanStack Query)

```bash
cd frontend
npm install
```

### 5. Regenerate API types from OpenAPI schema

```bash
cd frontend
npm run generate:api
```

### 6. Start the frontend

```bash
cd frontend
npm run dev
```

### 7. Verify

1. Open `http://localhost:5173` in a browser
2. Open browser developer tools (F12)
3. Check the Console tab — food bank data should be logged

## Running Tests

### Backend

```bash
cd backend
pytest apps/foodbanks/tests/
```

### Frontend

```bash
cd frontend
npm test
```
