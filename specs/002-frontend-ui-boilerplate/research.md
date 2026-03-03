# Research: Frontend UI Boilerplate

**Feature**: 002-frontend-ui-boilerplate
**Date**: 2026-02-26

## R1: Accessibility Testing Framework

**Decision**: Playwright with @axe-core/playwright for E2E accessibility testing; eslint-plugin-jsx-a11y for static analysis

**Rationale**:
- Playwright is the user's explicit requirement and is the most popular modern E2E testing framework
- @axe-core/playwright (v4.11) is the most widely adopted accessibility testing engine (used by Google, Microsoft, US government sites), integrating directly into Playwright tests via AxeBuilder
- axe-core can automatically detect ~57% of WCAG violations; remaining issues require manual testing
- eslint-plugin-jsx-a11y (v6.10) catches accessibility issues at development time through static JSX analysis, using the `strict` preset for maximum enforcement
- Combined approach covers both build-time (lint) and run-time (E2E) accessibility validation

**Alternatives Considered**:
- Pa11y: Simpler but less flexible; no native Playwright integration; smaller community
- Lighthouse CI: Good for audits but not granular per-page testing; harder to integrate into test suites
- jest-axe: Only works with jsdom (no real browser rendering); misses CSS-related accessibility issues
- Storybook a11y addon: Useful for component-level but doesn't test page-level navigation flows

## R2: WCAG Compliance Level

**Decision**: WCAG 2.1 AA as baseline, with enhanced AAA targets for body text contrast (7:1 ratio) and touch target sizes (44x44px minimum)

**Rationale**:
- WCAG 2.1 AA is the legal standard in the UK (Equality Act 2010, Public Sector Bodies Accessibility Regulations 2018) and the accepted industry minimum
- Given the target audience includes older users, enhanced contrast (AAA 7:1 for body text) addresses age-related vision decline
- 44x44px touch targets (WCAG 2.2 AAA) accommodate reduced fine motor control in older users
- Full AAA compliance across all criteria is impractical (e.g., sign language interpretation), so selective AAA enhancements are more effective

**Alternatives Considered**:
- WCAG 2.1 AA only: Insufficient for older-user audience; minimum legal requirement but not optimal
- Full WCAG 2.2 AAA: Impractical to achieve across all criteria; selective AAA targets are more effective

## R3: Typography and Font Sizing Strategy

**Decision**: Body text at 18px (1.125rem) minimum, headings using Fraunces serif at 2rem+ (h1) / 1.5rem+ (h2), all sizes in rem units, line-height 1.6

**Rationale**:
- Wireframe uses Fraunces (serif, headings) and DM Sans (sans-serif, body) — both Google Fonts with good readability
- 18px body text exceeds the standard 16px minimum and is the recommended size for older users per NNGroup research
- rem units ensure text respects browser zoom settings (WCAG 1.4.4 Resize Text requirement)
- Line-height 1.6 matches the wireframe and exceeds the WCAG 1.4.12 minimum of 1.5
- DM Sans at 18px has excellent x-height ratio for readability

**Alternatives Considered**:
- 16px body text: Standard web default but suboptimal for older users
- px units: Would break browser zoom accessibility; violates WCAG 1.4.4
- System fonts only: Would lose the branded Fraunces/DM Sans identity from the wireframe

## R4: Color Contrast Verification

