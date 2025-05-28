import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import RequestForm from './components/RequestForm';
import RequestsList from './components/RequestsList';
import './App.css'

function App() {
  return (
    <Router>
      <nav style={{ padding: '1rem', backgroundColor: '#f4f4f4' }}>
        <Link to="/" style={{ marginRight: '1rem' }}>Submit Request</Link>
        <Link to="/requests">View Requests</Link>
      </nav>
      <Routes>
        <Route path="/" element={<RequestForm />} />
        <Route path="/requests" element={<RequestsList />} />
      </Routes>
    </Router>
  );
}

export default App;
