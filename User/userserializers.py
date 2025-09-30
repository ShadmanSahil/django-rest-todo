from rest_framework import serializers
from User.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'first_name', 'last_name', 'birthday', 'is_active', 'user_type', 'created_at', 'last_modified'] # is everything included?