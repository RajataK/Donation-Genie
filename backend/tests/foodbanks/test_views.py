import pytest
from django.test import Client

from apps.foodbanks.models import FoodBank


@pytest.mark.django_db
def test_food_bank_list_returns_200(api_client: Client):
    response = api_client.get("/api/food-banks/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_food_bank_list_returns_empty_array_when_no_data(api_client: Client):
    response = api_client.get("/api/food-banks/")
    assert response.json() == []


@pytest.mark.django_db
def test_food_bank_list_returns_all_food_banks(api_client: Client):
    FoodBank.objects.create(
        name="Test Food Bank 1",
        postcode="E1 1AA",
        latitude="51.517000",
        longitude="-0.073000",
        address="1 Test Street, London E1 1AA",
        families_served_weekly=100,
        urgency_level="urgent",
    )
    FoodBank.objects.create(
        name="Test Food Bank 2",
        postcode="W1 2BB",
        latitude="51.514000",
        longitude="-0.142000",
        address="2 Test Road, London W1 2BB",
        families_served_weekly=50,
        urgency_level="normal",
    )

    response = api_client.get("/api/food-banks/")
    data = response.json()
    assert len(data) == 2


@pytest.mark.django_db
def test_food_bank_list_contains_all_required_fields(api_client: Client):
    FoodBank.objects.create(
        name="Hackney Food Bank",
        postcode="E8 1DY",
        latitude="51.543800",
        longitude="-0.055300",
        address="29 Dalston Lane, London E8 1DY",
        families_served_weekly=150,
        urgency_level="urgent",
    )

    response = api_client.get("/api/food-banks/")
    data = response.json()
    assert len(data) == 1

    food_bank = data[0]
    required_fields = {
        "id",
        "name",
        "postcode",
        "latitude",
        "longitude",
        "address",
        "families_served_weekly",
        "urgency_level",
        "last_updated",
    }
    assert required_fields.issubset(food_bank.keys())

    assert food_bank["name"] == "Hackney Food Bank"
    assert food_bank["postcode"] == "E8 1DY"
    assert food_bank["families_served_weekly"] == 150
    assert food_bank["urgency_level"] == "urgent"


@pytest.mark.django_db
def test_food_bank_list_requires_no_authentication(api_client: Client):
    response = api_client.get("/api/food-banks/")
    assert response.status_code != 401
    assert response.status_code != 403
