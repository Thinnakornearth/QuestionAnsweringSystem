import './App.css';
import Topbar from './components/topbar/topbar';
import Header from './components/header/Header';
import Searchbar from './components/autocomplete/Searchbar';

function App() {
  return (
    <div className="App">
      <Topbar/>
      <Header/>
      <Searchbar/>
    </div>
  );
}

export default App;
