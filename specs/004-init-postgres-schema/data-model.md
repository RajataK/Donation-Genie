# Data Model: Initialize PostgreSQL Schema (Updated)

**Feature**: 004-init-postgres-schema
**Date**: 2026-03-05

## Overview

The Donation Genie schema consists of 9 entities across three Django apps (`foodbanks`, `donations`, `accounts`), plus a shared abstract mixin in `core`. All entities use UUID primary keys and include creation timestamps. The schema supports food bank management, AI-generated recipes, donation tracking, admin authentication, QR analytics, and delivery fulfilment.

## Entities

### TimestampMixin (abstract -- `core` app)

Abstract base model providing `created_at` to domain entities. Models that also need `updated_at` add it explicitly.

| Field      | Type     | Constraints          | Description                     |
|------------|----------|----------------------|---------------------------------|
| created_at | datetime | auto-set on create   | When the record was created     |

**Notes**: Abstract model -- no database table. Provides only `created_at`; `updated_at` or other timestamps are added per-model where the user schema specifies them.

---

### FoodBank (`foodbanks` app)

The core entity representing a food bank organisation.

| Field                 | Type              | Constraints            | Description                              |
|-----------------------|-------------------|------------------------|------------------------------------------|
| id                    | UUIDField         | PK, default=uuid4      | Unique identifier                        |
| name                  | TextField         | required               | Name of the food bank                    |
| postcode              | TextField         | required               | Location postcode                        |
| latitude              | DecimalField(9,6) | required               | Geographic latitude for distance calculations |
| longitude             | DecimalField(9,6) | required               | Geographic longitude for distance calculations |
| address               | TextField         | required               | Full address                             |
| families_served_weekly| PositiveIntegerField | required, default=0  | Number of families served per week       |
| urgency_level         | CharField(10)     | choices: urgent, active, normal | Current need level            |
| last_updated          | DateTimeField     | auto-set on save       | When the wish list was last updated      |
| created_at            | DateTimeField     | auto-set on create     | Record creation time                     |

**Notes**:
- `urgency_level` uses TextChoices: `URGENT = "urgent"`, `ACTIVE = "active"`, `NORMAL = "normal"`.
- `last_updated` uses `auto_now=True` (updates on every save).
- No `email`, `phone`, `website`, `top_needs`, or `impact_story` -- removed per new schema.

---

### WishListItem (`foodbanks` app)

An individual item a food bank currently needs. Belongs to a Food Bank.

| Field           | Type              | Constraints                        | Description                           |
|-----------------|-------------------|------------------------------------|---------------------------------------|
| id              | UUIDField         | PK, default=uuid4                  | Unique identifier                     |
| food_bank       | ForeignKey        | FK -> FoodBank, CASCADE            | Parent food bank                      |
| item_name       | TextField         | required                           | Name of the item (e.g. "Tinned tomatoes") |
| category        | CharField(20)     | choices: tinned_goods, dried_goods, fresh, dairy, baby, hygiene | Item category |
| urgency         | CharField(10)     | choices: urgent, needed, optional  | How urgently it is needed             |
| quantity_needed | PositiveIntegerField | required, default=0              | Target quantity requested             |
| unit            | TextField         | required                           | Unit of measure (e.g. tins, packets)  |
| notes           | TextField         | blank allowed                      | Any additional context from the food bank |
| created_at      | DateTimeField     | auto-set on create                 | Record creation time                  |

**Notes**:
- `category` uses TextChoices enum with 6 values.
- `urgency` uses TextChoices with 3 values (adds `optional` vs previous schema).
- No `updated_at` -- user schema only specifies `created_at`.

---

### GeneratedRecipe (`foodbanks` app)

An AI-generated recipe produced from a food bank's wish list. Cached per food bank.

| Field              | Type              | Constraints                 | Description                                    |
|--------------------|-------------------|-----------------------------|------------------------------------------------|
| id                 | UUIDField         | PK, default=uuid4           | Unique identifier                              |
| food_bank          | ForeignKey        | FK -> FoodBank, CASCADE     | Food bank this was generated for               |
| recipe_name        | TextField         | required                    | Name of the recipe                             |
| description        | TextField         | required                    | Short description                              |
| serves             | PositiveIntegerField | required                 | Number of people the recipe feeds              |
| cook_time_minutes  | PositiveIntegerField | required                 | Estimated cooking time in minutes              |
| ingredients        | JSONField         | required                    | List of ingredients with quantities/units, mapped to wish list items |
| instructions       | TextField         | required                    | Step-by-step cooking instructions              |
| emoji              | TextField         | required                    | Emoji representing the dish                    |
| estimated_cost     | DecimalField(10,2)| required                    | Approximate cost of the full ingredient kit    |
| generated_at       | DateTimeField     | auto-set on create          | When the recipe was generated                  |
| expires_at         | DateTimeField     | required                    | Cache expiry time (24h after generation)       |

