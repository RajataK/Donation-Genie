from django.urls import path

from .views import FoodBankListView, MealKitDetailView, MealKitGenerateView, MealKitListView

urlpatterns = [
    path("food-banks/", FoodBankListView.as_view(), name="food-bank-list"),
    path("food-banks/<uuid:pk>/generate-meal-kits/", MealKitGenerateView.as_view(), name="food-bank-generate-meal-kits"),
    path("food-banks/<uuid:pk>/meal-kits/", MealKitListView.as_view(), name="food-bank-meal-kit-list"),
    path("food-banks/<uuid:pk>/meal-kits/<uuid:recipe_id>/", MealKitDetailView.as_view(), name="food-bank-meal-kit-detail"),
]
