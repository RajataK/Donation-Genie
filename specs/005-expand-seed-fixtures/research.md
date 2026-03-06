# Research: Expand Seed Fixtures

## R1: UK Food Bank Geographic Distribution

**Decision**: Distribute 40 food banks across major UK cities and towns covering all four nations.

**Rationale**: The UK has approximately 2,500+ food banks. Selecting 40 locations ensures coverage of major population centers and geographic diversity for map/proximity testing.

**Distribution plan**:
- England (28): London (5), Manchester (2), Birmingham (2), Leeds (1), Liverpool (1), Bristol (1), Sheffield (1), Newcastle (1), Nottingham (1), Leicester (1), Southampton (1), Brighton (1), Oxford (1), Cambridge (1), Plymouth (1), Norwich (1), York (1), Bath (1), Exeter (1), Coventry (1), Reading (1)
- Scotland (5): Edinburgh (2), Glasgow (2), Aberdeen (1)
- Wales (4): Cardiff (2), Swansea (1), Bangor (1)
- Northern Ireland (3): Belfast (2), Derry/Londonderry (1)

**Alternatives considered**: Random coordinate generation (rejected — produces unrealistic locations), using only major cities (rejected — insufficient spread).

## R2: Wishlist Item Variety

**Decision**: Use 40+ distinct product names across all 6 categories.

**Rationale**: Real food banks publish diverse wishlists. Using realistic product names enables meaningful testing of search, filter, and display features.

**Product name examples by category**:
- **tinned_goods**: Baked Beans, Tinned Tomatoes, Tinned Soup, Tinned Tuna, Tinned Sweetcorn, Tinned Fruit, Tinned Spaghetti, Tinned Chickpeas
- **dried_goods**: Rice, Pasta, Cereal, Porridge Oats, Flour, Couscous, Lentils, Instant Noodles
- **fresh**: Potatoes, Onions, Carrots, Apples, Bananas, Bread, Eggs
- **dairy**: UHT Milk, Long-Life Juice, Powdered Milk, Cheese Spread
- **baby**: Baby Formula, Nappies (Size 3), Nappies (Size 5), Baby Wipes, Baby Food Pouches
- **hygiene**: Toothpaste, Shampoo, Soap, Deodorant, Washing-Up Liquid, Laundry Detergent, Toilet Roll, Sanitary Products

**Alternatives considered**: Using generic item names like "Item 1" (rejected — unrealistic, poor test coverage).

## R3: Django Fixture Format Constraints

**Decision**: Continue using Django's native JSON fixture format with hardcoded UUIDs.

**Rationale**: The existing `seed.json` already follows this format. Django's `loaddata` handles idempotent loading when PKs are specified. No need to change the approach.

**Key constraints verified**:
- All `pk` fields must be valid UUID v4 strings
- All `model` fields must use `app_label.modelname` format (lowercase)
- Foreign key fields reference the UUID of the related record
- `auto_now` and `auto_now_add` fields can be included in fixtures (Django sets them during load)
- JSON fields (ingredients, items) must be valid JSON objects/arrays

**Alternatives considered**: Using Django's dumpdata to generate fixtures (rejected — we need handcrafted realistic data), using factory_boy for dynamic generation (rejected — spec requires a static fixture file).

## R4: Related Table Record Counts

**Decision**: Scale related tables proportionally to the 40 food banks.

**Rationale**: Not every food bank needs every related record. A realistic distribution means some food banks have more activity than others.

**Distribution plan**:
- FoodBankSettings: 25 records (not all food banks have configured settings yet)
- FoodBankSupermarketPreference: 40 records (1-3 per food bank with settings)
- GeneratedRecipe: 12 records (spread across 8 food banks)
- Donation: 18 records (mix of recipe_kit and individual_items)
- DeliveryTracking: 12 records (one per delivered/dispatched donation)
- QRScan: 15 records (spread across 10 food banks, varied sources)

**Alternatives considered**: Equal records per food bank (rejected — unrealistic, real data is uneven).
