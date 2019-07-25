import React from "react";
import PropTypes from "prop-types";


const Categories = (categories) => {

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

Categories.propTypes = {
  caterogies: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired
    })
  )
};

Categories.defaultProps = {
  categories: []
};

export default Categories;
