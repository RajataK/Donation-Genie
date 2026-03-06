# Data Model: Expand Seed Fixtures

No schema changes are required for this feature. This document describes the existing models and the seed data distribution plan.

## Existing Models (unchanged)

### foodbanks.FoodBank
| Field | Type | Constraints | Seed Notes |
|-------|------|-------------|------------|
| id | UUID | PK | 40 unique hardcoded UUIDs |
| name | Text | Required | Realistic UK food bank names |
| postcode | Text | Required | Valid UK postcodes matching location |
| latitude | Decimal(9,6) | Required | Real UK coordinates (49.9–60.8°N) |
| longitude | Decimal(9,6) | Required | Real UK coordinates (-8.2–1.8°E) |
| address | Text | Required | Realistic UK street addresses |
| families_served_weekly | PositiveInt | Default 0 | Range 20–500 |
| urgency_level | Choice | urgent/active/normal | Mixed distribution |
| created_at | DateTime | Auto | Fixed seed timestamp |
| last_updated | DateTime | Auto | Fixed seed timestamp |

### foodbanks.WishListItem
| Field | Type | Constraints | Seed Notes |
|-------|------|-------------|------------|
| id | UUID | PK | 120+ unique hardcoded UUIDs |
| food_bank | FK → FoodBank | Required | 3-5 items per food bank |
| item_name | Text | Required | 40+ distinct product names |
| category | Choice | tinned_goods/dried_goods/fresh/dairy/baby/hygiene | All 6 represented |
| urgency | Choice | urgent/needed/optional | All 3 represented |
| quantity_needed | PositiveInt | Default 0 | Range 5–100 |
| unit | Text | Required | tins/kg/litres/packs/items/boxes/rolls |
| notes | Text | Blank OK | Optional details |
| created_at | DateTime | Auto | Fixed seed timestamp |

### foodbanks.GeneratedRecipe
| Field | Type | Constraints | Seed Notes |
|-------|------|-------------|------------|
| id | UUID | PK | 12 unique UUIDs |
| food_bank | FK → FoodBank | Required | Spread across 8 food banks |
| recipe_name | Text | Required | Realistic recipe names |
| description | Text | Required | Short recipe descriptions |
| serves | PositiveInt | Required | 2–6 |
| cook_time_minutes | PositiveInt | Required | 10–60 |
| ingredients | JSON | Required | Array of {name, quantity, unit, wish_list_match} |
| instructions | Text | Required | Numbered steps |
| emoji | Text | Required | Food emoji |
| estimated_cost | Decimal(10,2) | Required | 2.00–8.00 |
| generated_at | DateTime | Auto | Fixed seed timestamp |
| expires_at | DateTime | Required | generated_at + 24h |

### donations.Donation
| Field | Type | Constraints | Seed Notes |
|-------|------|-------------|------------|
| id | UUID | PK | 18 unique UUIDs |
| food_bank | FK → FoodBank | Required | Spread across multiple food banks |
| donation_type | Choice | recipe_kit/individual_items | ~60/40 split |
| recipe | FK → GeneratedRecipe | Nullable | Set for recipe_kit type |
| items | JSON | Required | Array of {name, quantity, unit_price} |
| total_cost | Decimal(10,2) | Required | Sum of item costs |
| postcode | Char(10) | Required | UK donor postcodes |
| completed | Boolean | Default false | Mix of true/false |
| created_at | DateTime | Auto | Fixed seed timestamp |

### donations.DeliveryTracking
| Field | Type | Constraints | Seed Notes |
|-------|------|-------------|------------|
| id | UUID | PK | 12 unique UUIDs |
| donation | FK → Donation | Required | One per tracked donation |
| supermarket | Text | Required | Tesco/Sainsburys/Asda/Waitrose |
| status | Choice | pending/dispatched/delivered/received | All 4 represented |
| tracking_number | Text | Blank OK | TRK-2026-NNN format |
| estimated_delivery | DateTime | Nullable | Set for dispatched+ |
| actual_delivery | DateTime | Nullable | Set for delivered+ |
| received_confirmed | Boolean | Default false | True for received status |
| notes | Text | Blank OK | Optional delivery notes |
| created_at | DateTime | Auto | Fixed seed timestamp |
| updated_at | DateTime | Auto | Fixed seed timestamp |

### foodbanks.FoodBankSettings
| Field | Type | Constraints | Seed Notes |
|-------|------|-------------|------------|
| id | UUID | PK | 25 unique UUIDs |
| food_bank | OneToOne → FoodBank | Required | 25 of 40 food banks |
| pepesto_enabled | Boolean | Default false | Mixed true/false |
| accept_direct_delivery | Boolean | Default true | Mostly true |
| allow_donor_collection | Boolean | Default false | Some true |
| delivery_notes | Text | Blank OK | Varied delivery instructions |
| created_at | DateTime | Auto | Fixed seed timestamp |
| updated_at | DateTime | Auto | Fixed seed timestamp |

### foodbanks.FoodBankSupermarketPreference
| Field | Type | Constraints | Seed Notes |
|-------|------|-------------|------------|
| id | UUID | PK | 40 unique UUIDs |
| food_bank | FK → FoodBank | Required | 1-3 per food bank with settings |
| supermarket | Choice | tesco/sainsburys/asda/waitrose | All 4 represented |
| enabled | Boolean | Default true | Mostly true |
| delivery_time_days | PositiveInt | Default 1 | 1–5 |
| created_at | DateTime | Auto | Fixed seed timestamp |
| Unique constraint | (food_bank, supermarket) | | No duplicates |

### foodbanks.QRScan
| Field | Type | Constraints | Seed Notes |
|-------|------|-------------|------------|
| id | UUID | PK | 15 unique UUIDs |
| food_bank | FK → FoodBank | Required | Spread across 10 food banks |
| source | Choice | qr_poster/qr_sticker/qr_social | All 3 represented |
| scanned_at | DateTime | Auto | Varied timestamps |
| converted_to_donation | Boolean | Default false | ~40% true |
| donation | FK → Donation | Nullable | Set when converted |

## Relationships

```text
FoodBank (40)
├── WishListItem (120+)         many-to-one
├── GeneratedRecipe (12)        many-to-one
├── Donation (18)               many-to-one
│   └── DeliveryTracking (12)   many-to-one
├── FoodBankSettings (25)       one-to-one
├── FoodBankSupermarketPreference (40)  many-to-one
└── QRScan (15)                 many-to-one
    └── Donation (nullable FK)  many-to-one
```

## Validation Rules (for tests)

1. All UUIDs unique across entire fixture
2. All FK references point to existing records in fixture
3. All choice field values match model TextChoices definitions
4. Latitude range: 49.9–60.8 (UK bounds)
5. Longitude range: -8.2–1.8 (UK bounds)
6. families_served_weekly: 20–500
7. FoodBankSupermarketPreference: no duplicate (food_bank, supermarket) pairs
8. FoodBankSettings: no duplicate food_bank (one-to-one)
9. Donation with donation_type="recipe_kit" must have non-null recipe FK
10. DeliveryTracking with status="received" must have received_confirmed=true
