from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from utils.response_utils import ErrorResponse, SuccessResponse

from .models import RefreshToken
from .serializers import (LoginSerializer, RefreshTokenSerializer,
                          RegisterSerializer)


class RegisterUserView(APIView, SuccessResponse, ErrorResponse):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return self.created(serializer.data)

        return self.bad_request_error(serializer.errors)


class ObtainAuthTokenView(APIView, SuccessResponse, ErrorResponse):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']

            try:
                Token.objects.filter(user=user).delete()

                token, _ = Token.objects.get_or_create(user=user)
                refresh_token = RefreshToken.objects.create(user=user)
            except Exception as e:
                return self.internal_server_error(exception=e)

            return self.created({
                'userId': user._id,
                'token': token.key,
                'refreshToken': refresh_token.token
            })

        return self.bad_request_error(
            message='Invalid user and password.',
            errors=serializer.errors)


class RefreshAuthTokenView(APIView, SuccessResponse, ErrorResponse):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RefreshTokenSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RefreshTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)

            return self.success({'token': token.key})

        return self.bad_request_error(serializer.errors)
