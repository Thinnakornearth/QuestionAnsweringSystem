import "./searchbar.css";
import { useState, useEffect } from "react";
import axios from "axios";

const Searchbar = () => {
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
    setSuggestion([]);
  };

  const onChangeHandler = (text) => {
    let matches = [];
    if (text.length > 0) {
      matches = questions.filter((question) => {
        const regex = new RegExp(`${text}`, "gi");
        return question.s.match(regex);
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

  // Render
  return (
    <>
      <div className="search">
        <div className="left">
          <input
            type="text"
            placeholder="Input question"
            onChange={(e) => onChangeHandler(e.target.value)}
            value={text}
            onBlur={() => {
              setTimeout(() => {
                setSuggestion([]);
              }, 100);
            }}
          />
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
        <div className="right">
          <button onClick={searchResult}>Search</button>
        </div>
      </div>
      <div className="result-boundary">
        {results &&
          results.map((result, i) => {
            return (
              <div className="result-container" key={i}>
                <div className="result">
                  <h3> {result.subject}</h3>
                  <p>{result.o}</p>
                </div>
              </div>
            );
          })}
      </div>
    </>
  );
};

export default Searchbar;
