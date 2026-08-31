from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.pagination import StandardResultsPagination
from apps.common.permissions import IsAdminOnly

from .models import ContactMessage, NewsletterSubscriber
from .serializers import (
    ContactAdminSerializer,
    ContactMessageSerializer,
    NewsletterSubscriberSerializer,
)


class ContactMessageCreateView(generics.CreateAPIView):
    """Public endpoint — anyone can submit a contact / prayer request message."""

    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]


class ContactAdminListView(generics.ListAPIView):
    """Admin-only inbox of contact messages."""

    queryset = ContactMessage.objects.all()
    serializer_class = ContactAdminSerializer
    permission_classes = [IsAdminOnly]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_read', 'is_prayer_request']
    search_fields = ['first_name', 'last_name', 'email', 'subject', 'message']
    ordering_fields = ['created_at']


class ContactAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactAdminSerializer
    permission_classes = [IsAdminOnly]


class NewsletterSubscribeView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = (request.data.get('email') or '').strip().lower()
        if not email:
            return Response({'email': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.unsubscribed_at = None
            subscriber.save()

        return Response(
            NewsletterSubscriberSerializer(subscriber).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class NewsletterUnsubscribeView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = (request.data.get('email') or '').strip().lower()
        try:
            subscriber = NewsletterSubscriber.objects.get(email=email)
        except NewsletterSubscriber.DoesNotExist:
            return Response({'detail': 'No such subscription.'}, status=status.HTTP_404_NOT_FOUND)

        subscriber.is_active = False
        subscriber.unsubscribed_at = timezone.now()
        subscriber.save()
        return Response({'detail': 'Unsubscribed successfully.'}, status=status.HTTP_200_OK)
