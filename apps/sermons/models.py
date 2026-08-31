from django.db import models


class Sermon(models.Model):
    title = models.CharField(max_length=255)
    speaker = models.ForeignKey(
        'leadership.Leadership',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sermons',
    )
    description = models.TextField(blank=True, null=True)
    scripture = models.CharField(max_length=255, blank=True, null=True, help_text='e.g. John 3:16-21')
    category = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True, help_text='e.g. 45 min')
    video_url = models.URLField(blank=True, null=True, help_text='YouTube or Vimeo URL')
    audio_file = models.FileField(upload_to='sermons/audio/', blank=True, null=True)
    pdf_transcript = models.FileField(upload_to='sermons/pdf/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='sermons/thumbnails/', blank=True, null=True)
    preach_date = models.DateTimeField()
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.speaker.full_name if self.speaker else 'Unknown Speaker'}"

    class Meta:
        ordering = ['-preach_date']
