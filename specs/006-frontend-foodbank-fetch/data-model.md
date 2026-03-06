# Data Model: Frontend Food Bank Data Fetch

## Existing Entity: FoodBank

The `FoodBank` model already exists in `backend/apps/foodbanks/models.py`. No schema changes required.

### Fields Exposed via API

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| name | Text | Food bank name |
| postcode | Text | UK postcode |
| latitude | Decimal(9,6) | Geographic latitude |
| longitude | Decimal(9,6) | Geographic longitude |
| address | Text | Full address |
| families_served_weekly | Positive Integer | Number of families served per week |
| urgency_level | Enum (urgent, active, normal) | Current urgency status |
| last_updated | DateTime | Auto-set on save |

### Relationships (not exposed in this feature)

- `wish_list_items` → WishListItem (one-to-many)
- `generated_recipes` → GeneratedRecipe (one-to-many)
- `settings` → FoodBankSettings (one-to-one)
- `supermarket_preferences` → FoodBankSupermarketPreference (one-to-many)
- `qr_scans` → QRScan (one-to-many)

### Notes

- No new models or migrations needed
- The serializer will expose all fields listed above as read-only
- Related entities are excluded from this endpoint (flat list only)
- The `created_at` field from `TimestampMixin` is excluded as it is internal metadata
