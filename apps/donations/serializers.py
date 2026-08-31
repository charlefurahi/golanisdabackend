from rest_framework import serializers
from .models import Campaign, Donation


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'amount',
            'giving_type', 'method', 'transaction_id', 'date', 'message',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CampaignSerializer(serializers.ModelSerializer):
    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            'id', 'title', 'description', 'goal_amount', 'raised_amount',
            'progress_percent', 'is_active', 'start_date', 'end_date',
            'image', 'created_at', 'updated_at',
        ]

    def get_progress_percent(self, obj):
        if not obj.goal_amount:
            return 0
        return round(float(obj.raised_amount) / float(obj.goal_amount) * 100, 1)
