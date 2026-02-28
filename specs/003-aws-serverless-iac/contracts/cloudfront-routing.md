# Contract: CloudFront URL Routing

**Feature**: 003-aws-serverless-iac
**Date**: 2026-02-27

## Overview

A single CloudFront distribution serves both the frontend and backend under one domain. The routing is determined by URL path pattern matching.

## URL Routing Rules

| Path Pattern | Origin | Cache Policy | Behavior |
|-------------|--------|-------------|----------|
| `/api/*` | ALB (internal) | CachingDisabled | All HTTP methods forwarded. Headers, cookies, query strings forwarded (except Host). |
| `/*` (default) | S3 Bucket | CachingOptimized | GET/HEAD only. Static assets cached at edge. |

## Frontend (Default Behavior)

**Base URL**: `https://<distribution-id>.cloudfront.net/`

- All requests not matching `/api/*` are served from the S3 bucket.
- The S3 bucket contains the built React SPA (`index.html`, JS bundles, CSS, images).
- Client-side routes (e.g., `/search`, `/admin`, `/food-bank/123`) are handled by returning `index.html` for 403/404 responses from S3 (custom error response configuration).
- Static assets include content hashes in filenames and are cached with long TTL.
- Compression (gzip/brotli) is enabled.

**SPA Routing Error Responses**:

| S3 Error Code | CloudFront Response Code | Response Page Path |
|---------------|--------------------------|-------------------|
| 403 | 200 | `/index.html` |
| 404 | 200 | `/index.html` |

## Backend API (Ordered Behavior)

**Base URL**: `https://<distribution-id>.cloudfront.net/api/`

- All requests to `/api/*` are forwarded to the internal ALB.
- The ALB routes to ECS Fargate tasks running Django.
- All HTTP methods are allowed: GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE.
- No caching at CloudFront edge (dynamic API responses).
- The `Host` header is rewritten to the ALB's DNS name (via `AllViewerExceptHostHeader` origin request policy).
- All other headers, cookies, and query strings are forwarded to the backend.

**Known API Endpoints** (existing):

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health/` | GET | Health check (used by ALB) |
| `/api/schema/` | GET | OpenAPI 3.0 schema |
| `/api/schema/swagger-ui/` | GET | Interactive API documentation |

## Protocol

- Viewer protocol policy: `redirect-to-https` on all behaviors.
- Origin protocol (ALB): HTTPS (443) — ALB listener on 443 with CloudFront managed prefix list.
- Origin protocol (S3): S3 REST API via OAC (not website endpoint).

## CORS

No CORS configuration is needed. Both frontend and backend are served from the same CloudFront domain, eliminating cross-origin issues.
