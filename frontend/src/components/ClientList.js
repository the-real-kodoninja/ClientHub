// frontend/src/components/ClientList.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ClientList() {
  const [clients, setClients] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/clients/')
      .then(response => setClients(response.data))
      .catch(error => console.error('Error fetching clients:', error));
  }, []);

  return (
    <div>
      <h1>Client List</h1>
      <ul>
        {clients.map(client => (
          <li key={client.id}>
            {client.name} - {client.platform} (Priority: {client.priority})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ClientList;