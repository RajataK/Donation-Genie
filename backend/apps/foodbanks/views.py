from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.utils import timezone

from .models import FoodBank, WishListItem
from .serializers import (
    FoodBankSerializer,
    GenerateMealKitsRequestSerializer,
    GeneratedRecipeSerializer,
    WishListItemSerializer,
)
from .services import generate_meal_kits


class FoodBankListView(ListAPIView):
    queryset = FoodBank.objects.all()
    serializer_class = FoodBankSerializer
    authentication_classes = []
    permission_classes = []


class WishListView(ListAPIView):
    """Return all wish-list items for a specific food bank."""

    serializer_class = WishListItemSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        return WishListItem.objects.filter(food_bank_id=self.kwargs["food_bank_id"])


class GenerateMealKitsView(APIView):
    """Generate meal-kit recipes for a food bank constrained by its wish list.

    Accepts an optional list of ``dietary_restrictions`` (e.g. ``vegetarian``,
    ``vegan``, ``gluten_free``, ``dairy_free``, ``nut_free``) to further
    filter the returned recipes.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request: Request, food_bank_id: str) -> Response:
        try:
            food_bank = FoodBank.objects.get(pk=food_bank_id)
        except FoodBank.DoesNotExist:
            return Response({"detail": "Food bank not found."}, status=404)

        request_serializer = GenerateMealKitsRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        dietary_restrictions: list[str] = request_serializer.validated_data.get(
            "dietary_restrictions", []
        )

        recipes = generate_meal_kits(food_bank, dietary_restrictions)
        response_serializer = GeneratedRecipeSerializer(recipes, many=True)
        return Response(response_serializer.data, status=200)


class MealKitListView(ListAPIView):
    """Return previously generated (non-expired) meal-kit recipes for a food bank."""

    serializer_class = GeneratedRecipeSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        try:
            food_bank = FoodBank.objects.get(pk=self.kwargs["food_bank_id"])
        except FoodBank.DoesNotExist:
            raise Http404
        return (
            food_bank.generated_recipes.filter(expires_at__gt=timezone.now())
            .order_by("recipe_name")
        )

