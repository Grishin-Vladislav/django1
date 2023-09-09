from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework import serializers


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=128)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def validate_password(self, value):
        return make_password(value)
