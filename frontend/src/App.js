// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import ClientList from './components/ClientList';
import AssignmentView from './components/AssignmentView';
import PromoBanner from './components/PromoBanner';
import Logs from './components/Logs';
import Messages from './components/Messages';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <PromoBanner />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/clients" element={<ClientList />} />
          <Route path="/assignment/:id" element={<AssignmentView />} />
          <Route path="/logs" element={<Logs />} />
          <Route path="/messages" element={<Messages />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;