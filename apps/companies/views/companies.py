"""Company views."""

# Django REST Framework
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Serializers
from apps.companies.serializers import (
    CompanyModelSerializer,
    CompanyChangeStatusSerializer,
)

# Models
from apps.companies.models import Company


class CompanyViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """Company viewset."""

    serializer_class = CompanyModelSerializer
    lookup_field = 'id'

    # Filters
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('id', 'name', 'symbol')
    ordering_fields = ('name', 'created')
    ordering = ('name',)
    filter_fields = ('symbol',)

    def get_queryset(self):
        """Restrict list to active-only."""
        queryset = Company.objects.all()
        if self.action == 'list':
            return queryset.filter(is_active=True)
        return queryset

    @action(detail=True, methods=['patch'])
    def change_status(self, request, id=None):
        company = self.get_object()
        serializer = CompanyChangeStatusSerializer(data=request.data)
        if serializer.is_valid():
            company.is_active = request.data['is_active']
            company.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
