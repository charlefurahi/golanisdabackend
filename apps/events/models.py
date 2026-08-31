from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True, help_text='Venue name or Google Maps link')
    speaker_name = models.CharField(max_length=255, blank=True, null=True)
    bible_verse = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    max_attendees = models.PositiveIntegerField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    rsvp_required = models.BooleanField(default=False)
    banner = models.ImageField(upload_to='events/banners/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.start_date.strftime('%Y-%m-%d')})"

    @property
    def rsvp_count(self):
        return self.rsvps.aggregate(total=models.Sum('guests'))['total'] or 0

    @property
    def is_past(self):
        return self.start_date < timezone.now()

    class Meta:
        ordering = ['start_date']


class EventRSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    guests = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} -> {self.event.title}"

    class Meta:
        ordering = ['-created_at']
