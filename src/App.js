import React, { useEffect } from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import { SocketProvider } from './context/SocketContext';
import MainPage from './pages/mainPage';
import BoostPage from './pages/boostPage';
import TradePage from './pages/tradePage';
import "./styles/App.css"



function App() {

  const tg = window.Telegram.WebApp
  useEffect(() =>
  {
    tg.ready();
  }
  , [])

  return (
    <SocketProvider>
      <Router>
        <Routes>
          <Route path="/" element={<MainPage/>}/>
          <Route path='/boost' element={<BoostPage/>}/>
          <Route path='/trade' element={<TradePage/>}/>
        </Routes>
      </Router>
    </SocketProvider>
  );
}

export default App;
