"""
Meal kit generation service.

Converts a food bank's wish list into complete meal kits, constrained to items
actually on the wish list and filtered by optional dietary restrictions.
"""
from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from django.utils import timezone

from .models import FoodBank, GeneratedRecipe, WishListItem

# ---------------------------------------------------------------------------
# Recipe templates
# Each template describes a meal that can be assembled from food-bank staples.
# ingredient_slots: list of ingredient "slots" — a slot is filled when ANY of
#   its keywords appear (case-insensitively) in a wish-list item name.
# min_slots_required: minimum filled slots before the recipe is considered
#   viable (allows recipes to be generated even if not every optional
#   ingredient is available).
# dietary_tags: the dietary restrictions this recipe satisfies.
# ---------------------------------------------------------------------------

RECIPE_TEMPLATES: list[dict] = [
    {
        "name": "Tomato & Pasta",
        "emoji": "🍝",
        "description": (
            "A hearty, simple pasta dish built around tinned tomatoes — "
            "one of the most requested food-bank staples."
        ),
        "serves": 4,
        "cook_time_minutes": 20,
        "dietary_tags": ["vegetarian", "vegan", "dairy_free", "nut_free"],
        "ingredient_slots": [
            {"name": "Pasta", "keywords": ["pasta", "spaghetti", "macaroni", "noodle", "penne"], "unit": "g", "quantity": 400},
            {"name": "Tinned Tomatoes", "keywords": ["tinned tomatoes", "chopped tomatoes", "tomato"], "unit": "tins", "quantity": 2},
            {"name": "Onion", "keywords": ["onion"], "unit": "whole", "quantity": 1},
            {"name": "Garlic", "keywords": ["garlic"], "unit": "cloves", "quantity": 2},
            {"name": "Oil", "keywords": ["oil", "olive oil", "vegetable oil", "sunflower oil"], "unit": "tbsp", "quantity": 2},
        ],
        "min_slots_required": 2,
        "instructions": (
            "1. Cook pasta in boiling salted water according to pack instructions.\n"
            "2. Fry diced onion (and garlic if available) in oil over a medium heat until soft, about 5 minutes.\n"
            "3. Add tinned tomatoes, season with salt and pepper, and simmer for 10 minutes.\n"
            "4. Drain pasta, toss with the tomato sauce, and serve."
        ),
        "estimated_cost": Decimal("2.50"),
    },
    {
        "name": "Red Lentil Soup",
        "emoji": "🍲",
        "description": (
            "A warming, protein-rich soup made from red lentils — "
            "naturally gluten-free and vegan, perfect for all the family."
        ),
        "serves": 4,
        "cook_time_minutes": 30,
        "dietary_tags": ["vegetarian", "vegan", "gluten_free", "dairy_free", "halal", "nut_free"],
        "ingredient_slots": [
            {"name": "Red Lentils", "keywords": ["lentil", "red lentil", "lentils"], "unit": "g", "quantity": 250},
            {"name": "Onion", "keywords": ["onion"], "unit": "whole", "quantity": 1},
            {"name": "Carrot", "keywords": ["carrot", "carrots"], "unit": "whole", "quantity": 2},
            {"name": "Tinned Tomatoes", "keywords": ["tinned tomatoes", "chopped tomatoes", "tomato"], "unit": "tins", "quantity": 1},
            {"name": "Oil", "keywords": ["oil", "olive oil", "vegetable oil", "sunflower oil"], "unit": "tbsp", "quantity": 1},
        ],
        "min_slots_required": 2,
        "instructions": (
            "1. Soften diced onion and carrot in oil for 5 minutes.\n"
            "2. Rinse lentils and add to the pan with tinned tomatoes and 800 ml of water.\n"
            "3. Bring to the boil, then simmer for 20–25 minutes until lentils are tender.\n"
            "4. Season well, blend partially for a thicker texture if desired, and serve."
        ),
        "estimated_cost": Decimal("2.00"),
    },
    {
        "name": "Rice & Kidney Beans",
        "emoji": "🍛",
        "description": (
            "A filling plant-based staple dish — high in protein and fibre, "
            "naturally gluten-free and suitable for almost any dietary requirement."
        ),
        "serves": 4,
        "cook_time_minutes": 25,
        "dietary_tags": ["vegetarian", "vegan", "gluten_free", "dairy_free", "halal", "nut_free"],
        "ingredient_slots": [
            {"name": "Rice", "keywords": ["rice", "long grain rice", "basmati"], "unit": "g", "quantity": 300},
            {"name": "Kidney Beans", "keywords": ["kidney beans", "beans", "mixed beans", "baked beans", "chickpeas", "chick peas"], "unit": "tins", "quantity": 1},
            {"name": "Tinned Tomatoes", "keywords": ["tinned tomatoes", "chopped tomatoes", "tomato"], "unit": "tins", "quantity": 1},
            {"name": "Onion", "keywords": ["onion"], "unit": "whole", "quantity": 1},
            {"name": "Oil", "keywords": ["oil", "olive oil", "vegetable oil", "sunflower oil"], "unit": "tbsp", "quantity": 1},
        ],
        "min_slots_required": 2,
        "instructions": (
            "1. Cook rice according to pack instructions.\n"
            "2. Fry onion in oil until golden, about 6 minutes.\n"
            "3. Add tinned tomatoes and drained beans; simmer for 10 minutes.\n"
            "4. Season with salt, pepper and any available spices. Serve over rice."
        ),
        "estimated_cost": Decimal("2.20"),
    },
    {
        "name": "Tuna Pasta Bake",
        "emoji": "🐟",
        "description": (
            "A classic family favourite made from tinned tuna and pasta — "
            "quick, affordable and always popular."
        ),
        "serves": 4,
        "cook_time_minutes": 35,
        "dietary_tags": ["nut_free"],
        "ingredient_slots": [
            {"name": "Pasta", "keywords": ["pasta", "spaghetti", "macaroni", "penne", "noodle"], "unit": "g", "quantity": 400},
            {"name": "Tinned Tuna", "keywords": ["tuna", "tinned tuna", "canned tuna"], "unit": "tins", "quantity": 2},
            {"name": "Tinned Tomatoes", "keywords": ["tinned tomatoes", "chopped tomatoes", "tomato"], "unit": "tins", "quantity": 1},
            {"name": "Cheese", "keywords": ["cheese", "cheddar"], "unit": "g", "quantity": 80},
            {"name": "Onion", "keywords": ["onion"], "unit": "whole", "quantity": 1},
        ],
        "min_slots_required": 2,
        "instructions": (
            "1. Preheat oven to 180 °C. Cook pasta until just tender, drain.\n"
            "2. Mix pasta with drained tuna, tinned tomatoes, and onion (diced).\n"
            "3. Pour into a baking dish, top with grated cheese if available.\n"
            "4. Bake for 20 minutes until golden and bubbling."
        ),
        "estimated_cost": Decimal("3.80"),
    },
    {
        "name": "Vegetable Chickpea Curry",
        "emoji": "🍜",
        "description": (
            "A fragrant, filling curry using tinned chickpeas and vegetables — "
            "naturally vegan and gluten-free."
        ),
        "serves": 4,
        "cook_time_minutes": 30,
        "dietary_tags": ["vegetarian", "vegan", "gluten_free", "dairy_free", "halal", "nut_free"],
        "ingredient_slots": [
            {"name": "Rice", "keywords": ["rice", "long grain rice", "basmati"], "unit": "g", "quantity": 300},
            {"name": "Chickpeas", "keywords": ["chickpeas", "chick peas", "chickpea"], "unit": "tins", "quantity": 1},
            {"name": "Tinned Tomatoes", "keywords": ["tinned tomatoes", "chopped tomatoes", "tomato"], "unit": "tins", "quantity": 1},
            {"name": "Onion", "keywords": ["onion"], "unit": "whole", "quantity": 1},
            {"name": "Oil", "keywords": ["oil", "olive oil", "vegetable oil", "sunflower oil"], "unit": "tbsp", "quantity": 1},
        ],
        "min_slots_required": 2,
        "instructions": (
            "1. Cook rice according to pack instructions.\n"
            "2. Fry diced onion in oil for 5 minutes; stir in any available curry spices or powder.\n"
            "3. Add drained chickpeas and tinned tomatoes. Simmer 15 minutes, adding a little water if too thick.\n"
            "4. Serve over rice."
        ),
        "estimated_cost": Decimal("2.80"),
    },
    {
        "name": "Creamy Porridge",
        "emoji": "🥣",
        "description": (
            "A warming, nutritious breakfast made from oats and milk — "
            "simple, filling and easy to prepare."
        ),
        "serves": 2,
        "cook_time_minutes": 10,
        "dietary_tags": ["vegetarian", "nut_free"],
        "ingredient_slots": [
            {"name": "Oats", "keywords": ["oats", "porridge oats", "oatmeal", "rolled oats"], "unit": "g", "quantity": 160},
            {"name": "Milk", "keywords": ["milk", "uht milk", "long life milk", "dried milk", "powdered milk"], "unit": "ml", "quantity": 400},
            {"name": "Sugar or Honey", "keywords": ["sugar", "honey", "jam"], "unit": "tbsp", "quantity": 2},
        ],
        "min_slots_required": 2,
        "instructions": (
            "1. Combine oats and milk in a saucepan over a medium heat.\n"
            "2. Stir continuously until thick and creamy, about 5 minutes.\n"
            "3. Sweeten with sugar, honey or jam if available and serve immediately."
        ),
        "estimated_cost": Decimal("1.20"),
    },
    {
        "name": "Bean Chilli",
        "emoji": "🌶️",
        "description": (
            "A hearty, spicy chilli made entirely from store-cupboard tins — "
            "vegan, gluten-free and incredibly satisfying."
        ),
        "serves": 4,
        "cook_time_minutes": 30,
        "dietary_tags": ["vegetarian", "vegan", "gluten_free", "dairy_free", "halal", "nut_free"],
        "ingredient_slots": [
            {"name": "Kidney Beans", "keywords": ["kidney beans", "mixed beans", "beans", "baked beans"], "unit": "tins", "quantity": 2},
            {"name": "Tinned Tomatoes", "keywords": ["tinned tomatoes", "chopped tomatoes", "tomato"], "unit": "tins", "quantity": 1},
            {"name": "Onion", "keywords": ["onion"], "unit": "whole", "quantity": 1},
            {"name": "Rice", "keywords": ["rice", "long grain rice", "basmati"], "unit": "g", "quantity": 300},
            {"name": "Oil", "keywords": ["oil", "olive oil", "vegetable oil", "sunflower oil"], "unit": "tbsp", "quantity": 1},
        ],
        "min_slots_required": 2,
        "instructions": (
            "1. Cook rice according to pack instructions.\n"
            "2. Fry diced onion in oil until softened. Add any available chilli powder or spices.\n"
            "3. Stir in drained beans and tinned tomatoes; simmer 20 minutes.\n"
            "4. Serve over rice, topped with cheese if available."
        ),
        "estimated_cost": Decimal("2.30"),
    },
    {
        "name": "Sardines on Toast",
        "emoji": "🐠",
        "description": (
            "A quick, protein-packed snack or light meal using tinned sardines "
            "on wholemeal or white bread — classic British comfort food."
        ),
        "serves": 2,
        "cook_time_minutes": 10,
        "dietary_tags": ["dairy_free", "nut_free"],
        "ingredient_slots": [
            {"name": "Tinned Sardines", "keywords": ["sardines", "tinned sardines", "pilchards", "mackerel"], "unit": "tins", "quantity": 1},
            {"name": "Bread", "keywords": ["bread", "wholemeal bread", "white bread", "rolls", "sliced bread"], "unit": "slices", "quantity": 4},
            {"name": "Lemon Juice or Vinegar", "keywords": ["lemon", "lemon juice", "vinegar"], "unit": "tsp", "quantity": 1},
        ],
        "min_slots_required": 2,
        "instructions": (
            "1. Toast the bread.\n"
            "2. Drain and mash sardines with a splash of lemon juice or vinegar.\n"
            "3. Spread generously on toast and serve."
        ),
        "estimated_cost": Decimal("1.50"),
    },
    {
        "name": "Chicken & Rice Pot",
        "emoji": "🍗",
        "description": (
            "A simple one-pot meal using tinned or fresh chicken with rice — "
            "high in protein and naturally gluten-free."
        ),
        "serves": 4,
        "cook_time_minutes": 35,
        "dietary_tags": ["gluten_free", "dairy_free", "halal", "nut_free"],
        "ingredient_slots": [
            {"name": "Rice", "keywords": ["rice", "long grain rice", "basmati"], "unit": "g", "quantity": 300},
            {"name": "Chicken", "keywords": ["chicken", "tinned chicken", "canned chicken"], "unit": "g", "quantity": 400},
            {"name": "Onion", "keywords": ["onion"], "unit": "whole", "quantity": 1},
            {"name": "Tinned Tomatoes", "keywords": ["tinned tomatoes", "chopped tomatoes", "tomato"], "unit": "tins", "quantity": 1},
            {"name": "Oil", "keywords": ["oil", "olive oil", "vegetable oil", "sunflower oil"], "unit": "tbsp", "quantity": 1},
        ],
        "min_slots_required": 2,
        "instructions": (
            "1. Fry diced onion in oil until golden, about 6 minutes.\n"
            "2. Add chicken pieces (or drained tinned chicken) and brown lightly.\n"
            "3. Stir in tinned tomatoes and 600 ml water; bring to a boil.\n"
            "4. Add rice, reduce heat, cover and cook 18–20 minutes until rice is tender.\n"
            "5. Season to taste and serve."
        ),
        "estimated_cost": Decimal("4.00"),
    },
    {
        "name": "Pea & Ham Soup",
        "emoji": "🫛",
        "description": (
            "A thick, comforting soup made from split peas — high in protein, "
            "naturally gluten-free and very budget-friendly."
        ),
        "serves": 4,
        "cook_time_minutes": 45,
        "dietary_tags": ["gluten_free", "dairy_free", "nut_free"],
        "ingredient_slots": [
            {"name": "Split Peas", "keywords": ["split peas", "peas", "yellow peas", "green peas", "dried peas"], "unit": "g", "quantity": 250},
            {"name": "Onion", "keywords": ["onion"], "unit": "whole", "quantity": 1},
            {"name": "Carrot", "keywords": ["carrot", "carrots"], "unit": "whole", "quantity": 1},
            {"name": "Ham or Luncheon Meat", "keywords": ["ham", "luncheon meat", "tinned ham", "corned beef"], "unit": "g", "quantity": 200},
        ],
        "min_slots_required": 2,
        "instructions": (
            "1. Rinse split peas. Fry onion and carrot in a little oil until softened.\n"
            "2. Add peas and 1.2 litres of water; bring to the boil and simmer 35–40 minutes.\n"
            "3. Stir in diced ham, season well, and serve with bread if available."
        ),
        "estimated_cost": Decimal("2.60"),
    },
]


