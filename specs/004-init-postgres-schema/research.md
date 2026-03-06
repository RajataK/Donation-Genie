# Research: Initialize PostgreSQL Schema (Updated)

**Feature**: 004-init-postgres-schema
**Date**: 2026-03-05

## Decision 1: UUID Primary Keys

**Decision**: Use `UUIDField(primary_key=True, default=uuid.uuid4, editable=False)` for all models.

**Rationale**: The user-provided schema specifies UUID for all entity IDs. Django's `UUIDField` is well-supported and maps to PostgreSQL's native `uuid` type. UUIDs prevent sequential ID enumeration (security benefit), enable distributed ID generation, and are safe for URL exposure.

**Alternatives considered**:
- `BigAutoField` (previous implementation): Simpler but sequential IDs are guessable and not suitable for public-facing APIs.
- `ULID` or `KSUID`: Sortable but require third-party libraries. No current requirement for time-ordered IDs.

## Decision 2: JSON Fields for Ingredients and Donation Items

**Decision**: Use `JSONField` for `GeneratedRecipe.ingredients` and `Donation.items`.

**Rationale**: The user schema specifies JSON type for both fields. Django's `JSONField` maps to PostgreSQL's native `jsonb` type, which supports indexing and querying. This avoids separate join tables for recipe ingredients (which are AI-generated and cached) and donation line items (which are a snapshot at donation time). Both are document-like data that doesn't need relational querying.

**Alternatives considered**:
- Separate `RecipeIngredient` / `BasketItem` models (previous implementation): Over-normalized for data that is generated/snapshotted and rarely queried independently.
- `TextField` with JSON serialization: Loses database-level JSON validation and querying capabilities.

## Decision 3: Category and Status Enums

**Decision**: Use Django `TextChoices` for all enum fields: `urgency_level`, `category`, `urgency`, `donation_type`, `source`, `supermarket`, `status`.

**Rationale**: TextChoices is the standard Django pattern. Stores human-readable strings in the database, provides validation, and integrates with DRF serializers. All enum values come directly from the user-provided schema.

**Enum definitions**:
- FoodBank.urgency_level: `urgent`, `active`, `normal`
- WishListItem.category: `tinned_goods`, `dried_goods`, `fresh`, `dairy`, `baby`, `hygiene`
- WishListItem.urgency: `urgent`, `needed`, `optional`
- Donation.donation_type: `recipe_kit`, `individual_items`
- QRScan.source: `qr_poster`, `qr_sticker`, `qr_social`
- FoodBankSupermarketPreference.supermarket: `tesco`, `sainsburys`, `asda`, `waitrose`
- DeliveryTracking.status: `pending`, `dispatched`, `delivered`, `received`

## Decision 4: FoodBankAdmin Authentication Model

**Decision**: Use Django's `AbstractBaseUser` with a custom manager for `FoodBankAdmin`.

**Rationale**: The user schema includes `password_hash` and `email` fields for food bank administrators. Django's `AbstractBaseUser` provides secure password hashing (PBKDF2 by default), password validation, and session authentication — all battle-tested. Rolling custom password hashing would violate Constitution Principle II (Proven Solutions). Set `AUTH_USER_MODEL = "accounts.FoodBankAdmin"` in settings.

**Alternatives considered**:
- Raw `password_hash` TextField: Requires manual hashing/verification, easy to get wrong, no Django admin integration.
- Django's built-in `User` model with profile: Adds unnecessary username field and doesn't match the user's schema intent of a dedicated admin model.

## Decision 5: FoodBankSettings as OneToOneField

**Decision**: Use `OneToOneField(FoodBank)` for FoodBankSettings to enforce "one record per food bank".

**Rationale**: The user schema specifies `food_bank_id` as unique, meaning exactly one settings record per food bank. Django's `OneToOneField` enforces this at the database level and provides convenient `food_bank.settings` reverse access.

## Decision 6: App Organization (Updated)

**Decision**: Three domain apps: `foodbanks` (6 models), `donations` (2 models), `accounts` (1 model). Plus shared `core` app for TimestampMixin.

**Rationale**:
- `foodbanks`: FoodBank, WishListItem, GeneratedRecipe, FoodBankSettings, FoodBankSupermarketPreference, QRScan — all directly tied to food bank management.
- `donations`: Donation, DeliveryTracking — donation events and fulfilment.
- `accounts`: FoodBankAdmin — must be separate because Django's `AUTH_USER_MODEL` requires the model to exist in a stable app before any migrations run.

## Decision 7: Timestamp Field Naming

**Decision**: Follow the user's schema field names exactly: `created_at`, `last_updated` (FoodBank), `generated_at`/`expires_at` (GeneratedRecipe), `scanned_at` (QRScan), `updated_at` (where specified).

**Rationale**: The user schema uses different timestamp field names for different tables rather than a uniform `created_at`/`updated_at` pair. We preserve these exactly. TimestampMixin provides `created_at` only where both `created_at` and `updated_at` are present. Models with custom timestamp fields (e.g., FoodBank with `last_updated`, GeneratedRecipe with `generated_at`/`expires_at`) define their own fields instead.

**Implementation note**: TimestampMixin will be simplified to only provide `created_at` (auto_now_add). Models that need `updated_at` or custom timestamp fields will add them explicitly. This avoids inheriting an `updated_at` field that conflicts with `last_updated` or isn't needed.

## Decision 8: Monetary Values

**Decision**: Use `DecimalField(max_digits=10, decimal_places=2)` for monetary fields (`estimated_cost`, `total_cost`).

**Rationale**: Same as previous — DecimalField avoids floating-point rounding. Increased to max_digits=10 for slightly more headroom with recipe costs that aggregate multiple items.

## Decision 9: Geographic Coordinates

**Decision**: Use `DecimalField(max_digits=9, decimal_places=6)` for latitude/longitude (unchanged from previous).

**Rationale**: 6 decimal places provides ~0.11m precision. No PostGIS dependency needed at this stage.
