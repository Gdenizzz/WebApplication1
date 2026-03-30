import React, { useState } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [page, setPage] = useState('login');

  const handleLogin = (token) => {
    localStorage.setItem('token', token);
    setToken(token);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setPage('login');
  };

  if (token) {
    return <Dashboard token={token} onLogout={handleLogout} />;
  }

  return (
    <div className="app">
      <div className="auth-container">
        <h1>🛒 Microservices App</h1>
        <div className="tab-buttons">
          <button
            className={page === 'login' ? 'active' : ''}
            onClick={() => setPage('login')}
          >
            Giriş Yap
          </button>
          <button
            className={page === 'register' ? 'active' : ''}
            onClick={() => setPage('register')}
          >
            Kayıt Ol
          </button>
        </div>
        {page === 'login' ? (
          <Login onLogin={handleLogin} />
        ) : (
          <Register onRegister={() => setPage('login')} />
        )}
      </div>
    </div>
  );
}

export default App;