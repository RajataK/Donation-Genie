# Feature Specification: Initialize PostgreSQL Schema

**Feature Branch**: `004-init-postgres-schema`
**Created**: 2026-03-05
**Status**: Draft
**Input**: User description: "Initialize the PostgreSQL schema. Generate all necessary Django models.py definitions and the corresponding migrations to set up the database schema from scratch."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Store and Retrieve Food Bank Information (Priority: P1)

A food bank administrator registers their organization in the system. The system persists the food bank's name, location, contact details, urgency status, families served count, and impact story. A donor later searches for nearby food banks and the system retrieves matching records with all relevant display information.

**Why this priority**: Food banks are the central entity in the donation workflow. Every other feature (wish lists, recipe kits, donations) depends on food banks existing in the database first.

**Independent Test**: Can be fully tested by creating a food bank record, then retrieving it and verifying all fields are persisted correctly.

**Acceptance Scenarios**:

1. **Given** an empty database with migrations applied, **When** a food bank record is created with all required fields (name, location, urgency status, families served, impact story), **Then** the record is persisted and can be retrieved with all fields intact.
2. **Given** multiple food banks exist, **When** a query filters by urgency status, **Then** only food banks matching the specified status are returned.
3. **Given** a food bank exists, **When** its urgency status or families served count is updated, **Then** the updated values are persisted and reflected on subsequent retrieval.

---

### User Story 2 - Manage Wish List Items for a Food Bank (Priority: P1)

A food bank administrator creates and maintains a wish list of needed items. Each item has a name, description, urgency level, category, and estimated price. Donors browse these items when deciding what to donate.

**Why this priority**: Wish list items are the primary mechanism for food banks to communicate their needs. This is tied with food banks as the core data that powers the donation flow.

**Independent Test**: Can be tested by creating a food bank, adding wish list items to it, and verifying items are correctly associated and retrievable.

**Acceptance Scenarios**:

1. **Given** a food bank exists, **When** a wish list item is created with name, description, urgency level, category, and estimated price, **Then** the item is persisted and associated with that food bank.
2. **Given** a food bank has multiple wish list items, **When** items are retrieved for that food bank, **Then** all associated items are returned with correct field values.
3. **Given** a wish list item exists, **When** its urgency level is changed from "needed" to "urgent", **Then** the change is persisted.
4. **Given** a food bank is removed from the system, **When** the database enforces referential integrity, **Then** all associated wish list items are also removed.

---

### User Story 3 - Build and Store Donation Baskets (Priority: P2)

A donor selects items (either directly from the wish list or via a recipe kit) and builds a donation basket targeted at a specific food bank. The system persists the basket with its line items, delivery cost, total cost, and donation type. The donor can review their basket before completing the donation.

**Why this priority**: Donation baskets represent the core transaction of the application. Without persisting baskets, there is no record of donor intent or completed donations.

**Independent Test**: Can be tested by creating a food bank with wish list items, building a basket with line items, and verifying the basket and its items are correctly persisted and totals are accurate.

**Acceptance Scenarios**:

1. **Given** a food bank exists, **When** a donation basket is created with line items, delivery cost, and donation type, **Then** the basket is persisted with correct totals and associated with the food bank.
2. **Given** a basket exists with multiple line items, **When** the basket is retrieved, **Then** all line items are returned with correct quantities and prices.
3. **Given** a basket was created via the recipe kit flow, **When** the basket is retrieved, **Then** the donation type is "recipe-kit" and the recipe name is stored.
4. **Given** a basket exists, **When** the associated food bank is retrieved, **Then** the food bank record reflects the relationship to the basket.

---

### User Story 4 - Store Recipe Kits with Ingredients (Priority: P2)

The system stores AI-generated recipe kits associated with food banks. Each kit contains a name, servings info, prep time, total cost, and a list of ingredients. Ingredients indicate whether they match wish list items. Donors browse recipe kits as an alternative way to select donation items.

