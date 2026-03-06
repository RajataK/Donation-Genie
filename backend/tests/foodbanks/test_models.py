import uuid
from datetime import timedelta

import pytest
from decimal import Decimal
from django.utils import timezone

from django.db import IntegrityError

from apps.foodbanks.models import (
    FoodBank, WishListItem, GeneratedRecipe,
    FoodBankSettings, FoodBankSupermarketPreference, QRScan,
)
from apps.donations.models import Donation


@pytest.mark.django_db
class TestFoodBank:
    def _create_food_bank(self, **overrides):
        defaults = {
            "name": "Test Food Bank",
            "postcode": "E1 6AN",
            "latitude": Decimal("51.517000"),
            "longitude": Decimal("-0.073000"),
            "address": "123 Main St, London",
            "families_served_weekly": 100,
            "urgency_level": FoodBank.UrgencyLevel.ACTIVE,
        }
        defaults.update(overrides)
        return FoodBank.objects.create(**defaults)

    def test_create_with_all_fields(self):
        fb = self._create_food_bank()
        retrieved = FoodBank.objects.get(pk=fb.pk)
        assert retrieved.name == "Test Food Bank"
        assert retrieved.postcode == "E1 6AN"
        assert retrieved.latitude == Decimal("51.517000")
        assert retrieved.longitude == Decimal("-0.073000")
        assert retrieved.address == "123 Main St, London"
        assert retrieved.families_served_weekly == 100
        assert retrieved.urgency_level == "active"

    def test_uuid_primary_key(self):
        fb = self._create_food_bank()
        assert isinstance(fb.pk, uuid.UUID)

    def test_filter_by_urgency_level(self):
        self._create_food_bank(name="Active Bank", urgency_level=FoodBank.UrgencyLevel.ACTIVE)
        self._create_food_bank(name="Urgent Bank", urgency_level=FoodBank.UrgencyLevel.URGENT)
        self._create_food_bank(name="Normal Bank", urgency_level=FoodBank.UrgencyLevel.NORMAL)
        assert FoodBank.objects.filter(urgency_level="active").count() == 1
        assert FoodBank.objects.filter(urgency_level="urgent").count() == 1
        assert FoodBank.objects.filter(urgency_level="normal").count() == 1

    def test_update_fields(self):
        fb = self._create_food_bank()
        fb.urgency_level = FoodBank.UrgencyLevel.URGENT
        fb.families_served_weekly = 200
        fb.save()
        fb.refresh_from_db()
        assert fb.urgency_level == "urgent"
        assert fb.families_served_weekly == 200

    def test_created_at_auto_populated(self):
        fb = self._create_food_bank()
        assert fb.created_at is not None

    def test_last_updated_auto_populated(self):
        fb = self._create_food_bank()
        assert fb.last_updated is not None

    def test_str_returns_name(self):
        fb = self._create_food_bank(name="My Food Bank")
        assert str(fb) == "My Food Bank"

    def test_urgency_level_choices(self):
        choices = [c[0] for c in FoodBank.UrgencyLevel.choices]
        assert "urgent" in choices
        assert "active" in choices
        assert "normal" in choices


def _make_food_bank(**overrides):
    defaults = {
        "name": "Test Food Bank",
        "postcode": "E1 6AN",
        "latitude": Decimal("51.517000"),
        "longitude": Decimal("-0.073000"),
        "address": "123 Main St, London",
        "families_served_weekly": 100,
        "urgency_level": FoodBank.UrgencyLevel.ACTIVE,
    }
    defaults.update(overrides)
    return FoodBank.objects.create(**defaults)


