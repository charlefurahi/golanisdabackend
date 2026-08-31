from django.db import models


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    is_prayer_request = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.first_name} {self.last_name} - {self.subject or 'No Subject'}"

    class Meta:
        ordering = ['-created_at']


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-subscribed_at']