**Why this priority**: Recipe kits are a key differentiating feature of Donation Genie. They depend on food banks and wish list items existing first, but are needed before the full donation flow is complete.

**Independent Test**: Can be tested by creating a food bank, adding a recipe kit with ingredients, and verifying the kit and its ingredients are correctly persisted and retrievable.

**Acceptance Scenarios**:

1. **Given** a food bank exists, **When** a recipe kit is created with name, servings, prep time, total cost, and ingredients, **Then** the kit and all ingredients are persisted and associated with the food bank.
2. **Given** a recipe kit exists with ingredients, **When** the kit is retrieved, **Then** all ingredients are returned in order with their matched status.
3. **Given** a food bank is removed, **When** referential integrity is enforced, **Then** all associated recipe kits and their ingredients are also removed.

---

### User Story 5 - Configure Supermarket Partners and Delivery Preferences (Priority: P3)

A food bank administrator configures which supermarket partners are available for fulfilling donations and sets delivery preferences. Donors see these configurations when completing their donations.

**Why this priority**: Partner and delivery configuration is an administrative feature that enhances the donation experience but is not required for the core donation flow.

**Independent Test**: Can be tested by creating a food bank, adding supermarket partners and delivery preferences, and verifying the configurations are correctly stored and retrievable.

**Acceptance Scenarios**:

1. **Given** a food bank exists, **When** supermarket partners are associated with delivery times and availability status, **Then** the partner configurations are persisted.
2. **Given** a food bank exists, **When** delivery preferences are configured with labels, descriptions, and enabled status, **Then** the preferences are persisted and retrievable.
3. **Given** a supermarket partner is disabled, **When** partner configurations are retrieved, **Then** the disabled partner is included with its availability marked accordingly.

---

### Edge Cases

- What happens when a wish list item is created without a parent food bank? The system MUST reject the record and return a clear error indicating a food bank association is required.
- What happens when a basket line item references a negative quantity or zero price? The system MUST enforce that quantities are at least 1 and prices are positive.
- What happens when two food banks have wish list items with the same name? The system MUST allow this since items are scoped to their parent food bank.
- What happens when the database migrations are run against an empty database? All tables, indexes, and constraints MUST be created successfully without errors.
- What happens when migrations are run against a database that already has the schema applied? The system MUST detect that migrations are already applied and skip them without errors.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST persist food bank organizations with: name, address (street, city, postcode, country), geographic coordinates (latitude and longitude) for proximity search, contact information (email, phone number, website URL), urgency status (urgent or active), families served count, top needs list, and impact story.
- **FR-002**: The system MUST persist wish list items associated with a food bank, each with: name, description, urgency level (urgent or needed), category, and estimated price.
- **FR-003**: The system MUST persist recipe kits associated with a food bank, each with: name, icon, servings info, prep time, total cost, and an ordered list of ingredients.
- **FR-004**: The system MUST persist recipe ingredients associated with a recipe kit, each with: name and a flag indicating whether it matches a wish list item.
- **FR-005**: The system MUST persist donation baskets associated with a food bank, each with: delivery cost, total cost, donation type (direct or recipe-kit), optional recipe name, and a status indicating the basket's lifecycle stage (draft, submitted, completed, or cancelled).
- **FR-006**: The system MUST persist basket line items associated with a donation basket, each with: product name, quantity (minimum 1), and unit price (positive value).
- **FR-007**: The system MUST persist supermarket partners with: name, typical delivery time, availability status, and enabled status.
- **FR-008**: The system MUST support a many-to-many relationship between food banks and supermarket partners.
- **FR-009**: The system MUST persist delivery preferences associated with a food bank, each with: label, description, and enabled status.
- **FR-010**: The system MUST enforce referential integrity so that removing a food bank cascades removal of its wish list items, recipe kits (and their ingredients), donation baskets (and their line items), and delivery preferences.
- **FR-011**: The system MUST automatically track creation and last-modified timestamps on all records.
- **FR-012**: The system MUST generate unique identifiers for all records automatically.
- **FR-013**: The system MUST provide schema versioning so that the database can be set up from scratch or incrementally updated through sequential schema changes.
- **FR-014**: The system MUST support QR code format configurations associated with a food bank, each with: label, description, and file type.

