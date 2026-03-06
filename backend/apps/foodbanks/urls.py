from django.urls import path

from .views import FoodBankListView

urlpatterns = [
    path("food-banks/", FoodBankListView.as_view(), name="food-bank-list"),
]
