import React from "react";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import axios from "axios";
import { useState, useEffect } from "react";

function SearchBar() {
  const [questions, setQuestions] = useState([]);
  const [text, setText] = useState("");
  const [suggestion, setSuggestion] = useState([]);
  const [results, setResults] = useState([]);
  const apiLink = "http://localhost:12345/";

  useEffect(() => {
    const loadData = async () => {
      const response = await axios.get(apiLink);
      setQuestions(response.data);
    };
    loadData();
  }, []);

  const onSuggestHandler = (text) => {
    setText(text);
    document.getElementById("outlined-basic").value = text
    setSuggestion([]);
  };

  const onChangeHandler = (text) => {
    let matches = [];
    let count = 0;
    const inputValue = text.toLowerCase();
    const inputLegth = inputValue.length;

    if (text.length > 0) {
      matches = questions.filter((question) => {
        const keep =
          count < 10 && question.s.slice(0,inputLegth).toLowerCase() === inputValue;

        if (keep) {
          count += 1;
        }
        return keep;
      });
    }
    setSuggestion(matches);
    setText(text);
  };

  const searchResult = () => {
    let apiText = text.replaceAll(" ", "+");
    let apiSearch = apiLink + `search?query=${apiText}`;
    const fetchData = async () => {
      const data = await axios.get(apiSearch);
      console.log(data.data);
      setResults(data.data);
    };
    fetchData();
  };



  return (
    <div className="main">
      <div>
      <form>
        <fieldset>
          <legend>Dementia Question and Answer System</legend>
          <div class="inner-form">
            <div class="input-field">
              <button class="btn-search" type="button">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                >
                  <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"></path>
                </svg>
              </button>
              <input
                id="outlined-basic"
                type="text"
                placeholder="Enter Keyword or question"
                data-keeper-edited="yes"
                onChange={(e) => onChangeHandler(e.target.value)}
                value={text}
                onBlur={() => {
                  setTimeout(() => {
                    setSuggestion([]);
                  }, 100);
                }} ></input>        
                {suggestion &&
                  suggestion.map((suggestion, i) => (
                    <div
                      key={i}
                      className="suggestion-bar"
                      onClick={() => onSuggestHandler(suggestion.s)}
                    >
                      {suggestion.s}
                  
                
                    </div>
                  ))}

            </div>
          </div>
          <div class="suggestion-wrap">
          <button className="sample">What is agitation in dementia?</button>
          <button className="sample">How to treatment agitation in dementia?</button>
          <button className="sample">What causes agitation in dementia?</button>

          </div>
        </fieldset>
      </form>
      </div>
      <Button
        variant="contained"
        style={{
          backgroundColor: "#395B64",
        }}
        onClick={searchResult}
      >
        Advance Search
      </Button>
      <div className="results">
        {results &&
          results.map((result, i) => {
            return (
              <div className="result-container" key={i}>
                <div className="result">
                  <h6> {result.subject}</h6>
                  <p>{result.o}</p>
                </div>
              </div>
            );
          })}
      </div>
    </div>
  );
}

export default SearchBar;
