from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets

from apps.common.pagination import StandardResultsPagination
from apps.common.permissions import IsAdminOnly, IsAdminOrReadOnly

from .models import Leadership, LeadershipInquiry
from .serializers import LeadershipInquirySerializer, LeadershipSerializer


class LeadershipViewSet(viewsets.ModelViewSet):
    queryset = Leadership.objects.all()
    serializer_class = LeadershipSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['full_name', 'role_title', 'bio']
    ordering_fields = ['order', 'full_name', 'created_at']


class LeadershipInquiryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = LeadershipInquiry.objects.all()
    serializer_class = LeadershipInquirySerializer
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_read', 'leader']
    search_fields = ['name', 'email', 'message']
    ordering_fields = ['created_at']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [IsAdminOnly()]
