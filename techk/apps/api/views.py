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
        return Response(status=status.HTTP_200_OK)


class Categories(APIView):
    queryset = models.Category.objects.all()

    def get(self, request):
        categories = models.Category.objects.all()
        serializer = serializers.Category(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
