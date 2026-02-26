---
description: "Task list for Frontend UI Boilerplate feature"
---

# Tasks: Frontend UI Boilerplate

**Input**: Design documents from `/specs/002-frontend-ui-boilerplate/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: TDD is NON-NEGOTIABLE per constitution Principle I. Every user story phase writes failing tests FIRST, then implements to make them pass.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install test tooling, configure Playwright, ESLint, and create shared test fixtures

- [x] T001 Install Playwright, @axe-core/playwright, and eslint-plugin-jsx-a11y as devDependencies in frontend/package.json
- [x] T002 [P] Create Playwright configuration with 6 device profiles (Desktop Chrome, Desktop Firefox, Desktop Safari, Pixel 7, iPhone 14, iPad) and webServer pointing to Vite dev server in frontend/playwright.config.ts
- [x] T003 [P] Create ESLint flat config with jsx-a11y strict preset and TypeScript support in frontend/eslint.config.js
- [x] T004 [P] Create reusable AxeBuilder fixture with WCAG 2.1 AA tags (wcag2a, wcag2aa, wcag21a, wcag21aa) in frontend/e2e/fixtures/axe-test.ts
- [x] T005 Add npm scripts for Playwright test commands (test:e2e, test:e2e:ui, test:a11y, test:responsive) and ESLint (lint) in frontend/package.json

**Checkpoint**: Test infrastructure ready. `npx playwright test` and `npx eslint src/` both execute (even if no tests/source yet).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Design system, TypeScript interfaces, mock data, layout shell, and router. MUST complete before ANY user story.

**CRITICAL**: No user story work can begin until this phase is complete.

- [x] T006 Create design tokens CSS file with all color, typography, spacing, and breakpoint variables from wireframe in frontend/src/styles/tokens.css
- [x] T007 [P] Create global styles file with CSS reset, Google Fonts import (Fraunces, DM Sans), base body styles (18px text, 1.6 line-height), and prefers-reduced-motion media query in frontend/src/styles/global.css
- [x] T008 [P] Create TypeScript interfaces for all 10 entities (FoodBank, WishListItem, RecipeKit, RecipeIngredient, BasketItem, DonationBasket, SupermarketProduct, QRCodeFormat, DeliveryPreference, SupermarketPartner) per data-model.md in frontend/src/data/types.ts
- [x] T009 Create mock data files with placeholder data matching wireframe examples: food banks (3 entries), wish list items (6 items), recipe kits (3 kits), supermarket products, QR formats, delivery preferences, supermarket partners in frontend/src/data/mock-data.ts
- [x] T010 Create Button component (primary and secondary variants) with 44px min touch target and proper focus styles in frontend/src/components/ui/Button.tsx
- [x] T011 [P] Create Card component with hover effects and border styles matching wireframe in frontend/src/components/ui/Card.tsx
- [x] T012 [P] Create Badge component (urgent and active variants) with aria-label for urgency level in frontend/src/components/ui/Badge.tsx
- [x] T013 [P] Create Input component (text input with label association and placeholder styling) in frontend/src/components/ui/Input.tsx
- [x] T014 Create PageShell layout component with semantic landmarks (header, nav, main, footer) in frontend/src/components/layout/PageShell.tsx
- [x] T015 Create Navigation component with Donor Journey / Admin toggle matching wireframe nav bar, using aria-current for active state in frontend/src/components/layout/Navigation.tsx
- [x] T016 Configure TanStack Router with all 8 routes (/, /search, /food-bank/:id, /food-bank/:id/direct-items, /food-bank/:id/recipe-kits, /food-bank/:id/checkout, /admin, /admin/management) with placeholder page components in frontend/src/router.tsx
- [x] T017 Update App.tsx to wrap RouterProvider with PageShell layout and import global styles in frontend/src/App.tsx
- [x] T018 Import design tokens and global styles in frontend/src/main.tsx entry point

**Checkpoint**: Foundation ready. App renders with navigation, all routes resolve to placeholder pages, design tokens applied. User story implementation can now begin.

---

## Phase 3: User Story 1 - Donor Discovers Nearby Food Banks (Priority: P1) MVP

**Goal**: Donor enters postcode on landing page, sees food bank search results with AI summary and food bank cards.

**Independent Test**: Navigate to landing page, enter postcode, see results page with 3 food bank cards rendered from placeholder data.

### Tests for User Story 1 (TDD — RED phase)

> **Write these tests FIRST. They MUST FAIL before implementation begins.**

- [x] T019 [P] [US1] Write Playwright accessibility test for LandingPage: page has h1 with app name, labeled postcode input, search button with descriptive text, main landmark, no WCAG AA violations in frontend/e2e/accessibility/landing-page.spec.ts
- [x] T020 [P] [US1] Write Playwright accessibility test for SearchResultsPage: AI summary section with aria-label, food bank cards in list markup, urgency badges with aria-labels, keyboard-focusable cards, no WCAG AA violations in frontend/e2e/accessibility/search-results.spec.ts
- [x] T021 [P] [US1] Write Playwright navigation test: navigate to /, enter postcode, click search, verify redirect to /search with results; click food bank card, verify redirect to /food-bank/:id in frontend/e2e/navigation/donor-journey.spec.ts (US1 section)
- [x] T022 [P] [US1] Write Playwright responsive test for LandingPage and SearchResultsPage: verify layout at 375px, 768px, 1280px viewports — no horizontal overflow, cards stack on mobile in frontend/e2e/responsive/donor-pages.spec.ts (US1 section)

### Implementation for User Story 1 (TDD — GREEN phase)

- [x] T023 [US1] Create LandingPage with branded header (Donation Genie + tagline), postcode input with associated label, and search button that navigates to /search?postcode={value} in frontend/src/pages/donor/LandingPage.tsx
- [x] T024 [US1] Create FoodBankCard component displaying food bank name, distance, urgency Badge, families served count, top needs list, and select button in frontend/src/components/donor/FoodBankCard.tsx
- [x] T025 [US1] Create AISummary component displaying the AI-generated needs summary annotation with aria-label in frontend/src/components/donor/AISummary.tsx
- [x] T026 [US1] Create SearchResultsPage that reads postcode from query params, renders AISummary and list of FoodBankCards from mock data, with select action navigating to /food-bank/:id in frontend/src/pages/donor/SearchResultsPage.tsx
- [x] T027 [US1] Update router.tsx to wire LandingPage to / and SearchResultsPage to /search routes, replacing placeholder components

**Checkpoint**: User Story 1 complete. Landing → Search Results flow works. All US1 Playwright tests pass.

---

## Phase 4: User Story 2 - Donor Views Wish List and Chooses Donation Method (Priority: P1)

**Goal**: Donor sees food bank detail page with impact story, wish list items, and two donation method options.

**Independent Test**: Navigate to /food-bank/:id, verify wish list items with urgency badges, impact story, and two donation option cards render correctly.

### Tests for User Story 2 (TDD — RED phase)

- [x] T028 [P] [US2] Write Playwright accessibility test for FoodBankDetailPage: heading hierarchy, impact story section, wish list items with urgency in accessible name, donation options in role="group" with aria-label, no WCAG AA violations in frontend/e2e/accessibility/food-bank-detail.spec.ts
- [x] T029 [P] [US2] Write Playwright navigation test: from /food-bank/:id click "Donate Individual Items" → verify /food-bank/:id/direct-items; click "Create Recipe Kits" → verify /food-bank/:id/recipe-kits in frontend/e2e/navigation/donor-journey.spec.ts (US2 section)
- [x] T030 [P] [US2] Write Playwright responsive test for FoodBankDetailPage: wish list grid adapts columns at 375px/768px/1280px, donation option cards stack on mobile in frontend/e2e/responsive/donor-pages.spec.ts (US2 section)

### Implementation for User Story 2 (TDD — GREEN phase)

- [x] T031 [P] [US2] Create ImpactStory component with gradient background and heading per wireframe in frontend/src/components/donor/ImpactStory.tsx
- [x] T032 [P] [US2] Create WishListItemCard component displaying item name, urgency Badge, description in a Card with accessible urgency in frontend/src/components/donor/WishListItemCard.tsx
- [x] T033 [P] [US2] Create DonationOptionCard component for the two donation methods (icon, title, description, button) with recommended indicator on Recipe Kits in frontend/src/components/donor/DonationOptionCard.tsx
- [x] T034 [US2] Create FoodBankDetailPage composing food bank header, ImpactStory, wish list grid of WishListItemCards, and DonationOptionCard pair; reads :id param and uses mock data in frontend/src/pages/donor/FoodBankDetailPage.tsx
- [x] T035 [US2] Update router.tsx to wire FoodBankDetailPage to /food-bank/:id route

**Checkpoint**: User Story 2 complete. Food bank detail page with wish list and donation options renders. All US2 tests pass.

---

## Phase 5: User Story 3 - Donor Builds a Direct Item Donation (Priority: P2)

**Goal**: Donor selects individual items with quantity controls, sees a running donation basket with totals.

**Independent Test**: Navigate to /food-bank/:id/direct-items, adjust quantities, add items to basket, verify basket total updates, checkout button accessible.

### Tests for User Story 3 (TDD — RED phase)

- [x] T036 [P] [US3] Write Playwright accessibility test for DirectItemsPage: quantity inputs with aria-labels including item name, +/- buttons with aria-labels, basket total with aria-live="polite", checkout button disabled with aria-disabled when basket empty, no WCAG AA violations in frontend/e2e/accessibility/direct-items.spec.ts
- [x] T037 [P] [US3] Write Vitest component test for DonationBasket: adding items updates total, removing last item shows empty state, checkout disabled when empty in frontend/tests/components/DonationBasket.test.tsx
- [x] T038 [P] [US3] Write Playwright navigation test: add items, click "Proceed to Checkout" → verify /food-bank/:id/checkout in frontend/e2e/navigation/donor-journey.spec.ts (US3 section)
- [x] T039 [P] [US3] Write Playwright responsive test for DirectItemsPage: item grid and basket stack on mobile, quantity controls remain usable at 375px in frontend/e2e/responsive/donor-pages.spec.ts (US3 section)

### Implementation for User Story 3 (TDD — GREEN phase)

- [x] T040 [P] [US3] Create QuantityControl component with decrement button, number input, increment button, and add button; all with proper aria-labels including item name in frontend/src/components/donor/QuantityControl.tsx
- [x] T041 [P] [US3] Create DonationBasket component displaying selected items, quantities, unit prices, total cost, and "Proceed to Checkout" button with aria-live region for dynamic updates in frontend/src/components/donor/DonationBasket.tsx
- [x] T042 [US3] Create DirectItemsPage composing item cards with QuantityControl and DonationBasket; manage basket state with useState; disable checkout when basket empty in frontend/src/pages/donor/DirectItemsPage.tsx
- [x] T043 [US3] Update router.tsx to wire DirectItemsPage to /food-bank/:id/direct-items route

**Checkpoint**: User Story 3 complete. Direct item selection with interactive basket works. All US3 Playwright and Vitest tests pass.

---

## Phase 6: User Story 4 - Donor Selects an AI Recipe Kit (Priority: P2)

**Goal**: Donor sees AI-generated recipe kit cards and selects one to proceed to checkout.

**Independent Test**: Navigate to /food-bank/:id/recipe-kits, verify 3 recipe cards with all fields, click select navigates to checkout.

### Tests for User Story 4 (TDD — RED phase)

- [x] T044 [P] [US4] Write Playwright accessibility test for RecipeKitsPage: recipe cards keyboard-navigable, ingredient lists use semantic ul, aria-live region for kit selection, no WCAG AA violations in frontend/e2e/accessibility/recipe-kits.spec.ts
- [x] T045 [P] [US4] Write Playwright navigation test: click "Select This Kit" → verify /food-bank/:id/checkout in frontend/e2e/navigation/donor-journey.spec.ts (US4 section)
- [x] T046 [P] [US4] Write Playwright responsive test for RecipeKitsPage: recipe card grid adapts at 375px/768px/1280px in frontend/e2e/responsive/donor-pages.spec.ts (US4 section)

### Implementation for User Story 4 (TDD — GREEN phase)

- [x] T047 [P] [US4] Create RecipeCard component with image area (emoji icon), recipe title, servings/time metadata, ingredient list (ul), total cost, and select button in frontend/src/components/donor/RecipeCard.tsx
- [x] T048 [US4] Create RecipeKitsPage composing recipe intro, RecipeCard grid from mock data, and ImpactStory; selecting a kit navigates to /food-bank/:id/checkout in frontend/src/pages/donor/RecipeKitsPage.tsx
- [x] T049 [US4] Update router.tsx to wire RecipeKitsPage to /food-bank/:id/recipe-kits route

**Checkpoint**: User Story 4 complete. Recipe kit selection works. All US4 tests pass.

---

## Phase 7: User Story 5 - Donor Reviews Basket and Proceeds to Checkout (Priority: P2)

**Goal**: Donor sees checkout review with flow diagram, itemized basket, and complete/modify actions.

**Independent Test**: Navigate to /food-bank/:id/checkout, verify flow diagram, itemized products with prices, total, and both action buttons.

### Tests for User Story 5 (TDD — RED phase)

- [x] T050 [P] [US5] Write Playwright accessibility test for CheckoutPage: flow diagram with aria-label, basket items in semantic table or description list, primary action first in tab order, no WCAG AA violations in frontend/e2e/accessibility/checkout.spec.ts
- [x] T051 [P] [US5] Write Playwright navigation test: click "Modify Items" navigates back; "Complete Donation" shows confirmation or remains on page in frontend/e2e/navigation/donor-journey.spec.ts (US5 section)
- [x] T052 [P] [US5] Write Playwright responsive test for CheckoutPage: flow diagram goes vertical on mobile, basket remains readable at 375px in frontend/e2e/responsive/donor-pages.spec.ts (US5 section)

### Implementation for User Story 5 (TDD — GREEN phase)

- [x] T053 [P] [US5] Create FlowDiagram component showing 4 donation process steps with arrows, responsive vertical layout on mobile, with overall aria-label in frontend/src/components/donor/FlowDiagram.tsx
- [x] T054 [P] [US5] Create CheckoutBasket component displaying donation kit name, supermarket product list with prices, delivery cost, total, and delivery note in frontend/src/components/donor/CheckoutBasket.tsx
- [x] T055 [US5] Create CheckoutPage composing FlowDiagram, CheckoutBasket with mock supermarket products, "Complete Donation" primary button, and "Modify Items" secondary button in frontend/src/pages/donor/CheckoutPage.tsx
- [x] T056 [US5] Update router.tsx to wire CheckoutPage to /food-bank/:id/checkout route

**Checkpoint**: User Story 5 complete. Full donor journey (landing → checkout) navigable end-to-end. All US5 tests pass.

---

## Phase 8: User Story 6 - Admin Onboards a Food Bank (Priority: P3)

**Goal**: Admin sees onboarding page with upload zone, AI extraction preview, and confirm/edit actions.

**Independent Test**: Navigate to /admin, verify upload zone with format descriptions, AI-extracted items grid with categories, and action buttons.

### Tests for User Story 6 (TDD — RED phase)

- [x] T057 [P] [US6] Write Playwright accessibility test for OnboardingPage: upload zone has role="button" with aria-label, extracted items grid uses semantic list markup, action buttons have descriptive labels, no WCAG AA violations in frontend/e2e/accessibility/onboarding.spec.ts
- [x] T058 [P] [US6] Write Playwright responsive test for OnboardingPage: upload zone and items grid adapt at 375px/768px/1280px in frontend/e2e/responsive/admin-pages.spec.ts (US6 section)

### Implementation for User Story 6 (TDD — GREEN phase)

- [x] T059 [P] [US6] Create UploadZone component with dashed border, icon, description of accepted formats, choose file button, and email alternative; role="button" with aria-label in frontend/src/components/admin/UploadZone.tsx
- [x] T060 [P] [US6] Create ExtractedItemsPreview component displaying items grid with checkmark, item name, and category label from mock data in frontend/src/components/admin/ExtractedItemsPreview.tsx
- [x] T061 [US6] Create OnboardingPage composing welcome header, UploadZone, AI processing annotation, ExtractedItemsPreview, confirm/edit buttons, and next-steps ImpactStory in frontend/src/pages/admin/OnboardingPage.tsx
- [x] T062 [US6] Update router.tsx to wire OnboardingPage to /admin route

**Checkpoint**: User Story 6 complete. Admin onboarding page renders. All US6 tests pass.

---

## Phase 9: User Story 7 - Admin Manages QR Codes and Integration Settings (Priority: P3)

**Goal**: Admin sees QR code generator, delivery preferences, and supermarket partner settings.

**Independent Test**: Navigate to /admin/management, verify QR formats, delivery checkboxes, partner cards, and save/test buttons.

### Tests for User Story 7 (TDD — RED phase)

- [x] T063 [P] [US7] Write Playwright accessibility test for ManagementPage: checkboxes have associated labels, disabled partner cards have aria-disabled with explanation, sections use fieldset/legend, no WCAG AA violations in frontend/e2e/accessibility/management.spec.ts
- [x] T064 [P] [US7] Write Playwright responsive test for ManagementPage: QR section grid, partner cards adapt at 375px/768px/1280px in frontend/e2e/responsive/admin-pages.spec.ts (US7 section)

### Implementation for User Story 7 (TDD — GREEN phase)

- [x] T065 [P] [US7] Create QRCodeSection component with QR placeholder, format download options (poster PDF, sticker PNG, social media JPG), and "Generate All Formats" button in frontend/src/components/admin/QRCodeSection.tsx
- [x] T066 [P] [US7] Create IntegrationSettings component with Pepesto status card, delivery preference checkboxes with labels, delivery notes textarea, and supermarket partner cards (enabled/disabled) using fieldset/legend in frontend/src/components/admin/IntegrationSettings.tsx
- [x] T067 [US7] Create ManagementPage composing QRCodeSection, IntegrationSettings, and save/test action buttons from mock data in frontend/src/pages/admin/ManagementPage.tsx
- [x] T068 [US7] Update router.tsx to wire ManagementPage to /admin/management route

**Checkpoint**: User Story 7 complete. Admin management page renders. All US7 tests pass.

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Full end-to-end validation, edge cases, and final quality checks

- [x] T069 Write Playwright end-to-end navigation test covering complete donor journey: / → /search → /food-bank/:id → /food-bank/:id/direct-items → /food-bank/:id/checkout (and recipe kit path) in frontend/e2e/navigation/full-donor-journey.spec.ts
- [x] T070 [P] Write Playwright test for cross-journey navigation: switch between Donor Journey and Admin via Navigation component, verify correct routes and active states in frontend/e2e/navigation/cross-journey.spec.ts
- [x] T071 [P] Write Playwright test for edge cases: empty search results message, empty wish list message, empty basket with disabled checkout in frontend/e2e/navigation/edge-cases.spec.ts
- [x] T071b [P] Write Playwright test for text overflow edge case: long food bank names and item descriptions truncate with CSS ellipsis and full text is accessible (title attribute or expandable) in frontend/e2e/navigation/edge-cases.spec.ts
- [x] T072 Run ESLint with jsx-a11y strict across all frontend source: `npx eslint src/` must report zero errors
- [x] T073 Run full Playwright test suite across all 6 device profiles: `npx playwright test` must pass on all projects (Chromium, Firefox, WebKit, Pixel 7, iPhone 14, iPad)
- [x] T074 Run Vitest suite: `npx vitest run` must pass all component tests
- [x] T075 Verify visual fidelity by comparing each rendered page against wireframe screenshots at desktop (1280px) viewport

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in priority order (P1 → P2 → P3)
  - US1 and US2 (both P1) can run in parallel after Foundational
  - US3, US4, US5 (all P2) can run in parallel after Foundational
  - US6 and US7 (both P3) can run in parallel after Foundational
- **Polish (Phase 10)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational — No dependencies on other stories
- **US2 (P1)**: Can start after Foundational — No dependencies on other stories
- **US3 (P2)**: Can start after Foundational — independently testable (uses mock data for basket)
- **US4 (P2)**: Can start after Foundational — independently testable (uses mock data for recipe kits)
- **US5 (P2)**: Can start after Foundational — independently testable (uses mock data for checkout basket)
- **US6 (P3)**: Can start after Foundational — independently testable (admin journey separate from donor)
- **US7 (P3)**: Can start after Foundational — independently testable (admin journey separate from donor)

### Within Each User Story (TDD Order)

1. Tests (Playwright E2E + a11y + responsive) MUST be written and FAIL before implementation
2. Components before pages
3. Pages before router wiring
4. Story complete and all tests passing before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002, T003, T004)
- All Foundational UI primitives marked [P] can run in parallel (T010-T013)
- All test tasks within a user story marked [P] can run in parallel
- All component tasks within a user story marked [P] can run in parallel
- US1 and US2 can run in parallel (both P1, no shared dependencies)
- US3, US4, US5 can run in parallel (all P2, no shared dependencies)
- US6 and US7 can run in parallel (both P3, no shared dependencies)

---

## Parallel Example: User Story 1

```bash
# Launch all US1 tests together (RED phase):
Task: "Playwright a11y test for LandingPage in e2e/accessibility/landing-page.spec.ts"
Task: "Playwright a11y test for SearchResultsPage in e2e/accessibility/search-results.spec.ts"
Task: "Playwright navigation test in e2e/navigation/donor-journey.spec.ts (US1)"
Task: "Playwright responsive test in e2e/responsive/donor-pages.spec.ts (US1)"

