from rest_framework import serializers
from .models import Event, EventRSVP


class EventRSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRSVP
        fields = ['id', 'event', 'name', 'email', 'phone', 'guests', 'notes', 'created_at']
        read_only_fields = ['id', 'event', 'created_at']


class EventSerializer(serializers.ModelSerializer):
    banner_url = serializers.SerializerMethodField()
    rsvp_count = serializers.ReadOnlyField()
    is_past = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date', 'location',
            'speaker_name', 'bible_verse', 'category', 'max_attendees',
            'is_featured', 'is_online', 'rsvp_required', 'banner', 'banner_url',
            'rsvp_count', 'is_past', 'created_at', 'updated_at',
        ]

    def get_banner_url(self, obj):
        request = self.context.get('request')
        if obj.banner:
            return request.build_absolute_uri(obj.banner.url) if request else obj.banner.url
        return None

    def validate(self, attrs):
        end_date = attrs.get('end_date', getattr(self.instance, 'end_date', None))
        start_date = attrs.get('start_date', getattr(self.instance, 'start_date', None))
        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError({'end_date': 'End date cannot be before start date.'})
        return attrs
