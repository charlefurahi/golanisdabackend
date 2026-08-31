from rest_framework import serializers
from .models import Sermon
from apps.leadership.serializers import LeadershipSerializer


class SermonSerializer(serializers.ModelSerializer):
    speaker_details = LeadershipSerializer(source='speaker', read_only=True)
    audio_file_url = serializers.SerializerMethodField()
    pdf_transcript_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Sermon
        fields = [
            'id', 'title', 'speaker', 'speaker_details', 'description', 'scripture',
            'category', 'duration', 'video_url', 'audio_file', 'audio_file_url',
            'pdf_transcript', 'pdf_transcript_url', 'thumbnail', 'thumbnail_url',
            'preach_date', 'is_featured', 'is_published', 'created_at', 'updated_at',
        ]
        extra_kwargs = {
            'audio_file': {'write_only': True, 'required': False},
            'pdf_transcript': {'write_only': True, 'required': False},
            'thumbnail': {'write_only': True, 'required': False},
        }

    def _abs_url(self, field):
        if not field:
            return None
        request = self.context.get('request')
        return request.build_absolute_uri(field.url) if request else field.url

    def get_audio_file_url(self, obj):
        return self._abs_url(obj.audio_file)

    def get_pdf_transcript_url(self, obj):
        return self._abs_url(obj.pdf_transcript)

    def get_thumbnail_url(self, obj):
        return self._abs_url(obj.thumbnail)
