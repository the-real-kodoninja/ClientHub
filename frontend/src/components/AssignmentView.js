// frontend/src/components/AssignmentView.js
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function AssignmentView() {
  const { id } = useParams();
  const [status, setStatus] = useState('');

  useEffect(() => {
    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/assignment/${id}`);
    ws.onmessage = (event) => setStatus(event.data);
    return () => ws.close();
  }, [id]);

  return (
    <div>
      <h1>Assignment {id}</h1>
      <p>Current Status: {status}</p>
    </div>
  );
}

export default AssignmentView;