# Launch US1 components together (GREEN phase):
Task: "Create FoodBankCard in src/components/donor/FoodBankCard.tsx"
Task: "Create AISummary in src/components/donor/AISummary.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1 (LandingPage + SearchResultsPage)
4. **STOP and VALIDATE**: All US1 Playwright tests pass, ESLint clean
5. Deploy/demo if ready — donor can search for food banks

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 (Landing + Search) → Test independently → Demo (MVP!)
3. Add US2 (Food Bank Detail) → Test independently → Demo
4. Add US3 + US4 + US5 (Direct Items + Recipe Kits + Checkout) → Full donor journey → Demo
5. Add US6 + US7 (Admin pages) → Complete platform → Demo
6. Polish → Final quality validation

### Parallel Team Strategy

With multiple developers after Foundational is done:

- Developer A: US1 (Landing + Search) and US3 (Direct Items)
- Developer B: US2 (Food Bank Detail) and US4 (Recipe Kits)
- Developer C: US5 (Checkout) and US6 + US7 (Admin pages)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- TDD: Verify tests FAIL before implementing (Red-Green-Refactor per constitution Principle I)
- Commit after each TDD cycle (test → implementation → refactor)
- Stop at any checkpoint to validate story independently
- All Playwright tests use the shared AxeBuilder fixture from frontend/e2e/fixtures/axe-test.ts
- Mock data in frontend/src/data/mock-data.ts is shared across all stories
