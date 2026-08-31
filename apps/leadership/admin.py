from django.contrib import admin
from .models import Leadership, LeadershipInquiry


@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role_title', 'role', 'order', 'is_active', 'created_at')
    search_fields = ('full_name', 'role_title', 'bio')
    list_filter = ('role', 'is_active')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(LeadershipInquiry)
class LeadershipInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'leader', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'message')
