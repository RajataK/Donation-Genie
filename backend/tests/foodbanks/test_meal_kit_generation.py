"""
Tests for meal-kit generation functionality including dietary restriction filtering.
"""
import json
from datetime import timedelta
from decimal import Decimal

import pytest
from django.test import Client
from django.utils import timezone

from apps.foodbanks.models import FoodBank, GeneratedRecipe, WishListItem
from apps.foodbanks.services import MealKitGenerator, RECIPE_TEMPLATES


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_food_bank(**overrides) -> FoodBank:
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


def _add_wish_list_items(food_bank: FoodBank, item_names: list[str]) -> list[WishListItem]:
    items = []
    for name in item_names:
        items.append(
            WishListItem.objects.create(
                food_bank=food_bank,
                item_name=name,
                category=WishListItem.Category.TINNED_GOODS,
                urgency=WishListItem.Urgency.NEEDED,
                quantity_needed=5,
                unit="tins",
            )
        )
    return items


# ---------------------------------------------------------------------------
# Service-level tests
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestMealKitGenerator:
    def test_returns_list_of_generated_recipe_instances(self):
        fb = _make_food_bank()
        _add_wish_list_items(fb, ["Tinned Tomatoes", "Pasta"])
        recipes = MealKitGenerator().generate(fb)
        assert isinstance(recipes, list)
        assert all(isinstance(r, GeneratedRecipe) for r in recipes)

    def test_recipes_are_persisted(self):
        fb = _make_food_bank()
        _add_wish_list_items(fb, ["Tinned Tomatoes", "Pasta"])
        MealKitGenerator().generate(fb)
        assert GeneratedRecipe.objects.filter(food_bank=fb).count() > 0

    def test_recipes_linked_to_correct_food_bank(self):
        fb = _make_food_bank()
        _add_wish_list_items(fb, ["Tinned Tomatoes", "Pasta"])
        recipes = MealKitGenerator().generate(fb)
        for recipe in recipes:
            assert recipe.food_bank == fb

    def test_recipes_have_expiry_in_future(self):
        fb = _make_food_bank()
        _add_wish_list_items(fb, ["Tinned Tomatoes", "Pasta"])
        before = timezone.now()
        recipes = MealKitGenerator().generate(fb)
        for recipe in recipes:
            assert recipe.expires_at > before

    def test_recipes_expire_approximately_24_hours_from_now(self):
        fb = _make_food_bank()
        _add_wish_list_items(fb, ["Tinned Tomatoes", "Pasta"])
        before = timezone.now()
        recipes = MealKitGenerator().generate(fb)
        expected_expiry = before + timedelta(hours=24)
        for recipe in recipes:
            diff = abs((recipe.expires_at - expected_expiry).total_seconds())
            assert diff < 60, "Expiry should be approximately 24 hours from now"

    def test_recipes_constrained_by_wish_list_items(self):
        """Recipes whose ingredient slots cannot be filled by the wish list are skipped."""
        fb = _make_food_bank()
        # Only add items that match "Tomato & Pasta" (pasta + tomatoes)
        _add_wish_list_items(fb, ["Tinned Tomatoes", "Pasta"])
        recipes = MealKitGenerator().generate(fb)
        # Every returned recipe must have at least min_slots_required matches
        for recipe in recipes:
            template = next(
                (t for t in RECIPE_TEMPLATES if t["name"] == recipe.recipe_name),
                None,
            )
            assert template is not None, f"Unknown recipe: {recipe.recipe_name}"
            item_names = ["tinned tomatoes", "pasta"]
            filled = sum(
                1
                for slot in template["ingredient_slots"]
                if any(kw.lower() in n for kw in slot["keywords"] for n in item_names)
            )
            assert filled >= template["min_slots_required"]

    def test_no_recipes_generated_when_no_wish_list_matches(self):
        """If wish-list items match no recipe template, nothing is generated."""
        fb = _make_food_bank()
        # Items that don't match any ingredient keywords
        _add_wish_list_items(fb, ["Nappies", "Shampoo"])
        recipes = MealKitGenerator().generate(fb)
        assert recipes == []

    def test_all_templates_eligible_when_no_wish_list(self):
        """With no wish list at all, all templates are eligible (no item constraint)."""
        fb = _make_food_bank()
        recipes = MealKitGenerator().generate(fb)
        assert len(recipes) == len(RECIPE_TEMPLATES)

    def test_dietary_restriction_filter_vegan(self):
        fb = _make_food_bank()
        recipes = MealKitGenerator().generate(fb, dietary_restrictions=["vegan"])
        for recipe in recipes:
            assert "vegan" in recipe.dietary_restrictions

    def test_dietary_restriction_filter_gluten_free(self):
        fb = _make_food_bank()
        recipes = MealKitGenerator().generate(fb, dietary_restrictions=["gluten_free"])
        for recipe in recipes:
            assert "gluten_free" in recipe.dietary_restrictions

    def test_dietary_restriction_filter_multiple(self):
        """All returned recipes must satisfy every requested restriction."""
        fb = _make_food_bank()
        restrictions = ["vegan", "gluten_free"]
        recipes = MealKitGenerator().generate(fb, dietary_restrictions=restrictions)
        for recipe in recipes:
            for r in restrictions:
                assert r in recipe.dietary_restrictions

    def test_dietary_restriction_halal(self):
        fb = _make_food_bank()
        recipes = MealKitGenerator().generate(fb, dietary_restrictions=["halal"])
        for recipe in recipes:
            assert "halal" in recipe.dietary_restrictions

    def test_dietary_restriction_dairy_free(self):
        fb = _make_food_bank()
        recipes = MealKitGenerator().generate(fb, dietary_restrictions=["dairy_free"])
        for recipe in recipes:
            assert "dairy_free" in recipe.dietary_restrictions

    def test_dietary_restriction_nut_free(self):
        fb = _make_food_bank()
        recipes = MealKitGenerator().generate(fb, dietary_restrictions=["nut_free"])
        for recipe in recipes:
            assert "nut_free" in recipe.dietary_restrictions

    def test_dietary_restriction_filters_out_non_matching(self):
        """Recipes that do NOT satisfy all restrictions must be excluded."""
        fb = _make_food_bank()
        # Tuna Pasta Bake is NOT vegan — it should be filtered out
        all_recipes = MealKitGenerator().generate(fb)
        tuna_pasta_names = {r.recipe_name for r in all_recipes if r.recipe_name == "Tuna Pasta Bake"}
        assert tuna_pasta_names, "Tuna Pasta Bake must be generated without any dietary filter"
        # Now generate with vegan restriction
        GeneratedRecipe.objects.all().delete()
        vegan_recipes = MealKitGenerator().generate(fb, dietary_restrictions=["vegan"])
        vegan_names = {r.recipe_name for r in vegan_recipes}
        assert "Tuna Pasta Bake" not in vegan_names

    def test_ingredients_include_availability_flag(self):
        fb = _make_food_bank()
        _add_wish_list_items(fb, ["Tinned Tomatoes", "Pasta"])
        recipes = MealKitGenerator().generate(fb)
        for recipe in recipes:
            for ingredient in recipe.ingredients:
                assert "available_from_wish_list" in ingredient
                assert isinstance(ingredient["available_from_wish_list"], bool)

    def test_ingredients_flag_true_for_matched_items(self):
        fb = _make_food_bank()
        _add_wish_list_items(fb, ["Tinned Tomatoes", "Pasta"])
        recipes = MealKitGenerator().generate(fb)
        tomato_pasta = next((r for r in recipes if r.recipe_name == "Tomato & Pasta"), None)
        assert tomato_pasta is not None
        pasta_ingredient = next(
            (i for i in tomato_pasta.ingredients if i["name"] == "Pasta"), None
        )
        assert pasta_ingredient is not None
        assert pasta_ingredient["available_from_wish_list"] is True

    def test_recipe_has_required_fields(self):
        fb = _make_food_bank()
        _add_wish_list_items(fb, ["Tinned Tomatoes", "Pasta"])
        recipes = MealKitGenerator().generate(fb)
        assert recipes
        recipe = recipes[0]
        assert recipe.recipe_name
        assert recipe.description
        assert recipe.serves > 0
        assert recipe.cook_time_minutes > 0
        assert isinstance(recipe.ingredients, list)
        assert recipe.instructions
        assert recipe.emoji
        assert recipe.estimated_cost > 0
        assert isinstance(recipe.dietary_restrictions, list)

    def test_empty_restrictions_list_returns_all_viable(self):
        """An empty dietary_restrictions list should not filter anything."""
        fb = _make_food_bank()
        recipes_no_arg = MealKitGenerator().generate(fb)
        count_no_arg = len(recipes_no_arg)
        GeneratedRecipe.objects.all().delete()
        recipes_empty = MealKitGenerator().generate(fb, dietary_restrictions=[])
        assert len(recipes_empty) == count_no_arg


