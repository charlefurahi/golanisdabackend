from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from apps.common.permissions import IsAdminOrReadOnly

from .models import Ministry
from .serializers import MinistrySerializer


class MinistryViewSet(viewsets.ModelViewSet):
    queryset = Ministry.objects.all()
    serializer_class = MinistrySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['leader']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
