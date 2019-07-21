# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from multiprocessing import Pool
from timeit import default_timer as timer

import requests
from bs4 import BeautifulSoup

from apps.base import models
from apps.base.models import reset_db

BASE_URL = 'http://books.toscrape.com/'


def get_page(url):
    req = requests.get(url)
    req.encoding = 'utf-8'  # the default is ISO-8859-1 and has problems with some characters
    return BeautifulSoup(req.text, 'html.parser')


def scrap_process():
    """
    Benchmark without parallel processing:
    scrap categories: 0.060 seconds
    scrap 1000 books: 579.192 seconds
    total: 579.252 seconds

    Benchmark with parallel processing (50 processes for pages and 100 for books):
    scrap categories: 0.381 seconds
    scrap 50 book list pages: 1.558 seconds
    scrap 1000 books: 11.844 seconds
    save 1000 books on database: 9.726 seconds
    total: 23.509 seconds
    """
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

    # scrap each page to get a list of product data (url and thumbnail)
    start = timer()
    page_indices = [i for i in range(1, number_of_pages + 1)]  # eg: [1, 2, ..., 50]
    book_data_list = []
    with Pool(50) as process:
        # scrap each page in parallel (page 1, 2, ..., 50)
        product_batches = process.map(scrap_product_list_page, page_indices)
        # product_batches = [
        #     [
        #         [books from page 1],
        #         [books from page 2],
        #         ...,
        #         [books from page 50],
        #     ]
        for batch in product_batches:  # consolidate books from every page into a single list
            book_data_list += batch
        # book_data_list = [
        #     {
        #         "product_url": ...,
        #         "thumbnail_url": ...
        #     },
        #     ... (1000 books)
        # ]
    end = timer()
    print(f'scrap pages: {end - start} seconds')

    # scrap each book page in parallel
    start = timer()
    with Pool(100) as process:
        final_book_data = process.map(scrap_book, book_data_list)
    end = timer()
    print(f'scrap books: {end - start} seconds')

    # save books on database
    start = timer()
    save_books_on_database(final_book_data)
    end = timer()
    print(f'save books on database: {end - start} seconds')


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


def scrap_product_list_page(page_number):
    """
    It gets a page with a list of products. For each product it saves a dict with product url and thumbnail.
    return example:
    [
        {
            "product_url": "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
            "thumbnail_url": "http://books.toscrape.com/media/cache/26/0c/260c6ae16bce31c8f8c95daddd9f4a1c.jpg"
        },
        ...
    ]
    """
    book_data_list = []
    # set url and get page object
    current_page_url = f'{BASE_URL}catalogue/page-{page_number}.html'
    page = get_page(current_page_url)
    # for each product section
    product_sections = page.select('.product_pod')
    for product_section in product_sections:
        # get product url and thumbnail
        product_href = product_section.select_one('a')['href'].strip()
        product_url = f'{BASE_URL}catalogue/{product_href}'
        thumbnail_src = product_section.select_one('.image_container a img')['src'][3:].strip()
        thumbnail_url = f'{BASE_URL}{thumbnail_src}'
        book_dict = {
            "product_url": product_url,
            "thumbnail_url": thumbnail_url,
        }
        book_data_list.append(book_dict)
    return book_data_list


def scrap_book(book_dict):
    """
    It scraps the information of a book page and saves it on the database.
    book_dict: A dictionary with product_url and thumbnail_url
    example of book_dict:
    {
        "product_url": "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
        "thumbnail_url": "http://books.toscrape.com/media/cache/26/0c/260c6ae16bce31c8f8c95daddd9f4a1c.jpg"
    }
    """
    page = get_page(book_dict['product_url'])
    # get category name
    category_name = page.select('.breadcrumb li a')[2].get_text(strip=True)  # 3rd link in the breadcrumb
    # get category from database and assign it to the book
    category, created = models.Category.objects.get_or_create(name=category_name)
    # get the title and assign it to the book
    title = page.select_one('.product_main h1').get_text(strip=True)
    # get the price and assign it to the book
    price = page.select('.product_main p')[0].get_text(strip=True)
    # get the stock and assign it to the book
    stock_text = page.select_one('.availability').get_text(strip=True)  # eg: In stock (22 available)
    stock_text_words = re.split('\W+', stock_text)  # eg: ['In', 'stock', '22', 'available', '']
    stock_index = stock_text_words.index('available')  # eg: 3
    stock_number = stock_text_words[stock_index]  # eg: '22'
    stock = stock_number != '0'
    # get the product description and assign it to the book
    product_description = page.select_one('.product_page > p')
    if product_description:
        product_description = product_description.get_text(strip=True)
    else:
        product_description = ''
    # get the upc and assign it to the book
    upc = page.select('.product_page table td')[0].get_text(strip=True)
    # return final book data
    book_data = {
        'category': category.id,
        'title': title,
        'thumbnail_url': book_dict['thumbnail_url'],
        'price': price,
        'stock': stock,
        'product_description': product_description,
        'upc': upc,
    }
    return book_data


def save_books_on_database(book_data_list):
    """
    book_data_list: list or arrays describing books to be saved
    example of book_data_list:
    {
        'category': 3954,
        'title': 'Tipping the Velvet',
        'thumbnail_url': 'http://books.toscrape.com/media/cache/26/0c/ddd9f4a1c.jpg',
        'price': '£53.74',
        'stock': True,
        'product_description': 'Through a friend at the box office, ...',
        'upc': '90fa61229261140a'
    }

    note: models are not saved in parallel to prevent sqlite from exploding
    django.db.utils.OperationalError: database is locked
    """
    for book_data in book_data_list:
        category_id = book_data.pop('category')
        category = models.Category.objects.get(id=category_id)
        models.Book.objects.create(category=category, **book_data)
