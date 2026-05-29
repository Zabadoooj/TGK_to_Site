import './App.css';

import Header from './Components/Header';
import PostList from './Components/PostsList';
import Backround from './Components/Backround';


function App() {
  return (
    <div className="App">

      <Header/>

      <PostList/>

      <Backround />

    </div>
  );
}

export default App;
