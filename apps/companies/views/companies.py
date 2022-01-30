"""Circle views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Serializers
from apps.companies.serializers import CompanyModelSerializer

# Models
from apps.companies.models import Company


class CompanyViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """Company view set."""

    serializer_class = CompanyModelSerializer

    def get_queryset(self):
        """Get the objects we want in the request.
        If in the future we want filters or segmentations we can do it here."""
        queryset = Company.objects.all()
        return queryset
