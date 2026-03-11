from rest_framework import serializers

from .models import FoodBank, GeneratedRecipe, WishListItem


class FoodBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodBank
        fields = [
            "id",
            "name",
            "postcode",
            "latitude",
            "longitude",
            "address",
            "families_served_weekly",
            "urgency_level",
            "last_updated",
        ]
        read_only_fields = fields


class WishListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishListItem
        fields = [
            "id",
            "item_name",
            "category",
            "urgency",
            "quantity_needed",
            "unit",
            "notes",
            "created_at",
        ]
        read_only_fields = fields


class GeneratedRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedRecipe
        fields = [
            "id",
            "food_bank",
            "recipe_name",
            "description",
            "serves",
            "cook_time_minutes",
            "ingredients",
            "instructions",
            "emoji",
            "estimated_cost",
            "dietary_tags",
            "generated_at",
            "expires_at",
        ]
        read_only_fields = fields


class GenerateMealKitsRequestSerializer(serializers.Serializer):
    dietary_restrictions = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        default=list,
        help_text=(
            "Optional list of dietary restriction tags to filter recipes by. "
            "Supported values: vegetarian, vegan, gluten_free, dairy_free, nut_free."
        ),
    )