**Notes**:
- Replaces previous `RecipeKit` + `RecipeIngredient` models.
- `ingredients` is a JSON array; no separate ingredient table.
- `generated_at` replaces `created_at` -- uses `auto_now_add=True`.
- `expires_at` is set by application logic (generated_at + 24 hours).

---

### Donation (`donations` app)

A recorded donation event, used for analytics and delivery tracking.

| Field          | Type              | Constraints                         | Description                                |
|----------------|-------------------|-------------------------------------|--------------------------------------------|
| id             | UUIDField         | PK, default=uuid4                   | Unique identifier                          |
| food_bank      | ForeignKey        | FK -> FoodBank, CASCADE             | Recipient food bank                        |
| donation_type  | CharField(20)     | choices: recipe_kit, individual_items | How the donor donated                    |
| recipe         | ForeignKey        | FK -> GeneratedRecipe, SET_NULL, null, blank | Selected recipe (if applicable)   |
| items          | JSONField         | required                            | List of donated items with quantities      |
| total_cost     | DecimalField(10,2)| required                            | Total estimated value of the donation      |
| postcode       | CharField(10)     | required                            | Donor's postcode (first 4 chars, anonymised) |
| completed      | BooleanField      | default=False                       | Whether donation was completed to checkout |
| created_at     | DateTimeField     | auto-set on create                  | Record creation time                       |

**Notes**:
- Replaces previous `DonationBasket` + `BasketItem` models.
- `items` is a JSON array; no separate line item table.
- `recipe` uses `SET_NULL` (not CASCADE) -- donation record survives recipe cache expiry/deletion.
- No `updated_at` -- user schema only specifies `created_at`.

---

### FoodBankAdmin (`accounts` app)

An authenticated administrator account for a food bank.

| Field      | Type         | Constraints                    | Description                        |
|------------|--------------|--------------------------------|------------------------------------|
| id         | UUIDField    | PK, default=uuid4              | Unique identifier                  |
| food_bank  | ForeignKey   | FK -> FoodBank, CASCADE        | Managed food bank                  |
| email      | EmailField   | required, unique               | Admin's email address              |
| password   | CharField    | managed by AbstractBaseUser    | Hashed password (Django handles)   |
| created_at | DateTimeField| auto-set on create             | Record creation time               |

**Notes**:
- Extends `AbstractBaseUser` for Django's built-in password hashing and auth.
- `USERNAME_FIELD = "email"` -- email is the login identifier.
- No `updated_at` per user schema.
- Deviation from user schema: `password_hash` field implemented via Django's `AbstractBaseUser.password` which stores the hash using Django's password hashing framework (PBKDF2 by default).

---

### QRScan (`foodbanks` app)

An analytics event recorded each time a food bank's QR code is scanned.

| Field                 | Type         | Constraints                              | Description                                |
|-----------------------|--------------|------------------------------------------|--------------------------------------------|
| id                    | UUIDField    | PK, default=uuid4                        | Unique identifier                          |
| food_bank             | ForeignKey   | FK -> FoodBank, CASCADE                  | Food bank whose QR was scanned             |
| source                | CharField(20)| choices: qr_poster, qr_sticker, qr_social | Which QR format was scanned              |
| scanned_at            | DateTimeField| auto-set on create                       | When the scan occurred                     |
| converted_to_donation | BooleanField | default=False                            | Whether the scan led to a completed donation |
| donation              | ForeignKey   | FK -> Donation, SET_NULL, null, blank    | Resulting donation (if applicable)         |

**Notes**:
- `scanned_at` replaces `created_at` -- uses `auto_now_add=True`.
- `donation` uses SET_NULL so scan records survive donation deletion.

---

### FoodBankSettings (`foodbanks` app)

Delivery and integration preferences for a food bank. One record per food bank.

