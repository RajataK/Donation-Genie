from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FoodBank, GeneratedRecipe
from .serializers import (
    FoodBankSerializer,
    GeneratedRecipeSerializer,
    MealKitGenerationRequestSerializer,
)
from .services import MealKitGenerator


class FoodBankListView(ListAPIView):
    queryset = FoodBank.objects.all()
    serializer_class = FoodBankSerializer
    authentication_classes = []
    permission_classes = []


class MealKitGenerateView(APIView):
    """
    Generate meal-kit recipes for a food bank from its current wish list.

    POST /api/food-banks/{id}/generate-meal-kits/

    Request body (all fields optional):
        dietary_restrictions: list of restriction tags, e.g. ["vegan", "gluten_free"]

    Returns the list of generated recipes, each built exclusively from items
    on the food bank's wish list and satisfying the requested dietary
    restrictions.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request, pk):
        try:
            food_bank = FoodBank.objects.get(pk=pk)
        except FoodBank.DoesNotExist:
            return Response(
                {"detail": "Food bank not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        req_serializer = MealKitGenerationRequestSerializer(data=request.data)
        if not req_serializer.is_valid():
            return Response(req_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dietary_restrictions = list(req_serializer.validated_data.get("dietary_restrictions", []))

        generator = MealKitGenerator()
        recipes = generator.generate(food_bank, dietary_restrictions=dietary_restrictions)

        resp_serializer = GeneratedRecipeSerializer(recipes, many=True)
        return Response(resp_serializer.data, status=status.HTTP_201_CREATED)


class MealKitListView(ListAPIView):
    """
    List all non-expired generated meal-kit recipes for a food bank.

    GET /api/food-banks/{id}/meal-kits/

    Supports optional filtering by dietary restrictions via query params:
        ?dietary_restrictions=vegan&dietary_restrictions=gluten_free
    """

    serializer_class = GeneratedRecipeSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        from django.utils import timezone

        pk = self.kwargs["pk"]
        return GeneratedRecipe.objects.filter(
            food_bank_id=pk,
            expires_at__gt=timezone.now(),
        ).order_by("-generated_at")

    def get(self, request, *args, **kwargs):
        try:
            FoodBank.objects.get(pk=kwargs["pk"])
        except FoodBank.DoesNotExist:
            return Response(
                {"detail": "Food bank not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return super().get(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        dietary_restrictions = self.request.query_params.getlist("dietary_restrictions")
        if dietary_restrictions:
            from django.db import connection

            if connection.features.supports_json_field_contains:
                # Use efficient DB-level containment (PostgreSQL)
                for restriction in dietary_restrictions:
                    queryset = queryset.filter(dietary_restrictions__contains=[restriction])
            else:
                # Fallback: Python-level filtering (SQLite / test environments)
                queryset = [
                    recipe
                    for recipe in queryset
                    if all(dr in recipe.dietary_restrictions for dr in dietary_restrictions)
                ]
        return queryset


class MealKitDetailView(RetrieveAPIView):
    """
    Retrieve a single generated meal-kit recipe.

    GET /api/food-banks/{id}/meal-kits/{recipe_id}/
    """

    serializer_class = GeneratedRecipeSerializer
    authentication_classes = []
    permission_classes = []
    lookup_url_kwarg = "recipe_id"

    def get_queryset(self):
        return GeneratedRecipe.objects.filter(food_bank_id=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        try:
            FoodBank.objects.get(pk=kwargs["pk"])
        except FoodBank.DoesNotExist:
            return Response(
                {"detail": "Food bank not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return super().get(request, *args, **kwargs)
