from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import IsAdminOrReadOnly
from apps.leadership.models import Leadership
from apps.leadership.serializers import LeadershipSerializer

from .models import Sermon
from .serializers import SermonSerializer


class SermonViewSet(viewsets.ModelViewSet):
    serializer_class = SermonSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'speaker', 'is_featured', 'is_published']
    search_fields = ['title', 'description', 'scripture']
    ordering_fields = ['preach_date', 'created_at', 'title']

    def get_queryset(self):
        qs = Sermon.objects.all().select_related('speaker')
        user = self.request.user
        if not (user.is_authenticated and (user.is_staff or getattr(user, 'role', None) == 'admin')):
            qs = qs.filter(is_published=True)
        return qs

    @action(detail=False, methods=['get'])
    def featured(self, request):
        qs = self.filter_queryset(self.get_queryset().filter(is_featured=True))
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        cats = (
            Sermon.objects.exclude(category__isnull=True)
            .exclude(category__exact='')
            .values_list('category', flat=True)
            .distinct()
            .order_by('category')
        )
        return Response(list(cats))

    @action(detail=False, methods=['get'])
    def speakers(self, request):
        speakers = Leadership.objects.filter(sermons__isnull=False).distinct().order_by('full_name')
        serializer = LeadershipSerializer(speakers, many=True, context={'request': request})
        return Response(serializer.data)
