# Research: Frontend Food Bank Data Fetch

## Decision 1: Frontend Data Fetching Library

**Decision**: TanStack Query v5 (`@tanstack/react-query`)
**Rationale**: User explicitly requested TanStack Query. It is the industry-standard React data fetching/caching library with active maintenance, excellent documentation, and wide community adoption. Works alongside the existing `openapi-fetch` client (TanStack Query manages caching/state, openapi-fetch handles the HTTP call).
**Alternatives considered**:
- SWR: Lighter but less feature-rich; user specifically requested TanStack Query
- Raw `useEffect` + `fetch`: No caching, no error/loading state management — violates FR-005

## Decision 2: Backend API Pattern

**Decision**: DRF `ListAPIView` with `ModelSerializer` for the food bank list endpoint
**Rationale**: The project already uses Django REST Framework with drf-spectacular. A `ListAPIView` is the simplest DRF generic view for read-only list endpoints. `ModelSerializer` auto-generates serialization from the existing `FoodBank` model. This follows the constitution's "Proven Solutions" principle and the "Layered Architecture" standard (thin view, serializer handles data shaping).
**Alternatives considered**:
- `ModelViewSet`: Overkill — we only need list, not CRUD
- `APIView` with manual serialization: More code, less DRF convention
- Function-based view: Works but doesn't leverage DRF generics

## Decision 3: Frontend-Backend Communication During Development

**Decision**: Vite dev server proxy to Django backend
**Rationale**: The frontend `apiClient` uses `baseUrl: "/api"` (relative path). Adding a Vite proxy for `/api` to `http://localhost:8000` avoids CORS configuration entirely during development. This is simpler than adding `django-cors-headers` and matches the existing `apiClient` setup.
**Alternatives considered**:
- `django-cors-headers`: Adds a dependency and configuration; proxy is simpler for dev
- Hardcoded absolute URL: Breaks deployment flexibility

## Decision 4: Where to Trigger the Fetch

**Decision**: Create a `FoodBankLogger` component that uses the `useFoodBanks` hook and logs data via `useEffect`. Render it in the root layout or landing page.
**Rationale**: Keeps the fetch logic in a dedicated hook (`useFoodBanks`) that can be reused by future UI features. The logger component is temporary (per spec assumptions) and can be removed cleanly. Triggering on app load satisfies FR-003.
**Alternatives considered**:
- Fetch in `App.tsx` directly: Mixes concerns; harder to remove later
- Route loader: TanStack Router loaders would require different setup and don't use TanStack Query's caching

## Decision 5: OpenAPI Schema + Type Generation

**Decision**: Regenerate `api.d.ts` from the updated OpenAPI schema after adding the food bank endpoint, then use the generated types with `openapi-fetch` inside the TanStack Query hook.
**Rationale**: The project follows contract-first API development (constitution requirement). The `generate:api` script already exists in `package.json`. Using generated types ensures frontend-backend type safety.
**Alternatives considered**:
- Manual TypeScript types: Diverges from contract-first principle; types can drift from API
- Skip type generation: Violates constitution's contract-first standard
