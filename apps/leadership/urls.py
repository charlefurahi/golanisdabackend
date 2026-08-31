from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LeadershipInquiryViewSet, LeadershipViewSet

router = DefaultRouter()
router.register(r'leaders', LeadershipViewSet, basename='leader')
router.register(r'inquiries', LeadershipInquiryViewSet, basename='leadership-inquiry')

urlpatterns = [
    path('', include(router.urls)),
]
