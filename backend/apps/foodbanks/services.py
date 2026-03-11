"""
Meal kit generation service.

Generates recipe-based meal kits from a food bank's wish list items,
constrained to ingredients available on the wish list.  Supports optional
filtering by dietary restrictions so that every returned recipe meets all
of the caller's requirements.
"""

from __future__ import annotations

import re
from datetime import timedelta
from decimal import Decimal
from typing import Any

from django.utils import timezone

from .models import FoodBank, GeneratedRecipe, WishListItem

# ---------------------------------------------------------------------------
# Supported dietary tags
# ---------------------------------------------------------------------------

DIETARY_TAG_VEGETARIAN = "vegetarian"
DIETARY_TAG_VEGAN = "vegan"
DIETARY_TAG_GLUTEN_FREE = "gluten_free"
DIETARY_TAG_DAIRY_FREE = "dairy_free"
DIETARY_TAG_NUT_FREE = "nut_free"

ALL_DIETARY_TAGS: list[str] = [
    DIETARY_TAG_VEGETARIAN,
    DIETARY_TAG_VEGAN,
    DIETARY_TAG_GLUTEN_FREE,
    DIETARY_TAG_DAIRY_FREE,
    DIETARY_TAG_NUT_FREE,
]

# ---------------------------------------------------------------------------
# Recipe templates
#
# Each template describes a meal that can be assembled from typical food-bank
# wish-list items.  The matching logic checks whether at least one wish-list
# item name contains each of the strings in ``required_keywords``.
#
# ``ingredient_keywords`` lists (keyword, label, unit, quantity) tuples used
# to build the ``ingredients`` JSON list from the matched wish-list items.
# ---------------------------------------------------------------------------