### Key Entities

- **Food Bank**: A charitable food bank organization. Central entity that owns wish lists, recipe kits, donation baskets, delivery preferences, QR code formats, and supermarket partner associations. Key attributes: name, address (street, city, postcode, country), geographic coordinates (latitude, longitude), contact info (email, phone, website), urgency status, families served, impact story.
- **Wish List Item**: An individual item a food bank needs. Belongs to one food bank. Key attributes: name, description, urgency level, category, estimated price.
- **Recipe Kit**: An AI-generated meal kit composed of ingredients. Belongs to one food bank. Key attributes: name, servings, prep time, total cost.
- **Recipe Ingredient**: A single ingredient within a recipe kit. Belongs to one recipe kit. Key attributes: name, matched status.
- **Donation Basket**: A donor's collection of items targeted at one food bank. Key attributes: delivery cost, total cost, donation type, recipe name, status (draft → submitted → completed / cancelled).
- **Basket Item**: A line item in a donation basket. Belongs to one basket. Key attributes: product name, quantity, unit price.
- **Supermarket Partner**: A supermarket that can fulfill donations. Can be associated with many food banks. Key attributes: name, delivery time, availability.
- **Delivery Preference**: A delivery configuration option for a food bank. Belongs to one food bank. Key attributes: label, description, enabled status.
- **QR Code Format**: A downloadable QR code format for a food bank. Belongs to one food bank. Key attributes: label, description, file type.

## Clarifications

### Session 2026-03-05

- Q: What location fields should be stored for a Food Bank? → A: Address (street, city, postcode, country) plus geographic coordinates (latitude/longitude) for proximity search.
- Q: Should donation baskets track lifecycle status? → A: Yes, add a status field with states: draft, submitted, completed, cancelled.
- Q: Should records be soft-deleted or hard-deleted? → A: Hard delete with cascade for the initial schema; audit trail / soft-delete is a future feature.
- Q: What contact information fields should Food Bank store? → A: Email, phone number, and website URL.

## Assumptions

- The database engine is PostgreSQL, consistent with the project's existing infrastructure (Docker Compose with PostgreSQL, AWS RDS PostgreSQL in production).
- Django's built-in User model is sufficient for authentication at this stage; a custom user model is not required for the initial schema.
- Currency values are stored in GBP as the application targets UK-based food banks (inferred from the frontend data model using GBP pricing).
- The "top needs" field on food banks is stored as a list of strings rather than a separate entity, since it is a display-only summary derived from wish list item data.
- Recipe ingredient ordering within a kit matters and is preserved.
- Donation baskets do not require a user/donor association at this stage; donor identity tracking is a future feature.
- Supermarket product mapping (matching wish list items to specific supermarket products) is a future feature and not part of the initial schema.
- Hard delete with cascade is used for all referential integrity; soft-delete and audit trails are deferred to a future feature.
- New donation baskets default to "draft" status.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running the schema setup from scratch against an empty database completes without errors and creates all expected tables and relationships.
- **SC-002**: All entity types can be created, read, updated, and deleted through the application's data layer with full field persistence verified.
- **SC-003**: Removing a food bank automatically removes all dependent records (wish list items, recipe kits, ingredients, baskets, basket items, delivery preferences, QR code formats) without orphaned data.
- **SC-004**: Creating records with invalid data (missing required fields, negative prices, zero quantities) is rejected with clear error messages.
- **SC-005**: Running the schema setup process multiple times (idempotent application) succeeds without errors or data loss.
- **SC-006**: All records include automatically generated unique identifiers and creation/modification timestamps without manual input.
