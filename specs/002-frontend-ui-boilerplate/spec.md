# Feature Specification: Frontend UI Boilerplate

**Feature Branch**: `002-frontend-ui-boilerplate`
**Created**: 2026-02-26
**Status**: Draft
**Input**: User description: "Add boilerplate frontend UI based on donation-genie-wireframes-v1.html file."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Donor Discovers Nearby Food Banks (Priority: P1)

A donor visits the platform and enters their postcode on the landing page to find nearby food banks. The system displays the branded landing page with a postcode input field and a search action. After searching, the donor sees a list of nearby food banks displayed as cards showing each food bank's name, distance, urgency status, number of families served, and top-needed items. An AI-generated summary at the top provides an overview of aggregate needs across results.

**Why this priority**: The postcode-to-results flow is the foundational entry point of the entire donor journey. Without it, no other donor functionality is reachable.

**Independent Test**: Can be fully tested by navigating to the landing page, entering a postcode, and seeing the food bank results list rendered with placeholder data. Delivers the core navigation spine of the donor experience.

**Acceptance Scenarios**:

1. **Given** a donor is on the landing page, **When** the page loads, **Then** the branded header ("Donation Genie"), tagline, postcode input field, and search button are visible
2. **Given** a donor has entered a postcode, **When** they activate the search, **Then** the food bank results page displays with an AI summary section and a list of food bank cards showing name, distance, urgency badge, families served count, and top needs
3. **Given** the food bank results are displayed, **When** the donor selects a food bank, **Then** they navigate to that food bank's detail page

---

### User Story 2 - Donor Views Wish List and Chooses Donation Method (Priority: P1)

After selecting a food bank, the donor sees the food bank's detail page including an impact story, the current wish list displayed as item cards with urgency indicators, and two donation method options: donating individual items directly or choosing AI-generated recipe kits.

**Why this priority**: The wish list and donation choice screen is equally critical as it represents the core value proposition and the branching point of the two donation flows.

**Independent Test**: Can be tested by navigating to a food bank detail page and verifying the wish list items display with urgency badges, the impact story renders, and both donation option cards are visible and navigable.

**Acceptance Scenarios**:

1. **Given** a donor has selected a food bank, **When** the detail page loads, **Then** the food bank name, distance, families served, urgency status, and an impact story section are displayed
2. **Given** the detail page is loaded, **When** the donor views the wish list, **Then** individual item cards are displayed with item name, urgency badge (Urgent/Needed), and brief description
3. **Given** the detail page is loaded, **When** the donor views the donation options, **Then** two option cards are displayed: "Direct Items" (select individual items) and "Recipe Kits" (AI-generated meal kits), with Recipe Kits marked as recommended

---

### User Story 3 - Donor Builds a Direct Item Donation (Priority: P2)

When the donor chooses the direct items option, they see a selection screen with item cards featuring quantity controls (increment/decrement buttons and a quantity input). As items are added, a donation basket section shows selected items with quantities and estimated costs, along with a total and a checkout action.

**Why this priority**: Direct item donation is one of two core donation flows, offering donors granular control over their contribution.

**Independent Test**: Can be tested by selecting "Direct Items", adjusting quantities on item cards, verifying the basket updates with correct items and totals, and confirming the checkout button is accessible.

**Acceptance Scenarios**:

1. **Given** a donor chose "Direct Items", **When** the selection page loads, **Then** item cards display with name, description, urgency badge, and quantity controls (decrement, input, increment, add button)
2. **Given** items are available, **When** the donor adjusts quantity and adds an item, **Then** the donation basket section updates to show the item, quantity, and estimated cost
3. **Given** items are in the basket, **When** the donor reviews the basket, **Then** a total cost is displayed along with a "Proceed to Checkout" action

---

### User Story 4 - Donor Selects an AI Recipe Kit (Priority: P2)

When the donor chooses the recipe kits option, they see AI-generated recipe cards. Each recipe card displays a visual icon, recipe name, serving information, preparation time, a list of ingredients from the wish list, a kit total cost, and a selection action. An impact story section reinforces the value of the donation.

**Why this priority**: Recipe kits are the flagship AI-driven feature that differentiates the platform, making donations more meaningful and complete.

