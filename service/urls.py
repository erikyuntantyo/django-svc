from django.contrib import admin
from django.urls import include, path

from .views import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('v1/account/', include('account.urls')),
    path('v1/songs/', include('songs.urls')),
    path('v1/users/', include('users.urls')),
]
