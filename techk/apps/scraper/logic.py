# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
import requests
from timeit import default_timer as timer
import re

from apps.base import models
from apps.base.models import reset_db

BASE_URL = 'http://books.toscrape.com/'


def get_page(url):
    req = requests.get(url)
    req.encoding = 'utf-8'  # the default is ISO-8859-1 and has problems with some characters
    return BeautifulSoup(req.text, 'html.parser')


def scrap_process():
    # delete books and categories for a fresh start
    reset_db()
    # get home page object
    page = get_page(BASE_URL)
    # scrap categories
    start = timer()
    scrap_categories(page)
    end = timer()
    print(f'scrap categories: {end - start} seconds')
    # get number of pages
    number_of_pages = scrap_total_pages(page)
    # scrap each page
    start = timer()
    scrap_each_page(number_of_pages)  # 579 s for 1.000 books without running in parallel
    end = timer()
    print(f'scrap books: {end - start} seconds')


def scrap_categories(page):
    # get categories from the sidebar
    side_categories = page.select('.side_categories ul li ul li a')
    # save categories in database
    for side_category in side_categories:
        category_name = side_category.get_text(strip=True)
        models.Category.objects.get_or_create(name=category_name)


def scrap_total_pages(page):
    pager_text = page.select_one('.pager .current').get_text(strip=True)  # "Page 1 of 50"
    number_of_pages = pager_text.split(" ")[-1]  # "50"
    number_of_pages = int(number_of_pages)  # 50
    return number_of_pages


def scrap_each_page(number_of_pages):
    for i in range(1, number_of_pages + 1):
        # set url and get page object
        current_page_url = f'{BASE_URL}catalogue/page-{i}.html'
        page = get_page(current_page_url)
        # for each product section
        product_sections = page.select('.product_pod')
        for product_section in product_sections:
            # get product url and thumbnail
            product_href = product_section.select_one('a')['href'].strip()
            product_url = f'{BASE_URL}catalogue/{product_href}'
            thumbnail_src = product_section.select_one('.image_container a img')['src'][3:].strip()
            thumbnail_url = f'{BASE_URL}{thumbnail_src}'
            book = models.Book(thumbnail_url=thumbnail_url)
            # scrap book page to fill the other fields
            scrap_book(book, product_url)


def scrap_book(book, product_url):
    """
    book: Book model instance
    url: url of the product, eg: http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
    """
    page = get_page(product_url)
    # get category name
    category_name = page.select('.breadcrumb li a')[2].get_text(strip=True)  # 3rd link in the breadcrumb
    # get category from database and assign it to the book
    category, created = models.Category.objects.get_or_create(name=category_name)
    book.category = category
    # get the title and assign it to the book
    title = page.select_one('.product_main h1').get_text(strip=True)
    book.title = title
    # get the price and assign it to the book
    price = page.select('.product_main p')[0].get_text(strip=True)[1:]
    book.price = price
    # get the stock and assign it to the book
    stock_text = page.select_one('.availability').get_text(strip=True)  # eg: In stock (22 available)
    stock_text_words = re.split('\W+', stock_text)  # eg: ['In', 'stock', '22', 'available', '']
    stock_index = stock_text_words.index('available')  # eg: 3
    stock = stock_text_words[stock_index]  # eg: 22
    book.stock = stock != '0'
    # get the product description and assign it to the book
    product_description = page.select_one('.product_page > p')
    if product_description:
        product_description = product_description.get_text(strip=True)
    else:
        product_description = ''
    book.product_description = product_description
    # get the upc and assign it to the book
    upc = page.select('.product_page table td')[0].get_text(strip=True)
    book.upc = upc
    book.save()
