# API Contract: List Food Banks

## Endpoint

```
GET /api/food-banks/
```

## Authentication

None required.

## Request

No query parameters, no request body.

## Response

### 200 OK

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Hackney Food Bank",
    "postcode": "E8 1DY",
    "latitude": "51.543800",
    "longitude": "-0.055300",
    "address": "29 Dalston Lane, London E8 1DY",
    "families_served_weekly": 150,
    "urgency_level": "urgent",
    "last_updated": "2026-03-06T12:00:00Z"
  }
]
```

### Field Types

| Field | JSON Type | Format | Nullable |
|-------|-----------|--------|----------|
| id | string | UUID v4 | No |
| name | string | - | No |
| postcode | string | UK postcode | No |
| latitude | string | Decimal (9,6) | No |
| longitude | string | Decimal (9,6) | No |
| address | string | - | No |
| families_served_weekly | integer | >= 0 | No |
| urgency_level | string | Enum: urgent, active, normal | No |
| last_updated | string | ISO 8601 datetime | No |

### Notes

- Returns all food bank records (no pagination)
- Response is a JSON array at the top level
- Empty array `[]` returned when no food banks exist
- Decimal fields are serialized as strings by DRF (standard behavior)
- Field names use snake_case (Django/DRF convention)
