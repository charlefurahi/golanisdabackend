from django.contrib import admin
from .models import Campaign, Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'amount', 'giving_type', 'method', 'date')
    list_filter = ('giving_type', 'method', 'date')
    search_fields = ('first_name', 'last_name', 'email', 'transaction_id', 'message')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'goal_amount', 'raised_amount', 'is_active', 'start_date', 'end_date')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
