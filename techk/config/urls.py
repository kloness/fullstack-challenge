"""techk URL Configuration"""
from django.urls import path, include
from django.contrib import admin
from apps.base.views import index


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('apps.api.urls')),
    path('', include('apps.frontend.urls')),
]
