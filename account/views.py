from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated

from custom_auth.models import ExpiringToken
from utils.custom_api_view import CustomResponseAPIView
from utils.custom_response import (CreatedResponse,
                                   InternalServerErrorException,
                                   SuccessResponse, UnauthorizedException)

from .models import RefreshToken
from .serializers import (LoginSerializer, RefreshTokenSerializer,
                          RegisterSerializer)


class RegisterUserView(CustomResponseAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return CreatedResponse(serializer.data)

        raise ValidationError(serializer.errors)


class ObtainAuthTokenView(CustomResponseAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']

            try:
                old_token = ExpiringToken.objects.get(user=user)
                old_refresh_token = RefreshToken.objects.get(user=user)

                old_token.delete()
                old_refresh_token.delete()
            except Exception:
                pass

            token, _ = ExpiringToken.objects.get_or_create(user=user)
            refresh_token = RefreshToken.objects.create(user=user)

            return SuccessResponse({
                'userId': user._id,
                'token': token.key,
                'refreshToken': refresh_token.token
            })

        raise ValidationError('Invalid user and password.')


class RefreshAuthTokenView(CustomResponseAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RefreshTokenSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RefreshTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            ExpiringToken.objects.filter(user=user).delete()
            token, _ = ExpiringToken.objects.get_or_create(user=user)

            return SuccessResponse({'token': token.key})

        raise ValidationError(serializer.errors)


class RevokeTokenView(CustomResponseAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = ExpiringToken.objects.get(user=request.user)
            refresh_token = RefreshToken.objects.get(user=request.user)

            token.delete()
            refresh_token.delete()

            return SuccessResponse({'message': 'Successfully logged out.'})
        except ExpiringToken.DoesNotExist:
            raise UnauthorizedException("Invalid token or user not logged in.")
        except Exception as e:
            raise InternalServerErrorException(e)
