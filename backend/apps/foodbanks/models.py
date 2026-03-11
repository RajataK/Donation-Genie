import uuid

from django.db import models

from apps.core.models import TimestampMixin


class FoodBank(TimestampMixin):
    class UrgencyLevel(models.TextChoices):
        URGENT = "urgent", "Urgent"
        ACTIVE = "active", "Active"
        NORMAL = "normal", "Normal"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    postcode = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField()
    families_served_weekly = models.PositiveIntegerField(default=0)
    urgency_level = models.CharField(
        max_length=10,
        choices=UrgencyLevel.choices,
    )
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WishListItem(TimestampMixin):
    class Category(models.TextChoices):
        TINNED_GOODS = "tinned_goods", "Tinned Goods"
        DRIED_GOODS = "dried_goods", "Dried Goods"
        FRESH = "fresh", "Fresh"
        DAIRY = "dairy", "Dairy"
        BABY = "baby", "Baby"
        HYGIENE = "hygiene", "Hygiene"

    class Urgency(models.TextChoices):
        URGENT = "urgent", "Urgent"
        NEEDED = "needed", "Needed"
        OPTIONAL = "optional", "Optional"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food_bank = models.ForeignKey(
        FoodBank,
        on_delete=models.CASCADE,
        related_name="wish_list_items",
    )
    item_name = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices)
    urgency = models.CharField(max_length=10, choices=Urgency.choices)
    quantity_needed = models.PositiveIntegerField(default=0)
    unit = models.TextField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.item_name


class GeneratedRecipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food_bank = models.ForeignKey(
        FoodBank,
        on_delete=models.CASCADE,
        related_name="generated_recipes",
    )
    recipe_name = models.TextField()
    description = models.TextField()
    serves = models.PositiveIntegerField()
    cook_time_minutes = models.PositiveIntegerField()
    ingredients = models.JSONField()
    instructions = models.TextField()
    emoji = models.TextField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    dietary_tags = models.JSONField(default=list)
    generated_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.recipe_name


class FoodBankSettings(TimestampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food_bank = models.OneToOneField(
        FoodBank,
        on_delete=models.CASCADE,
        related_name="settings",
    )
    pepesto_enabled = models.BooleanField(default=False)
    accept_direct_delivery = models.BooleanField(default=True)
    allow_donor_collection = models.BooleanField(default=False)
    delivery_notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.food_bank.name}"


class FoodBankSupermarketPreference(TimestampMixin):
    class Supermarket(models.TextChoices):
        TESCO = "tesco", "Tesco"
        SAINSBURYS = "sainsburys", "Sainsburys"
        ASDA = "asda", "Asda"
        WAITROSE = "waitrose", "Waitrose"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food_bank = models.ForeignKey(
        FoodBank,
        on_delete=models.CASCADE,
        related_name="supermarket_preferences",
    )
    supermarket = models.CharField(max_length=20, choices=Supermarket.choices)
    enabled = models.BooleanField(default=True)
    delivery_time_days = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["food_bank", "supermarket"],
                name="unique_food_bank_supermarket",
            ),
        ]

    def __str__(self):
        return f"{self.get_supermarket_display()} for {self.food_bank.name}"


class QRScan(models.Model):
    class Source(models.TextChoices):
        QR_POSTER = "qr_poster", "QR Poster"
        QR_STICKER = "qr_sticker", "QR Sticker"
        QR_SOCIAL = "qr_social", "QR Social"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food_bank = models.ForeignKey(
        FoodBank,
        on_delete=models.CASCADE,
        related_name="qr_scans",
    )
    source = models.CharField(max_length=20, choices=Source.choices)
    scanned_at = models.DateTimeField(auto_now_add=True)
    converted_to_donation = models.BooleanField(default=False)
    donation = models.ForeignKey(
        "donations.Donation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="qr_scans",
    )

    def __str__(self):
        return f"QR Scan {self.pk}"
