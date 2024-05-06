import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from "./components/NavBar/navbar";
import Home from './pages/Home/home';
import Reports from './pages/Reports/reports';
import Products from './pages/Products/products';
import './App.css';

function App() {
  return (
    <>
      <Router>
        <Navbar/>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/reports' element={<Reports />} />
          <Route path='/products' element={<Products />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
