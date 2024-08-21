from django.urls import path

from .views import (ObtainAuthTokenView, RefreshAuthTokenView,
                    RegisterUserView, RevokeTokenView)

urlpatterns = [
    path('login', ObtainAuthTokenView.as_view(), name='login'),
    path('signup', RegisterUserView.as_view(), name='account-signup'),
    path('token/refresh', RefreshAuthTokenView.as_view(), name='refresh-token'),
    path('token/revoke', RevokeTokenView.as_view(), name='revoke-token'),
]
