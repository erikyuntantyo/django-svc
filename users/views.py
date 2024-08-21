from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from utils.custom_api_view import CustomResponseAPIView

from .models import User
from .serializers import UserSerializer


class UserPagination(PageNumberPagination):
    page_size = settings.REST_FRAMEWORK.get('PAGE_SIZE', 10)


class UsersListView(ListCreateAPIView, CustomResponseAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination
    permission_classes = [IsAuthenticated]


class RegisterUserView(CreateAPIView, CustomResponseAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
