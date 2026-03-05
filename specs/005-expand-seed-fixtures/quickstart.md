# Quickstart: Expand Seed Fixtures

## What Changed

The seed fixture file `backend/fixtures/seed.json` has been expanded from ~10 records (1 food bank) to ~300+ records (40 food banks) with realistic UK-wide data.

## Loading the Fixtures

```bash
cd backend
python manage.py loaddata seed
```

This loads all seed data into the database. It is idempotent — running it multiple times will not create duplicates (UUIDs are hardcoded).

## Verifying the Data

```bash
cd backend
python manage.py shell -c "
from apps.foodbanks.models import FoodBank, WishListItem, GeneratedRecipe, FoodBankSettings, FoodBankSupermarketPreference, QRScan
from apps.donations.models import Donation, DeliveryTracking
print(f'Food banks: {FoodBank.objects.count()}')
print(f'Wishlist items: {WishListItem.objects.count()}')
print(f'Recipes: {GeneratedRecipe.objects.count()}')
print(f'Donations: {Donation.objects.count()}')
print(f'Delivery tracking: {DeliveryTracking.objects.count()}')
print(f'Settings: {FoodBankSettings.objects.count()}')
print(f'Supermarket prefs: {FoodBankSupermarketPreference.objects.count()}')
print(f'QR scans: {QRScan.objects.count()}')
"
```

## Running Fixture Validation Tests

```bash
cd backend
pytest tests/core/test_seed_fixtures.py -v
```

## Data Overview

| Model | Count | Notes |
|-------|-------|-------|
| FoodBank | 40 | Across England, Scotland, Wales, NI |
| WishListItem | 120+ | 6 categories, 3 urgency levels |
| GeneratedRecipe | 12 | Spread across 8 food banks |
| Donation | 18 | Mix of recipe_kit and individual_items |
| DeliveryTracking | 12 | All 4 statuses represented |
| FoodBankSettings | 25 | Varied configurations |
| FoodBankSupermarketPreference | 40 | All 4 supermarkets |
| QRScan | 15 | All 3 sources represented |
