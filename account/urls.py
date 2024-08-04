from django.urls import path

from .views import ObtainAuthTokenView, RegisterUserView, RefreshAuthTokenView

urlpatterns = [
    path('login/', ObtainAuthTokenView.as_view(), name='login'),
    path('signup/', RegisterUserView.as_view(), name='account-signup'),
    path('token/refresh/', RefreshAuthTokenView.as_view(), name='refresh-token')
]
