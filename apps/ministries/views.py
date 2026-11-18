from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import IsAdminOrReadOnly

from .models import Ministry
from .serializers import MinistrySerializer


class MinistryViewSet(viewsets.ModelViewSet):
    queryset = Ministry.objects.all().select_related('leader', 'parent').prefetch_related('sub_ministries')
    serializer_class = MinistrySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['leader', 'parent']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    @action(detail=False, methods=['get'], url_path='top_level')
    def top_level(self, request):
        """Major ministries only, each with its sub_ministries nested inline.

        Handy for both the public Ministries page and the admin panel, which
        both want the grouped major/sub view rather than one flat list.
        """
        qs = self.filter_queryset(self.get_queryset().filter(parent__isnull=True))
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page if page is not None else qs, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)
