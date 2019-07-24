import React, { useEffect } from "react";


const Categories = () => {
  async function fetchData() {
    console.log('fetchData');
    const res = await fetch("/api/categories");
    console.log('res:');
    console.log(res);
    res.json()
      .then(res => console.log(res))
      .catch(err => console.error(err));
  }

  useEffect(() => {
    console.log('userEffect');
    fetchData();
  });

  return (
    <div>
      <h1 className="subtitle">Categorías</h1>
    </div>
  )
};

export default Categories;