# ---------------------------------------------------------------------------
# API endpoint tests
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestMealKitGenerateEndpoint:
    def test_returns_201_on_success(self, api_client: Client):
        fb = _make_food_bank()
        _add_wish_list_items(fb, ["Tinned Tomatoes", "Pasta"])
        response = api_client.post(
            f"/api/food-banks/{fb.pk}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == 201

    def test_returns_404_for_unknown_food_bank(self, api_client: Client):
        import uuid
        response = api_client.post(
            f"/api/food-banks/{uuid.uuid4()}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_returns_list_of_recipes(self, api_client: Client):
        fb = _make_food_bank()
        _add_wish_list_items(fb, ["Tinned Tomatoes", "Pasta"])
        response = api_client.post(
            f"/api/food-banks/{fb.pk}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_recipes_contain_required_fields(self, api_client: Client):
        fb = _make_food_bank()
        _add_wish_list_items(fb, ["Tinned Tomatoes", "Pasta"])
        response = api_client.post(
            f"/api/food-banks/{fb.pk}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        recipe = response.json()[0]
        required_fields = {
            "id", "food_bank", "recipe_name", "description", "serves",
            "cook_time_minutes", "ingredients", "instructions", "emoji",
            "estimated_cost", "dietary_restrictions", "generated_at", "expires_at",
        }
        assert required_fields.issubset(recipe.keys())

    def test_dietary_restriction_filter_via_api(self, api_client: Client):
        fb = _make_food_bank()
        response = api_client.post(
            f"/api/food-banks/{fb.pk}/generate-meal-kits/",
            data=json.dumps({"dietary_restrictions": ["vegan"]}),
            content_type="application/json",
        )
        assert response.status_code == 201
        for recipe in response.json():
            assert "vegan" in recipe["dietary_restrictions"]

    def test_invalid_dietary_restriction_returns_400(self, api_client: Client):
        fb = _make_food_bank()
        response = api_client.post(
            f"/api/food-banks/{fb.pk}/generate-meal-kits/",
            data=json.dumps({"dietary_restrictions": ["invalid_restriction"]}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_no_wish_list_generates_all_template_recipes(self, api_client: Client):
        fb = _make_food_bank()
        response = api_client.post(
            f"/api/food-banks/{fb.pk}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == 201
        assert len(response.json()) == len(RECIPE_TEMPLATES)

    def test_no_authentication_required(self, api_client: Client):
        fb = _make_food_bank()
        response = api_client.post(
            f"/api/food-banks/{fb.pk}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code not in (401, 403)


@pytest.mark.django_db
class TestMealKitListEndpoint:
    def test_returns_200(self, api_client: Client):
        fb = _make_food_bank()
        response = api_client.get(f"/api/food-banks/{fb.pk}/meal-kits/")
        assert response.status_code == 200

    def test_returns_404_for_unknown_food_bank(self, api_client: Client):
        import uuid
        response = api_client.get(f"/api/food-banks/{uuid.uuid4()}/meal-kits/")
        assert response.status_code == 404

    def test_returns_empty_list_when_no_recipes(self, api_client: Client):
        fb = _make_food_bank()
        response = api_client.get(f"/api/food-banks/{fb.pk}/meal-kits/")
        assert response.json() == []

    def test_lists_generated_recipes(self, api_client: Client):
        fb = _make_food_bank()
        _add_wish_list_items(fb, ["Tinned Tomatoes", "Pasta"])
        # Generate first
        api_client.post(
            f"/api/food-banks/{fb.pk}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        response = api_client.get(f"/api/food-banks/{fb.pk}/meal-kits/")
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_excludes_expired_recipes(self, api_client: Client):
        fb = _make_food_bank()
        # Create an expired recipe directly
        GeneratedRecipe.objects.create(
            food_bank=fb,
            recipe_name="Old Recipe",
            description="Old",
            serves=4,
            cook_time_minutes=20,
            ingredients=[],
            instructions="Old instructions.",
            emoji="🍽️",
            estimated_cost=Decimal("2.00"),
            dietary_restrictions=[],
            expires_at=timezone.now() - timedelta(hours=1),
        )
        response = api_client.get(f"/api/food-banks/{fb.pk}/meal-kits/")
        assert response.json() == []

    def test_filter_by_dietary_restriction_query_param(self, api_client: Client):
        fb = _make_food_bank()
        api_client.post(
            f"/api/food-banks/{fb.pk}/generate-meal-kits/",
            data=json.dumps({}),
            content_type="application/json",
        )
        response = api_client.get(
            f"/api/food-banks/{fb.pk}/meal-kits/?dietary_restrictions=vegan"
        )
        assert response.status_code == 200
        for recipe in response.json():
            assert "vegan" in recipe["dietary_restrictions"]

    def test_no_authentication_required(self, api_client: Client):
        fb = _make_food_bank()
        response = api_client.get(f"/api/food-banks/{fb.pk}/meal-kits/")
        assert response.status_code not in (401, 403)


@pytest.mark.django_db
class TestMealKitDetailEndpoint:
    def test_returns_200_for_existing_recipe(self, api_client: Client):
        fb = _make_food_bank()
        recipe = GeneratedRecipe.objects.create(
            food_bank=fb,
            recipe_name="Test Recipe",
            description="Test",
            serves=4,
            cook_time_minutes=20,
            ingredients=[{"name": "Pasta", "quantity": 400, "unit": "g", "available_from_wish_list": True}],
            instructions="Cook.",
            emoji="🍝",
            estimated_cost=Decimal("2.50"),
            dietary_restrictions=["vegan"],
            expires_at=timezone.now() + timedelta(hours=24),
        )
        response = api_client.get(f"/api/food-banks/{fb.pk}/meal-kits/{recipe.pk}/")
        assert response.status_code == 200

    def test_returns_correct_recipe_data(self, api_client: Client):
        fb = _make_food_bank()
        recipe = GeneratedRecipe.objects.create(
            food_bank=fb,
            recipe_name="Lentil Soup",
            description="Warming soup",
            serves=4,
            cook_time_minutes=30,
            ingredients=[],
            instructions="Cook lentils.",
            emoji="🍲",
            estimated_cost=Decimal("2.00"),
            dietary_restrictions=["vegan", "gluten_free"],
            expires_at=timezone.now() + timedelta(hours=24),
        )
        response = api_client.get(f"/api/food-banks/{fb.pk}/meal-kits/{recipe.pk}/")
        data = response.json()
        assert data["recipe_name"] == "Lentil Soup"
        assert "vegan" in data["dietary_restrictions"]
        assert "gluten_free" in data["dietary_restrictions"]

    def test_returns_404_for_unknown_food_bank(self, api_client: Client):
        import uuid
        recipe_id = uuid.uuid4()
        food_bank_id = uuid.uuid4()
        response = api_client.get(f"/api/food-banks/{food_bank_id}/meal-kits/{recipe_id}/")
        assert response.status_code == 404

    def test_returns_404_for_unknown_recipe(self, api_client: Client):
        import uuid
        fb = _make_food_bank()
        response = api_client.get(f"/api/food-banks/{fb.pk}/meal-kits/{uuid.uuid4()}/")
        assert response.status_code == 404

    def test_no_authentication_required(self, api_client: Client):
        fb = _make_food_bank()
        recipe = GeneratedRecipe.objects.create(
            food_bank=fb,
            recipe_name="Test",
            description="Test",
            serves=2,
            cook_time_minutes=10,
            ingredients=[],
            instructions="Test.",
            emoji="🍴",
            estimated_cost=Decimal("1.00"),
            dietary_restrictions=[],
            expires_at=timezone.now() + timedelta(hours=24),
        )
        response = api_client.get(f"/api/food-banks/{fb.pk}/meal-kits/{recipe.pk}/")
        assert response.status_code not in (401, 403)
