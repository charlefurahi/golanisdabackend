from rest_framework import serializers
from .models import Album, GalleryCategory, Photo


class GalleryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryCategory
        fields = ['id', 'name', 'created_at']


class PhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'album', 'image', 'image_url', 'caption', 'created_at']
        extra_kwargs = {'image': {'write_only': True}}

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class AlbumSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()
    category_name = serializers.ReadOnlyField(source='category.name')
    photo_count = serializers.ReadOnlyField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = [
            'id', 'title', 'description', 'cover_image', 'cover_image_url',
            'category', 'category_name', 'date', 'photo_count', 'photos',
            'created_at', 'updated_at',
        ]

    def get_cover_image_url(self, obj):
        request = self.context.get('request')
        if obj.cover_image:
            return request.build_absolute_uri(obj.cover_image.url) if request else obj.cover_image.url
        return None
