from rest_framework.serializers import (CharField, EmailField, ModelSerializer,
                                        Serializer, ValidationError)

from users.models import User


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
