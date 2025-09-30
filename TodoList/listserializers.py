from rest_framework import serializers
from TodoList.models import TodoList
from TodoItem.models import TodoItem

class ListSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(
        many=True, queryset=TodoItem.objects.all()
    )
    class Meta:
        model = TodoList
        fields = ['id', 'owner', 'items', 'created_at', 'last_modified']