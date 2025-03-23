// frontend/src/components/Dashboard.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [analytics, setAnalytics] = useState({ total_clients: 0, assignment_status: {} });

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/analytics/')
      .then(response => setAnalytics(response.data))
      .catch(error => console.error('Error fetching analytics:', error));
  }, []);

  return (
    <div>
      <h1>ClientHub Dashboard</h1>
      <p>Total Clients: {analytics.total_clients}</p>
      <p>Assignment Status: {JSON.stringify(analytics.assignment_status)}</p>
      <ul>
        <li><a href="/clients">View Clients</a></li>
      </ul>
    </div>
  );
}

export default Dashboard;