from django.db import models
from django.utils import timezone


class Donation(models.Model):
    GIVING_TITHE = 'tithe'
    GIVING_OFFERING = 'offering'
    GIVING_CHURCH_DEVELOPMENT = 'church_development'
    GIVING_OTHER = 'other'
    GIVING_TYPE_CHOICES = [
        (GIVING_TITHE, 'Tithe'),
        (GIVING_OFFERING, 'Offering'),
        (GIVING_CHURCH_DEVELOPMENT, 'Church Development'),
        (GIVING_OTHER, 'Other'),
    ]

    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    giving_type = models.CharField(max_length=30, choices=GIVING_TYPE_CHOICES, default=GIVING_OFFERING)
    method = models.CharField(max_length=50, blank=True, null=True, help_text='e.g., Cash, PayPal, Stripe, M-Pesa')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        donor = f"{self.first_name or ''} {self.last_name or ''}".strip() or 'Anonymous'
        return f"{donor} - {self.amount} ({self.date.strftime('%Y-%m-%d')})"

    class Meta:
        ordering = ['-date']


class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    raised_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='donations/campaigns/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-is_active', '-created_at']
