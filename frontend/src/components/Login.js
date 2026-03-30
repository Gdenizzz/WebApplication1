import React, { useState } from 'react';
import axios from 'axios';

function Login({ onLogin }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const res = await axios.post('http://localhost:8000/auth/login', {
                email,
                password,
            });
            onLogin(res.data.access_token);
        } catch (err) {
            setError('Email veya şifre hatalı.');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="form-group">
                <label>Email</label>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="email@example.com"
                    required
                />
            </div>
            <div className="form-group">
                <label>Şifre</label>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                />
            </div>
            {error && <p className="error">{error}</p>}
            <button type="submit" className="btn">Giriş Yap</button>
        </form>
    );
}

export default Login;