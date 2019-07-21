from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from apps.base import models
from apps.scraper.logic import scrap_process


class Scraping(APIView):
    # it doesn't ask for permission for now so we can quickly try it
    # http://0.0.0.0:8000/api/scraping
    queryset = models.Category.objects.none()  # Required for DjangoModelPermissions

    def get(self, request):
        print('Scraping')
        scrap_process()
        return Response(status=status.HTTP_200_OK)
