import React, { useState } from 'react';
import axios from 'axios';

function Register({ onRegister }) {
    const [form, setForm] = useState({
        email: '',
        password: '',
        full_name: '',
        role: 'customer',
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        try {
            await axios.post('http://localhost:8003/auth/register', form);
            setSuccess('Kayıt başarılı! Giriş yapabilirsiniz.');
            setTimeout(() => onRegister(), 1500);
        } catch (err) {
            setError('Kayıt başarısız. Bu email zaten kayıtlı olabilir.');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="form-group">
                <label>Ad Soyad</label>
                <input
                    type="text"
                    name="full_name"
                    value={form.full_name}
                    onChange={handleChange}
                    placeholder="İsim Soyisim"
                />
            </div>
            <div className="form-group">
                <label>Email</label>
                <input
                    type="email"
                    name="email"
                    value={form.email}
                    onChange={handleChange}
                    placeholder="email@example.com"
                    required
                />
            </div>
            <div className="form-group">
                <label>Şifre</label>
                <input
                    type="password"
                    name="password"
                    value={form.password}
                    onChange={handleChange}
                    placeholder="••••••••"
                    required
                />
            </div>
            {error && <p className="error">{error}</p>}
            {success && <p className="success">{success}</p>}
            <button type="submit" className="btn">Kayıt Ol</button>
        </form>
    );
}

export default Register;