**Independent Test**: Can be tested by selecting "Recipe Kits" and verifying recipe cards display with all required fields (name, servings, time, ingredients, cost) and the selection action works.

**Acceptance Scenarios**:

1. **Given** a donor chose "Recipe Kits", **When** the page loads, **Then** recipe cards are displayed with recipe name, visual icon, serving/time metadata, ingredient list, kit total cost, and a select button
2. **Given** recipe cards are displayed, **When** the donor selects a recipe kit, **Then** they proceed to the checkout/basket step

---

### User Story 5 - Donor Reviews Basket and Proceeds to Checkout (Priority: P2)

After selecting items (direct or recipe kit), the donor sees a checkout review screen. This screen shows a flow diagram illustrating the donation process (selection, AI mapping, basket creation, checkout), the complete basket with individual supermarket products and prices, delivery information, and actions to complete the donation or modify items.

**Why this priority**: The checkout screen completes the donor journey and is the final step before donation commitment.

**Independent Test**: Can be tested by arriving at the checkout screen and verifying the flow diagram, itemized basket, total, delivery note, and both action buttons (complete donation, modify items) are displayed.

**Acceptance Scenarios**:

1. **Given** the donor has items in their basket, **When** the checkout page loads, **Then** a visual flow diagram shows the donation process steps (selection, AI mapping, basket creation, checkout)
2. **Given** the checkout page is loaded, **When** the donor reviews the basket, **Then** individual supermarket products are listed with prices, a delivery line item, and a total cost
3. **Given** the checkout page is loaded, **When** the donor looks at available actions, **Then** a primary "Complete Donation" button and a secondary "Modify Items" button are visible

---

### User Story 6 - Admin Onboards a Food Bank (Priority: P3)

A food bank administrator accesses the admin section to set up their food bank profile. They see a welcome screen with a file upload zone that accepts various formats (photos, PDFs, documents, screenshots). After uploading, the system shows an AI-extracted preview of wish list items organized by category, with options to confirm and publish or edit the items.

**Why this priority**: Admin onboarding is essential for populating the platform with food banks but is secondary to the donor-facing experience for the boilerplate UI.

**Independent Test**: Can be tested by navigating to the admin section, viewing the upload zone, and confirming the AI-extracted items preview renders with category labels and confirm/edit actions.

**Acceptance Scenarios**:

1. **Given** an admin accesses the admin section, **When** the onboarding page loads, **Then** a welcome message, a file upload zone with accepted format descriptions, and an email alternative are displayed
2. **Given** the upload zone is visible, **When** the page shows the AI extraction preview, **Then** extracted items are displayed in a grid with item name, category label, and checkmark indicators
3. **Given** extracted items are shown, **When** the admin reviews the preview, **Then** "Confirm & Publish" and "Edit Items" action buttons are available

---

### User Story 7 - Admin Manages QR Codes and Integration Settings (Priority: P3)

An admin can access tools for generating QR codes in multiple formats (in-store poster, sticker/label, social media) and managing delivery/integration settings including delivery preferences (direct delivery, donor collection, delivery notes) and supermarket partner selection.

**Why this priority**: Marketing and integration management is important for food bank engagement but is the least critical screen for the initial boilerplate.

**Independent Test**: Can be tested by navigating to the QR/integration page and verifying QR format options, delivery preference checkboxes, supermarket partner cards, and save/test actions render correctly.

**Acceptance Scenarios**:

1. **Given** an admin is on the management page, **When** the QR section loads, **Then** a QR code placeholder, format download options (poster PDF, sticker PNG, social media JPG), and a "Generate All Formats" action are displayed
2. **Given** the management page is loaded, **When** the admin views delivery preferences, **Then** checkboxes for direct delivery, donor collection, and delivery notes (with a text area) are displayed
3. **Given** the management page is loaded, **When** the admin views supermarket partners, **Then** partner cards for available retailers (with enabled/disabled states) and save/test actions are visible

---

### Edge Cases

