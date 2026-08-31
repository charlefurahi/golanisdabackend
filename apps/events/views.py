from django.db.models import Sum
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import IsAdminOnly, IsAdminOrReadOnly

from .models import Event, EventRSVP
from .serializers import EventRSVPSerializer, EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured', 'is_online', 'rsvp_required']
    search_fields = ['title', 'description', 'location', 'speaker_name']
    ordering_fields = ['start_date', 'created_at']

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        qs = self.filter_queryset(self.get_queryset().filter(start_date__gte=timezone.now()).order_by('start_date'))
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page if page is not None else qs, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='all_events')
    def all_events(self, request):
        qs = self.filter_queryset(self.get_queryset().order_by('start_date'))
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def past(self, request):
        qs = self.filter_queryset(self.get_queryset().filter(start_date__lt=timezone.now()).order_by('-start_date'))
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page if page is not None else qs, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        qs = self.filter_queryset(self.get_queryset().filter(is_featured=True).order_by('start_date'))
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        cats = (
            Event.objects.exclude(category__isnull=True)
            .exclude(category__exact='')
            .values_list('category', flat=True)
            .distinct()
            .order_by('category')
        )
        return Response(list(cats))

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def rsvp(self, request, pk=None):
        event = self.get_object()
        serializer = EventRSVPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        guests = serializer.validated_data.get('guests', 1)
        if event.max_attendees is not None:
            current = event.rsvps.aggregate(total=Sum('guests'))['total'] or 0
            if current + guests > event.max_attendees:
                return Response(
                    {'detail': 'This event is full.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer.save(event=event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], permission_classes=[IsAdminOnly])
    def rsvps(self, request, pk=None):
        event = self.get_object()
        qs = event.rsvps.all().order_by('-created_at')
        page = self.paginate_queryset(qs)
        serializer = EventRSVPSerializer(page if page is not None else qs, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)
