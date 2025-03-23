// frontend/src/components/Login.js
import React, { useState } from 'react';
import axios from 'axios';

function Login({ setToken }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/token', { username, password });
      setToken(response.data.access_token);
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <div>
      <h1>Login</h1>
      <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
      <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="Password" />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default Login;