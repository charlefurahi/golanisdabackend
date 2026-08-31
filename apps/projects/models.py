from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # Linking to the Ministry model
    ministry = models.ForeignKey(
        'ministries.Ministry', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='projects'
    )
    poster_image = models.ImageField(upload_to='projects/posters/', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_date']