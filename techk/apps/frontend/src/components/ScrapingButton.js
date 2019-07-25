import React, { useState } from "react";


const ScrapingButton = () => {
  const [loading, setLoading] = useState(false);

  async function scrape() {
    setLoading(true);
    const res = await fetch("/api/scraping");
    res.json()
      .then(res => console.log(res))
      .catch(err => console.error(err));
    setLoading(false);
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

export default ScrapingButton;
