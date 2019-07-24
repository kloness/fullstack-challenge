import React from "react";
import Categories from "./Categories";
import Books from "./Books";


const App = () => (
  <div className="section">
    <div className="container">
      <div className="columns">
        <Categories />
        <Books />
      </div>
    </div>
  </div>
);

export default App;
