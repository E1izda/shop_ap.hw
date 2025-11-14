from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )
        user.generate_confirmation_code()
        return user


class ConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self,  username):
        try:
            user = User.objects.get(email=username['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        if user.confirmation_code != username['code']:
            raise serializers.ValidationError("Неверный код подтверждения")

        username['user'] = user
        return username

    def save(self):
        user = self.validated_data['user']
        user.is_active = True
        user.confirmation_code = None
        user.save()
        return user
