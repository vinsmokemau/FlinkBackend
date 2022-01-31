"""Company model."""

# Django
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Utilities
import uuid
from apps.utils.models import BaseModel


class Company(BaseModel):
    """Company model
    ."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    market_values = ArrayField(
        models.DecimalField(max_digits=19, decimal_places=2),
        blank=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
