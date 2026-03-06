import uuid

from django.db import models

from apps.core.models import TimestampMixin
from apps.foodbanks.models import FoodBank, GeneratedRecipe


class Donation(TimestampMixin):
    class DonationType(models.TextChoices):
        RECIPE_KIT = "recipe_kit", "Recipe Kit"
        INDIVIDUAL_ITEMS = "individual_items", "Individual Items"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food_bank = models.ForeignKey(
        FoodBank,
        on_delete=models.CASCADE,
        related_name="donations",
    )
    donation_type = models.CharField(
        max_length=20,
        choices=DonationType.choices,
    )
    recipe = models.ForeignKey(
        GeneratedRecipe,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="donations",
    )
    items = models.JSONField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    postcode = models.CharField(max_length=10)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Donation {self.pk}"


class DeliveryTracking(TimestampMixin):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        DISPATCHED = "dispatched", "Dispatched"
        DELIVERED = "delivered", "Delivered"
        RECEIVED = "received", "Received"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    donation = models.ForeignKey(
        Donation,
        on_delete=models.CASCADE,
        related_name="delivery_tracking",
    )
    supermarket = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
    )
    tracking_number = models.TextField(blank=True)
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    actual_delivery = models.DateTimeField(null=True, blank=True)
    received_confirmed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tracking {self.pk}"
