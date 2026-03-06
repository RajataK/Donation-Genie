import uuid

import pytest
from decimal import Decimal

from apps.foodbanks.models import FoodBank
from apps.accounts.models import FoodBankAdmin


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
class TestFoodBankAdmin:
    def test_create_with_email_and_password(self):
        fb = _make_food_bank()
        admin = FoodBankAdmin.objects.create_user(
            email="admin@foodbank.org",
            password="securepass123",
            food_bank=fb,
        )
        retrieved = FoodBankAdmin.objects.get(pk=admin.pk)
        assert retrieved.email == "admin@foodbank.org"
        assert retrieved.food_bank == fb
        assert retrieved.check_password("securepass123")

    def test_uuid_primary_key(self):
        fb = _make_food_bank()
        admin = FoodBankAdmin.objects.create_user(
            email="admin@foodbank.org", password="pass123", food_bank=fb,
        )
        assert isinstance(admin.pk, uuid.UUID)

    def test_email_unique(self):
        fb = _make_food_bank()
        FoodBankAdmin.objects.create_user(
            email="admin@foodbank.org", password="pass123", food_bank=fb,
        )
        from django.db import IntegrityError
        with pytest.raises(IntegrityError):
            FoodBankAdmin.objects.create_user(
                email="admin@foodbank.org", password="pass456", food_bank=fb,
            )

    def test_password_is_hashed(self):
        fb = _make_food_bank()
        admin = FoodBankAdmin.objects.create_user(
            email="admin@foodbank.org", password="securepass123", food_bank=fb,
        )
        assert admin.password != "securepass123"
        assert admin.check_password("securepass123")

    def test_cascade_delete_from_food_bank(self):
        fb = _make_food_bank()
        FoodBankAdmin.objects.create_user(
            email="admin@foodbank.org", password="pass123", food_bank=fb,
        )
        fb.delete()
        assert FoodBankAdmin.objects.count() == 0

    def test_created_at_auto_populated(self):
        fb = _make_food_bank()
        admin = FoodBankAdmin.objects.create_user(
            email="admin@foodbank.org", password="pass123", food_bank=fb,
        )
        assert admin.created_at is not None

    def test_str_returns_email(self):
        fb = _make_food_bank()
        admin = FoodBankAdmin.objects.create_user(
            email="admin@foodbank.org", password="pass123", food_bank=fb,
        )
        assert str(admin) == "admin@foodbank.org"

    def test_email_required(self):
        fb = _make_food_bank()
        with pytest.raises(ValueError, match="Email is required"):
            FoodBankAdmin.objects.create_user(
                email="", password="pass123", food_bank=fb,
            )
