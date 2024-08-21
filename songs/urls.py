from django.urls import path

from .views import SongDetailView, SongsListView

urlpatterns = [
    path('', SongsListView.as_view(), name='song-list'),
    path('<int:pk>', SongDetailView.as_view(), name='song-detail'),
]
