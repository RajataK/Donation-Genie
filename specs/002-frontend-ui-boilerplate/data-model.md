# Data Model: Frontend UI Boilerplate

**Feature**: 002-frontend-ui-boilerplate
**Date**: 2026-02-26

> This feature uses static placeholder data only. No database models or backend changes are required.
> The data model below defines the TypeScript interfaces for the mock data that powers the UI.

## Entities

### FoodBank

Represents a charitable food bank organization displayed in search results and detail pages.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | string | Unique identifier | Required, non-empty |
| name | string | Display name of the food bank | Required, non-empty |
| distance | string | Human-readable distance from donor (e.g., "0.8 miles away") | Required |
| distanceMiles | number | Numeric distance for sorting | Required, >= 0 |
| urgencyStatus | "urgent" \| "active" | Current urgency level | Required |
| familiesServed | number | Number of families served per week | Required, >= 0 |
| topNeeds | string[] | List of most-needed item names | Required, min 1 item |
| impactStory | string | Narrative describing the food bank's impact | Required, non-empty |

### WishListItem

An individual item on a food bank's wish list.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | string | Unique identifier | Required, non-empty |
| name | string | Item name (e.g., "Tinned Tomatoes") | Required, non-empty |
| description | string | Brief detail (e.g., "400g tins") | Required |
| urgencyLevel | "urgent" \| "needed" | Priority indicator | Required |
| category | string | Item category (e.g., "Tinned goods") | Required, non-empty |
| estimatedPrice | number | Estimated cost per unit in GBP | Required, > 0 |

### RecipeKit

An AI-generated meal kit composed of wish list items.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | string | Unique identifier | Required, non-empty |
| name | string | Recipe name (e.g., "Spaghetti Bolognese Kit") | Required, non-empty |
| icon | string | Visual emoji indicator | Required |
| servings | string | Serving info (e.g., "Feeds family of 4") | Required |
| prepTime | string | Preparation time (e.g., "Ready in 30 mins") | Required |
| ingredients | RecipeIngredient[] | List of ingredients in the kit | Required, min 1 |
| totalCost | number | Kit total cost in GBP | Required, > 0 |

### RecipeIngredient

A single ingredient within a recipe kit.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| name | string | Ingredient description (e.g., "Pasta (500g)") | Required, non-empty |
| matched | boolean | Whether it maps to a wish list item | Required |

### BasketItem

A line item in the donor's donation basket.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | string | Unique identifier | Required, non-empty |
| name | string | Product name | Required, non-empty |
| quantity | number | Number of units | Required, >= 1 |
| unitPrice | number | Cost per unit in GBP | Required, > 0 |

### DonationBasket

The donor's complete basket at checkout.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| foodBankId | string | Target food bank ID | Required |
| foodBankName | string | Target food bank name | Required |
| items | BasketItem[] | Line items in the basket | Required |
| deliveryCost | number | Delivery fee in GBP | Required, >= 0 |
| totalCost | number | Grand total (items + delivery) | Computed |
| donationType | "direct" \| "recipe-kit" | How items were selected | Required |
| recipeName | string \| null | Recipe name if recipe-kit type | Required if donationType is "recipe-kit" |

### SupermarketProduct

A mapped supermarket product shown in the checkout basket.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| name | string | Supermarket-specific product name | Required, non-empty |
| retailer | string | Supermarket name (e.g., "Tesco") | Required |
| price | number | Product price in GBP | Required, > 0 |

### QRCodeFormat

A downloadable QR code format option.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | string | Unique identifier | Required |
| label | string | Format label (e.g., "In-Store Poster") | Required |
| description | string | Brief description | Required |
| fileType | string | Download format (e.g., "PDF", "PNG", "JPG") | Required |

### DeliveryPreference

An admin delivery configuration option.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | string | Unique identifier | Required |
| label | string | Preference name | Required |
| description | string | Explanation of the preference | Required |
| enabled | boolean | Whether this preference is active | Required |

### SupermarketPartner

A supermarket partner configuration.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | string | Unique identifier | Required |
| name | string | Supermarket name | Required |
| deliveryTime | string | Typical delivery time | Required |
| available | boolean | Whether this partner is currently available | Required |
| enabled | boolean | Whether this partner is selected by the admin | Required |

## Relationships

```
FoodBank 1──* WishListItem       (food bank has many wish list items)
FoodBank 1──* RecipeKit          (food bank has many AI-generated recipe kits)
RecipeKit 1──* RecipeIngredient  (recipe kit contains ingredients)
DonationBasket *──1 FoodBank     (basket targets one food bank)
DonationBasket 1──* BasketItem   (basket contains line items)
FoodBank 1──* QRCodeFormat       (food bank has multiple QR formats)
FoodBank 1──* DeliveryPreference (food bank has delivery preferences)
FoodBank *──* SupermarketPartner (food bank selects partners)
```

## State Transitions

### Donor Journey Navigation State

```
Landing → SearchResults → FoodBankDetail → DirectItems → Checkout
                                         → RecipeKits  → Checkout
```

### Basket State

```
Empty → ItemAdded → ItemUpdated → ReadyForCheckout
                  → ItemRemoved → Empty (if last item)
```
