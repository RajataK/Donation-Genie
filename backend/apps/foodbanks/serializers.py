from rest_framework import serializers

from .models import FoodBank, GeneratedRecipe


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
            "dietary_restrictions",
            "generated_at",
            "expires_at",
        ]
        read_only_fields = fields


class MealKitGenerationRequestSerializer(serializers.Serializer):
    dietary_restrictions = serializers.MultipleChoiceField(
        choices=GeneratedRecipe.DietaryRestriction.values,
        required=False,
        default=list,
        help_text=(
            "Optional list of dietary restrictions to filter recipes by. "
            "Only recipes satisfying ALL listed restrictions will be returned. "
            f"Allowed values: {', '.join(GeneratedRecipe.DietaryRestriction.values)}."
        ),
    )
