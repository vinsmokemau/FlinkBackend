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
            'created_at',
            'updated_at',
            'value',
        )

    def validate(self, data):
        if data.get('symbol', None):
            # Validate if the incoming symbol is a NYSE valid symbol.
            if not is_nyse_symbol(data["symbol"]):
                raise serializers.ValidationError(
                    "This symbol is'nt included in the NYSE"
                )
        return data

    def create(self, validated_data):
        # Extract the current value to make an initial list of market values.
        value = validated_data.pop("value")
        validated_data["market_values"] = [value]
        return Company.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("value", None):
            # Append the current value to the market values
            value = validated_data.pop("value")
            instance.market_values.append(value)

        for attr, value in validated_data.items():
            # Update instance with validated data
            setattr(instance, attr, value)
        instance.save()

        return instance


class CompanyChangeStatusSerializer(serializers.Serializer):
    """
    This serializer is used to get the active values and validate the attribute
    """

    is_active = serializers.BooleanField()