RECIPE_TEMPLATES: list[dict[str, Any]] = [
    {
        "recipe_name": "Pasta with Tomato Sauce",
        "emoji": "🍝",
        "description": (
            "A warming, filling pasta dish made with tinned tomatoes. "
            "Simple, nutritious, and loved by all ages."
        ),
        "required_keywords": ["pasta"],
        "ingredient_keywords": [
            ("pasta", "Pasta", "g", 500),
            ("tomato", "Tinned Tomatoes", "tins", 1),
            ("herb", "Dried Mixed Herbs", "tsp", 1),
        ],
        "serves": 4,
        "cook_time_minutes": 20,
        "dietary_tags": [
            DIETARY_TAG_VEGETARIAN,
            DIETARY_TAG_VEGAN,
            DIETARY_TAG_DAIRY_FREE,
            DIETARY_TAG_NUT_FREE,
        ],
        "instructions": (
            "1. Cook pasta in boiling salted water per packet instructions.\n"
            "2. Pour tinned tomatoes into a pan with a little oil.\n"
            "3. Simmer for 10 minutes; season with salt, pepper and dried herbs.\n"
            "4. Drain the pasta, mix with the sauce, and serve."
        ),
        "estimated_cost": Decimal("2.50"),
    },
    {
        "recipe_name": "Rice and Lentil Dahl",
        "emoji": "🍛",
        "description": (
            "A hearty and protein-rich dahl made from red lentils and rice. "
            "Packed with flavour from store-cupboard spices."
        ),
        "required_keywords": ["lentil"],
        "ingredient_keywords": [
            ("lentil", "Red Lentils", "g", 300),
            ("rice", "Rice", "g", 200),
            ("tomato", "Tinned Tomatoes", "tins", 1),
            ("onion", "Onion", "medium", 1),
            ("cumin", "Cumin", "tsp", 1),
            ("turmeric", "Turmeric", "tsp", 0.5),
        ],
        "serves": 4,
        "cook_time_minutes": 30,
        "dietary_tags": [
            DIETARY_TAG_VEGETARIAN,
            DIETARY_TAG_VEGAN,
            DIETARY_TAG_GLUTEN_FREE,
            DIETARY_TAG_DAIRY_FREE,
            DIETARY_TAG_NUT_FREE,
        ],
        "instructions": (
            "1. Rinse lentils thoroughly.\n"
            "2. Sauté chopped onion in oil until soft.\n"
            "3. Add spices and stir for 1 minute.\n"
            "4. Add lentils and tinned tomatoes; cover with water.\n"
            "5. Simmer for 20 minutes until lentils are tender.\n"
            "6. Cook rice separately and serve with the dahl."
        ),
        "estimated_cost": Decimal("2.00"),
    },
    {
        "recipe_name": "Tinned Tuna Pasta Bake",
        "emoji": "🐟",
        "description": (
            "A classic family favourite — creamy tuna pasta bake using "
            "tinned fish and store-cupboard staples."
        ),
        "required_keywords": ["pasta", "tuna"],
        "ingredient_keywords": [
            ("pasta", "Pasta", "g", 400),
            ("tuna", "Tinned Tuna", "tins", 2),
            ("milk", "Milk", "ml", 300),
            ("flour", "Plain Flour", "tbsp", 2),
            ("cheese", "Grated Cheese", "g", 100),
        ],
        "serves": 4,
        "cook_time_minutes": 40,
        "dietary_tags": [DIETARY_TAG_NUT_FREE],
        "instructions": (
            "1. Cook pasta until al dente; drain.\n"
            "2. Make a white sauce: melt butter, stir in flour, then gradually add milk.\n"
            "3. Stir drained tuna into the sauce.\n"
            "4. Mix with pasta and transfer to an oven dish.\n"
            "5. Top with grated cheese and bake at 200 °C for 20 minutes."
        ),
        "estimated_cost": Decimal("4.00"),
    },
    {
        "recipe_name": "Vegetable Rice Stir-Fry",
        "emoji": "🍚",
        "description": (
            "Quick and easy fried rice packed with vegetables. "
            "A great way to use tinned or dried goods."
        ),
        "required_keywords": ["rice"],
        "ingredient_keywords": [
            ("rice", "Rice", "g", 300),
            ("vegetable", "Mixed Vegetables (tinned or frozen)", "g", 200),
            ("soy sauce", "Soy Sauce", "tbsp", 2),
            ("egg", "Egg", "large", 2),
            ("oil", "Cooking Oil", "tbsp", 1),
        ],
        "serves": 3,
        "cook_time_minutes": 25,
        "dietary_tags": [
            DIETARY_TAG_VEGETARIAN,
            DIETARY_TAG_DAIRY_FREE,
            DIETARY_TAG_NUT_FREE,
        ],
        "instructions": (
            "1. Cook rice and let it cool slightly.\n"
            "2. Heat oil in a wok or large frying pan over high heat.\n"
            "3. Add vegetables and stir-fry for 3 minutes.\n"
            "4. Push to one side, scramble the eggs in the pan.\n"
            "5. Add rice and soy sauce; toss everything together.\n"
            "6. Season to taste and serve."
        ),
        "estimated_cost": Decimal("2.00"),
    },
    {
        "recipe_name": "Tomato and Bean Soup",
        "emoji": "🍲",
        "description": (
            "A thick, filling soup made with tinned tomatoes and beans. "
            "Perfect for a cold day and easily batch-cooked."
        ),
        "required_keywords": ["bean"],
        "ingredient_keywords": [
            ("bean", "Tinned Beans (haricot, kidney, or mixed)", "tins", 2),
            ("tomato", "Tinned Tomatoes", "tins", 1),
            ("onion", "Onion", "medium", 1),
            ("garlic", "Garlic (or garlic powder)", "cloves", 2),
            ("stock", "Vegetable Stock Cube", "cube", 1),
        ],
        "serves": 4,
        "cook_time_minutes": 25,
        "dietary_tags": [
            DIETARY_TAG_VEGETARIAN,
            DIETARY_TAG_VEGAN,
            DIETARY_TAG_GLUTEN_FREE,
            DIETARY_TAG_DAIRY_FREE,
            DIETARY_TAG_NUT_FREE,
        ],
        "instructions": (
            "1. Sauté chopped onion and garlic in oil until soft.\n"
            "2. Add tinned tomatoes and 500 ml of water with the stock cube.\n"
            "3. Drain and rinse the beans; add to the pot.\n"
            "4. Simmer for 15 minutes, mashing some beans for thickness.\n"
            "5. Season and serve with bread if available."
        ),
        "estimated_cost": Decimal("1.80"),
    },
    {
        "recipe_name": "Porridge with Fruit",
        "emoji": "🥣",
        "description": (
            "A nourishing breakfast for the whole family. "
            "Made with oats and sweetened with tinned or dried fruit."
        ),
        "required_keywords": ["oat"],
        "ingredient_keywords": [
            ("oat", "Porridge Oats", "g", 300),
            ("milk", "Milk (or water)", "ml", 600),
            ("fruit", "Tinned or Dried Fruit", "portion", 1),
            ("sugar", "Sugar or Honey", "tsp", 2),
        ],
        "serves": 4,
        "cook_time_minutes": 10,
        "dietary_tags": [
            DIETARY_TAG_VEGETARIAN,
            DIETARY_TAG_NUT_FREE,
        ],
        "instructions": (
            "1. Combine oats and milk (or water) in a saucepan.\n"
            "2. Cook over medium heat, stirring constantly, for 5 minutes.\n"
            "3. Sweeten with sugar or honey.\n"
            "4. Top with fruit and serve."
        ),
        "estimated_cost": Decimal("1.50"),
    },
    {
        "recipe_name": "Lentil Vegetable Soup",
        "emoji": "🥗",
        "description": (
            "A thick, comforting soup brimming with lentils and vegetables. "
            "Gluten-free, vegan, and packed with protein."
        ),
        "required_keywords": ["lentil"],
        "ingredient_keywords": [
            ("lentil", "Green or Red Lentils", "g", 250),
            ("carrot", "Carrot", "medium", 2),
            ("onion", "Onion", "medium", 1),
            ("celery", "Celery", "stalks", 2),
            ("stock", "Vegetable Stock Cube", "cube", 1),
            ("tomato", "Tinned Tomatoes", "tins", 1),
        ],
        "serves": 6,
        "cook_time_minutes": 35,
        "dietary_tags": [
            DIETARY_TAG_VEGETARIAN,
            DIETARY_TAG_VEGAN,
            DIETARY_TAG_GLUTEN_FREE,
            DIETARY_TAG_DAIRY_FREE,
            DIETARY_TAG_NUT_FREE,
        ],
        "instructions": (
            "1. Sauté diced onion, carrot and celery in oil for 5 minutes.\n"
            "2. Add lentils, tinned tomatoes, stock cube and 1 litre of water.\n"
            "3. Bring to the boil then simmer for 25 minutes until lentils are soft.\n"
            "4. Blend partially for a creamier texture, or leave chunky.\n"
            "5. Season to taste."
        ),
        "estimated_cost": Decimal("2.20"),
    },
    {
        "recipe_name": "Chickpea Curry",
        "emoji": "🍛",
        "description": (
            "A fragrant and filling chickpea curry that comes together quickly "
            "using tinned chickpeas and pantry spices."
        ),
        "required_keywords": ["chickpea"],
        "ingredient_keywords": [
            ("chickpea", "Tinned Chickpeas", "tins", 2),
            ("tomato", "Tinned Tomatoes", "tins", 1),
            ("onion", "Onion", "medium", 1),
            ("curry powder", "Curry Powder", "tbsp", 1),
            ("rice", "Rice (to serve)", "g", 300),
        ],
        "serves": 4,
        "cook_time_minutes": 25,
        "dietary_tags": [
            DIETARY_TAG_VEGETARIAN,
            DIETARY_TAG_VEGAN,
            DIETARY_TAG_GLUTEN_FREE,
            DIETARY_TAG_DAIRY_FREE,
            DIETARY_TAG_NUT_FREE,
        ],
        "instructions": (
            "1. Sauté chopped onion in oil until golden.\n"
            "2. Add curry powder and stir for 1 minute.\n"
            "3. Add drained chickpeas and tinned tomatoes.\n"
            "4. Simmer for 15 minutes until sauce thickens.\n"
            "5. Serve over cooked rice."
        ),
        "estimated_cost": Decimal("2.80"),
    },
    {
        "recipe_name": "Sardines on Toast",
        "emoji": "🐟",
        "description": (
            "A quick, protein-rich meal using tinned sardines served on toast. "
            "Ready in minutes and very nutritious."
        ),
        "required_keywords": ["sardine"],
        "ingredient_keywords": [
            ("sardine", "Tinned Sardines", "tins", 2),
            ("bread", "Bread", "slices", 4),
            ("lemon", "Lemon Juice (or vinegar)", "tsp", 1),
            ("pepper", "Black Pepper", "to taste", 1),
        ],
        "serves": 2,
        "cook_time_minutes": 5,
        "dietary_tags": [
            DIETARY_TAG_DAIRY_FREE,
            DIETARY_TAG_NUT_FREE,
        ],
        "instructions": (
            "1. Toast the bread.\n"
            "2. Drain the sardines and place on the toast.\n"
            "3. Add a squeeze of lemon juice and black pepper.\n"
            "4. Serve immediately."
        ),
        "estimated_cost": Decimal("1.50"),
    },
    {
        "recipe_name": "Rice Pudding",
        "emoji": "🍮",
        "description": (
            "A classic, creamy rice pudding that uses simple store-cupboard "
            "ingredients. Comforting and loved by children and adults alike."
        ),
        "required_keywords": ["rice"],
        "ingredient_keywords": [
            ("rice", "Pudding Rice (or short-grain rice)", "g", 150),
            ("milk", "Milk", "ml", 700),
            ("sugar", "Sugar", "tbsp", 3),
            ("vanilla", "Vanilla Extract", "tsp", 0.5),
        ],
        "serves": 4,
        "cook_time_minutes": 40,
        "dietary_tags": [
            DIETARY_TAG_VEGETARIAN,
            DIETARY_TAG_GLUTEN_FREE,
            DIETARY_TAG_NUT_FREE,
        ],
        "instructions": (
            "1. Combine rice, milk, and sugar in a heavy-bottomed saucepan.\n"
            "2. Bring to the boil, then reduce heat to very low.\n"
            "3. Simmer uncovered for 30–35 minutes, stirring often, until creamy.\n"
            "4. Stir in vanilla and serve warm or cold."
        ),
        "estimated_cost": Decimal("1.80"),
    },
]

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

