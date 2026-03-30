import React, { useState, useEffect } from 'react';
import axios from 'axios';

function CreateOrder({ token, onSuccess }) {
    const [products, setProducts] = useState([]);
    const [items, setItems] = useState([]);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const res = await axios.get('http://localhost:8003/products', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setProducts(res.data.products || []);
            } catch (err) {
                console.error(err);
            }
        };
        fetchProducts();
    }, [token]);

    const handleQuantityChange = (productId, quantity) => {
        const existing = items.find((i) => i.product_id === productId);
        if (quantity === 0) {
            setItems(items.filter((i) => i.product_id !== productId));
        } else if (existing) {
            setItems(items.map((i) =>
                i.product_id === productId ? { ...i, quantity } : i
            ));
        } else {
            setItems([...items, { product_id: productId, quantity }]);
        }
    };

    const handleSubmit = async () => {
        setError('');
        setSuccess('');
        if (items.length === 0) {
            setError('En az bir ürün seçmelisiniz.');
            return;
        }
        try {
            await axios.post(
                'http://localhost:8003/orders',
                { items },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            setSuccess('Sipariş oluşturuldu!');
            setTimeout(() => onSuccess(), 1500);
        } catch (err) {
            setError('Sipariş oluşturulamadı.');
        }
    };

    return (
        <div className="card">
            <h3>Sipariş Oluştur</h3>
            <div className="order-form">
                {products.map((p) => {
                    const item = items.find((i) => i.product_id === p.id);
                    const quantity = item ? item.quantity : 0;
                    return (
                        <div className="product-card" key={p.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <div>
                                <h4>{p.name}</h4>
                                <p className="price">{p.price} ₺</p>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                                <button
                                    className="btn btn-secondary"
                                    style={{ width: '32px', padding: '4px' }}
                                    onClick={() => handleQuantityChange(p.id, Math.max(0, quantity - 1))}
                                >
                                    -
                                </button>
                                <span style={{ minWidth: '24px', textAlign: 'center' }}>{quantity}</span>
                                <button
                                    className="btn"
                                    style={{ width: '32px', padding: '4px' }}
                                    onClick={() => handleQuantityChange(p.id, quantity + 1)}
                                >
                                    +
                                </button>
                            </div>
                        </div>
                    );
                })}
                {error && <p className="error">{error}</p>}
                {success && <p className="success">{success}</p>}
                <button className="btn" onClick={handleSubmit}>Siparişi Tamamla</button>
            </div>
        </div>
    );
}

export default CreateOrder;