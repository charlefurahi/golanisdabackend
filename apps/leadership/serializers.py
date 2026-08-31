from rest_framework import serializers
from .models import Leadership, LeadershipInquiry


class LeadershipSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Leadership
        fields = [
            'id', 'full_name', 'role', 'role_title', 'bio', 'email', 'phone',
            'order', 'is_active', 'photo', 'photo_url', 'social_links',
            'created_at', 'updated_at',
        ]

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.photo:
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url
        return None


class LeadershipInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadershipInquiry
        fields = ['id', 'name', 'email', 'phone', 'message', 'leader', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        # Public submissions can never set is_read themselves.
        validated_data.pop('is_read', None)
        return super().create(validated_data)
