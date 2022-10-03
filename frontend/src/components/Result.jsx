import React from 'react';

function Result(props){
          return (
            <div className="result">
              <h4>{props.question}</h4>
              <p>{props.answer}</p>
            </div>
          );
}

export default Result;