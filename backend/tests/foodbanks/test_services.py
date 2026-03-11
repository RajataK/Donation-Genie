"""
Tests for the meal kit generation service.
"""

import pytest
from decimal import Decimal

from apps.foodbanks.models import FoodBank, GeneratedRecipe, WishListItem
from apps.foodbanks.services import (
    ALL_DIETARY_TAGS,
    DIETARY_TAG_DAIRY_FREE,
    DIETARY_TAG_GLUTEN_FREE,
    DIETARY_TAG_NUT_FREE,
    DIETARY_TAG_VEGAN,
    DIETARY_TAG_VEGETARIAN,
    _item_matches_keyword,
    _match_templates,
    _normalise_restrictions,
    _wish_list_covers_keyword,
    generate_meal_kits,
)


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
# Unit tests for helper functions
# ---------------------------------------------------------------------------


class TestItemMatchesKeyword:
    def test_exact_match(self):
        assert _item_matches_keyword("Pasta", "pasta") is True

    def test_case_insensitive(self):
        assert _item_matches_keyword("TINNED TOMATOES", "tomato") is True

    def test_partial_match(self):
        assert _item_matches_keyword("Tinned Tuna in Spring Water", "tuna") is True

    def test_no_match(self):
        assert _item_matches_keyword("Rice", "pasta") is False


class TestNormaliseRestrictions:
    def test_empty_input(self):
        assert _normalise_restrictions(None) == []
        assert _normalise_restrictions([]) == []

    def test_valid_tags_returned(self):
        result = _normalise_restrictions(["vegetarian", "vegan"])
        assert set(result) == {"vegetarian", "vegan"}

    def test_unknown_tags_filtered(self):
        result = _normalise_restrictions(["vegetarian", "halal", "unknown"])
        assert result == ["vegetarian"]

    def test_duplicates_removed(self):
        result = _normalise_restrictions(["vegetarian", "vegetarian"])
        assert len(result) == 1


@pytest.mark.django_db
class TestWishListCoversKeyword:
    def test_keyword_found(self):
        fb = _make_food_bank()
        items = [
            WishListItem(food_bank=fb, item_name="Dried Pasta"),
            WishListItem(food_bank=fb, item_name="Rice"),
        ]
        assert _wish_list_covers_keyword(items, "pasta") is True

    def test_keyword_not_found(self):
        fb = _make_food_bank()
        items = [WishListItem(food_bank=fb, item_name="Rice")]
        assert _wish_list_covers_keyword(items, "pasta") is False

    def test_empty_wish_list(self):
        assert _wish_list_covers_keyword([], "pasta") is False


class TestMatchTemplates:
    def _make_items(self, names):
        return [WishListItem(item_name=n) for n in names]

    def test_returns_matching_template(self):
        items = self._make_items(["Dried Pasta", "Tinned Tomatoes"])
        result = _match_templates(items, [])
        names = [t["recipe_name"] for t in result]
        assert "Pasta with Tomato Sauce" in names

    def test_excludes_template_missing_required_keyword(self):
        items = self._make_items(["Rice", "Tinned Tomatoes"])
        result = _match_templates(items, [])
        names = [t["recipe_name"] for t in result]
        assert "Pasta with Tomato Sauce" not in names

    def test_dietary_filter_applied(self):
        items = self._make_items(["Pasta", "Tinned Tuna"])
        # Tuna pasta bake is not vegan
        result = _match_templates(items, [DIETARY_TAG_VEGAN])
        names = [t["recipe_name"] for t in result]
        assert "Tinned Tuna Pasta Bake" not in names

    def test_dietary_filter_keeps_compliant_recipe(self):
        items = self._make_items(["Red Lentils", "Rice", "Tinned Tomatoes"])
        result = _match_templates(items, [DIETARY_TAG_VEGAN, DIETARY_TAG_GLUTEN_FREE])
        names = [t["recipe_name"] for t in result]
        assert "Rice and Lentil Dahl" in names

    def test_no_items_returns_empty(self):
        result = _match_templates([], [])
        assert result == []


