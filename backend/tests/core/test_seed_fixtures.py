"""Tests for seed fixture data integrity.

Validates backend/fixtures/seed.json without requiring a database —
all checks operate on the raw JSON structure.
"""

import json
from pathlib import Path

import pytest

FIXTURE_PATH = Path(__file__).resolve().parents[2] / "fixtures" / "seed.json"


@pytest.fixture(scope="module")
def fixture_data():
    """Load and return the parsed seed fixture JSON."""
    with open(FIXTURE_PATH) as f:
        return json.load(f)


def records_by_model(fixture_data, model_name):
    """Return all fixture records matching the given model name."""
    return [r for r in fixture_data if r["model"] == model_name]


def all_pks(fixture_data):
    """Return all pk values from the fixture."""
    return [r["pk"] for r in fixture_data]


def pks_for_model(fixture_data, model_name):
    """Return the set of pk values for a given model."""
    return {r["pk"] for r in records_by_model(fixture_data, model_name)}


# ---------------------------------------------------------------------------
# US1: Food bank tests
# ---------------------------------------------------------------------------

FOOD_BANK_MODEL = "foodbanks.foodbank"


class TestFoodBanks:
    def test_exactly_40_food_banks(self, fixture_data):
        banks = records_by_model(fixture_data, FOOD_BANK_MODEL)
        assert len(banks) == 40

    def test_all_food_bank_uuids_unique(self, fixture_data):
        pks = [r["pk"] for r in records_by_model(fixture_data, FOOD_BANK_MODEL)]
        assert len(pks) == len(set(pks))

    def test_latitudes_within_uk_bounds(self, fixture_data):
        for r in records_by_model(fixture_data, FOOD_BANK_MODEL):
            lat = float(r["fields"]["latitude"])
            assert 49.9 <= lat <= 60.8, f"{r['fields']['name']} lat {lat} out of UK bounds"

    def test_longitudes_within_uk_bounds(self, fixture_data):
        for r in records_by_model(fixture_data, FOOD_BANK_MODEL):
            lon = float(r["fields"]["longitude"])
            assert -8.2 <= lon <= 1.8, f"{r['fields']['name']} lon {lon} out of UK bounds"

    def test_covers_at_least_10_uk_regions(self, fixture_data):
        expected_cities = {
            "London", "Manchester", "Birmingham", "Edinburgh", "Glasgow",
            "Cardiff", "Belfast", "Leeds", "Liverpool", "Bristol",
        }
        addresses = " ".join(
            r["fields"]["address"] for r in records_by_model(fixture_data, FOOD_BANK_MODEL)
        )
        found = {city for city in expected_cities if city in addresses}
        assert len(found) >= 10, f"Only found {found} — need at least 10 cities"

    def test_valid_urgency_levels(self, fixture_data):
        valid = {"urgent", "active", "normal"}
        for r in records_by_model(fixture_data, FOOD_BANK_MODEL):
            assert r["fields"]["urgency_level"] in valid, (
                f"{r['fields']['name']} has invalid urgency_level: {r['fields']['urgency_level']}"
            )

    def test_families_served_weekly_in_range(self, fixture_data):
        for r in records_by_model(fixture_data, FOOD_BANK_MODEL):
            val = r["fields"]["families_served_weekly"]
            assert 20 <= val <= 500, f"{r['fields']['name']} families_served_weekly={val}"

    def test_all_food_bank_names_unique(self, fixture_data):
        names = [r["fields"]["name"] for r in records_by_model(fixture_data, FOOD_BANK_MODEL)]
        assert len(names) == len(set(names))


# ---------------------------------------------------------------------------
# US2: Wishlist item tests
# ---------------------------------------------------------------------------

WISHLIST_MODEL = "foodbanks.wishlistitem"


