"""
Tests for new meal-kit API endpoints:
  - GET  /api/food-banks/<id>/wish-list/
  - POST /api/food-banks/<id>/generate-meal-kits/
  - GET  /api/food-banks/<id>/meal-kits/
"""

import json
from datetime import timedelta
from decimal import Decimal

import pytest
from django.test import Client
from django.utils import timezone

from apps.foodbanks.models import FoodBank, GeneratedRecipe, WishListItem


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


def _add_item(food_bank, item_name, category=WishListItem.Category.DRIED_GOODS):
    return WishListItem.objects.create(
        food_bank=food_bank,
        item_name=item_name,
        category=category,
        urgency=WishListItem.Urgency.NEEDED,
        quantity_needed=5,
        unit="items",
    )


# ---------------------------------------------------------------------------
# Wish-list endpoint tests
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestWishListView:
    def test_returns_200(self, api_client: Client):
        fb = _make_food_bank()
        response = api_client.get(f"/api/food-banks/{fb.id}/wish-list/")
        assert response.status_code == 200

    def test_returns_empty_list_when_no_items(self, api_client: Client):
        fb = _make_food_bank()
        response = api_client.get(f"/api/food-banks/{fb.id}/wish-list/")
        assert response.json() == []

    def test_returns_wish_list_items(self, api_client: Client):
        fb = _make_food_bank()
        _add_item(fb, "Dried Pasta")
        _add_item(fb, "Tinned Tomatoes", category=WishListItem.Category.TINNED_GOODS)
        response = api_client.get(f"/api/food-banks/{fb.id}/wish-list/")
        data = response.json()
        assert len(data) == 2

    def test_item_contains_required_fields(self, api_client: Client):
        fb = _make_food_bank()
        _add_item(fb, "Dried Pasta")
        response = api_client.get(f"/api/food-banks/{fb.id}/wish-list/")
        item = response.json()[0]
        required_fields = {
            "id", "item_name", "category", "urgency",
            "quantity_needed", "unit", "notes", "created_at",
        }
        assert required_fields.issubset(item.keys())
        assert item["item_name"] == "Dried Pasta"

    def test_returns_only_items_for_specified_food_bank(self, api_client: Client):
        fb1 = _make_food_bank(name="Bank 1")
        fb2 = _make_food_bank(name="Bank 2")
        _add_item(fb1, "Pasta")
        _add_item(fb2, "Rice")
        response = api_client.get(f"/api/food-banks/{fb1.id}/wish-list/")
        data = response.json()
        assert len(data) == 1
        assert data[0]["item_name"] == "Pasta"

    def test_no_authentication_required(self, api_client: Client):
        fb = _make_food_bank()
        response = api_client.get(f"/api/food-banks/{fb.id}/wish-list/")
        assert response.status_code not in (401, 403)


