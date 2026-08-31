from django.contrib import admin
from .models import Event, EventRSVP


class EventRSVPInline(admin.TabularInline):
    model = EventRSVP
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'location', 'category', 'is_featured', 'rsvp_required')
    list_filter = ('is_featured', 'is_online', 'rsvp_required', 'category', 'start_date')
    search_fields = ('title', 'description', 'location', 'speaker_name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [EventRSVPInline]


@admin.register(EventRSVP)
class EventRSVPAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'guests', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('event',)
