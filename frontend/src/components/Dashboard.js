// frontend/src/components/Dashboard.js
import React from 'react';

function Dashboard() {
  return (
    <div>
      <h1>ClientHub Dashboard</h1>
      <p>Become a freelance megastar with ClientHub!</p>
      <ul>
        <li><a href="/clients">View Clients</a></li>
        <li><a href="/logs">View Logs</a></li>
      </ul>
    </div>
  );
}

export default Dashboard;