from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from apps.common.permissions import IsAdminOrReadOnly

from .models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['priority', 'is_pinned', 'is_published']
    search_fields = ['title', 'content']
    ordering_fields = ['announcement_date', 'created_at', 'priority']

    def get_queryset(self):
        qs = Announcement.objects.all()
        user = self.request.user
        if not (user.is_authenticated and (user.is_staff or getattr(user, 'role', None) == 'admin')):
            qs = qs.filter(is_published=True)
        return qs.order_by('-is_pinned', '-announcement_date')
