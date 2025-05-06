import React from 'react';
import Registration from './components/Registration';

import './App.css';



function App() {
  const handleLogin = async (username, password) => {
    const response = await fetch('http://localhost:8080/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
      credentials: 'include', // including cookies for session management, this should mark start of session
      });
    
      if (response.ok) {
        await response.json();
        console.log('logged success');
      } else {
        console.error('login fail');
      }
    };

    const handleLogout = async () => {
      const response = await fetch ('http://localhost:8080/logout', {
        method: 'POST',
        credentials: 'include', // should mark end of session
      });

      if (response.ok) {
        console.log('logout success');
      } else {
        console.error('logout fail');
      }
    };

  return (
    <div>
      <h1>Matilda Tech Coding Test</h1>
      <Registration onLogin={handleLogin} onLogout={handleLogout} />
    </div>
  );
};

export default App;
