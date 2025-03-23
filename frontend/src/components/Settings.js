// frontend/src/components/Settings.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import detectEthereumProvider from '@metamask/detect-provider';

function Settings({ token }) {
  const [socialMedia, setSocialMedia] = useState({ twitter: {}, linkedin: {}, instagram: {} });
  const [freelanceAccounts, setFreelanceAccounts] = useState({ freelancer: '', fiverr: '', portfolio: '' });
  const [walletAddress, setWalletAddress] = useState('');

  useEffect(() => {
    const connectMetaMask = async () => {
      const provider = await detectEthereumProvider();
      if (provider) {
        const accounts = await provider.request({ method: 'eth_requestAccounts' });
        setWalletAddress(accounts[0]);
      }
    };
    connectMetaMask();
  }, []);

  const updateSettings = async () => {
    await axios.put(
      'http://127.0.0.1:8000/users/me',
      {
        social_media_configs: socialMedia,
        freelance_accounts: freelanceAccounts,
        wallet_address: walletAddress
      },
      { headers: { Authorization: `Bearer ${token}` } }
    );
  };

  return (
    <div>
      <h1>Settings</h1>
      <h2>Wallet</h2>
      <p>MetaMask Address: {walletAddress || 'Not connected'}</p>
      <h2>Social Media</h2>
      {/* Existing social media inputs */}
      <h2>Freelance Accounts</h2>
      {/* Existing freelance account inputs */}
      <button onClick={updateSettings}>Save Settings</button>
    </div>
  );
}

export default Settings;