| Field                  | Type         | Constraints                    | Description                                     |
|------------------------|--------------|--------------------------------|-------------------------------------------------|
| id                     | UUIDField    | PK, default=uuid4              | Unique identifier                               |
| food_bank              | OneToOneField| FK -> FoodBank, CASCADE, unique| Food bank (one settings record per bank)        |
| pepesto_enabled        | BooleanField | default=False                  | Whether Pepesto supermarket integration is active |
| accept_direct_delivery | BooleanField | default=True                   | Accept deliveries direct from supermarkets      |
| allow_donor_collection | BooleanField | default=False                  | Allow donors to collect and drop off items      |
| delivery_notes         | TextField    | blank allowed                  | Special delivery instructions                   |
| created_at             | DateTimeField| auto-set on create             | Record creation time                            |
| updated_at             | DateTimeField| auto-set on save               | Last settings update time                       |

---

### FoodBankSupermarketPreference (`foodbanks` app)

Records which supermarkets a food bank accepts donations from. One record per food bank / supermarket combination.

| Field              | Type              | Constraints                                     | Description                              |
|--------------------|-------------------|--------------------------------------------------|------------------------------------------|
| id                 | UUIDField         | PK, default=uuid4                                | Unique identifier                        |
| food_bank          | ForeignKey        | FK -> FoodBank, CASCADE                          | Parent food bank                         |
| supermarket        | CharField(20)     | choices: tesco, sainsburys, asda, waitrose        | Supermarket name                         |
| enabled            | BooleanField      | default=True                                     | Whether this supermarket is active       |
| delivery_time_days | PositiveIntegerField | required, default=1                           | Estimated delivery time in days          |
| created_at         | DateTimeField     | auto-set on create                               | Record creation time                     |

**Notes**:
- Unique constraint on `(food_bank, supermarket)` -- one preference record per combination.
- No `updated_at` per user schema.

---

### DeliveryTracking (`donations` app)

Tracks the fulfilment status of a donation from dispatch through to receipt confirmation.

| Field              | Type              | Constraints                                | Description                              |
|--------------------|-------------------|--------------------------------------------|------------------------------------------|
| id                 | UUIDField         | PK, default=uuid4                          | Unique identifier                        |
| donation           | ForeignKey        | FK -> Donation, CASCADE                    | Parent donation                          |
| supermarket        | TextField         | required                                   | Supermarket fulfilling the delivery      |
| status             | CharField(20)     | choices: pending, dispatched, delivered, received | Current delivery status           |
| tracking_number    | TextField         | blank allowed                              | Supermarket-issued tracking reference    |
| estimated_delivery | DateTimeField     | null, blank allowed                        | Expected delivery date and time          |
| actual_delivery    | DateTimeField     | null, blank allowed                        | Actual delivery date and time            |
| received_confirmed | BooleanField      | default=False                              | Whether the food bank confirmed receipt  |
| notes              | TextField         | blank allowed                              | Notes about the delivery                 |
| created_at         | DateTimeField     | auto-set on create                         | Record creation time                     |
| updated_at         | DateTimeField     | auto-set on save                           | Last status update time                  |

---

## Relationships

```text
FoodBank 1--* WishListItem                  (food bank has many wish list items; CASCADE)
FoodBank 1--* GeneratedRecipe               (food bank has many generated recipes; CASCADE)
FoodBank 1--* Donation                      (food bank receives many donations; CASCADE)
FoodBank 1--* FoodBankAdmin                 (food bank has many admins; CASCADE)
FoodBank 1--* QRScan                        (food bank has many QR scan events; CASCADE)
FoodBank 1--1 FoodBankSettings              (food bank has one settings record; CASCADE)
FoodBank 1--* FoodBankSupermarketPreference (food bank has supermarket preferences; CASCADE)
Donation  1--* DeliveryTracking             (donation has delivery tracking records; CASCADE)
GeneratedRecipe 1--* Donation               (recipe referenced by donations; SET_NULL)
Donation  1--* QRScan                       (donation referenced by QR scans; SET_NULL)
```

## State Transitions

### FoodBank Urgency Level

```text
normal <-> active <-> urgent
```

- Three levels: `normal`, `active`, `urgent`. Freely changeable.

### WishListItem Urgency

```text
optional <-> needed <-> urgent
```

- Three levels: `optional`, `needed`, `urgent`. Freely changeable.

### Delivery Tracking Status

```text
pending -> dispatched -> delivered -> received
```

- Linear progression. No reverse transitions.
- `pending`: Initial state when tracking record created.
- `dispatched`: Supermarket has dispatched the order.
- `delivered`: Delivery has arrived at food bank.
- `received`: Food bank has confirmed receipt.
