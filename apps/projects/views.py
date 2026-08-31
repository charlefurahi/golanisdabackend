from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from apps.common.permissions import IsAdminOrReadOnly

from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ministry']
    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'created_at']