- What happens when the postcode search returns no nearby food banks? The results page should display a friendly "no results" message with suggestions (try a different postcode, expand search radius).
- What happens when a food bank's wish list is empty? The detail page should show a message indicating the food bank has no current needs listed, with a suggestion to check back later.
- How does the interface handle very long food bank names or item descriptions? Text should truncate gracefully with ellipsis and full text available on hover or expansion.
- What happens when the donor's basket is empty and they try to proceed to checkout? The checkout action should be disabled with a message prompting them to add items first.
- How does navigation work between the two journeys (Donor vs Admin)? A top-level navigation allows switching between "Donor Journey" and "Admin: Food Bank Onboarding" views.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a branded landing page with the application name, tagline, postcode input field, and a search action
- **FR-002**: System MUST display food bank search results as a list of cards, each showing food bank name, distance, urgency badge, families served, top needs, and a selection action
- **FR-003**: System MUST display an AI-generated summary section above the food bank results aggregating needs across listed food banks
- **FR-004**: System MUST display a food bank detail page with impact story, current wish list as item cards with urgency indicators, and two donation method options
- **FR-005**: System MUST provide an individual item selection interface with quantity controls (increment, decrement, quantity input) and an add-to-basket action per item
- **FR-006**: System MUST display a running donation basket showing selected items, quantities, individual costs, and a total cost
- **FR-007**: System MUST display AI-generated recipe kit cards with recipe name, visual indicator, serving size, preparation time, ingredient list, kit total cost, and a selection action
- **FR-008**: System MUST display a checkout review page with a visual process flow diagram, itemized product list with prices, delivery information, and primary (complete) and secondary (modify) actions
- **FR-009**: System MUST provide an admin onboarding page with a file upload zone, accepted format descriptions, an email alternative, and an AI-extracted items preview with confirm/edit actions
- **FR-010**: System MUST provide an admin QR code management section with QR code preview, multiple download format options, and a bulk generation action
- **FR-011**: System MUST provide admin integration settings with delivery preference toggles, a delivery notes text area, and supermarket partner selection cards with enabled/disabled states
- **FR-012**: System MUST provide top-level navigation allowing users to switch between the Donor Journey and Admin sections
- **FR-013**: System MUST use the established visual design language: a green primary color palette, coral accent color, warm white background, serif headings, and sans-serif body text
- **FR-014**: System MUST be responsive, adapting layout for both desktop and mobile viewports with appropriate flow adjustments (e.g., vertical flow diagrams on mobile)

### Key Entities

- **Food Bank**: Represents a charitable organization with a name, location, distance from donor, urgency status, families served count, and a wish list of needed items
- **Wish List Item**: An individual item needed by a food bank, with a name, description, urgency level (urgent/needed), and category
- **Recipe Kit**: An AI-generated meal kit composed of wish list items, with a recipe name, serving size, preparation time, ingredient list, and estimated total cost
- **Donation Basket**: A collection of items (individual or from a recipe kit) selected by a donor, with quantities, per-item costs, delivery cost, and a total
- **QR Code**: A generated marketing asset for a food bank, available in multiple formats (poster, sticker, social media)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 7 page layouts from the wireframe are rendered and navigable within the application, with 100% of wireframed screens accessible through the user interface
- **SC-002**: Users can complete the full donor journey navigation flow (landing, search results, food bank detail, donation method, basket, checkout) in under 30 seconds using placeholder data
- **SC-003**: Users can switch between Donor Journey and Admin sections with a single click/tap, with the view updating within 1 second
- **SC-004**: All pages render correctly on both desktop (1400px width) and mobile (375px width) viewports without horizontal scrolling or content overflow
- **SC-005**: Every page has a visible `<h1>` heading describing its purpose and a visually prominent primary action button within the initial viewport (no scrolling required at 1280px desktop width)
- **SC-006**: Visual design elements (colors, typography, spacing, component styles) match the wireframe reference with at least 90% fidelity as judged by visual comparison

## Assumptions

- This feature covers the static UI shell and navigation structure only. Dynamic data fetching, AI integration, payment processing, and real supermarket API connections are out of scope.
- Placeholder/mock data will be used throughout to demonstrate the layout and flow without requiring backend services.
- The two-journey navigation (Donor vs Admin) will use a simple toggle or tab-based approach as shown in the wireframe.
- The visual design system (colors, fonts, component styles) is derived directly from the wireframe file and should be treated as the source of truth for this feature.
- The postcode search, recipe generation, and checkout actions will be non-functional placeholders that navigate to the next screen in the flow.
- Food bank data, wish list items, recipe kits, and basket contents will all use hardcoded sample data matching the wireframe examples.