class TestWishlistItems:
    def test_at_least_120_wishlist_items(self, fixture_data):
        items = records_by_model(fixture_data, WISHLIST_MODEL)
        assert len(items) >= 120

    def test_all_wishlist_uuids_unique(self, fixture_data):
        pks = [r["pk"] for r in records_by_model(fixture_data, WISHLIST_MODEL)]
        assert len(pks) == len(set(pks))

    def test_all_six_categories_represented(self, fixture_data):
        expected = {"tinned_goods", "dried_goods", "fresh", "dairy", "baby", "hygiene"}
        found = {r["fields"]["category"] for r in records_by_model(fixture_data, WISHLIST_MODEL)}
        assert expected == found & expected, f"Missing categories: {expected - found}"

    def test_all_three_urgency_levels_represented(self, fixture_data):
        expected = {"urgent", "needed", "optional"}
        found = {r["fields"]["urgency"] for r in records_by_model(fixture_data, WISHLIST_MODEL)}
        assert expected == found & expected, f"Missing urgency levels: {expected - found}"

    def test_at_least_30_distinct_item_names(self, fixture_data):
        names = {r["fields"]["item_name"] for r in records_by_model(fixture_data, WISHLIST_MODEL)}
        assert len(names) >= 30, f"Only {len(names)} distinct item names"

    def test_all_food_bank_fks_valid(self, fixture_data):
        bank_pks = pks_for_model(fixture_data, FOOD_BANK_MODEL)
        for r in records_by_model(fixture_data, WISHLIST_MODEL):
            fk = r["fields"]["food_bank"]
            assert fk in bank_pks, f"Wishlist item {r['pk']} references unknown food bank {fk}"


# ---------------------------------------------------------------------------
# US3: Related tables tests
# ---------------------------------------------------------------------------

RECIPE_MODEL = "foodbanks.generatedrecipe"
DONATION_MODEL = "donations.donation"
DELIVERY_MODEL = "donations.deliverytracking"
SETTINGS_MODEL = "foodbanks.foodbanksettings"
SUPERMARKET_MODEL = "foodbanks.foodbanksupermarketpreference"
QRSCAN_MODEL = "foodbanks.qrscan"


class TestGeneratedRecipes:
    def test_at_least_12_recipes(self, fixture_data):
        recipes = records_by_model(fixture_data, RECIPE_MODEL)
        assert len(recipes) >= 12

    def test_valid_food_bank_fks(self, fixture_data):
        bank_pks = pks_for_model(fixture_data, FOOD_BANK_MODEL)
        for r in records_by_model(fixture_data, RECIPE_MODEL):
            assert r["fields"]["food_bank"] in bank_pks

    def test_non_empty_ingredients(self, fixture_data):
        for r in records_by_model(fixture_data, RECIPE_MODEL):
            assert len(r["fields"]["ingredients"]) > 0, f"Recipe {r['pk']} has empty ingredients"


class TestDonations:
    def test_at_least_18_donations(self, fixture_data):
        donations = records_by_model(fixture_data, DONATION_MODEL)
        assert len(donations) >= 18

    def test_valid_food_bank_fks(self, fixture_data):
        bank_pks = pks_for_model(fixture_data, FOOD_BANK_MODEL)
        for r in records_by_model(fixture_data, DONATION_MODEL):
            assert r["fields"]["food_bank"] in bank_pks

    def test_valid_donation_types(self, fixture_data):
        valid = {"recipe_kit", "individual_items"}
        for r in records_by_model(fixture_data, DONATION_MODEL):
            assert r["fields"]["donation_type"] in valid

    def test_recipe_kit_has_valid_recipe_fk(self, fixture_data):
        recipe_pks = pks_for_model(fixture_data, RECIPE_MODEL)
        for r in records_by_model(fixture_data, DONATION_MODEL):
            if r["fields"]["donation_type"] == "recipe_kit":
                assert r["fields"]["recipe"] in recipe_pks, (
                    f"Donation {r['pk']} is recipe_kit but references invalid recipe"
                )


class TestDeliveryTracking:
    def test_at_least_12_delivery_records(self, fixture_data):
        records = records_by_model(fixture_data, DELIVERY_MODEL)
        assert len(records) >= 12

    def test_valid_donation_fks(self, fixture_data):
        donation_pks = pks_for_model(fixture_data, DONATION_MODEL)
        for r in records_by_model(fixture_data, DELIVERY_MODEL):
            assert r["fields"]["donation"] in donation_pks

    def test_valid_status_values(self, fixture_data):
        valid = {"pending", "dispatched", "delivered", "received"}
        for r in records_by_model(fixture_data, DELIVERY_MODEL):
            assert r["fields"]["status"] in valid

    def test_received_has_confirmed_true(self, fixture_data):
        for r in records_by_model(fixture_data, DELIVERY_MODEL):
            if r["fields"]["status"] == "received":
                assert r["fields"]["received_confirmed"] is True, (
                    f"Delivery {r['pk']} has status=received but received_confirmed is not True"
                )


