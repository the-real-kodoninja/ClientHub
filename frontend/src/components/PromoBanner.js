// frontend/src/components/PromoBanner.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function PromoBanner() {
  const [promo, setPromo] = useState({ message: '', links: {} });

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/promotions/?context=general')
      .then(response => setPromo(response.data))
      .catch(error => console.error('Error fetching promo:', error));
  }, []);

  return (
    <div style={{ background: '#4a7048', color: '#f5f5f0', padding: '10px', textAlign: 'center' }}>
      <p>{promo.message}</p>
      {Object.entries(promo.links).map(([name, url]) => (
        <span key={name}>
          <a href={url} target="_blank" rel="noopener noreferrer">{name}</a> | 
        </span>
      ))}
    </div>
  );
}

export default PromoBanner;