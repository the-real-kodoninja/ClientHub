// ClientHubMobile/screens/LoginScreen.js
import React, { useState } from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function LoginScreen({ navigation }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/token', { username, password });
      await AsyncStorage.setItem('token', response.data.access_token);
      navigation.navigate('Dashboard');
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#f5f5f0' }}>
      <Text style={{ color: '#4a7048', fontSize: 24 }}>Login to ClientHub</Text>
      <TextInput
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
        style={{ borderWidth: 1, padding: 10, margin: 10, width: 200 }}
      />
      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        style={{ borderWidth: 1, padding: 10, margin: 10, width: 200 }}
      />
      <Button title="Login" onPress={handleLogin} color="#8b6f47" />
    </View>
  );
}