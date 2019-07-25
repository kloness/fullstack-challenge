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
    console.log('categoryId:');
    console.log(categoryId);
    axios.get('/api/books')
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

  return (
    <div className="section">
      <div className="container">
        <ScrapingButton
          beforeScraping={resetData}
          afterScraping={fetchAllData}
        />
        <div className="columns is-desktop">
          <Categories categories={categories} />
          <Books books={books} />
        </div>
      </div>
    </div>
  )
};

export default App;
