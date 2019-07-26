from django.urls import path

from apps.api import views

app_name = 'api'

urlpatterns = [
    path('scraping', views.Scraping.as_view()),
    path('categories', views.Categories.as_view()),
    path('books', views.Books.as_view()),
    path('book/<int:book_id>', views.Book.as_view()),
]
