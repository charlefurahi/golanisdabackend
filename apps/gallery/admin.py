from django.contrib import admin
from .models import Album, GalleryCategory, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'photo_count', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    inlines = [PhotoInline]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'album', 'caption', 'created_at')
    list_filter = ('album',)
