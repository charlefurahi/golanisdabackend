from django.db import models


class GalleryCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Gallery Categories'


class Album(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='gallery/covers/', blank=True, null=True)
    category = models.ForeignKey(
        GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='albums'
    )
    date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def photo_count(self):
        return self.photos.count()

    class Meta:
        ordering = ['-date', '-created_at']


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='gallery/photos/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption or f"Photo #{self.pk} in {self.album.title}"

    class Meta:
        ordering = ['-created_at']
