from rest_framework import serializers
from .models import Ministry


class SubMinistrySerializer(serializers.ModelSerializer):
    """Lightweight representation of a sub-ministry, nested under its parent.

    Deliberately excludes `sub_ministries` itself — nesting stops at one level,
    so this never recurses.
    """
    leader_name = serializers.ReadOnlyField(source='leader.full_name')
    poster_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Ministry
        fields = [
            'id', 'name', 'description', 'leader', 'leader_name',
            'poster_image', 'poster_image_url', 'created_at', 'updated_at',
        ]

    def get_poster_image_url(self, obj):
        if obj.poster_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.poster_image.url) if request else obj.poster_image.url
        return None


class MinistrySerializer(serializers.ModelSerializer):
    leader_name = serializers.ReadOnlyField(source='leader.full_name')
    leader_photo = serializers.SerializerMethodField()
    poster_image_url = serializers.SerializerMethodField()
    parent_name = serializers.ReadOnlyField(source='parent.name')
    sub_ministries = SubMinistrySerializer(many=True, read_only=True)

    class Meta:
        model = Ministry
        fields = [
            'id', 'name', 'description', 'leader', 'leader_name', 'leader_photo',
            'parent', 'parent_name', 'sub_ministries',
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

    def validate_parent(self, value):
        if value is None:
            return value
        if self.instance and value.pk == self.instance.pk:
            raise serializers.ValidationError('A ministry cannot be its own parent.')
        # Nesting is one level deep only: a ministry that is already a sub-ministry
        # (i.e. has its own parent) cannot be used as someone else's parent.
        if value.parent_id is not None:
            raise serializers.ValidationError(
                'This ministry is already a sub-ministry, so other ministries cannot be nested under it. '
                'Only a top-level ministry can be chosen as a parent.'
            )
        if self.instance and self.instance.sub_ministries.exists():
            raise serializers.ValidationError(
                'This ministry already has sub-ministries of its own, so it cannot become a sub-ministry itself.'
            )
        return value
