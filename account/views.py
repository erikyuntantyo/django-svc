from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_400_BAD_REQUEST,
                                   HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.views import APIView

from .models import RefreshToken
from .serializers import (LoginSerializer, RefreshTokenSerializer,
                          RegisterSerializer)


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ObtainAuthTokenView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']

            try:
                token, _ = Token.objects.get_or_create(user=user)
                refresh_token = RefreshToken.objects.create(user=user)
            except Exception as e:
                return Response({'detail': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                'userId': user._id,
                'token': token.key,
                'refreshToken': refresh_token.token
            })

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class RefreshAuthTokenView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RefreshTokenSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RefreshTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key})

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
