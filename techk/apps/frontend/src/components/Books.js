import React from "react";
import PropTypes from "prop-types";


const Books = ({ books }) => {

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

Books.propTypes = {
  books: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      category_id: PropTypes.number.isRequired,
      title: PropTypes.string.isRequired,
      thumbnail_url: PropTypes.string.isRequired,
      price: PropTypes.string.isRequired,
      stock: PropTypes.bool.isRequired,
      product_description: PropTypes.string.isRequired,
      upc: PropTypes.string.isRequired
    }).isRequired
  )
};

Books.defaultProps = {
  books: []
};

export default Books;
