from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from apps.common.permissions import IsAdminOrReadOnly

from .models import Album, GalleryCategory, Photo
from .serializers import AlbumSerializer, GalleryCategorySerializer, PhotoSerializer


class GalleryCategoryViewSet(viewsets.ModelViewSet):
    queryset = GalleryCategory.objects.all()
    serializer_class = GalleryCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name']


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all().prefetch_related('photos')
    serializer_class = AlbumSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'created_at']


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['album']

    @action(detail=False, methods=['post'], url_path='bulk')
    def bulk(self, request):
        album_id = request.data.get('album')
        if not album_id:
            return Response({'album': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            album = Album.objects.get(pk=album_id)
        except Album.DoesNotExist:
            return Response({'album': ['Album not found.']}, status=status.HTTP_404_NOT_FOUND)

        files = request.FILES.getlist('images') or request.FILES.getlist('photos')
        if not files:
            return Response({'images': ['At least one file is required.']}, status=status.HTTP_400_BAD_REQUEST)

        created = [Photo.objects.create(album=album, image=f) for f in files]
        serializer = PhotoSerializer(created, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
