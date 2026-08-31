from django.db import models


class Leadership(models.Model):
    ROLE_PASTOR = 'pastor'
    ROLE_ELDER = 'elder'
    ROLE_DEACON = 'deacon'
    ROLE_YOUTH_LEADER = 'youth_leader'
    ROLE_OTHER = 'other'
    ROLE_CHOICES = [
        (ROLE_PASTOR, 'Pastor'),
        (ROLE_ELDER, 'Elder'),
        (ROLE_DEACON, 'Deacon'),
        (ROLE_YOUTH_LEADER, 'Youth Leader'),
        (ROLE_OTHER, 'Other'),
    ]

    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=ROLE_OTHER)
    role_title = models.CharField(max_length=255, help_text='e.g., Senior Pastor, Head Elder')
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text='Manual sort order, lower shows first')
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='leadership/profiles/', blank=True, null=True)
    social_links = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.role_title}"

    class Meta:
        verbose_name_plural = 'Leadership'
        ordering = ['order', 'full_name']


class LeadershipInquiry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True, null=True)
    message = models.TextField()
    leader = models.ForeignKey(
        Leadership, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries'
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Leadership Inquiries'
