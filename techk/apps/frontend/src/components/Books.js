import React, { useState, useEffect } from "react";


const Books = () => {
  const [books, setBooks] = useState([]);

  async function fetchBooks() {
    const res = await fetch("/api/books");
    res.json()
      .then(res => setBooks(res))
      .catch(err => console.error(err));
  }

  useEffect(() => {
    fetchBooks();
  }, []);

  function bookUI(book) {
    const { id, title, thumbnail_url, price, stock, product_description, upc } = book;
    return (
      <tr key={id}>
        <td><img src={thumbnail_url} alt="book thumbnail"/></td>
        <td>{title}</td>
        <td>{price}</td>
        <td>{stock ? 'Yes' : 'No'}</td>
        <td>{upc}</td>
        <td>
          <textarea className="textarea" readOnly cols="100" rows="3" value={product_description} />
        </td>
      </tr>
    );
  }

  return (
    <div className="column">
      <table className="table is-bordered is-striped">
        <thead>
        <tr>
          <th>Thumbnail</th>
          <th>Title</th>
          <th>Price</th>
          <th>In stock</th>
          <th>UPC</th>
          <th>Description</th>
        </tr>
        </thead>
        <tbody>
        {books.map(bookUI)}
        </tbody>
      </table>
    </div>
  )
};

export default Books;
