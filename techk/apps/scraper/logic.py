# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
import requests
from timeit import default_timer as timer

from apps.base import models
from apps.base.models import reset_db

BASE_URL = 'http://books.toscrape.com/'


def get_page(url):
    content = requests.get(url).text
    return BeautifulSoup(content, 'html.parser')


def scrap_process():
    # delete books and categories for a fresh start
    reset_db()
    # get page object
    page = get_page(BASE_URL)
    # scrap categories
    start = timer()
    scrap_categories(page)
    end = timer()
    print('scrap categories: ' + str((end - start)) + ' seconds')


def scrap_categories(page):
    # get categories from the sidebar
    side_categories = page.select('.side_categories ul li ul li a')
    # save categories in database
    for side_category in side_categories:
        category_name = side_category.get_text().strip()
        models.Category.objects.get_or_create(name=category_name)