**Decision**: Use wireframe color tokens with verified contrast ratios; adjust text-light (#5A5A5A) usage to meet AA minimum

**Rationale**:
- Primary text (#1A1A1A) on background (#FDFBF7): ~17.5:1 contrast ratio — exceeds AAA (7:1)
- Primary color (#2D5F4C) on white (#FFFFFF): ~6.5:1 contrast ratio — exceeds AA (4.5:1)
- Text-light (#5A5A5A) on background (#FDFBF7): ~5.5:1 contrast ratio — passes AA (4.5:1) but not AAA; acceptable for secondary/supplementary text at 18px+ (large text AA threshold is 3:1)
- Accent (#E8956B) on white: ~2.7:1 — fails for text; must only be used for decorative elements, backgrounds, or paired with dark text
- Badge-urgent red (#C53030) on light red (#FFE5E5): ~5.9:1 — passes AA

**Alternatives Considered**:
- Darkening text-light to meet AAA: Would deviate from wireframe design; acceptable since secondary text is used at 18px+ (large text threshold)
- Custom high-contrast theme: Overengineering for boilerplate; can be added later

## R5: Responsive Design Strategy

**Decision**: CSS Grid and Flexbox with mobile-first breakpoints at 375px (mobile), 768px (tablet), 1024px (desktop), 1400px (max-width container)

**Rationale**:
- Wireframe already specifies responsive behavior (flow diagrams go vertical on mobile, grid layouts adapt)
- Mobile-first approach ensures the simplest layout is the default, progressively enhancing for larger screens
- These breakpoints match the most common device categories and the wireframe's max-width of 1400px
- CSS Grid for card layouts (food bank results, wish list items, recipe kits) naturally handles responsive columns via `auto-fit` and `minmax()`
- No CSS framework needed — the design system is simple enough to implement with modern CSS

**Alternatives Considered**:
- Tailwind CSS: Adds build complexity and learning curve; the wireframe design is straightforward enough for custom CSS
- CSS Modules: Good for scoping but adds import boilerplate; CSS custom properties with BEM-like naming is simpler for this scope
- Styled Components / Emotion: Runtime CSS-in-JS adds bundle size; unnecessary for static boilerplate

## R6: Component Architecture

**Decision**: Flat component hierarchy with domain-based grouping (ui primitives, donor components, admin components); no external component library

**Rationale**:
- The wireframe defines ~15 distinct component types that are custom to this design (no standard library matches the aesthetic)
- UI primitives (Button, Card, Badge, Input) are simple enough to build from scratch with the wireframe's CSS
- Domain grouping (donor/admin) matches the two journeys and makes code ownership clear
- No state management library needed — placeholder data is static; React's built-in useState suffices for basket interactions

**Alternatives Considered**:
- Radix UI / Headless UI: Good for accessibility but adds dependency for ~15 simple components; would still need full custom styling
- Component library (MUI, Ant Design): Too opinionated; would fight the wireframe's custom aesthetic
- Atomic Design structure (atoms/molecules/organisms): Over-architecture for 15 components; simpler flat structure is sufficient

## R7: Routing Architecture

**Decision**: Extend existing TanStack Router setup with nested routes for donor journey and admin section; file-based organization matching page structure

**Rationale**:
- TanStack Router v1.95 is already configured in the project with a root route and home page
- Nested routes naturally model the two journeys: `/` (donor) and `/admin` (admin)
- Donor journey routes: `/` (landing), `/search` (results), `/food-bank/:id` (detail), `/food-bank/:id/direct-items`, `/food-bank/:id/recipe-kits`, `/food-bank/:id/checkout`
- Admin routes: `/admin` (onboarding), `/admin/management`
- Route parameters (`:id`) enable future dynamic data fetching without route restructuring

**Alternatives Considered**:
- Flat routes without nesting: Would lose the hierarchical relationship between food bank and its sub-pages
- Hash routing: No SEO benefit and unusual for modern SPAs
- Separate router for admin: Unnecessary complexity; single router with route grouping is sufficient

## R8: Playwright Test Organization

**Decision**: E2E tests in `frontend/e2e/` with three categories: accessibility, responsive, and navigation; shared AxeBuilder fixture; Playwright config at `frontend/playwright.config.ts`

**Rationale**:
- Separating E2E tests from unit tests (in `frontend/tests/`) keeps test concerns clear
- Three test categories map to the three testing requirements: accessibility (WCAG compliance), responsive (viewport adaptation), navigation (user flow)
- Shared AxeBuilder fixture with WCAG 2.1 AA tags ensures consistent accessibility scanning across all page tests
- Playwright projects configured for Desktop Chrome, Desktop Firefox, Desktop Safari, Mobile Chrome (Pixel 7), Mobile Safari (iPhone 14), and Tablet (iPad)
- Web server configuration points to Vite dev server on port 5173

**Alternatives Considered**:
- Tests at project root: Would complicate the frontend build/test scripts; keeping tests with their source is cleaner
- Single test file per journey: Would become unwieldy; per-page test files are more maintainable
- Cypress: User explicitly requested Playwright; Playwright has better multi-browser and mobile support

## R9: TDD Workflow for Frontend UI

**Decision**: Red-Green-Refactor with Playwright E2E tests as the primary "Red" phase; Vitest component tests for interactive components (basket, quantity controls); tests written per-page before page implementation

**Rationale**:
- Constitution Principle I mandates strict TDD with tests failing before implementation
- For a UI boilerplate feature, Playwright E2E tests are the most meaningful "Red" tests because they verify page structure, navigation, accessibility, and responsiveness against real browser rendering
- Vitest component tests complement E2E for interactive logic (basket state, quantity increment/decrement) where unit-level verification is faster and more precise
- Per-page test files (e.g., `e2e/accessibility/landing-page.spec.ts`) allow implementing one page at a time following TDD
- eslint-plugin-jsx-a11y provides continuous "Red" feedback during development — a11y lint errors are effectively failing tests that guide implementation

**Alternatives Considered**:
- Vitest-only TDD (jsdom rendering): Would miss CSS-related accessibility issues, responsive layout, and real navigation behavior; insufficient for WCAG compliance verification
- Storybook-driven development: Good for component isolation but doesn't test page-level concerns (routing, landmarks, focus management); adds tooling overhead
- Manual testing then retroactive tests: Violates constitution Principle I; tests would not drive the design
