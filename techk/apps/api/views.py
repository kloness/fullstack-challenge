from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from timeit import default_timer as timer

from apps.base import models
from apps.base.models import reset_db
from apps.scraper.logic import scrap_categories


class Scraping(APIView):
    queryset = models.Category.objects.none()  # Required for DjangoModelPermissions

    def get(self, request):
        print('Scraping')
        # delete books and categories for a fresh start
        reset_db()
        # scrap categories
        start = timer()
        scrap_categories()
        end = timer()
        print('scrap categories: ' + str((end - start)) + ' seconds')
        return Response({}, status=status.HTTP_200_OK)
