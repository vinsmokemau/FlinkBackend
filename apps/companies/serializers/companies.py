"""Company serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from apps.companies.models import Company

# Utilities
from apps.companies.utils import is_nyse_symbol


class CompanyModelSerializer(serializers.ModelSerializer):
    """Company model serializer."""

    value = serializers.DecimalField(
        max_digits=19,
        decimal_places=2,
        min_value=0.00,
        write_only=True,
    )
    market_values = serializers.ListField(
        child=serializers.DecimalField(
            max_digits=19,
            decimal_places=2,
            min_value=0.00,
        ),
        read_only=True,
    )
    is_active = serializers.BooleanField(
        read_only=True,
    )
    created_at = serializers.DateTimeField(
        read_only=True,
    )
    updated_at = serializers.DateTimeField(
        read_only=True,
    )

    class Meta:
        """Meta class."""
        model = Company
        fields = (
            'id',
            'name',
            'description',
            'symbol',
            'market_values',
            'is_active',
            'created_at',
            'updated_at',
            'value',
        )

    def validate(self, data):
        if data.get('symbol', None):
            if not is_nyse_symbol(data["symbol"]):
                raise serializers.ValidationError(
                    "This symbol is'nt included in the NYSE"
                )
        return data

    def create(self, validated_data):
        value = validated_data.pop("value")
        validated_data["market_values"] = [value]
        return Company.objects.create(**validated_data)
