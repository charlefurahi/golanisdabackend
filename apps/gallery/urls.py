from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AlbumViewSet, GalleryCategoryViewSet, PhotoViewSet

router = DefaultRouter()
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'categories', GalleryCategoryViewSet, basename='gallery-category')
router.register(r'photos', PhotoViewSet, basename='photo')

urlpatterns = [
    path('', include(router.urls)),
]
