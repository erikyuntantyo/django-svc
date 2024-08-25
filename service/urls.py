from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Service API",
        default_version='v1',
        description="Django Rest Framework example",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="erik.yuntantyo@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin', admin.site.urls),
    path('docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('v1/account/', include('account.urls')),
    re_path(r'v1/songs/?', include('songs.urls')),
    re_path(r'v1/users/?', include('users.urls')),
]
