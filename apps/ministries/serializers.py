from rest_framework import serializers
from .models import Ministry


class MinistrySerializer(serializers.ModelSerializer):
    leader_name = serializers.ReadOnlyField(source='leader.full_name')
    leader_photo = serializers.SerializerMethodField()
    poster_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Ministry
        fields = [
            'id', 'name', 'description', 'leader', 'leader_name', 'leader_photo',
            'poster_image', 'poster_image_url', 'created_at', 'updated_at',
        ]

    def get_leader_photo(self, obj):
        if obj.leader and obj.leader.photo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.leader.photo.url) if request else obj.leader.photo.url
        return None

    def get_poster_image_url(self, obj):
        if obj.poster_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.poster_image.url) if request else obj.poster_image.url
        return None
