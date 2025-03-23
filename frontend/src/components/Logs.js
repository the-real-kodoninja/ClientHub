// frontend/src/components/Logs.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Logs() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/logs/')
      .then(response => setLogs(response.data))
      .catch(error => console.error('Error fetching logs:', error));
  }, []);

  return (
    <div>
      <h1>Activity Logs</h1>
      <ul>
        {logs.map((log, index) => (
          <li key={index}>
            {log.timestamp} - {log.action}: {log.details}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Logs;