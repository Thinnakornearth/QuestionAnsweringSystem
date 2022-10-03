import React, { useState } from "react";
import Search from "./components/Search";
import Loading from "./components/Loading";
import FrequentQuestion from "./components/FrequentQuestion";
import Result from "./components/Result";
import Suggestion from "./components/Suggestion";
import Keyword from "./components/Keyword";
import { exit } from "process";

function App() {
  const [search, setSearch] = useState("");
  const [results, setResults] = useState([]);
  const [mainQuestion, setMainQuestion] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [shortResult, setShortResult] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    setLoading(true);
    e.preventDefault();
    if (search === "") return;
    let apiInput = search.replaceAll(" ", "+");
    const endpoint = `http://localhost:12345/search?query=${apiInput}`;
    let response;
    try {
      response = await fetch(endpoint);
    } catch (error) {
      console.log(error);
      exit();
    }
    setMainQuestion(search);
    const json = await response.json();
    setLoading(false);
    console.log(json);
    if (json === null) {
      setResults([]);
      setSuggestions([]);
      setShortResult([]);
      return;
      // throw Error(response.statusText);
    }

    if (json["Actual Result"]) {
      setResults(json["Actual Result"]);
    } else {
      setShortResult(json);
      setResults([]);
      setSuggestions([]);
    }

    if (json["Suggested Questions"]) {
      setSuggestions(json["Suggested Questions"]);
      console.log(json["Suggested Questions"]);
    }
  };

  return (
    <div className="App">
      <header>
        <legend>Dementia Question and Answer System</legend>
        <Search
          onValueChange={setSearch}
          search={search}
          submit={handleSearch}
        />
      </header>
      {loading && <Loading />}

      {mainQuestion !== "" &&
        suggestions.length === 0 &&
        shortResult.length === 0 && (
          <h3 className="noAnswerTag">Answer not found ...</h3>
        )}

      <div className="results">
        {results &&
          results !== "SQ_FOUND" &&
          results.length === 1 &&
          results.map((result, i) => {
            return <Result key={i} question={mainQuestion} answer={result.o} />;
          })}
        {results && results === "SQ_FOUND" && suggestions.length > 0 && (
          <div>
            <h3 className="noAnswerTag">
              Answer not found, below are suggested Questions...
            </h3>
          </div>
        )}
        {results && results !== "SQ_FOUND" && results.subject && (
          <Result question={mainQuestion} answer={results.o} />
        )}
      </div>

      <div className="suggestions">
        {suggestions &&
          suggestions.map((result, i) => {
            return (
              i < 10 && (
                <Suggestion
                  key={i}
                  question={result.Question}
                  answer={result.Answer}
                />
              )
            );
          })}

        {shortResult &&
          shortResult.map((result, i) => {
            return (
              i < 10 && <Keyword key={i} keyword={result.subject} answer={result.o} />
            );
          })}

        <FrequentQuestion setSearchValue={setSearch} search={handleSearch} />
      </div>
    </div>
  );
}

export default App;
