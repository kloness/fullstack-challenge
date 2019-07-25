import React from "react";
import Categories from "./Categories";
import Books from "./Books";
import ScrapingButton from "./ScrapingButton";


const App = () => (
  <div className="section">
    <div className="container">
      <ScrapingButton />
      <div className="columns is-desktop">
        <Categories />
        <Books />
      </div>
    </div>
  </div>
);

export default App;
