# Feature Specification: Expand Seed Fixtures

**Feature Branch**: `005-expand-seed-fixtures`
**Created**: 2026-03-05
**Status**: Draft
**Input**: User description: "Update db seed fixtures json file to have 40 food banks. Food bank location (lat and lon including) should be from across the UK. Also add more wishlist items with wider variety of food items. Also add more entries in other tables where it makes sense."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer Seeds Database with Realistic UK-Wide Data (Priority: P1)

A developer setting up a local environment runs the seed command and receives a database populated with 40 food banks spread geographically across the UK — including England, Scotland, Wales, and Northern Ireland — each with realistic names, addresses, postcodes, and coordinates.

**Why this priority**: Without realistic, geographically diverse food bank data, developers and testers cannot meaningfully verify map displays, proximity searches, or regional features.

**Independent Test**: Can be fully tested by loading the seed fixture and verifying that 40 food banks exist with valid UK coordinates that span the four nations.

**Acceptance Scenarios**:

1. **Given** an empty database, **When** the seed fixture is loaded, **Then** exactly 40 food bank records exist with unique names, valid UK postcodes, and lat/lon coordinates distributed across England, Scotland, Wales, and Northern Ireland.
2. **Given** the seed fixture is loaded, **When** the food bank coordinates are plotted, **Then** they visually cover major UK cities and regions (London, Manchester, Birmingham, Edinburgh, Cardiff, Belfast, etc.) rather than clustering in a single area.
3. **Given** the seed fixture is loaded, **When** the food bank records are inspected, **Then** each has a realistic address, postcode matching its region, and a families_served_weekly value between 20 and 500.

---

### User Story 2 - Developer Has Diverse Wishlist Items for Testing (Priority: P1)

A developer loads the seed fixture and finds each food bank has a varied selection of wishlist items spanning all available categories (tinned goods, dried goods, fresh, dairy, baby, hygiene) with different urgency levels, so they can test filtering, searching, and display logic against realistic data.

**Why this priority**: Wishlist items are a core entity that drive recipe generation and donation flows. A wide variety is essential for testing the full range of category and urgency combinations.

**Independent Test**: Can be tested by loading the fixture and verifying wishlist items exist across all categories and urgency levels for multiple food banks.

**Acceptance Scenarios**:

1. **Given** the seed fixture is loaded, **When** wishlist items are queried, **Then** at least 120 wishlist items exist across the 40 food banks.
2. **Given** the seed fixture is loaded, **When** wishlist items are grouped by category, **Then** all six categories (tinned_goods, dried_goods, fresh, dairy, baby, hygiene) are represented.
3. **Given** the seed fixture is loaded, **When** wishlist items are grouped by urgency, **Then** all three urgency levels (urgent, needed, optional) are represented with a realistic distribution.
4. **Given** the seed fixture is loaded, **When** wishlist items are inspected, **Then** item names reflect a wide variety of real food and household products (e.g., baked beans, pasta, nappies, toothpaste, rice, cereal, soup, baby formula, shampoo, cooking oil).

---

### User Story 3 - Developer Has Populated Related Tables for End-to-End Testing (Priority: P2)

A developer loads the seed fixture and finds that related tables (recipes, donations, delivery tracking, settings, supermarket preferences, QR scans) also contain multiple entries linked to various food banks, enabling end-to-end testing of the full donation workflow.

**Why this priority**: While food banks and wishlist items are the core data, having populated related tables enables more comprehensive integration and UI testing without manual data entry.

**Independent Test**: Can be tested by loading the fixture and verifying that records exist in all related tables with valid foreign key references.

**Acceptance Scenarios**:

1. **Given** the seed fixture is loaded, **When** generated recipes are queried, **Then** at least 10 recipes exist across multiple food banks, each with valid ingredient lists and realistic cooking details.
2. **Given** the seed fixture is loaded, **When** donations are queried, **Then** at least 15 donation records exist with a mix of recipe_kit and individual_items types, linked to various food banks.
3. **Given** the seed fixture is loaded, **When** delivery tracking records are queried, **Then** at least 10 records exist with a mix of statuses (pending, dispatched, delivered, received).
4. **Given** the seed fixture is loaded, **When** food bank settings are queried, **Then** at least 20 food banks have associated settings records with varied configurations.
5. **Given** the seed fixture is loaded, **When** supermarket preferences are queried, **Then** at least 30 preference records exist across multiple food banks and supermarkets (Tesco, Sainsburys, Asda, Waitrose).
6. **Given** the seed fixture is loaded, **When** QR scans are queried, **Then** at least 10 scan records exist with a mix of sources and conversion statuses.

---

### Edge Cases

- What happens if the fixture is loaded twice? (Idempotency — UUIDs are hardcoded so re-loading should update, not duplicate.)
- Are all foreign key references between fixture entries valid and consistent?
- Do all enum/choice field values match the model definitions exactly (e.g., urgency_level values, category values)?
- Are all UUID primary keys unique across the entire fixture file?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The seed fixture file MUST contain exactly 40 food bank records with unique UUIDs, names, and addresses.
- **FR-002**: Food bank locations MUST use real UK coordinates and postcodes distributed across England, Scotland, Wales, and Northern Ireland.
- **FR-003**: The fixture MUST contain at least 120 wishlist items spanning all six categories (tinned_goods, dried_goods, fresh, dairy, baby, hygiene) and all three urgency levels (urgent, needed, optional).
- **FR-004**: Wishlist item names MUST represent a wide variety of real food and household products, not just repeated items.
- **FR-005**: The fixture MUST contain at least 10 generated recipe records with realistic ingredient lists, cooking times, and cost estimates.
- **FR-006**: The fixture MUST contain at least 15 donation records with a mix of donation types (recipe_kit, individual_items).
- **FR-007**: The fixture MUST contain at least 10 delivery tracking records with varied statuses.
- **FR-008**: The fixture MUST contain at least 20 food bank settings records with varied configurations.
- **FR-009**: The fixture MUST contain at least 30 supermarket preference records distributed across available supermarket choices.
- **FR-010**: The fixture MUST contain at least 10 QR scan records with varied sources and conversion statuses.
- **FR-011**: All foreign key references in the fixture MUST be internally consistent (every referenced UUID must exist in the fixture).
- **FR-012**: All choice/enum field values MUST match the model definitions (urgency levels, categories, statuses, supermarket names, etc.).
- **FR-013**: All UUIDs in the fixture MUST be unique.

### Key Entities

- **FoodBank**: Core entity — 40 records with UK-wide geographic distribution, varied urgency levels and family counts.
- **WishListItem**: Items needed by food banks — 120+ records across 6 categories and 3 urgency levels with diverse product names.
- **GeneratedRecipe**: Recipes using wishlist items — 10+ records with ingredient lists and cooking details.
- **Donation**: Completed and in-progress donations — 15+ records of both types.
- **DeliveryTracking**: Delivery status records — 10+ with mixed statuses.
- **FoodBankSettings**: Configuration per food bank — 20+ records.
- **FoodBankSupermarketPreference**: Supermarket delivery preferences — 30+ records across 4 supermarkets.
- **QRScan**: QR code scan tracking — 10+ records from varied sources.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The seed fixture loads successfully without errors and populates all tables with the specified minimum record counts.
- **SC-002**: Food bank locations, when plotted on a map, cover at least 10 distinct UK cities/regions across all four nations.
- **SC-003**: Wishlist items represent at least 30 distinct product names across all 6 categories.
- **SC-004**: All foreign key relationships in the fixture are valid — zero orphaned references.
- **SC-005**: The fixture file can be loaded repeatedly without creating duplicate records (idempotent via hardcoded UUIDs).

## Assumptions

- The fixture file format remains a single JSON file at `backend/fixtures/seed.json` compatible with Django's `loaddata` command.
- Food bank names, addresses, and coordinates should be realistic but do not need to correspond to actual registered food banks.
- The existing seed data structure and field conventions are preserved (same date formats, same JSON structure for ingredients/items fields).
- No new models or schema changes are required — this feature only updates the fixture data file.
