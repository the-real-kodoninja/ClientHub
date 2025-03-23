// frontend/src/components/Messages.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Messages({ token }) {
  const [messages, setMessages] = useState([]);
  const [clientId, setClientId] = useState('');
  const [assignmentId, setAssignmentId] = useState('');
  const [content, setContent] = useState('');

  useEffect(() => {
    const fetchMessages = async () => {
      const params = {};
      if (clientId) params.client_id = clientId;
      if (assignmentId) params.assignment_id = assignmentId;
      const response = await axios.get('http://127.0.0.1:8000/messages/', {
        params,
        headers: { Authorization: `Bearer ${token}` }
      });
      setMessages(response.data);
    };
    fetchMessages();
  }, [clientId, assignmentId, token]);

  const sendMessage = async () => {
    await axios.post(
      'http://127.0.0.1:8000/messages/',
      { client_id: clientId || null, assignment_id: assignmentId || null, content },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    setContent('');
    const response = await axios.get('http://127.0.0.1:8000/messages/', {
      params: { client_id: clientId, assignment_id: assignmentId },
      headers: { Authorization: `Bearer ${token}` }
    });
    setMessages(response.data);
  };

  return (
    <div>
      <h1>Messages</h1>
      <input
        placeholder="Client ID (optional)"
        value={clientId}
        onChange={(e) => setClientId(e.target.value)}
      />
      <input
        placeholder="Assignment ID (optional)"
        value={assignmentId}
        onChange={(e) => setAssignmentId(e.target.value)}
      />
      <textarea
        placeholder="Type your message"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>
      <ul>
        {messages.map((msg, index) => (
          <li key={index}>{msg.sender}: {msg.content} ({msg.timestamp})</li>
        ))}
      </ul>
    </div>
  );
}

export default Messages;