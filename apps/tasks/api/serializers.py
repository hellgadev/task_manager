from rest_framework import serializers
from rest_framework.serializers import ALL_FIELDS

from apps.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ALL_FIELDS
        model = Task

    def create(self, validated_data):
        if self.context['request'].user.is_authenticated:
            validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
