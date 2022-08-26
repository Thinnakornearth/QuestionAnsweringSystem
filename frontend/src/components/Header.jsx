import React from "react";
import logo from "../images/logo-uow.png";
function Header() {
  return (
    <header>
        <img src={logo} alt="" /> <h3></h3>
        <div className = "nav1">
        <a href="/" onClick={()=>alert("TBD")}>About</a>
        </div>
        
    </header>
  );
}

export default Header;
