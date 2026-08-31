from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'ministry', 'start_date', 'end_date')
    list_filter = ('ministry', 'start_date')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')