RECIPE_EXPIRY_HOURS = 24


def generate_meal_kits(
    food_bank: FoodBank,
    dietary_restrictions: list[str] | None = None,
) -> list[GeneratedRecipe]:
    """Generate meal-kit recipes for *food_bank* constrained by its wish list.

    Only templates whose ``required_keywords`` all match at least one wish-list
    item name are considered.  If *dietary_restrictions* are given, only
    templates whose ``dietary_tags`` include **all** of the requested
    restrictions are returned.

    Previously generated (non-expired) recipes are replaced with a fresh set
    so that the returned list is always current.

    Args:
        food_bank: The :class:`~apps.foodbanks.models.FoodBank` instance.
        dietary_restrictions: Optional list of dietary tag strings (e.g.
            ``["vegetarian", "gluten_free"]``).  All values must come from
            :data:`ALL_DIETARY_TAGS`; unknown tags are silently ignored.

    Returns:
        A list of newly-created :class:`~apps.foodbanks.models.GeneratedRecipe`
        instances.
    """
    dietary_restrictions = _normalise_restrictions(dietary_restrictions)

    wish_list_items = list(
        food_bank.wish_list_items.exclude(
            category=WishListItem.Category.HYGIENE
        ).exclude(
            category=WishListItem.Category.BABY
        )
    )

    matched_templates = _match_templates(wish_list_items, dietary_restrictions)

    now = timezone.now()
    expires_at = now + timedelta(hours=RECIPE_EXPIRY_HOURS)

    # Remove any existing non-expired recipes for this food bank so we always
    # return a fresh, consistent set.
    food_bank.generated_recipes.filter(expires_at__gt=now).delete()

    recipes: list[GeneratedRecipe] = []
    for template in matched_templates:
        ingredients = _build_ingredients(template, wish_list_items)
        recipe = GeneratedRecipe.objects.create(
            food_bank=food_bank,
            recipe_name=template["recipe_name"],
            description=template["description"],
            serves=template["serves"],
            cook_time_minutes=template["cook_time_minutes"],
            ingredients=ingredients,
            instructions=template["instructions"],
            emoji=template["emoji"],
            estimated_cost=template["estimated_cost"],
            dietary_tags=template["dietary_tags"],
            expires_at=expires_at,
        )
        recipes.append(recipe)

    return recipes


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _normalise_restrictions(
    restrictions: list[str] | None,
) -> list[str]:
    """Return a deduplicated list of known dietary restriction tags."""
    if not restrictions:
        return []
    return [r for r in set(restrictions) if r in ALL_DIETARY_TAGS]


