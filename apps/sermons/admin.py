from django.contrib import admin
from .models import Sermon


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'category', 'preach_date', 'is_featured', 'is_published')
    list_filter = ('speaker', 'category', 'is_featured', 'is_published', 'preach_date')
    search_fields = ('title', 'description', 'scripture')
