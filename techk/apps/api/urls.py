from django.urls import path

from apps.api import views

app_name = 'api'

urlpatterns = [
    path('scraping', views.Scraping.as_view()),
]
