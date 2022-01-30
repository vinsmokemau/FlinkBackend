"""Circle serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from apps.companies.models import Company


class CompanyModelSerializer(serializers.ModelSerializer):
    """Company model serializer."""

    class Meta:
        """Meta class."""
        model = Company
        fields = (
            'name'
            'description'
            'symbol'
            'market_values'
        )
        read_only_fields = (
            'id',
        )

    # def validate(self, data):
        # raise serializers.ValidationError('Error')
        # return data
