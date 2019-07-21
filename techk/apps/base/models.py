from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "categories"


class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    thumbnail_url = models.URLField()
    price = models.CharField(max_length=20)
    stock = models.BooleanField()
    product_description = models.TextField()
    upc = models.CharField(max_length=50)
