"""Circle views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Serializers
from apps.companies.serializers import CompanyModelSerializer

# Models
from apps.companies.models import Company


class CompanyViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """Company viewset."""

    serializer_class = CompanyModelSerializer

    # Filters
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('uuid', 'name', 'symbol')
    ordering_fields = ('name', 'created')
    ordering = ('name')
    filter_fields = ('symbol')

    def get_queryset(self):
        """Get the objects we want in the request.
        If in the future we want filters or segmentations we can do it here."""
        queryset = Company.objects.all()
        return queryset
