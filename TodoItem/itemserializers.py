from rest_framework import serializers
from TodoItem.models import TodoItem

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ['id', 'title', 'description', 'status', 'assignee', 'created_at', 'last_modified']