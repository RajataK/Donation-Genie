# Donation-Genie Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-26

## Active Technologies
- HCL (Terraform >= 1.9), Python 3.13 (backend Dockerfile), TypeScript 5.7 (frontend build) + Terraform AWS Provider ~> 5.0, terraform-aws-modules/vpc/aws ~> 5.0 (003-aws-serverless-iac)
- RDS PostgreSQL 17 (db.t4g.micro for dev), S3 (frontend assets + Terraform state) (003-aws-serverless-iac)
- Python 3.13 (backend) + Django 5.2 LTS, Django REST Framework 3.15, drf-spectacular, django-environ, psycopg (004-init-postgres-schema)
- PostgreSQL 17 (local via Docker Compose, production via AWS RDS) (004-init-postgres-schema)
- Python 3.13 + Django 5.2 LTS, Django REST Framework 3.15, psycopg (PostgreSQL adapter) (004-init-postgres-schema)
- PostgreSQL 17 (local via Docker, production via AWS RDS) (004-init-postgres-schema)

- TypeScript 5.7 (frontend), Python 3.13 (backend - unchanged) + React 19, Vite 6, TanStack Router 1.95, openapi-fetch 0.13, @playwright/test 1.58, @axe-core/playwright 4.11, eslint-plugin-jsx-a11y 6.10 (002-frontend-ui-boilerplate)
- N/A (placeholder data only; no backend changes) (002-frontend-ui-boilerplate)
- TypeScript 5.7 (frontend), Python 3.13 (backend — unchanged) + React 19, Vite 6, TanStack Router 1.95, openapi-fetch 0.13, @playwright/test 1.58, @axe-core/playwright 4.11, eslint-plugin-jsx-a11y 6.10 (002-frontend-ui-boilerplate)

- Python 3.13 (backend), TypeScript 5.x (frontend), Node.js 24 LTS (tooling) + Django 5.2 LTS, Django REST Framework 3.15, drf-spectacular, React 19, Vite 6, TanStack Router, openapi-typescript, openapi-fetch (001-init-project-boilerplate)

## Project Structure

```text
backend/
frontend/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.13 (backend), TypeScript 5.x (frontend), Node.js 24 LTS (tooling): Follow standard conventions

## Recent Changes
- 004-init-postgres-schema: Added Python 3.13 + Django 5.2 LTS, Django REST Framework 3.15, psycopg (PostgreSQL adapter)
- 004-init-postgres-schema: Added Python 3.13 (backend) + Django 5.2 LTS, Django REST Framework 3.15, drf-spectacular, django-environ, psycopg
- 003-aws-serverless-iac: Added HCL (Terraform >= 1.9), Python 3.13 (backend Dockerfile), TypeScript 5.7 (frontend build) + Terraform AWS Provider ~> 5.0, terraform-aws-modules/vpc/aws ~> 5.0



<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
