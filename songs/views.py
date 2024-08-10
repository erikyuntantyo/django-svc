from django.conf import settings
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from utils.response_utils import SuccessResponse

from .models import Song
from .serializers import SongSerializer


class SongPagination(PageNumberPagination):
    page_size = settings.REST_FRAMEWORK.get('PAGE_SIZE', 10)


class SongListView(ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    pagination_class = SongPagination
    permission_classes = [IsAuthenticated]


class SongDetailView(RetrieveUpdateDestroyAPIView, SuccessResponse):
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

        return self.success(serializer.data)
