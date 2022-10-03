import React from 'react';

function Search(props){

    return(
        <form className="search-box" onSubmit={props.submit}>
        <input
          type="search"
          placeholder="Please enter your question..."
          value={props.search}
          onChange={(e) => props.onValueChange(e.target.value)}
        />
      </form>
    )
}

export default Search;