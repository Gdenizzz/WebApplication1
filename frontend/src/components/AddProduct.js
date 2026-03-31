import React, { useState } from 'react';
import axios from 'axios';

function AddProduct({ token, onSuccess }) {
    const [form, setForm] = useState({
        name: '',
        description: '',
        price: '',
        stock: '',
        category: '',
        is_active: true,
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleChange = (e) => {
        const value = e.target.name === 'is_active' ? e.target.checked : e.target.value;
        setForm({ ...form, [e.target.name]: value });
    };

    const handleSubmit = async () => {
        setError('');
        setSuccess('');
        try {
            await axios.post(
                'http://localhost:8003/products',
                {
                    ...form,
                    price: parseFloat(form.price),
                    stock: parseInt(form.stock),
                },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            setSuccess('Ürün başarıyla eklendi!');
            setForm({ name: '', description: '', price: '', stock: '', category: '', is_active: true });
            setTimeout(() => onSuccess(), 1500);
        } catch (err) {
            if (err.response?.status === 403) {
                setError('Bu işlem için admin yetkisi gerekiyor.');
            } else {
                setError('Ürün eklenemedi.');
            }
        }
    };

    return (
        <div className="card">
            <h3>Ürün Ekle</h3>
            <div className="form-group">
                <label>Ürün Adı</label>
                <input type="text" name="name" value={form.name} onChange={handleChange} placeholder="Ürün adı" />
            </div>
            <div className="form-group">
                <label>Açıklama</label>
                <input type="text" name="description" value={form.description} onChange={handleChange} placeholder="Açıklama" />
            </div>
            <div className="form-group">
                <label>Fiyat</label>
                <input type="number" name="price" value={form.price} onChange={handleChange} placeholder="0.00" />
            </div>
            <div className="form-group">
                <label>Stok</label>
                <input type="number" name="stock" value={form.stock} onChange={handleChange} placeholder="0" />
            </div>
            <div className="form-group">
                <label>Kategori</label>
                <input type="text" name="category" value={form.category} onChange={handleChange} placeholder="Kategori" />
            </div>
            {error && <p className="error">{error}</p>}
            {success && <p className="success">{success}</p>}
            <button className="btn" onClick={handleSubmit}>Ürün Ekle</button>
        </div>
    );
}

export default AddProduct;