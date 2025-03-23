// frontend/src/components/Settings.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import detectEthereumProvider from '@metamask/detect-provider';

function Settings({ token }) {
  const [socialMedia, setSocialMedia] = useState({});
  const [freelanceAccounts, setFreelanceAccounts] = useState({});
  const [newPlatform, setNewPlatform] = useState({ name: '', config: {} });
  const [newAccount, setNewAccount] = useState({ name: '', url: '' });
  const [walletAddress, setWalletAddress] = useState('');
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const connectMetaMask = async () => {
      const provider = await detectEthereumProvider();
      if (provider) {
        const accounts = await provider.request({ method: 'eth_requestAccounts' });
        setWalletAddress(accounts[0]);
      }
    };
    connectMetaMask();

    const fetchSettings = async () => {
      try {
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
  }, [token]);

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
      await axios.put(
        'http://127.0.0.1:8000/users/me',
        {
          social_media_configs: socialMedia,
          freelance_accounts: freelanceAccounts,
          wallet_address: walletAddress
        },
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
    <div>
      <h1>Settings</h1>
      {errors.fetch && <p style={{ color: 'red' }}>{errors.fetch}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}
      <h2>Wallet</h2>
      <p>MetaMask Address: {walletAddress || 'Not connected'}</p>
      <h2>Social Media</h2>
      {Object.entries(socialMedia).map(([platform, config]) => (
        <div key={platform}>
          <h3>{platform}</h3>
          {Object.entries(config).map(([key, value]) => (
            <input
              key={key}
              placeholder={`${key}`}
              value={value}
              onChange={(e) => setSocialMedia({
                ...socialMedia,
                [platform]: { ...config, [key]: e.target.value }
              })}
            />
          ))}
          <button onClick={() => deletePlatform(platform)} style={{ background: 'red' }}>Delete</button>
        </div>
      ))}
      <h3>Add New Platform</h3>
      <input
        placeholder="Platform Name"
        value={newPlatform.name}
        onChange={(e) => setNewPlatform({ ...newPlatform, name: e.target.value })}
      />
      {errors.platformName && <p style={{ color: 'red' }}>{errors.platformName}</p>}
      <input
        placeholder="Key (e.g., api_key)"
        onChange={(e) => setNewPlatform({
          ...newPlatform,
          config: { ...newPlatform.config, [e.target.placeholder.split(' ')[0].toLowerCase()]: '' }
        })}
      />
      <input
        placeholder="Value"
        onChange={(e) => {
          const key = Object.keys(newPlatform.config)[Object.keys(newPlatform.config).length - 1];
          setNewPlatform({
            ...newPlatform,
            config: { ...newPlatform.config, [key]: e.target.value }
          });
        }}
      />
      {errors.platformConfig && <p style={{ color: 'red' }}>{errors.platformConfig}</p>}
      <button onClick={addPlatform}>Add Platform</button>
      <h2>Freelance Accounts</h2>
      {Object.entries(freelanceAccounts).map(([name, url]) => (
        <div key={name}>
          <input
            placeholder={name}
            value={url}
            onChange={(e) => setFreelanceAccounts({ ...freelanceAccounts, [name]: e.target.value })}
          />
          <button onClick={() => deleteAccount(name)} style={{ background: 'red' }}>Delete</button>
        </div>
      ))}
      <h3>Add New Account</h3>
      <input
        placeholder="Account Name"
        value={newAccount.name}
        onChange={(e) => setNewAccount({ ...newAccount, name: e.target.value })}
      />
      {errors.accountName && <p style={{ color: 'red' }}>{errors.accountName}</p>}
      <input
        placeholder="URL"
        value={newAccount.url}
        onChange={(e) => setNewAccount({ ...newAccount, url: e.target.value })}
      />
      {errors.accountUrl && <p style={{ color: 'red' }}>{errors.accountUrl}</p>}
      <button onClick={addAccount}>Add Account</button>
      <button onClick={updateSettings}>Save Settings</button>
      {errors.save && <p style={{ color: 'red' }}>{errors.save}</p>}
    </div>
  );
}

export default Settings;