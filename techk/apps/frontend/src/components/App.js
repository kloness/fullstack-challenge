import React, { useState, useEffect } from "react";
import Categories from "./Categories";
import Books from "./Books";
import ScrapingButton from "./ScrapingButton";
import axios from 'axios';


const App = () => {
  // App holds the state of the app and gives props to child components
  const [categories, setCategories] = useState([]);
  const [categoryId, setCategoryId] = useState(null);
  const [books, setBooks] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [scrapingIsLoading, setScrapingIsLoading] = useState(false);
  const [searchText, setSearchText] = useState('');
  const booksPerPage = 4;

  async function fetchCategories() {
    axios.get('/api/categories')
      .then(res => setCategories(res.data))
      .catch(err => console.error(err));
  }

  async function fetchBooks(reset=false) {
    if (scrapingIsLoading) return;  // don't reload books before scraping finishes
    const start = reset ? 0 : (page - 1) * booksPerPage;
    const categoryIdValue = reset ? null : categoryId;
    const searchValue = reset ? '' : searchText;
    axios.get('/api/books', {
      params: {
        category_id: categoryIdValue,
        start: start,
        length: booksPerPage,
        search: searchValue
      }
    })
      .then(res => {
        const { total_pages, books } = res.data;
        setTotalPages(total_pages);
        setBooks(books);
      })
      .catch(err => console.error(err));
  }

  function resetData() {
    setScrapingIsLoading(true);
    setCategories([]);
    setCategoryId(categoryId);
    setBooks([]);
    setTotalPages(0);
    setSearchText('');
    setPage(1);
  }

  function fetchAllData() {
    setScrapingIsLoading(false);
    fetchCategories();
    fetchBooks(true);
  }

  useEffect(() => {
    // when page loads, call fetchCategories
    fetchCategories();
  }, []);

  useEffect(() => {
    // if categoryId, page or searchText changes, call fetchBooks
    fetchBooks();
  }, [categoryId, page, searchText]);

  function onCategoryChange(categoryId) {
    setPage(1);
    setCategoryId(categoryId);
  }

  function onSearchChange(searchValue) {
    setPage(1);
    setSearchText(searchValue);
  }

  return (
    <div className="section">
      <div className="container">
        <ScrapingButton
          beforeScraping={resetData}
          afterScraping={fetchAllData}
        />
        <div className="columns is-desktop">
          <Categories
            categories={categories}
            categoryId={categoryId}
            onCategoryChange={onCategoryChange}
          />
          <Books
            books={books}
            page={page}
            setPage={setPage}
            setSearchText={onSearchChange}
            totalPages={totalPages}
          />
        </div>
      </div>
    </div>
  )
};

export default App;
