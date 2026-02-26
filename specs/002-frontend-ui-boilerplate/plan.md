# Implementation Plan: Frontend UI Boilerplate

**Branch**: `002-frontend-ui-boilerplate` | **Date**: 2026-02-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-frontend-ui-boilerplate/spec.md`

## Summary

Build the complete frontend UI shell for Donation Genie based on the wireframes in `donation-genie-wireframes-v1.html`. This covers 7 page layouts across two journeys (Donor and Admin) using React 19 with TanStack Router, implementing the full navigation flow with static/placeholder data. The frontend follows WCAG 2.1 AA accessibility standards with enhanced considerations for older users (larger touch targets, high contrast, simple navigation). All pages are responsive (desktop, tablet, mobile). Testing follows strict TDD: Playwright with @axe-core/playwright for E2E and accessibility tests, Vitest for component tests, eslint-plugin-jsx-a11y for static analysis. Tests are written first and must fail before implementation.

## Technical Context

**Language/Version**: TypeScript 5.7 (frontend), Python 3.13 (backend — unchanged)
**Primary Dependencies**: React 19, Vite 6, TanStack Router 1.95, openapi-fetch 0.13, @playwright/test 1.58, @axe-core/playwright 4.11, eslint-plugin-jsx-a11y 6.10
**Storage**: N/A (placeholder data only; no backend changes)
**Testing**: Vitest (unit/component — existing), Playwright + @axe-core/playwright (E2E + accessibility — new)
**Target Platform**: Web (desktop 1280px+, tablet 768px+, mobile 375px+)
**Project Type**: Web application (frontend-only changes)
**Performance Goals**: All pages render within 1 second on standard broadband; view transitions under 300ms
**Constraints**: WCAG 2.1 AA minimum; 44x44px minimum touch targets; body text 18px+; color contrast 4.5:1 minimum (7:1 target for body text)
**Scale/Scope**: 7 page layouts, 2 navigation journeys, ~15 reusable components

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Phase 0 Gate Evaluation

| Principle | Status | Evidence |
|-----------|--------|----------|
| **I. TDD (NON-NEGOTIABLE)** | PASS | Plan mandates Playwright E2E/a11y tests + Vitest component tests written before implementation. Tasks template enforces Red-Green-Refactor ordering. Acceptance scenarios from spec map directly to executable Playwright tests. |
| **II. Proven Solutions** | PASS | All chosen dependencies are battle-tested: React 19 (most popular UI library), TanStack Router (standard React router), Playwright (most popular E2E framework), axe-core (industry-standard a11y engine used by Google/Microsoft), eslint-plugin-jsx-a11y (most popular JSX a11y linter). No custom abstractions where libraries exist. |
| **III. No Premature Optimization** | PASS | Using static placeholder data — no caching, no state management library, no API layer beyond existing openapi-fetch. CSS custom properties for theming instead of CSS-in-JS runtime. No design patterns beyond what the current 15 components require. |

### Development Standards Check

| Standard | Status | Evidence |
|----------|--------|----------|
| **Accessibility** | PASS | WCAG 2.1 AA baseline enforced via @axe-core/playwright and eslint-plugin-jsx-a11y strict. Enhanced AAA targets for body text contrast and touch targets. Semantic HTML landmarks required per route contracts. |
| **Layered architecture** | N/A | No backend changes in this feature. |
| **Contract-first** | N/A | No new API endpoints. Existing OpenAPI schema unchanged. |
| **Responsive design** | PASS | Playwright projects configured for 6 device profiles (Desktop Chrome/Firefox/Safari, Pixel 7, iPhone 14, iPad). CSS breakpoints at 375/768/1024/1400px. |

### Quality Gates Readiness

| Gate | Status | How satisfied |
|------|--------|---------------|
| All tests pass | PLANNED | Vitest, Playwright (E2E, a11y, responsive) configured in plan |
| Linting clean | PLANNED | ESLint with jsx-a11y strict preset configured |
| TDD evidence | PLANNED | Task ordering mandates tests before implementation |
| No [NEEDS CLARIFICATION] | PASS | Spec has zero unresolved markers |
| Accessibility audit | PLANNED | @axe-core/playwright WCAG 2.1 AA scan on all 8 routes |

**Gate result: PASS — no violations. Proceeding to Phase 0.**

### Post-Phase 1 Re-evaluation

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. TDD** | PASS | Route contracts in `contracts/ui-routes.md` define per-page accessibility requirements that map to testable assertions. Data model interfaces in `data-model.md` are TypeScript types — type checking serves as a continuous test. |
| **II. Proven Solutions** | PASS | Research in `research.md` documents 8 decisions with rationale. Every decision cites community precedent. Alternatives rejected with specific reasoning. |
| **III. No Premature Optimization** | PASS | Data model uses simple TypeScript interfaces — no ORM, no state management, no factory patterns. Route structure is flat with one level of nesting. No abstractions beyond what the 7 pages require. |

**Post-design gate result: PASS — no violations.**

## Project Structure

### Documentation (this feature)

```text
specs/002-frontend-ui-boilerplate/
├── plan.md              # This file
├── research.md          # Phase 0 output (8 research decisions)
├── data-model.md        # Phase 1 output (10 TypeScript interfaces)
├── quickstart.md        # Phase 1 output (setup, commands, design tokens)
├── contracts/
│   └── ui-routes.md     # Phase 1 output (8 route contracts with a11y specs)
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── components/
│   │   ├── ui/              # Design system primitives (Button, Card, Badge, Input, etc.)
│   │   ├── layout/          # Layout components (Header, Navigation, PageShell)
│   │   ├── donor/           # Donor journey components (FoodBankCard, WishListItem, RecipeCard, DonationBasket, FlowDiagram)
│   │   └── admin/           # Admin journey components (UploadZone, QRCodeSection, IntegrationSettings)
│   ├── pages/
│   │   ├── donor/           # LandingPage, SearchResultsPage, FoodBankDetailPage, DirectItemsPage, RecipeKitsPage, CheckoutPage
│   │   └── admin/           # OnboardingPage, ManagementPage
│   ├── data/                # Static placeholder/mock data
│   ├── hooks/               # Custom React hooks
│   ├── styles/              # Global styles, CSS variables, design tokens
│   ├── router.tsx           # TanStack Router configuration (updated)
│   ├── api/                 # API client (existing, unchanged)
│   ├── App.tsx              # Root component (existing, updated)
│   └── main.tsx             # Entry point (existing, unchanged)
│
├── e2e/
│   ├── fixtures/
│   │   └── axe-test.ts      # Reusable AxeBuilder fixture (WCAG 2.1 AA tags)
│   ├── accessibility/       # Per-page a11y tests (@a11y tag)
│   ├── responsive/          # Viewport adaptation tests (@responsive tag)
│   └── navigation/          # End-to-end user flow tests
│
├── tests/                   # Vitest unit/component tests (existing dir)
├── eslint.config.js         # ESLint with jsx-a11y strict (new)
├── playwright.config.ts     # Playwright multi-browser/viewport config (new)
└── package.json             # Updated dependencies
```

**Structure Decision**: Extends the existing `frontend/` web application structure from `001-init-project-boilerplate`. Components organized by domain (ui primitives, donor journey, admin journey). E2E tests in `frontend/e2e/` separated from unit tests in `frontend/tests/`. No backend changes.

## Complexity Tracking

> **Foundational UI primitives without preceding unit tests (Phase 2: T010–T015)**
> Constitution Principle I mandates "Tests MUST fail before any production code
> is written for that behavior." The 6 foundational components (Button, Card,
> Badge, Input, PageShell, Navigation) are implemented in Phase 2 before any
> explicit test tasks. This is justified by research decision R9: for a UI
> boilerplate feature, Playwright E2E tests are the most meaningful TDD
> mechanism because they verify components in-context (page structure,
> accessibility, responsiveness, real browser rendering). Each component's
> behavior is tested when the first user story that uses it enters its RED
> phase (Phase 3+). Simple presentational primitives with no interactive logic
> do not benefit from isolated unit tests that would duplicate E2E assertions.
> Interactive components (DonationBasket, QuantityControl) DO have dedicated
> Vitest tests per R9.