@pytest.mark.django_db
class TestWishListItem:
    def test_create_with_all_fields(self):
        fb = _make_food_bank()
        item = WishListItem.objects.create(
            food_bank=fb,
            item_name="Tinned Tomatoes",
            category=WishListItem.Category.TINNED_GOODS,
            urgency=WishListItem.Urgency.NEEDED,
            quantity_needed=10,
            unit="tins",
            notes="400g tins, any brand",
        )
        retrieved = WishListItem.objects.get(pk=item.pk)
        assert retrieved.food_bank == fb
        assert retrieved.item_name == "Tinned Tomatoes"
        assert retrieved.category == "tinned_goods"
        assert retrieved.urgency == "needed"
        assert retrieved.quantity_needed == 10
        assert retrieved.unit == "tins"
        assert retrieved.notes == "400g tins, any brand"

    def test_uuid_primary_key(self):
        fb = _make_food_bank()
        item = WishListItem.objects.create(
            food_bank=fb, item_name="Rice",
            category=WishListItem.Category.DRIED_GOODS,
            urgency=WishListItem.Urgency.NEEDED,
            quantity_needed=5, unit="kg",
        )
        assert isinstance(item.pk, uuid.UUID)

    def test_category_enum_values(self):
        choices = [c[0] for c in WishListItem.Category.choices]
        assert "tinned_goods" in choices
        assert "dried_goods" in choices
        assert "fresh" in choices
        assert "dairy" in choices
        assert "baby" in choices
        assert "hygiene" in choices

    def test_urgency_enum_values(self):
        choices = [c[0] for c in WishListItem.Urgency.choices]
        assert "urgent" in choices
        assert "needed" in choices
        assert "optional" in choices

    def test_cascade_delete(self):
        fb = _make_food_bank()
        WishListItem.objects.create(
            food_bank=fb, item_name="Rice",
            category=WishListItem.Category.DRIED_GOODS,
            urgency=WishListItem.Urgency.NEEDED,
            quantity_needed=5, unit="kg",
        )
        fb.delete()
        assert WishListItem.objects.count() == 0

    def test_reverse_relation(self):
        fb = _make_food_bank()
        WishListItem.objects.create(
            food_bank=fb, item_name="Rice",
            category=WishListItem.Category.DRIED_GOODS,
            urgency=WishListItem.Urgency.NEEDED,
            quantity_needed=5, unit="kg",
        )
        WishListItem.objects.create(
            food_bank=fb, item_name="Pasta",
            category=WishListItem.Category.DRIED_GOODS,
            urgency=WishListItem.Urgency.OPTIONAL,
            quantity_needed=10, unit="packets",
        )
        assert fb.wish_list_items.count() == 2

    def test_notes_blank_allowed(self):
        fb = _make_food_bank()
        item = WishListItem.objects.create(
            food_bank=fb, item_name="Rice",
            category=WishListItem.Category.DRIED_GOODS,
            urgency=WishListItem.Urgency.NEEDED,
            quantity_needed=5, unit="kg",
            notes="",
        )
        item.refresh_from_db()
        assert item.notes == ""

    def test_str_returns_item_name(self):
        fb = _make_food_bank()
        item = WishListItem.objects.create(
            food_bank=fb, item_name="Tinned Tomatoes",
            category=WishListItem.Category.TINNED_GOODS,
            urgency=WishListItem.Urgency.URGENT,
            quantity_needed=20, unit="tins",
        )
        assert str(item) == "Tinned Tomatoes"


