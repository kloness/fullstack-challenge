from django.db import models


def reset_db():
    Category.objects.all().delete()
    Book.objects.all().delete()


class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    thumbnail_url = models.URLField()
    price = models.CharField(max_length=20)
    stock = models.BooleanField()
    product_description = models.TextField()
    upc = models.CharField(max_length=50)
