from rest_framework import serializers
from .models import ContactMessage, NewsletterSubscriber


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'subject',
            'message', 'is_prayer_request', 'is_read', 'created_at',
        ]
        read_only_fields = ['id', 'is_read', 'created_at']


class ContactAdminSerializer(ContactMessageSerializer):
    class Meta(ContactMessageSerializer.Meta):
        read_only_fields = ['id', 'created_at']


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['id', 'email', 'is_active', 'subscribed_at']
        read_only_fields = ['id', 'is_active', 'subscribed_at']
