from django.urls import path

from .views import RegisterUserView

urlpatterns = [
    path('create/', RegisterUserView.as_view(), name='create-user'),
]
