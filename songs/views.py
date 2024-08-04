from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Song
from .serializers import SongSerializer


class SongPagination(PageNumberPagination):
    page_size = settings.REST_FRAMEWORK.get('PAGE_SIZE', 10)


class SongListView(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    pagination_class = SongPagination
    permission_classes = [IsAuthenticated]


class SongDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete']

    def patch(self, request, *args, **kwargs):
        partial = True

        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=partial
        )

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(serializer.data)
