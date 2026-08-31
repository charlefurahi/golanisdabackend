from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'announcement_date', 'priority', 'is_pinned', 'is_published', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('priority', 'is_pinned', 'is_published', 'announcement_date')
