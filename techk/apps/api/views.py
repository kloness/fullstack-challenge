from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from apps.base import models
from apps.scraper.logic import scrap_process


class Scraping(APIView):
    queryset = models.Category.objects.none()  # Required for DjangoModelPermissions

    def get(self, request):
        print('Scraping')
        scrap_process()
        return Response(status=status.HTTP_200_OK)