@pytest.mark.django_db
class TestGeneratedRecipe:
    def test_create_with_all_fields(self):
        fb = _make_food_bank()
        expires = timezone.now() + timedelta(hours=24)
        recipe = GeneratedRecipe.objects.create(
            food_bank=fb,
            recipe_name="Spaghetti Bolognese",
            description="A classic Italian pasta dish",
            serves=4,
            cook_time_minutes=30,
            ingredients=[
                {"name": "Pasta", "quantity": 500, "unit": "g"},
                {"name": "Tinned Tomatoes", "quantity": 2, "unit": "tins"},
            ],
            instructions="1. Cook pasta. 2. Make sauce. 3. Combine.",
            emoji="🍝",
            estimated_cost=Decimal("4.50"),
            expires_at=expires,
        )
        retrieved = GeneratedRecipe.objects.get(pk=recipe.pk)
        assert retrieved.food_bank == fb
        assert retrieved.recipe_name == "Spaghetti Bolognese"
        assert retrieved.description == "A classic Italian pasta dish"
        assert retrieved.serves == 4
        assert retrieved.cook_time_minutes == 30
        assert len(retrieved.ingredients) == 2
        assert retrieved.instructions == "1. Cook pasta. 2. Make sauce. 3. Combine."
        assert retrieved.emoji == "🍝"
        assert retrieved.estimated_cost == Decimal("4.50")
        assert retrieved.expires_at is not None

    def test_uuid_primary_key(self):
        fb = _make_food_bank()
        recipe = GeneratedRecipe.objects.create(
            food_bank=fb, recipe_name="Test", description="Test",
            serves=2, cook_time_minutes=15,
            ingredients=[], instructions="Test",
            emoji="🍳", estimated_cost=Decimal("3.00"),
            expires_at=timezone.now() + timedelta(hours=24),
        )
        assert isinstance(recipe.pk, uuid.UUID)

    def test_generated_at_auto_populated(self):
        fb = _make_food_bank()
        recipe = GeneratedRecipe.objects.create(
            food_bank=fb, recipe_name="Test", description="Test",
            serves=2, cook_time_minutes=15,
            ingredients=[], instructions="Test",
            emoji="🍳", estimated_cost=Decimal("3.00"),
            expires_at=timezone.now() + timedelta(hours=24),
        )
        assert recipe.generated_at is not None

    def test_cascade_delete_from_food_bank(self):
        fb = _make_food_bank()
        GeneratedRecipe.objects.create(
            food_bank=fb, recipe_name="Test", description="Test",
            serves=2, cook_time_minutes=15,
            ingredients=[], instructions="Test",
            emoji="🍳", estimated_cost=Decimal("3.00"),
            expires_at=timezone.now() + timedelta(hours=24),
        )
        fb.delete()
        assert GeneratedRecipe.objects.count() == 0

    def test_json_ingredients_field(self):
        fb = _make_food_bank()
        ingredients_data = [
            {"name": "Rice", "quantity": 1, "unit": "kg", "wish_list_item_id": str(uuid.uuid4())},
        ]
        recipe = GeneratedRecipe.objects.create(
            food_bank=fb, recipe_name="Rice Bowl", description="Simple",
            serves=2, cook_time_minutes=20,
            ingredients=ingredients_data, instructions="Cook rice.",
            emoji="🍚", estimated_cost=Decimal("1.50"),
            expires_at=timezone.now() + timedelta(hours=24),
        )
        recipe.refresh_from_db()
        assert recipe.ingredients == ingredients_data

    def test_str_returns_recipe_name(self):
        fb = _make_food_bank()
        recipe = GeneratedRecipe.objects.create(
            food_bank=fb, recipe_name="Spaghetti Bolognese", description="Classic",
            serves=4, cook_time_minutes=30,
            ingredients=[], instructions="Cook.",
            emoji="🍝", estimated_cost=Decimal("4.50"),
            expires_at=timezone.now() + timedelta(hours=24),
        )
        assert str(recipe) == "Spaghetti Bolognese"


@pytest.mark.django_db
class TestFoodBankSettings:
    def test_create_with_defaults(self):
        fb = _make_food_bank()
        settings = FoodBankSettings.objects.create(food_bank=fb)
        settings.refresh_from_db()
        assert settings.food_bank == fb
        assert settings.pepesto_enabled is False
        assert settings.accept_direct_delivery is True
        assert settings.allow_donor_collection is False
        assert settings.delivery_notes == ""

    def test_uuid_primary_key(self):
        fb = _make_food_bank()
        settings = FoodBankSettings.objects.create(food_bank=fb)
        assert isinstance(settings.pk, uuid.UUID)

    def test_one_to_one_enforcement(self):
        fb = _make_food_bank()
        FoodBankSettings.objects.create(food_bank=fb)
        with pytest.raises(IntegrityError):
            FoodBankSettings.objects.create(food_bank=fb)

    def test_cascade_delete_from_food_bank(self):
        fb = _make_food_bank()
        FoodBankSettings.objects.create(food_bank=fb)
        fb.delete()
        assert FoodBankSettings.objects.count() == 0

    def test_delivery_notes_blank(self):
        fb = _make_food_bank()
        settings = FoodBankSettings.objects.create(
            food_bank=fb, delivery_notes="Leave at back door",
        )
        settings.refresh_from_db()
        assert settings.delivery_notes == "Leave at back door"

    def test_timestamps(self):
        fb = _make_food_bank()
        settings = FoodBankSettings.objects.create(food_bank=fb)
        assert settings.created_at is not None
        assert settings.updated_at is not None

    def test_str_representation(self):
        fb = _make_food_bank()
        settings = FoodBankSettings.objects.create(food_bank=fb)
        assert str(fb.name) in str(settings)


