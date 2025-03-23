// ClientHubMobile/screens/SettingsScreen.js
import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, ScrollView } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function SettingsScreen() {
  const [socialMedia, setSocialMedia] = useState({});
  const [freelanceAccounts, setFreelanceAccounts] = useState({});
  const [newPlatform, setNewPlatform] = useState({ name: '', config: {} });
  const [newAccount, setNewAccount] = useState({ name: '', url: '' });
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const token = await AsyncStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/users/me', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setSocialMedia(response.data.social_media_configs || {});
        setFreelanceAccounts(response.data.freelance_accounts || {});
      } catch (error) {
        setErrors({ fetch: 'Failed to load settings: ' + error.message });
      }
    };
    fetchSettings();
  }, []);

  const validateUrl = (url) => {
    const urlPattern = /^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w- ./?%&=]*)?$/;
    return urlPattern.test(url);
  };

  const addPlatform = () => {
    const newErrors = {};
    if (!newPlatform.name) newErrors.platformName = 'Platform name is required';
    if (socialMedia[newPlatform.name]) newErrors.platformName = 'Platform already exists';
    if (Object.keys(newPlatform.config).length === 0) newErrors.platformConfig = 'At least one config field is required';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setSocialMedia({ ...socialMedia, [newPlatform.name]: newPlatform.config });
    setNewPlatform({ name: '', config: {} });
    setErrors({});
  };

  const deletePlatform = (platform) => {
    const updatedSocialMedia = { ...socialMedia };
    delete updatedSocialMedia[platform];
    setSocialMedia(updatedSocialMedia);
  };

  const addAccount = () => {
    const newErrors = {};
    if (!newAccount.name) newErrors.accountName = 'Account name is required';
    if (!newAccount.url) newErrors.accountUrl = 'URL is required';
    if (freelanceAccounts[newAccount.name]) newErrors.accountName = 'Account already exists';
    if (newAccount.url && !validateUrl(newAccount.url)) newErrors.accountUrl = 'Invalid URL';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setFreelanceAccounts({ ...freelanceAccounts, [newAccount.name]: newAccount.url });
    setNewAccount({ name: '', url: '' });
    setErrors({});
  };

  const deleteAccount = (name) => {
    const updatedAccounts = { ...freelanceAccounts };
    delete updatedAccounts[name];
    setFreelanceAccounts(updatedAccounts);
  };

  const updateSettings = async () => {
    try {
      const token = await AsyncStorage.getItem('token');
      await axios.put(
        'http://127.0.0.1:8000/users/me',
        { social_media_configs: socialMedia, freelance_accounts: freelanceAccounts },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSuccess('Settings saved successfully!');
      setErrors({});
      setTimeout(() => setSuccess(''), 3000);
    } catch (error) {
      setErrors({ save: 'Failed to save settings: ' + error.message });
    }
  };

  return (
    <ScrollView style={{ flex: 1, backgroundColor: '#f5f5f0', padding: 10 }}>
      <Text style={{ color: '#4a7048', fontSize: 24 }}>Settings</Text>
      {errors.fetch && <Text style={{ color: 'red' }}>{errors.fetch}</Text>}
      {success && <Text style={{ color: 'green' }}>{success}</Text>}
      <Text style={{ color: '#8b6f47' }}>Social Media</Text>
      {Object.entries(socialMedia).map(([platform, config]) => (
        <View key={platform} style={{ marginBottom: 10 }}>
          <Text>{platform}</Text>
          {Object.entries(config).map(([key, value]) => (
            <TextInput
              key={key}
              placeholder={`${key}`}
              value={value}
              onChangeText={(text) => setSocialMedia({
                ...socialMedia,
                [platform]: { ...config, [key]: text }
              })}
              style={{ borderWidth: 1, padding: 10, margin: 5 }}
            />
          ))}
          <Button title="Delete" onPress={() => deletePlatform(platform)} color="red" />
        </View>
      ))}
      <Text style={{ color: '#8b6f47' }}>Add New Platform</Text>
      <TextInput
        placeholder="Platform Name"
        value={newPlatform.name}
        onChangeText={(text) => setNewPlatform({ ...newPlatform, name: text })}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      {errors.platformName && <Text style={{ color: 'red' }}>{errors.platformName}</Text>}
      <TextInput
        placeholder="Key (e.g., api_key)"
        onChangeText={(text) => setNewPlatform({
          ...newPlatform,
          config: { ...newPlatform.config, [text]: '' }
        })}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      <TextInput
        placeholder="Value"
        onChangeText={(text) => {
          const key = Object.keys(newPlatform.config)[Object.keys(newPlatform.config).length - 1];
          setNewPlatform({
            ...newPlatform,
            config: { ...newPlatform.config, [key]: text }
          });
        }}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      {errors.platformConfig && <Text style={{ color: 'red' }}>{errors.platformConfig}</Text>}
      <Button title="Add Platform" onPress={addPlatform} color="#8b6f47" />
      <Text style={{ color: '#8b6f47' }}>Freelance Accounts</Text>
      {Object.entries(freelanceAccounts).map(([name, url]) => (
        <View key={name} style={{ marginBottom: 10 }}>
          <TextInput
            placeholder={name}
            value={url}
            onChangeText={(text) => setFreelanceAccounts({ ...freelanceAccounts, [name]: text })}
            style={{ borderWidth: 1, padding: 10, margin: 5 }}
          />
          <Button title="Delete" onPress={() => deleteAccount(name)} color="red" />
        </View>
      ))}
      <Text style={{ color: '#8b6f47' }}>Add New Account</Text>
      <TextInput
        placeholder="Account Name"
        value={newAccount.name}
        onChangeText={(text) => setNewAccount({ ...newAccount, name: text })}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      {errors.accountName && <Text style={{ color: 'red' }}>{errors.accountName}</Text>}
      <TextInput
        placeholder="URL"
        value={newAccount.url}
        onChangeText={(text) => setNewAccount({ ...newAccount, url: text })}
        style={{ borderWidth: 1, padding: 10, margin: 5 }}
      />
      {errors.accountUrl && <Text style={{ color: 'red' }}>{errors.accountUrl}</Text>}
      <Button title="Add Account" onPress={addAccount} color="#8b6f47" />
      <Button title="Save Settings" onPress={updateSettings} color="#8b6f47" />
      {errors.save && <Text style={{ color: 'red' }}>{errors.save}</Text>}
    </ScrollView>
  );
}