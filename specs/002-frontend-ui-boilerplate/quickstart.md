# Quickstart: Frontend UI Boilerplate

**Feature**: 002-frontend-ui-boilerplate
**Date**: 2026-02-26

## Prerequisites

- Node.js 24 LTS
- npm (bundled with Node.js)
- Git

## Setup

```bash
# 1. Ensure you're on the feature branch
git checkout 002-frontend-ui-boilerplate

# 2. Install frontend dependencies (includes new Playwright and a11y packages)
cd frontend
npm install

# 3. Install Playwright browsers
npx playwright install

# 4. Start the dev server
npm run dev
```

The frontend dev server starts at `http://localhost:5173`.

## Development Workflow

### Running the app

```bash
# Dev server with hot reload
cd frontend && npm run dev

# Or via Docker (full stack including backend/nginx)
make up
```

### Running tests

```bash
# Unit/component tests (Vitest)
cd frontend && npm test

# E2E tests (Playwright - requires dev server running)
cd frontend && npx playwright test

# E2E tests with UI mode (interactive)
cd frontend && npx playwright test --ui

# Accessibility tests only
cd frontend && npx playwright test --grep @a11y

# Responsive tests only
cd frontend && npx playwright test --grep @responsive

# Lint (includes accessibility lint via jsx-a11y)
cd frontend && npx eslint src/
```

### Building

```bash
cd frontend && npm run build
```

## Key Files

| File | Purpose |
|------|---------|
| `frontend/src/router.tsx` | TanStack Router configuration with all routes |
| `frontend/src/styles/` | Design tokens (CSS custom properties) and global styles |
| `frontend/src/data/` | Static placeholder data matching wireframe examples |
| `frontend/src/components/ui/` | Reusable design system primitives |
| `frontend/src/components/donor/` | Donor journey components |
| `frontend/src/components/admin/` | Admin journey components |
| `frontend/src/pages/donor/` | Donor journey page components |
| `frontend/src/pages/admin/` | Admin journey page components |
| `frontend/e2e/` | Playwright E2E tests |
| `frontend/e2e/fixtures/axe-test.ts` | Reusable accessibility test fixture |
| `frontend/playwright.config.ts` | Playwright configuration |
| `frontend/eslint.config.js` | ESLint config with jsx-a11y |

## Design Tokens

The visual design system is defined as CSS custom properties in `frontend/src/styles/`:

```css
:root {
  /* Colors */
  --color-primary: #2D5F4C;
  --color-primary-light: #4A8B6F;
  --color-accent: #E8956B;
  --color-accent-light: #F4C4A8;
  --color-bg: #FDFBF7;
  --color-surface: #FFFFFF;
  --color-text: #1A1A1A;
  --color-text-light: #5A5A5A;
  --color-border: #E5E0D8;

  /* Typography */
  --font-heading: 'Fraunces', serif;
  --font-body: 'DM Sans', sans-serif;
  --font-size-body: 1.125rem;  /* 18px - optimized for older users */
  --line-height: 1.6;

  /* Spacing */
  --touch-target-min: 44px;  /* WCAG 2.2 AAA touch target */
  --container-max: 1400px;

  /* Breakpoints (used in media queries) */
  /* mobile: 375px+ (default) */
  /* tablet: 768px+ */
  /* desktop: 1024px+ */
  /* wide: 1400px+ */
}
```

## Routes

| URL | Page | Notes |
|-----|------|-------|
| `/` | Landing | Postcode search |
| `/search?postcode=...` | Search Results | Food bank cards |
| `/food-bank/:id` | Food Bank Detail | Wish list + options |
| `/food-bank/:id/direct-items` | Direct Items | Item selection |
| `/food-bank/:id/recipe-kits` | Recipe Kits | AI recipe cards |
| `/food-bank/:id/checkout` | Checkout | Basket review |
| `/admin` | Onboarding | Food bank setup |
| `/admin/management` | Management | QR codes + settings |

## TDD Workflow (Constitution Principle I — NON-NEGOTIABLE)

Every page and interactive component follows Red-Green-Refactor:

### For each page (e.g., LandingPage):

```bash
# 1. RED: Write failing Playwright E2E + accessibility tests
#    e2e/accessibility/landing-page.spec.ts
#    e2e/navigation/donor-journey.spec.ts (landing section)
#    e2e/responsive/landing-page.spec.ts
cd frontend && npx playwright test e2e/accessibility/landing-page.spec.ts
# → Tests FAIL (page doesn't exist yet)

# 2. GREEN: Implement the minimum page to make tests pass
#    src/pages/donor/LandingPage.tsx
#    src/router.tsx (add route)
cd frontend && npx playwright test e2e/accessibility/landing-page.spec.ts
# → Tests PASS

# 3. REFACTOR: Clean up while keeping tests green
cd frontend && npx playwright test e2e/accessibility/landing-page.spec.ts
# → Tests still PASS
```

### For interactive components (e.g., DonationBasket):

```bash
# 1. RED: Write failing Vitest component test
#    tests/components/DonationBasket.test.tsx
cd frontend && npx vitest run tests/components/DonationBasket.test.tsx
# → Tests FAIL

# 2. GREEN: Implement component
# 3. REFACTOR: Clean up
```

### Commit ordering

Constitution requires TDD evidence in commit history:

```
feat: add failing Playwright tests for LandingPage
feat: implement LandingPage to pass tests
refactor: clean up LandingPage styles
```

## Accessibility Checklist for Development

When building each component/page, verify:

- [ ] All interactive elements are keyboard-accessible (Tab, Enter, Space, Escape)
- [ ] All form inputs have associated `<label>` elements
- [ ] All images/icons have alt text or `aria-hidden="true"` if decorative
- [ ] Color is not the only way to convey information (use text + icon)
- [ ] Touch targets are at least 44x44px
- [ ] Body text is at least 18px (1.125rem)
- [ ] `prefers-reduced-motion` is respected for animations
- [ ] Page has proper landmark structure (`<header>`, `<nav>`, `<main>`, `<footer>`)
- [ ] Heading hierarchy is logical (h1 → h2 → h3, no skipping)
- [ ] Dynamic content updates use `aria-live` regions
