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
    return (
      <tr key={category.id}>
        <td>{category.name}</td>
      </tr>
    );
  }

  return (
    <div className="column is-3-desktop">
      <div className="category-column">
        <h1 className="subtitle has-text-centered pt-10">Categories</h1>
        <table className="table is-fullwidth is-narrow">
          <tbody>
          <tr className="is-selected">
            <td>All</td>
          </tr>
          {categories.map(categoryUI)}
          </tbody>
        </table>
      </div>
    </div>
  )
};

export default Categories;
