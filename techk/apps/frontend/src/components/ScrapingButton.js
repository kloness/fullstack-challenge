import React, { useState } from "react";
import PropTypes from "prop-types";


const ScrapingButton = ({ beforeScraping, afterScraping }) => {
  const [loading, setLoading] = useState(false);

  async function scrape() {
    setLoading(true);
    beforeScraping();
    const res = await fetch("/api/scraping");
    res.json()
      .then(res => console.log(res))
      .catch(err => console.error(err));
    setLoading(false);
    afterScraping();
  }

  return (
    <div className="buttons is-centered">
      <button
        onClick={scrape} disabled={loading}
        className={"button is-large is-link is-rounded " + (loading ? "is-loading" : "")}
      >
        Scraping process
      </button>
    </div>
  )
};

ScrapingButton.propTypes = {
  beforeScraping: PropTypes.func,
  afterScraping: PropTypes.func
};

ScrapingButton.defaultProps = {
  beforeScraping: () => {},
  afterScraping: () => {}
};

export default ScrapingButton;
