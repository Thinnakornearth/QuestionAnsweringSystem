import React from "react";

function Suggestion(props) {
  return (
    <div key={props.question} className="suggestion">
      <h6>Suggested Question</h6>
      <h4>{props.question}</h4>
      {props.answer.length > 1 &&
        props.answer.map((ans, i) => (
          <div>
            <a href="#" className="title">
              <p key={ans[0].subject} >{ans[0].subject}</p>
            </a>
            <p key={ans[0].o} className="details" >{ans[0].o}</p>
          </div>
        ))}

      <p>{props.answer.length === 1 && props.answer[0].o}</p>
    </div>
  );
}

export default Suggestion;
