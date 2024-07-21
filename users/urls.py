from django.urls import path

from .views import ObtainAuthTokenView, RegisterUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('token/', ObtainAuthTokenView.as_view(), name='token'),
]