def _item_names_set(wish_list_items: list[WishListItem]) -> list[str]:
    """Return a list of lowercased wish-list item names."""
    return [item.item_name.lower() for item in wish_list_items]


def _slot_is_filled(slot: dict, item_names: list[str]) -> bool:
    """Return True if any wish-list item name contains any of the slot's keywords."""
    for keyword in slot["keywords"]:
        kw = keyword.lower()
        if any(kw in name for name in item_names):
            return True
    return False


def _build_ingredients(template: dict, item_names: list[str]) -> list[dict]:
    """
    Build the ingredients list for a recipe instance.

    Filled slots use the canonical ingredient name; unfilled optional slots are
    still included so the donor knows the full kit composition.
    """
    result = []
    for slot in template["ingredient_slots"]:
        result.append(
            {
                "name": slot["name"],
                "quantity": slot["quantity"],
                "unit": slot["unit"],
                "available_from_wish_list": _slot_is_filled(slot, item_names),
            }
        )
    return result


class MealKitGenerator:
    """
    Generates `GeneratedRecipe` meal-kit instances for a food bank.

    Recipes are constrained to items present on the food bank's wish list and
    can optionally be filtered by dietary restrictions.
    """

    EXPIRY_HOURS = 24

    def generate(
        self,
        food_bank: FoodBank,
        dietary_restrictions: list[str] | None = None,
    ) -> list[GeneratedRecipe]:
        """
        Generate meal kits for *food_bank* based on its current wish list.

        Parameters
        ----------
        food_bank:
            The food bank whose wish list drives ingredient availability.
        dietary_restrictions:
            Optional list of restriction tags (e.g. ``["vegan", "gluten_free"]``).
            When provided, only recipes that satisfy **all** listed restrictions
            are considered.

        Returns
        -------
        list[GeneratedRecipe]
            Newly created (and saved) recipe instances.
        """
        dietary_restrictions = dietary_restrictions or []
        wish_list_items = list(food_bank.wish_list_items.all())
        item_names = _item_names_set(wish_list_items)
        expires_at = timezone.now() + timedelta(hours=self.EXPIRY_HOURS)

        generated: list[GeneratedRecipe] = []

        for template in RECIPE_TEMPLATES:
            # --- dietary restriction filter ---
            if dietary_restrictions:
                template_tags = set(template["dietary_tags"])
                if not all(r in template_tags for r in dietary_restrictions):
                    continue

            # --- wish-list ingredient matching ---
            if wish_list_items:
                filled = sum(
                    1
                    for slot in template["ingredient_slots"]
                    if _slot_is_filled(slot, item_names)
                )
                if filled < template["min_slots_required"]:
                    continue

            ingredients = _build_ingredients(template, item_names)

            recipe = GeneratedRecipe.objects.create(
                food_bank=food_bank,
                recipe_name=template["name"],
                description=template["description"],
                serves=template["serves"],
                cook_time_minutes=template["cook_time_minutes"],
                ingredients=ingredients,
                instructions=template["instructions"],
                emoji=template["emoji"],
                estimated_cost=template["estimated_cost"],
                dietary_restrictions=template["dietary_tags"],
                expires_at=expires_at,
            )
            generated.append(recipe)

        return generated
