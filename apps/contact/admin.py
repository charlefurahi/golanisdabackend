from django.contrib import admin
from .models import ContactMessage, NewsletterSubscriber


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject', 'is_prayer_request', 'is_read', 'created_at')
    readonly_fields = ('created_at',)
    list_filter = ('is_read', 'is_prayer_request')
    search_fields = ('first_name', 'last_name', 'email', 'message')


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active',)
    search_fields = ('email',)
