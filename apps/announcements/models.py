from django.db import models


class Announcement(models.Model):
    PRIORITY_LOW = 'low'
    PRIORITY_NORMAL = 'normal'
    PRIORITY_HIGH = 'high'
    PRIORITY_URGENT = 'urgent'
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_NORMAL, 'Normal'),
        (PRIORITY_HIGH, 'High'),
        (PRIORITY_URGENT, 'Urgent'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    announcement_date = models.DateField()
    expire_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_NORMAL)
    is_pinned = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    poster_image = models.ImageField(upload_to='announcements/posters/', null=True, blank=True)
    pdf_file = models.FileField(upload_to='announcements/pdfs/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-is_pinned', '-announcement_date']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
