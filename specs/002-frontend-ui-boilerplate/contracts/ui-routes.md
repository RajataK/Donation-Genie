# UI Route Contracts: Frontend UI Boilerplate

**Feature**: 002-frontend-ui-boilerplate
**Date**: 2026-02-26

## Route Map

| Route | Page | Journey | Description |
|-------|------|---------|-------------|
| `/` | LandingPage | Donor | Postcode search with branded header |
| `/search?postcode={postcode}` | SearchResultsPage | Donor | Food bank results with AI summary |
| `/food-bank/:id` | FoodBankDetailPage | Donor | Wish list, impact story, donation options |
| `/food-bank/:id/direct-items` | DirectItemsPage | Donor | Individual item selection with basket |
| `/food-bank/:id/recipe-kits` | RecipeKitsPage | Donor | AI recipe kit selection |
| `/food-bank/:id/checkout` | CheckoutPage | Donor | Basket review and checkout |
| `/admin` | OnboardingPage | Admin | Food bank setup with file upload |
| `/admin/management` | ManagementPage | Admin | QR codes and integration settings |

## Route Parameters

### `/search`

| Param | Type | Location | Required | Description |
|-------|------|----------|----------|-------------|
| postcode | string | Query string | Yes | UK postcode entered by donor |

### `/food-bank/:id`

| Param | Type | Location | Required | Description |
|-------|------|----------|----------|-------------|
| id | string | Path | Yes | Food bank identifier |

### `/food-bank/:id/direct-items`

| Param | Type | Location | Required | Description |
|-------|------|----------|----------|-------------|
| id | string | Path | Yes | Food bank identifier |

### `/food-bank/:id/recipe-kits`

| Param | Type | Location | Required | Description |
|-------|------|----------|----------|-------------|
| id | string | Path | Yes | Food bank identifier |

### `/food-bank/:id/checkout`

| Param | Type | Location | Required | Description |
|-------|------|----------|----------|-------------|
| id | string | Path | Yes | Food bank identifier |

## Navigation Flows

### Donor Journey (Primary Flow)

```
LandingPage (/)
  └─ [Enter postcode + search] ──→ SearchResultsPage (/search?postcode=SW1A+1AA)
      └─ [Select food bank] ──→ FoodBankDetailPage (/food-bank/camden-food-bank)
          ├─ [Choose Direct Items] ──→ DirectItemsPage (/food-bank/camden-food-bank/direct-items)
          │   └─ [Proceed to Checkout] ──→ CheckoutPage (/food-bank/camden-food-bank/checkout)
          └─ [Choose Recipe Kits] ──→ RecipeKitsPage (/food-bank/camden-food-bank/recipe-kits)
              └─ [Select kit] ──→ CheckoutPage (/food-bank/camden-food-bank/checkout)
```

### Admin Journey

```
OnboardingPage (/admin)
  └─ [After setup] ──→ ManagementPage (/admin/management)
```

### Cross-Journey Navigation

Top-level navigation bar provides switching between:
- "Donor Journey" → `/`
- "Admin" → `/admin`

Visible on all pages. Active state indicates current journey.

## Page Contracts

### LandingPage (`/`)

**Renders**: Branded header, tagline, postcode input, search button
**User Actions**:
- Enter postcode in input field
- Click "Find Local Food Banks" → navigates to `/search?postcode={input}`
**Accessibility**:
- Input has associated `<label>` element
- Search button has descriptive text (not icon-only)
- Page has `<main>` landmark
- H1 contains application name

### SearchResultsPage (`/search?postcode={postcode}`)

**Renders**: AI summary annotation, list of FoodBank cards (3 sample entries)
**User Actions**:
- Click "Select This Food Bank" on any card → navigates to `/food-bank/:id`
**Accessibility**:
- Results list uses `<ul>` with `<li>` items or equivalent landmark
- Each card is keyboard-focusable
- Urgency badges have `aria-label` describing urgency level
- AI summary section has `aria-label="AI-generated needs summary"`

### FoodBankDetailPage (`/food-bank/:id`)

**Renders**: Food bank header, impact story, wish list grid, donation option cards
**User Actions**:
- Click "Donate Individual Items" → navigates to `/food-bank/:id/direct-items`
- Click "Create Recipe Kits" → navigates to `/food-bank/:id/recipe-kits`
**Accessibility**:
- Donation options are in a visually distinct section with `role="group"` and `aria-label`
- Impact story uses semantic heading hierarchy
- Wish list items include urgency in accessible name

### DirectItemsPage (`/food-bank/:id/direct-items`)

**Renders**: Item cards with quantity controls, donation basket summary
**User Actions**:
- Adjust quantity with +/- buttons or number input
- Click "Add" to add item to basket
- Click "Proceed to Checkout" → navigates to `/food-bank/:id/checkout`
**Accessibility**:
- Quantity input has `aria-label` including item name
- +/- buttons have `aria-label` (e.g., "Increase quantity of Tinned Tomatoes")
- Basket total uses `aria-live="polite"` for dynamic updates
- Checkout button is disabled with `aria-disabled` when basket is empty

### RecipeKitsPage (`/food-bank/:id/recipe-kits`)

**Renders**: Recipe kit cards (3 sample kits), impact story
**User Actions**:
- Click "Select This Kit" → navigates to `/food-bank/:id/checkout`
**Accessibility**:
- Recipe cards are keyboard-navigable
- Ingredient lists use semantic `<ul>` elements
- Kit selection communicates choice via `aria-live` region

### CheckoutPage (`/food-bank/:id/checkout`)

**Renders**: Flow diagram, itemized basket, total, delivery info, action buttons
**User Actions**:
- Click "Complete Donation via Tesco" (placeholder — shows confirmation or no-op)
- Click "Modify Items" → navigates back to previous page
**Accessibility**:
- Flow diagram has `aria-label` describing the overall process
- Individual flow steps are not interactive (decorative)
- Basket items are in a semantic `<table>` or description list
- Primary action button is visually prominent and first in tab order among actions

### OnboardingPage (`/admin`)

**Renders**: Welcome message, file upload zone, AI extraction preview grid
**User Actions**:
- Click/drag upload zone (placeholder — no actual upload)
- Click "Confirm & Publish" or "Edit Items" (placeholder actions)
**Accessibility**:
- Upload zone has `role="button"` with descriptive `aria-label`
- Extracted items grid uses semantic list markup
- Action buttons have clear, descriptive labels

### ManagementPage (`/admin/management`)

**Renders**: QR code section, delivery preferences, supermarket partners
**User Actions**:
- Click download buttons for QR formats (placeholder)
- Toggle delivery preference checkboxes
- Select/deselect supermarket partners
- Click "Save Settings" or "Test Integration" (placeholder)
**Accessibility**:
- Checkboxes have associated `<label>` elements
- Disabled supermarket cards have `aria-disabled="true"` with explanation
- Sections use `<fieldset>` and `<legend>` for grouping related controls
