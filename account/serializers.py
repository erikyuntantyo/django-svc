from django.utils import timezone
from rest_framework.serializers import (CharField, EmailField, ModelSerializer,
                                        Serializer, UUIDField, ValidationError)

from users.models import User

from .models import RefreshToken


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user


class LoginSerializer(Serializer):
    email = EmailField()
    password = CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError('Invalid credentials')

            if not user.check_password(password):
                raise ValidationError('Invalid credentials')
        else:
            raise ValidationError('Both "email" and "password" are required')

        data['user'] = user

        return data


class RefreshTokenSerializer(Serializer):
    refreshToken = CharField(required=True)

    def validate(self, data):
        refresh_token = data.get('refreshToken')

        if not refresh_token:
            raise ValidationError('Refresh token is required')

        try:
            token = RefreshToken.objects.get(
                token=refresh_token, expires_at__gt=timezone.now())
        except RefreshToken.DoesNotExist:
            raise ValidationError(
                'Invalid or expired refresh token')

        data['user'] = token.user

        return data
