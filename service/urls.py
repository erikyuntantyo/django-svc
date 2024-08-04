from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/account/', include('account.urls')),
    path('v1/songs/', include('songs.urls')),
    path('v1/users/', include('users.urls')),
]
