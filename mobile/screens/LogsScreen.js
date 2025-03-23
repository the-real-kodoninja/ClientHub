// ClientHubMobile/screens/LogsScreen.js
import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView } from 'react-native';
import axios from 'axios';

export default function LogsScreen() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/logs/')
      .then(response => setLogs(response.data))
      .catch(error => console.error('Error fetching logs:', error));
  }, []);

  return (
    <ScrollView style={{ flex: 1, backgroundColor: '#f5f5f0', padding: 10 }}>
      <Text style={{ color: '#4a7048', fontSize: 24 }}>Activity Logs</Text>
      {logs.map((log, index) => (
        <Text key={index} style={{ color: '#8b6f47', marginVertical: 5 }}>
          {log.timestamp} - {log.action}: {log.details}
        </Text>
      ))}
    </ScrollView>
  );
}