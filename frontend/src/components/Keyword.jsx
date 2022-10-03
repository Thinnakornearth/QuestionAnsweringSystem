import React from "react";

function Keyword(props) {
  return <div className="suggestion">
    <h6>Related Keyword</h6>
    <h4>{props.keyword}</h4>
    <p>{props.answer}</p>
  </div>
}

export default Keyword;
