from django.urls import path

from .views import FoodBankListView, GenerateMealKitsView, MealKitListView, WishListView

urlpatterns = [
    path("food-banks/", FoodBankListView.as_view(), name="food-bank-list"),
    path(
        "food-banks/<uuid:food_bank_id>/wish-list/",
        WishListView.as_view(),
        name="food-bank-wish-list",
    ),
    path(
        "food-banks/<uuid:food_bank_id>/generate-meal-kits/",
        GenerateMealKitsView.as_view(),
        name="food-bank-generate-meal-kits",
    ),
    path(
        "food-banks/<uuid:food_bank_id>/meal-kits/",
        MealKitListView.as_view(),
        name="food-bank-meal-kits",
    ),
]
