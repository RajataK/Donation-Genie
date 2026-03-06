from rest_framework import serializers

from .models import FoodBank


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
