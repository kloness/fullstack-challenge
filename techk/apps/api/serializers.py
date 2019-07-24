from rest_framework import serializers

from apps.base import models


class Category(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name')


class Book(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = (
            'id',
            'category_id',
            'title',
            'thumbnail_url',
            'price',
            'stock',
            'product_description',
            'upc',
        )
