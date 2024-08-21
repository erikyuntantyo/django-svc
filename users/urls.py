from django.urls import path

from .views import RegisterUserView, UsersListView

urlpatterns = [
    path('', UsersListView.as_view(), name='users-list'),
    path('create', RegisterUserView.as_view(), name='create-user'),
]
