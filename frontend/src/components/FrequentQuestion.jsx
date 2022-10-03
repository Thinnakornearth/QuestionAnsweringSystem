import React from 'react';

function FrequentQuestion(props){
    return(
        <div className="frequenctQ">
        <h4>Frequenct Asked Question</h4>

        <a
          onMouseEnter={() => props.setSearchValue("What is agitation in dementia?")}
          onMouseLeave={() => props.setSearchValue("")}
          onClick={props.search}
        >
          What is agitation in dementia?
        </a>
        <br></br>
        <br></br>
        <a
          onMouseEnter={() => props.setSearchValue("What are the treatments for dementia patient?")}
          onMouseLeave={() => props.setSearchValue("")}
          onClick={props.search}
        >
          What are the treatments for dementia patient?
        </a>
        <br></br>
        <br></br>
        <a
          onMouseEnter={() => props.setSearchValue("How to treat dementia?")}
          onMouseLeave={() => props.setSearchValue("")}
          onClick={props.search}
        >
          How to treat dementia?
        </a>
      </div>

    )
}

export default FrequentQuestion;