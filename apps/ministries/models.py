from django.db import models

class Ministry(models.Model):
    name = models.CharField(max_length=255, help_text="e.g., Youth, Music, Health")
    description = models.TextField(blank=True, null=True)
    # Linking to the Leadership model from the leadership app
    leader = models.ForeignKey(
        'leadership.Leadership', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='ministries_led'
    )
    # A sub-ministry (e.g. "Youth Choir") belongs to a major ministry (e.g. "Youth").
    # SET_NULL so deleting a major ministry doesn't delete its sub-ministries —
    # they just become top-level, matching how `leader` is handled above.
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_ministries',
        help_text='Leave blank for a major ministry. Set this to nest it under another ministry.',
    )
    poster_image = models.ImageField(upload_to='ministries/posters/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Ministries"
        ordering = ['name']