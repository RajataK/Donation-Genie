import uuid
from datetime import timedelta

import pytest
from decimal import Decimal
from django.utils import timezone

from apps.foodbanks.models import FoodBank, GeneratedRecipe
from apps.donations.models import Donation, DeliveryTracking


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


def _make_recipe(food_bank):
    return GeneratedRecipe.objects.create(
        food_bank=food_bank,
        recipe_name="Test Recipe",
        description="A test recipe",
        serves=4,
        cook_time_minutes=30,
        ingredients=[{"name": "Rice", "quantity": 1, "unit": "kg"}],
        instructions="Cook rice.",
        emoji="🍚",
        estimated_cost=Decimal("3.00"),
        expires_at=timezone.now() + timedelta(hours=24),
    )


@pytest.mark.django_db
class TestDonation:
    def test_create_with_all_fields(self):
        fb = _make_food_bank()
        recipe = _make_recipe(fb)
        donation = Donation.objects.create(
            food_bank=fb,
            donation_type=Donation.DonationType.RECIPE_KIT,
            recipe=recipe,
            items=[
                {"name": "Rice", "quantity": 1, "unit": "kg"},
                {"name": "Tinned Tomatoes", "quantity": 2, "unit": "tins"},
            ],
            total_cost=Decimal("5.50"),
            postcode="E1 6",
            completed=True,
        )
        retrieved = Donation.objects.get(pk=donation.pk)
        assert retrieved.food_bank == fb
        assert retrieved.donation_type == "recipe_kit"
        assert retrieved.recipe == recipe
        assert len(retrieved.items) == 2
        assert retrieved.total_cost == Decimal("5.50")
        assert retrieved.postcode == "E1 6"
        assert retrieved.completed is True

    def test_uuid_primary_key(self):
        fb = _make_food_bank()
        donation = Donation.objects.create(
            food_bank=fb,
            donation_type=Donation.DonationType.INDIVIDUAL_ITEMS,
            items=[{"name": "Rice", "quantity": 1}],
            total_cost=Decimal("1.50"),
            postcode="SW1A",
        )
        assert isinstance(donation.pk, uuid.UUID)

    def test_donation_type_enum(self):
        choices = [c[0] for c in Donation.DonationType.choices]
        assert "recipe_kit" in choices
        assert "individual_items" in choices

    def test_completed_defaults_false(self):
        fb = _make_food_bank()
        donation = Donation.objects.create(
            food_bank=fb,
            donation_type=Donation.DonationType.INDIVIDUAL_ITEMS,
            items=[{"name": "Rice", "quantity": 1}],
            total_cost=Decimal("1.50"),
            postcode="SW1A",
        )
        assert donation.completed is False

    def test_recipe_set_null_on_delete(self):
        fb = _make_food_bank()
        recipe = _make_recipe(fb)
        donation = Donation.objects.create(
            food_bank=fb,
            donation_type=Donation.DonationType.RECIPE_KIT,
            recipe=recipe,
            items=[{"name": "Rice", "quantity": 1}],
            total_cost=Decimal("3.00"),
            postcode="E1 6",
        )
        recipe.delete()
        donation.refresh_from_db()
        assert donation.recipe is None

    def test_cascade_delete_from_food_bank(self):
        fb = _make_food_bank()
        Donation.objects.create(
            food_bank=fb,
            donation_type=Donation.DonationType.INDIVIDUAL_ITEMS,
            items=[{"name": "Rice", "quantity": 1}],
            total_cost=Decimal("1.50"),
            postcode="SW1A",
        )
        fb.delete()
        assert Donation.objects.count() == 0

    def test_created_at_auto_populated(self):
        fb = _make_food_bank()
        donation = Donation.objects.create(
            food_bank=fb,
            donation_type=Donation.DonationType.INDIVIDUAL_ITEMS,
            items=[], total_cost=Decimal("0.00"), postcode="SW1A",
        )
        assert donation.created_at is not None

    def test_str_representation(self):
        fb = _make_food_bank()
        donation = Donation.objects.create(
            food_bank=fb,
            donation_type=Donation.DonationType.INDIVIDUAL_ITEMS,
            items=[], total_cost=Decimal("0.00"), postcode="SW1A",
        )
        assert str(donation.pk) in str(donation)


@pytest.mark.django_db
class TestDeliveryTracking:
    def _make_donation(self):
        fb = _make_food_bank()
        return Donation.objects.create(
            food_bank=fb,
            donation_type=Donation.DonationType.INDIVIDUAL_ITEMS,
            items=[{"name": "Rice", "quantity": 1}],
            total_cost=Decimal("1.50"),
            postcode="SW1A",
        )

    def test_create_with_all_fields(self):
        donation = self._make_donation()
        est = timezone.now() + timedelta(days=2)
        tracking = DeliveryTracking.objects.create(
            donation=donation,
            supermarket="Tesco",
            status=DeliveryTracking.Status.PENDING,
            tracking_number="TRK-123",
            estimated_delivery=est,
            notes="Leave at reception",
        )
        retrieved = DeliveryTracking.objects.get(pk=tracking.pk)
        assert retrieved.donation == donation
        assert retrieved.supermarket == "Tesco"
        assert retrieved.status == "pending"
        assert retrieved.tracking_number == "TRK-123"
        assert retrieved.estimated_delivery is not None
        assert retrieved.received_confirmed is False

    def test_uuid_primary_key(self):
        donation = self._make_donation()
        tracking = DeliveryTracking.objects.create(
            donation=donation, supermarket="Tesco",
            status=DeliveryTracking.Status.PENDING,
        )
        assert isinstance(tracking.pk, uuid.UUID)

    def test_status_enum_values(self):
        choices = [c[0] for c in DeliveryTracking.Status.choices]
        assert "pending" in choices
        assert "dispatched" in choices
        assert "delivered" in choices
        assert "received" in choices

    def test_cascade_delete_from_donation(self):
        donation = self._make_donation()
        DeliveryTracking.objects.create(
            donation=donation, supermarket="Tesco",
            status=DeliveryTracking.Status.PENDING,
        )
        donation.delete()
        assert DeliveryTracking.objects.count() == 0

    def test_optional_fields_nullable(self):
        donation = self._make_donation()
        tracking = DeliveryTracking.objects.create(
            donation=donation, supermarket="Tesco",
            status=DeliveryTracking.Status.PENDING,
        )
        tracking.refresh_from_db()
        assert tracking.tracking_number == ""
        assert tracking.estimated_delivery is None
        assert tracking.actual_delivery is None
        assert tracking.notes == ""

    def test_timestamps(self):
        donation = self._make_donation()
        tracking = DeliveryTracking.objects.create(
            donation=donation, supermarket="Tesco",
            status=DeliveryTracking.Status.PENDING,
        )
        assert tracking.created_at is not None
        assert tracking.updated_at is not None

    def test_str_representation(self):
        donation = self._make_donation()
        tracking = DeliveryTracking.objects.create(
            donation=donation, supermarket="Tesco",
            status=DeliveryTracking.Status.PENDING,
        )
        assert str(tracking.pk) in str(tracking)
