import React from "react";
import PropTypes from "prop-types";


const Categories = ({ categories, categoryId, onCategoryChange }) => {

  function categoryClick(categoryId) {
    onCategoryChange(categoryId);
  }

  function resetSelectedCategoryId() {
    // using this function in render instead of an inline function prevents unnecesary renders
    categoryClick(null);
  }

  function categoryUI(category) {
    const isSelectedClass = (category.id === categoryId) ? 'is-selected' : '';
    return (
      <tr key={category.id} className={isSelectedClass}>
        <td onClick={() => categoryClick(category.id)}>{category.name}</td>
      </tr>
    );
  }

  return (
    <div className="column is-2-desktop">
      <div className="category-column">
        <h1 className="subtitle has-text-centered pt-10">Categories</h1>
        <table className="table is-fullwidth is-narrow is-hoverable">
          <tbody>
          {categories.length > 0 &&
          <tr className={categoryId === null ? "is-selected" : ""}>
            <td onClick={resetSelectedCategoryId}>All</td>
          </tr>
          }
          {categories.map(categoryUI)}
          </tbody>
        </table>
      </div>
    </div>
  )
};

Categories.propTypes = {
  categories: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired
    }).isRequired
  ),
  categoryId: PropTypes.number,
  onCategoryChange: PropTypes.func.isRequired
};

export default Categories;