class TestFoodBankSettings:
    def test_at_least_25_settings(self, fixture_data):
        records = records_by_model(fixture_data, SETTINGS_MODEL)
        assert len(records) >= 25

    def test_valid_food_bank_fks(self, fixture_data):
        bank_pks = pks_for_model(fixture_data, FOOD_BANK_MODEL)
        for r in records_by_model(fixture_data, SETTINGS_MODEL):
            assert r["fields"]["food_bank"] in bank_pks

    def test_no_duplicate_food_banks(self, fixture_data):
        fks = [r["fields"]["food_bank"] for r in records_by_model(fixture_data, SETTINGS_MODEL)]
        assert len(fks) == len(set(fks)), "Duplicate food_bank in settings (violates one-to-one)"


class TestSupermarketPreferences:
    def test_at_least_40_preferences(self, fixture_data):
        records = records_by_model(fixture_data, SUPERMARKET_MODEL)
        assert len(records) >= 40

    def test_valid_food_bank_fks(self, fixture_data):
        bank_pks = pks_for_model(fixture_data, FOOD_BANK_MODEL)
        for r in records_by_model(fixture_data, SUPERMARKET_MODEL):
            assert r["fields"]["food_bank"] in bank_pks

    def test_valid_supermarket_values(self, fixture_data):
        valid = {"tesco", "sainsburys", "asda", "waitrose"}
        for r in records_by_model(fixture_data, SUPERMARKET_MODEL):
            assert r["fields"]["supermarket"] in valid

    def test_no_duplicate_food_bank_supermarket_pairs(self, fixture_data):
        pairs = [
            (r["fields"]["food_bank"], r["fields"]["supermarket"])
            for r in records_by_model(fixture_data, SUPERMARKET_MODEL)
        ]
        assert len(pairs) == len(set(pairs)), "Duplicate (food_bank, supermarket) pair"


class TestQRScans:
    def test_at_least_15_qr_scans(self, fixture_data):
        records = records_by_model(fixture_data, QRSCAN_MODEL)
        assert len(records) >= 15

    def test_valid_food_bank_fks(self, fixture_data):
        bank_pks = pks_for_model(fixture_data, FOOD_BANK_MODEL)
        for r in records_by_model(fixture_data, QRSCAN_MODEL):
            assert r["fields"]["food_bank"] in bank_pks

    def test_valid_source_values(self, fixture_data):
        valid = {"qr_poster", "qr_sticker", "qr_social"}
        for r in records_by_model(fixture_data, QRSCAN_MODEL):
            assert r["fields"]["source"] in valid

    def test_converted_scans_have_valid_donation_fks(self, fixture_data):
        donation_pks = pks_for_model(fixture_data, DONATION_MODEL)
        for r in records_by_model(fixture_data, QRSCAN_MODEL):
            if r["fields"]["converted_to_donation"]:
                assert r["fields"]["donation"] in donation_pks, (
                    f"QR scan {r['pk']} is converted but references invalid donation"
                )


# ---------------------------------------------------------------------------
# Cross-cutting tests
# ---------------------------------------------------------------------------


class TestFixtureIntegrity:
    def test_all_uuids_globally_unique(self, fixture_data):
        pks = all_pks(fixture_data)
        assert len(pks) == len(set(pks)), "Duplicate pk found across models"

    def test_all_fk_references_valid(self, fixture_data):
        all_pk_set = set(all_pks(fixture_data))
        fk_fields = {
            WISHLIST_MODEL: ["food_bank"],
            RECIPE_MODEL: ["food_bank"],
            DONATION_MODEL: ["food_bank", "recipe"],
            DELIVERY_MODEL: ["donation"],
            SETTINGS_MODEL: ["food_bank"],
            SUPERMARKET_MODEL: ["food_bank"],
            QRSCAN_MODEL: ["food_bank", "donation"],
        }
        for model, fields in fk_fields.items():
            for r in records_by_model(fixture_data, model):
                for field in fields:
                    val = r["fields"].get(field)
                    if val is not None:
                        assert val in all_pk_set, (
                            f"{model} {r['pk']} field '{field}' references unknown pk {val}"
                        )