# ---------------------------------------------------------------------------
# Integration tests for generate_meal_kits service
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestGenerateMealKits:
    def test_returns_list_of_generated_recipe_instances(self):
        fb = _make_food_bank()
        _add_item(fb, "Dried Pasta")
        recipes = generate_meal_kits(fb)
        assert isinstance(recipes, list)
        assert all(isinstance(r, GeneratedRecipe) for r in recipes)

    def test_recipes_persisted_in_database(self):
        fb = _make_food_bank()
        _add_item(fb, "Dried Pasta")
        recipes = generate_meal_kits(fb)
        assert len(recipes) > 0
        assert GeneratedRecipe.objects.filter(food_bank=fb).count() == len(recipes)

    def test_empty_wish_list_returns_empty(self):
        fb = _make_food_bank()
        recipes = generate_meal_kits(fb)
        assert recipes == []

    def test_hygiene_items_excluded_from_matching(self):
        fb = _make_food_bank()
        _add_item(fb, "Pasta", category=WishListItem.Category.HYGIENE)
        recipes = generate_meal_kits(fb)
        assert recipes == []

    def test_baby_items_excluded_from_matching(self):
        fb = _make_food_bank()
        _add_item(fb, "Pasta", category=WishListItem.Category.BABY)
        recipes = generate_meal_kits(fb)
        assert recipes == []

    def test_dietary_restriction_filter(self):
        fb = _make_food_bank()
        _add_item(fb, "Dried Pasta")
        _add_item(fb, "Tinned Tuna")
        recipes = generate_meal_kits(fb, dietary_restrictions=["vegan"])
        for recipe in recipes:
            assert "vegan" in recipe.dietary_tags

    def test_dietary_tags_stored_on_recipe(self):
        fb = _make_food_bank()
        _add_item(fb, "Red Lentils")
        _add_item(fb, "Rice")
        recipes = generate_meal_kits(fb)
        assert any(len(r.dietary_tags) > 0 for r in recipes)

    def test_recipe_fields_populated(self):
        fb = _make_food_bank()
        _add_item(fb, "Dried Pasta")
        recipes = generate_meal_kits(fb)
        assert len(recipes) > 0
        recipe = recipes[0]
        assert recipe.recipe_name
        assert recipe.description
        assert recipe.serves > 0
        assert recipe.cook_time_minutes > 0
        assert isinstance(recipe.ingredients, list)
        assert len(recipe.ingredients) > 0
        assert recipe.instructions
        assert recipe.emoji
        assert recipe.estimated_cost > 0
        assert recipe.expires_at is not None
        assert recipe.generated_at is not None

    def test_ingredients_use_wish_list_item_names(self):
        fb = _make_food_bank()
        _add_item(fb, "Wholewheat Pasta Shapes")
        recipes = generate_meal_kits(fb)
        pasta_recipe = next(
            (r for r in recipes if "Pasta" in r.recipe_name), None
        )
        assert pasta_recipe is not None
        ingredient_names = [i["name"] for i in pasta_recipe.ingredients]
        assert "Wholewheat Pasta Shapes" in ingredient_names

    def test_previous_non_expired_recipes_replaced(self):
        fb = _make_food_bank()
        _add_item(fb, "Dried Pasta")
        generate_meal_kits(fb)
        first_count = GeneratedRecipe.objects.filter(food_bank=fb).count()
        generate_meal_kits(fb)
        second_count = GeneratedRecipe.objects.filter(food_bank=fb).count()
        assert second_count == first_count

    def test_unknown_dietary_tags_ignored(self):
        fb = _make_food_bank()
        _add_item(fb, "Dried Pasta")
        # Should not raise and should ignore unknown tag
        recipes = generate_meal_kits(fb, dietary_restrictions=["halal", "vegetarian"])
        for recipe in recipes:
            assert "vegetarian" in recipe.dietary_tags

    def test_multiple_dietary_restrictions(self):
        fb = _make_food_bank()
        _add_item(fb, "Red Lentils")
        _add_item(fb, "Rice")
        _add_item(fb, "Tinned Tomatoes")
        recipes = generate_meal_kits(
            fb,
            dietary_restrictions=[
                DIETARY_TAG_VEGAN,
                DIETARY_TAG_GLUTEN_FREE,
                DIETARY_TAG_NUT_FREE,
            ],
        )
        for recipe in recipes:
            assert DIETARY_TAG_VEGAN in recipe.dietary_tags
            assert DIETARY_TAG_GLUTEN_FREE in recipe.dietary_tags
            assert DIETARY_TAG_NUT_FREE in recipe.dietary_tags

    def test_all_supported_dietary_tags_present_in_constants(self):
        assert DIETARY_TAG_VEGETARIAN in ALL_DIETARY_TAGS
        assert DIETARY_TAG_VEGAN in ALL_DIETARY_TAGS
        assert DIETARY_TAG_GLUTEN_FREE in ALL_DIETARY_TAGS
        assert DIETARY_TAG_DAIRY_FREE in ALL_DIETARY_TAGS
        assert DIETARY_TAG_NUT_FREE in ALL_DIETARY_TAGS
