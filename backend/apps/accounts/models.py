import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class FoodBankAdminManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class FoodBankAdmin(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food_bank = models.ForeignKey(
        "foodbanks.FoodBank",
        on_delete=models.CASCADE,
        related_name="admins",
    )
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = FoodBankAdminManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