@pytest.mark.django_db
class TestFoodBankSupermarketPreference:
    def test_create_with_all_fields(self):
        fb = _make_food_bank()
        pref = FoodBankSupermarketPreference.objects.create(
            food_bank=fb,
            supermarket=FoodBankSupermarketPreference.Supermarket.TESCO,
            enabled=True,
            delivery_time_days=2,
        )
        retrieved = FoodBankSupermarketPreference.objects.get(pk=pref.pk)
        assert retrieved.food_bank == fb
        assert retrieved.supermarket == "tesco"
        assert retrieved.enabled is True
        assert retrieved.delivery_time_days == 2

    def test_uuid_primary_key(self):
        fb = _make_food_bank()
        pref = FoodBankSupermarketPreference.objects.create(
            food_bank=fb,
            supermarket=FoodBankSupermarketPreference.Supermarket.SAINSBURYS,
        )
        assert isinstance(pref.pk, uuid.UUID)

    def test_supermarket_enum_values(self):
        choices = [c[0] for c in FoodBankSupermarketPreference.Supermarket.choices]
        assert "tesco" in choices
        assert "sainsburys" in choices
        assert "asda" in choices
        assert "waitrose" in choices

    def test_unique_constraint_food_bank_supermarket(self):
        fb = _make_food_bank()
        FoodBankSupermarketPreference.objects.create(
            food_bank=fb,
            supermarket=FoodBankSupermarketPreference.Supermarket.TESCO,
        )
        with pytest.raises(IntegrityError):
            FoodBankSupermarketPreference.objects.create(
                food_bank=fb,
                supermarket=FoodBankSupermarketPreference.Supermarket.TESCO,
            )

    def test_cascade_delete_from_food_bank(self):
        fb = _make_food_bank()
        FoodBankSupermarketPreference.objects.create(
            food_bank=fb,
            supermarket=FoodBankSupermarketPreference.Supermarket.TESCO,
        )
        fb.delete()
        assert FoodBankSupermarketPreference.objects.count() == 0

    def test_defaults(self):
        fb = _make_food_bank()
        pref = FoodBankSupermarketPreference.objects.create(
            food_bank=fb,
            supermarket=FoodBankSupermarketPreference.Supermarket.ASDA,
        )
        assert pref.enabled is True
        assert pref.delivery_time_days == 1

    def test_str_representation(self):
        fb = _make_food_bank()
        pref = FoodBankSupermarketPreference.objects.create(
            food_bank=fb,
            supermarket=FoodBankSupermarketPreference.Supermarket.TESCO,
        )
        assert "tesco" in str(pref).lower() or "Tesco" in str(pref)


@pytest.mark.django_db
class TestQRScan:
    def test_create_with_all_fields(self):
        fb = _make_food_bank()
        donation = Donation.objects.create(
            food_bank=fb,
            donation_type=Donation.DonationType.INDIVIDUAL_ITEMS,
            items=[{"name": "Rice", "quantity": 1}],
            total_cost=Decimal("1.50"),
            postcode="SW1A",
            completed=True,
        )
        scan = QRScan.objects.create(
            food_bank=fb,
            source=QRScan.Source.QR_POSTER,
            converted_to_donation=True,
            donation=donation,
        )
        retrieved = QRScan.objects.get(pk=scan.pk)
        assert retrieved.food_bank == fb
        assert retrieved.source == "qr_poster"
        assert retrieved.converted_to_donation is True
        assert retrieved.donation == donation

    def test_uuid_primary_key(self):
        fb = _make_food_bank()
        scan = QRScan.objects.create(
            food_bank=fb, source=QRScan.Source.QR_STICKER,
        )
        assert isinstance(scan.pk, uuid.UUID)

    def test_source_enum_values(self):
        choices = [c[0] for c in QRScan.Source.choices]
        assert "qr_poster" in choices
        assert "qr_sticker" in choices
        assert "qr_social" in choices

    def test_scanned_at_auto_populated(self):
        fb = _make_food_bank()
        scan = QRScan.objects.create(
            food_bank=fb, source=QRScan.Source.QR_POSTER,
        )
        assert scan.scanned_at is not None

    def test_donation_set_null_on_delete(self):
        fb = _make_food_bank()
        donation = Donation.objects.create(
            food_bank=fb,
            donation_type=Donation.DonationType.INDIVIDUAL_ITEMS,
            items=[], total_cost=Decimal("0.00"), postcode="SW1A",
        )
        scan = QRScan.objects.create(
            food_bank=fb, source=QRScan.Source.QR_POSTER,
            converted_to_donation=True, donation=donation,
        )
        donation.delete()
        scan.refresh_from_db()
        assert scan.donation is None

    def test_cascade_delete_from_food_bank(self):
        fb = _make_food_bank()
        QRScan.objects.create(
            food_bank=fb, source=QRScan.Source.QR_POSTER,
        )
        fb.delete()
        assert QRScan.objects.count() == 0

    def test_converted_to_donation_defaults_false(self):
        fb = _make_food_bank()
        scan = QRScan.objects.create(
            food_bank=fb, source=QRScan.Source.QR_SOCIAL,
        )
        assert scan.converted_to_donation is False
