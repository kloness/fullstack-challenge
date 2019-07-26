import React, { useState, useEffect } from "react";
import Categories from "./Categories";
import Books from "./Books";
import ScrapingButton from "./ScrapingButton";
import axios from 'axios';


const App = () => {
  const [categories, setCategories] = useState([]);
  const [books, setBooks] = useState([]);

  async function fetchCategories() {
    axios.get('/api/categories')
      .then(res => setCategories(res.data))
      .catch(err => console.error(err));
  }

  async function fetchBooks(categoryId=null) {
    axios.get('/api/books', {
      params: {
        category_id: categoryId
      }
    })
      .then(res => setBooks(res.data))
      .catch(err => console.error(err));
  }

  function resetData() {
    setCategories([]);
    setBooks([]);
  }

  function fetchAllData() {
    fetchCategories();
    fetchBooks();
  }

  useEffect(() => {
    fetchAllData();
  }, []);

  function onCategoryChange(categoryId) {
    fetchBooks(categoryId);
  }

  return (
    <div className="section">
      <div className="container">
        <ScrapingButton
          beforeScraping={resetData}
          afterScraping={fetchAllData}
        />
        <div className="columns is-desktop">
          <Categories categories={categories} onCategoryChange={onCategoryChange} />
          <Books books={books} />
        </div>
      </div>
    </div>
  )
};

export default App;
