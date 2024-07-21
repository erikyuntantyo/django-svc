from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class RegisterUserView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class ObtainAuthTokenView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = get_user_model().objects.get(email=email)

        if user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key})

        return Response({'error': 'Invalid credentials'}, status=400)
