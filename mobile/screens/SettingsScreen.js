// ClientHubMobile/screens/SettingsScreen.js
import React, { useState } from 'react';
import { View, Text, TextInput, Button, ScrollView } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function SettingsScreen() {
  const [socialMedia, setSocialMedia] = useState({ twitter: {}, linkedin: {}, instagram: {} });
  const [freelanceAccounts, setFreelanceAccounts] = useState({ freelancer: '', fiverr: '', portfolio: '' });

  const updateSettings = async () => {
    const token = await AsyncStorage.getItem('token');
    await axios.put(
      'http://127.0.0.1:8000/users/me',
      { social_media_configs: socialMedia, freelance_accounts: freelanceAccounts },
      { headers: { Authorization: `Bearer ${token}` } }
    );
  };

  return (
    <ScrollView style={{ flex: 1, backgroundColor: '#f5f5f0', padding: 10 }}>
      <Text style={{ color: '#4a7048', fontSize: 24 }}>Settings</Text>
      <Text style={{ color: '#8b6f47' }}>Social Media</Text>
      <TextInput
        placeholder="Twitter API Key"
        value={socialMedia.twitter.api_key || ''}
        onChangeText={(text) => setSocialMedia({ ...socialMedia, twitter: { ...socialMedia.twitter, api_key: text } })}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      <TextInput
        placeholder="Twitter API Secret"
        value={socialMedia.twitter.api_secret || ''}
        onChangeText={(text) => setSocialMedia({ ...socialMedia, twitter: { ...socialMedia.twitter, api_secret: text } })}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      <TextInput
        placeholder="Twitter Access Token"
        value={socialMedia.twitter.access_token || ''}
        onChangeText={(text) => setSocialMedia({ ...socialMedia, twitter: { ...socialMedia.twitter, access_token: text } })}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      <TextInput
        placeholder="Twitter Access Token Secret"
        value={socialMedia.twitter.access_token_secret || ''}
        onChangeText={(text) => setSocialMedia({ ...socialMedia, twitter: { ...socialMedia.twitter, access_token_secret: text } })}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      <TextInput
        placeholder="LinkedIn Email"
        value={socialMedia.linkedin.email || ''}
        onChangeText={(text) => setSocialMedia({ ...socialMedia, linkedin: { ...socialMedia.linkedin, email: text } })}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      <TextInput
        placeholder="LinkedIn Password"
        value={socialMedia.linkedin.password || ''}
        onChangeText={(text) => setSocialMedia({ ...socialMedia, linkedin: { ...socialMedia.linkedin, password: text } })}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      <TextInput
        placeholder="Instagram Username"
        value={socialMedia.instagram.username || ''}
        onChangeText={(text) => setSocialMedia({ ...socialMedia, instagram: { ...socialMedia.instagram, username: text } })}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      <TextInput
        placeholder="Instagram Password"
        value={socialMedia.instagram.password || ''}
        onChangeText={(text) => setSocialMedia({ ...socialMedia, instagram: { ...socialMedia.instagram, password: text } })}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      <Text style={{ color: '#8b6f47' }}>Freelance Accounts</Text>
      <TextInput
        placeholder="Freelancer URL"
        value={freelanceAccounts.freelancer || ''}
        onChangeText={(text) => setFreelanceAccounts({ ...freelanceAccounts, freelancer: text })}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      <TextInput
        placeholder="Fiverr URL"
        value={freelanceAccounts.fiverr || ''}
        onChangeText={(text) => setFreelanceAccounts({ ...freelanceAccounts, fiverr: text })}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      <TextInput
        placeholder="Portfolio URL"
        value={freelanceAccounts.portfolio || ''}
        onChangeText={(text) => setFreelanceAccounts({ ...freelanceAccounts, portfolio: text })}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      <Button title="Save Settings" onPress={updateSettings} color="#8b6f47" />
    </ScrollView>
  );
}