import math

from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from apps.api import serializers
from apps.base import models
from apps.scraper.logic import scrape_process


class Scraping(APIView):
    # it doesn't ask for permission for now so we can quickly try it
    # http://0.0.0.0:8000/api/scraping
    queryset = models.Category.objects.none()  # Required for DjangoModelPermissions

    def get(self, request):
        print('Scraping')
        scrape_process()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class Categories(ListAPIView):
    serializer_class = serializers.Category

    def get_queryset(self):
        return models.Category.objects.all()


class Books(ListAPIView):
    total_pages = 1
    serializer_class = serializers.Book

    def get_queryset(self):
        queryset = models.Book.objects.all()

        # filter by category
        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            queryset = queryset.filter(category=category_id)

        # filter by search
        search = self.request.query_params.get('search', None)
        if search is not None:
            search = search.strip()
            if search:
                query = Q()
                for term in search.split():
                    query &= (
                        Q(title__icontains=term) |
                        Q(upc__icontains=term)
                    )
                queryset = queryset.filter(query)

        # pagination
        start = self.request.query_params.get('start', None)
        length = self.request.query_params.get('length', None)
        if start is not None and length is not None:
            start = int(start)
            length = int(length)
            if length < 1:
                length = 1
            self.total_pages = math.ceil(queryset.count() / length)
            queryset = queryset[start:start + length]

        return queryset

    def list(self, request, *args, **kwargs):
        # get books
        books_queryset = self.get_queryset()
        books = self.serializer_class(books_queryset, many=True).data
        # response
        data = {
            'total_pages': self.total_pages,
            'books': books
        }
        return Response(data)