def _item_matches_keyword(item_name: str, keyword: str) -> bool:
    """Return True if *keyword* appears as a word (or part of a word) in *item_name*."""
    return bool(re.search(re.escape(keyword), item_name, re.IGNORECASE))


def _wish_list_covers_keyword(
    wish_list_items: list[WishListItem], keyword: str
) -> bool:
    """Return True if any wish-list item name contains *keyword*."""
    return any(_item_matches_keyword(item.item_name, keyword) for item in wish_list_items)


def _match_templates(
    wish_list_items: list[WishListItem],
    dietary_restrictions: list[str],
) -> list[dict[str, Any]]:
    """Filter templates to those whose required ingredients appear on the wish list
    and whose dietary tags satisfy all requested restrictions."""
    matched = []
    for template in RECIPE_TEMPLATES:
        if not all(
            _wish_list_covers_keyword(wish_list_items, kw)
            for kw in template["required_keywords"]
        ):
            continue

        if dietary_restrictions and not all(
            tag in template["dietary_tags"] for tag in dietary_restrictions
        ):
            continue

        matched.append(template)

    return matched


def _build_ingredients(
    template: dict[str, Any],
    wish_list_items: list[WishListItem],
) -> list[dict[str, Any]]:
    """Build an ingredients list from the template, using actual wish-list item
    names where possible, falling back to the template label."""
    ingredients: list[dict[str, Any]] = []
    for keyword, label, unit, quantity in template["ingredient_keywords"]:
        matched_item = next(
            (
                item
                for item in wish_list_items
                if _item_matches_keyword(item.item_name, keyword)
            ),
            None,
        )
        ingredient_name = matched_item.item_name if matched_item else label
        ingredients.append(
            {
                "name": ingredient_name,
                "quantity": quantity,
                "unit": unit,
            }
        )
    return ingredients
