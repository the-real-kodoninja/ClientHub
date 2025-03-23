// frontend/src/components/Dashboard.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [analytics, setAnalytics] = useState({
    total_clients: 0,
    active_assignments: 0,
    completed_assignments: 0,
    promotion_posts: 0
  });

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/analytics/')
      .then(response => setAnalytics(response.data))
      .catch(error => console.error('Error fetching analytics:', error));
  }, []);

  return (
    <div>
      <h1>ClientHub Dashboard</h1>
      <p>Become a freelance megastar with ClientHub!</p>
      <ul>
        <li>Total Clients: {analytics.total_clients}</li>
        <li>Active Assignments: {analytics.active_assignments}</li>
        <li>Completed Assignments: {analytics.completed_assignments}</li>
        <li>Promotion Posts: {analytics.promotion_posts}</li>
      </ul>
      <ul>
        <li><a href="/clients">View Clients</a></li>
        <li><a href="/logs">View Logs</a></li>
        <li><a href="/messages">Messages</a></li>
      </ul>
    </div>
  );
}

export default Dashboard;