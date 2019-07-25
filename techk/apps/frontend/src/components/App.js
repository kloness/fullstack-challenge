import React, { useState, useEffect } from "react";
import Categories from "./Categories";
import Books from "./Books";
import ScrapingButton from "./ScrapingButton";


const App = () => {
  const [categories, setCategories] = useState([]);
  const [books, setBooks] = useState([]);

  async function fetchCategories() {
    const res = await fetch("/api/categories");
    res.json()
      .then(res => setCategories(res))
      .catch(err => console.error(err));
  }

  async function fetchBooks() {
    const res = await fetch("/api/books");
    res.json()
      .then(res => setBooks(res))
      .catch(err => console.error(err));
  }

  useEffect(() => {
    fetchCategories();
    fetchBooks();
  }, []);

  return (
    <div className="section">
      <div className="container">
        <ScrapingButton />
        <div className="columns is-desktop">
          <Categories categories={categories} />
          <Books books={books} />
        </div>
      </div>
    </div>
  )
};

export default App;