# ---------------------------------------------------------------------------
# Generate meal-kits endpoint tests
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestGenerateMealKitsView:
    def test_returns_200_with_matching_items(self, api_client: Client):
        fb = _make_food_bank()
        _add_item(fb, "Dried Pasta")
        response = api_client.post(
            f"/api/food-banks/{fb.id}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == 200

    def test_returns_404_for_unknown_food_bank(self, api_client: Client):
        import uuid
        response = api_client.post(
            f"/api/food-banks/{uuid.uuid4()}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_returns_recipes_as_list(self, api_client: Client):
        fb = _make_food_bank()
        _add_item(fb, "Dried Pasta")
        response = api_client.post(
            f"/api/food-banks/{fb.id}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert isinstance(response.json(), list)

    def test_recipe_response_contains_required_fields(self, api_client: Client):
        fb = _make_food_bank()
        _add_item(fb, "Dried Pasta")
        response = api_client.post(
            f"/api/food-banks/{fb.id}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        data = response.json()
        assert len(data) > 0
        recipe = data[0]
        required_fields = {
            "id", "food_bank", "recipe_name", "description", "serves",
            "cook_time_minutes", "ingredients", "instructions", "emoji",
            "estimated_cost", "dietary_tags", "generated_at", "expires_at",
        }
        assert required_fields.issubset(recipe.keys())

    def test_dietary_restrictions_filter_applied(self, api_client: Client):
        fb = _make_food_bank()
        _add_item(fb, "Dried Pasta")
        _add_item(fb, "Tinned Tuna")
        response = api_client.post(
            f"/api/food-banks/{fb.id}/generate-meal-kits/",
            data=json.dumps({"dietary_restrictions": ["vegan"]}),
            content_type="application/json",
        )
        data = response.json()
        for recipe in data:
            assert "vegan" in recipe["dietary_tags"]

    def test_empty_wish_list_returns_empty_list(self, api_client: Client):
        fb = _make_food_bank()
        response = api_client.post(
            f"/api/food-banks/{fb.id}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.json() == []

    def test_no_authentication_required(self, api_client: Client):
        fb = _make_food_bank()
        response = api_client.post(
            f"/api/food-banks/{fb.id}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code not in (401, 403)

    def test_recipes_saved_to_database(self, api_client: Client):
        fb = _make_food_bank()
        _add_item(fb, "Dried Pasta")
        api_client.post(
            f"/api/food-banks/{fb.id}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert GeneratedRecipe.objects.filter(food_bank=fb).count() > 0

    def test_dietary_tags_in_response(self, api_client: Client):
        fb = _make_food_bank()
        _add_item(fb, "Red Lentils")
        _add_item(fb, "Rice")
        response = api_client.post(
            f"/api/food-banks/{fb.id}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        data = response.json()
        assert any(len(r["dietary_tags"]) > 0 for r in data)


# ---------------------------------------------------------------------------
# Meal-kits list endpoint tests
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestMealKitListView:
    def _create_recipe(self, food_bank, **overrides):
        defaults = {
            "food_bank": food_bank,
            "recipe_name": "Test Recipe",
            "description": "Test description",
            "serves": 4,
            "cook_time_minutes": 20,
            "ingredients": [{"name": "Pasta", "quantity": 500, "unit": "g"}],
            "instructions": "Cook it.",
            "emoji": "🍝",
            "estimated_cost": Decimal("2.50"),
            "dietary_tags": ["vegetarian"],
            "expires_at": timezone.now() + timedelta(hours=24),
        }
        defaults.update(overrides)
        return GeneratedRecipe.objects.create(**defaults)

    def test_returns_200(self, api_client: Client):
        fb = _make_food_bank()
        response = api_client.get(f"/api/food-banks/{fb.id}/meal-kits/")
        assert response.status_code == 200

    def test_returns_404_for_unknown_food_bank(self, api_client: Client):
        import uuid
        response = api_client.get(f"/api/food-banks/{uuid.uuid4()}/meal-kits/")
        assert response.status_code == 404

    def test_returns_existing_non_expired_recipes(self, api_client: Client):
        fb = _make_food_bank()
        self._create_recipe(fb)
        response = api_client.get(f"/api/food-banks/{fb.id}/meal-kits/")
        assert len(response.json()) == 1

    def test_excludes_expired_recipes(self, api_client: Client):
        fb = _make_food_bank()
        self._create_recipe(
            fb, expires_at=timezone.now() - timedelta(hours=1)
        )
        response = api_client.get(f"/api/food-banks/{fb.id}/meal-kits/")
        assert response.json() == []

    def test_returns_only_recipes_for_specified_food_bank(self, api_client: Client):
        fb1 = _make_food_bank(name="Bank 1")
        fb2 = _make_food_bank(name="Bank 2")
        self._create_recipe(fb1, recipe_name="Recipe A")
        self._create_recipe(fb2, recipe_name="Recipe B")
        response = api_client.get(f"/api/food-banks/{fb1.id}/meal-kits/")
        data = response.json()
        assert len(data) == 1
        assert data[0]["recipe_name"] == "Recipe A"

    def test_recipe_response_includes_dietary_tags(self, api_client: Client):
        fb = _make_food_bank()
        self._create_recipe(fb, dietary_tags=["vegan", "gluten_free"])
        response = api_client.get(f"/api/food-banks/{fb.id}/meal-kits/")
        data = response.json()
        assert data[0]["dietary_tags"] == ["vegan", "gluten_free"]

    def test_no_authentication_required(self, api_client: Client):
        fb = _make_food_bank()
        response = api_client.get(f"/api/food-banks/{fb.id}/meal-kits/")
        assert response.status_code not in (401, 403)
