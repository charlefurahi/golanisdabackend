from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    # This allows the frontend to see the ministry name instead of just an ID
    ministry_name = serializers.ReadOnlyField(source='ministry.name')

    class Meta:
        model = Project
        fields = '__all__'