import React, { useState } from "react";
import PropTypes from "prop-types";
import Pagination from 'bulma-pagination-react';


const Search = ({ search }) => {
  const [searchValue, setSearchValue] = useState("");

  const handleSearchInputChanges = e => {
    setSearchValue(e.target.value);
  };

  const resetInputField = () => {
    setSearchValue("");
  };

  const callSearchFunction = e => {
    e.preventDefault();
    search(searchValue);
    resetInputField();
  };

  return (
    <form className="float-right w-300 mb-10 display-flex">
      <input
        type="text"
        value={searchValue}
        onChange={handleSearchInputChanges}
        className="input is-rounded"
      />
      <input
        type="submit"
        value="Search"
        onClick={callSearchFunction}
        className="button is-rounded"
      />
    </form>
  );
};


const Books = ({ books, page, setPage, totalPages, setSearchText }) => {

  function bookUI(book) {
    const { id, title, category, thumbnail_url, price, stock, product_description, upc } = book;
    return (
      <tr key={id}>
        <td><img src={thumbnail_url} alt="book thumbnail"/></td>
        <td>{title}</td>
        <td>{category}</td>
        <td>{price}</td>
        <td>{stock ? 'Yes' : 'No'}</td>
        <td>{upc}</td>
        <td>
          <textarea className="textarea" readOnly cols="100" rows="3" value={product_description} />
        </td>
      </tr>
    );
  }

  function search(searchValue) {
    setSearchText(searchValue);
  }

  return (
    <div className="column">
      <Search search={search} />
      <table className="table is-bordered is-striped books-table">
        <thead>
        <tr>
          <th>Thumbnail</th>
          <th>Title</th>
          <th>Category</th>
          <th>Price</th>
          <th>In stock</th>
          <th>UPC</th>
          <th>Description</th>
        </tr>
        </thead>
        <tbody>
        {books.map(bookUI)}
        {books.length === 0 &&
        <tr>
          <td colSpan={7}>
            No books
          </td>
        </tr>
        }
        </tbody>
      </table>

      {totalPages > 0 &&
      <Pagination
        pages={totalPages}
        currentPage={page}
        onChange={page => setPage(page)}
      />
      }
    </div>
  )
};

Books.propTypes = {
  books: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      category: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      thumbnail_url: PropTypes.string.isRequired,
      price: PropTypes.string.isRequired,
      stock: PropTypes.bool.isRequired,
      product_description: PropTypes.string.isRequired,
      upc: PropTypes.string.isRequired
    }).isRequired
  ),
  page: PropTypes.number.isRequired,
  setPage: PropTypes.func.isRequired,
  totalPages: PropTypes.number.isRequired
};

export default Books;
