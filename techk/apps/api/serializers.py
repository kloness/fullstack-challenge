from rest_framework import serializers

from apps.base import models


class Category(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name')
