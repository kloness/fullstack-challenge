from django.contrib import admin
from apps.base import models

admin.site.register(models.Category)
admin.site.register(models.Book)
