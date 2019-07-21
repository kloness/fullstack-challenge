# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
import requests

from apps.base import models

BASE_URL = 'http://books.toscrape.com/'


def get_page(url):
    content = requests.get(url).text
    return BeautifulSoup(content, 'html.parser')


def scrap_categories():
    # get page object
    page = get_page(BASE_URL)
    # get categories from the sidebar
    side_categories = page.select('.side_categories ul li ul li a')
    # save categories in database
    for side_category in side_categories:
        category_name = side_category.get_text().strip()
        models.Category.objects.get_or_create(name=category_name)
