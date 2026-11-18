from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    # This allows the frontend to see the ministry name instead of just an ID
    ministry_name = serializers.ReadOnlyField(source='ministry.name')
    poster_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_poster_image_url(self, obj):
        request = self.context.get('request')
        if obj.poster_image:
            return request.build_absolute_uri(obj.poster_image.url) if request else obj.poster_image.url
        return None