from django.db.models import Sum, Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import IsAdminOnly, IsAdminOrReadOnly

from .models import Campaign, Donation
from .serializers import CampaignSerializer, DonationSerializer


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['giving_type', 'method']
    search_fields = ['first_name', 'last_name', 'email', 'transaction_id']
    ordering_fields = ['date', 'amount']

    def get_permissions(self):
        # Anyone can submit a donation or verify a transaction; only admins can
        # view/list/edit donor records.
        if self.action in ('create', 'verify'):
            return [permissions.AllowAny()]
        return [IsAdminOnly()]

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOnly])
    def stats(self, request):
        qs = self.get_queryset()
        total = qs.aggregate(total=Sum('amount'), count=Count('id'))
        this_month = qs.filter(
            date__year=timezone.now().year, date__month=timezone.now().month
        ).aggregate(total=Sum('amount'), count=Count('id'))
        by_type = list(
            qs.values('giving_type').annotate(total=Sum('amount'), count=Count('id')).order_by('-total')
        )
        return Response({
            'total_amount': total['total'] or 0,
            'total_count': total['count'] or 0,
            'this_month_amount': this_month['total'] or 0,
            'this_month_count': this_month['count'] or 0,
            'by_giving_type': by_type,
        })

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def verify(self, request):
        transaction_id = request.data.get('transaction_id')
        if not transaction_id:
            return Response({'transaction_id': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

        donation = Donation.objects.filter(transaction_id=transaction_id).first()
        if donation:
            return Response({'verified': True, 'donation': DonationSerializer(donation).data})
        return Response({'verified': False, 'detail': 'No donation found with that transaction ID.'})


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'goal_amount', 'raised_amount']
