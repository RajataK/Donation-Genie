.PHONY: help setup up down teardown logs shell migrate seed test test-backend test-frontend generate-api
.DEFAULT_GOAL := help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## First-time setup: build images, run migrations, seed data
	docker compose build
	docker compose up -d db
	@echo "Waiting for database..."
	@sleep 5
	docker compose up -d django
	@sleep 5
	docker compose exec django python manage.py migrate --noinput
	docker compose exec django python manage.py loaddata fixtures/seed.json || true
	docker compose up -d
	@echo "Setup complete. Visit http://localhost"

up: ## Start all services
	docker compose up -d

down: ## Stop all services
	docker compose down

teardown: ## Stop all services and remove volumes
	docker compose down -v

logs: ## Tail logs from all services
	docker compose logs -f

shell: ## Open Django shell
	docker compose exec django python manage.py shell

migrate: ## Run Django migrations
	docker compose exec django python manage.py migrate --noinput

seed: ## Load seed data
	docker compose exec django python manage.py loaddata fixtures/seed.json

test: test-backend test-frontend ## Run all tests

test-backend: ## Run backend tests (pytest)
	cd backend && (test -d .venv || python3 -m venv .venv) && .venv/bin/pip install -q -r requirements/local.txt > /dev/null 2>&1 && .venv/bin/python -m pytest

test-frontend: ## Run frontend tests (vitest)
	cd frontend && npx vitest run

generate-api: ## Regenerate TypeScript types from OpenAPI schema
	cd frontend && npm run generate:api
