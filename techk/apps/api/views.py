from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from apps.base import models
from apps.base.models import reset_db


class Scraping(APIView):
    queryset = models.Category.objects.none()  # Required for DjangoModelPermissions

    def get(self, request):
        print('Scraping')
        # delete books and categories for a fresh start
        reset_db()
        return Response({}, status=status.HTTP_200_OK)
