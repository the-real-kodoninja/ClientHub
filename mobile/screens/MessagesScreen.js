// ClientHubMobile/screens/MessagesScreen.js
import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, ScrollView } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function MessagesScreen() {
  const [messages, setMessages] = useState([]);
  const [clientId, setClientId] = useState('');
  const [assignmentId, setAssignmentId] = useState('');
  const [content, setContent] = useState('');

  useEffect(() => {
    const fetchMessages = async () => {
      const token = await AsyncStorage.getItem('token');
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
  }, [clientId, assignmentId]);

  const sendMessage = async () => {
    const token = await AsyncStorage.getItem('token');
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
    <ScrollView style={{ flex: 1, backgroundColor: '#f5f5f0', padding: 10 }}>
      <Text style={{ color: '#4a7048', fontSize: 24 }}>Messages</Text>
      <TextInput
        placeholder="Client ID (optional)"
        value={clientId}
        onChangeText={setClientId}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      <TextInput
        placeholder="Assignment ID (optional)"
        value={assignmentId}
        onChangeText={setAssignmentId}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      <TextInput
        placeholder="Type your message"
        value={content}
        onChangeText={setContent}
        multiline
        style={{ borderWidth: 1, padding: 10, margin: 5, height: 100 }}
      />
      <Button title="Send" onPress={sendMessage} color="#8b6f47" />
      {messages.map((msg, index) => (
        <Text key={index} style={{ color: '#8b6f47', margin: 5 }}>
          {msg.sender}: {msg.content} ({msg.timestamp})
        </Text>
      ))}
    </ScrollView>
  );
}