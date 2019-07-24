import React, { useState, useEffect } from "react";


const Categories = () => {
  const [categories, setCategories] = useState([]);

  async function fetchCategories() {
    const res = await fetch("/api/categories");
    res.json()
      .then(res => setCategories(res))
      .catch(err => console.error(err));
  }

  useEffect(() => {
    fetchCategories();
  }, []);

  function categoryUI(category) {
    return (<li key={category.id}>{category.name}</li>);
  }

  return (
    <div className="column is-3-desktop">
      <div className="category-column">
        <h1 className="subtitle">Categories</h1>
        <ul>
          {categories.map(categoryUI)}
        </ul>
      </div>
    </div>
  )
};

export default Categories;
