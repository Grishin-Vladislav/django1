from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        request = self.context['request']
        """Метод для валидации. Вызывается при создании и обновлении."""
        if data.get('status') == 'OPEN' or request.method == "POST":
            count = 0
            for adv in request.user.advertisements.all():
                if adv.status == "OPEN":
                    count += 1
            if count > 10:
                raise ValidationError(
                    'Can\'t create more than 10 open posts, '
                    'delete or close some of your posts.'
                )
        return data
