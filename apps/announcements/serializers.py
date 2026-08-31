from rest_framework import serializers
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    poster_image = serializers.ImageField(required=False, allow_null=True, use_url=True)
    pdf_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'announcement_date', 'expire_date',
            'priority', 'is_pinned', 'is_published', 'poster_image',
            'pdf_file', 'pdf_file_url', 'created_at', 'updated_at',
        ]
        extra_kwargs = {'pdf_file': {'write_only': True, 'required': False}}

    def get_pdf_file_url(self, obj):
        request = self.context.get('request')
        if obj.pdf_file:
            return request.build_absolute_uri(obj.pdf_file.url) if request else obj.pdf_file.url
        return None
