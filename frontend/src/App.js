// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import ClientList from './components/ClientList';
import AssignmentView from './components/AssignmentView';
import PromoBanner from './components/PromoBanner';
import Logs from './components/Logs';
import Messages from './components/Messages';
import Settings from './components/Settings';
import Login from './components/Login';
import './App.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) localStorage.setItem('token', token);
    else localStorage.removeItem('token');
  }, [token]);

  return (
    <Router>
      <div className="app">
        {token && <PromoBanner />}
        <Routes>
          <Route path="/login" element={<Login setToken={setToken} />} />
          <Route path="/" element={token ? <Dashboard /> : <Navigate to="/login" />} />
          <Route path="/clients" element={token ? <ClientList /> : <Navigate to="/login" />} />
          <Route path="/assignment/:id" element={token ? <AssignmentView /> : <Navigate to="/login" />} />
          <Route path="/logs" element={token ? <Logs /> : <Navigate to="/login" />} />
          <Route path="/messages" element={token ? <Messages token={token} /> : <Navigate to="/login" />} />
          <Route path="/settings" element={token ? <Settings token={token} /> : <Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;