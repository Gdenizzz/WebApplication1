import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Orders({ token }) {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const res = await axios.get('http://localhost:8003/orders', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setOrders(res.data.orders || []);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchOrders();
    }, [token]);

    if (loading) return <p className="loading">Yükleniyor...</p>;

    return (
        <div className="card">
            <h3>Siparişlerim</h3>
            {orders.length === 0 ? (
                <p style={{ color: '#888' }}>Henüz sipariş yok.</p>
            ) : (
                orders.map((o) => (
                    <div className="order-item" key={o.id}>
                        <p className="order-id">Sipariş ID: {o.id}</p>
                        <p>Durum: <span style={{ color: '#7c83fd' }}>{o.status}</span></p>
                        <p className="order-total">Toplam: {o.total_price} ₺</p>
                        <div style={{ marginTop: '8px' }}>
                            {o.items.map((item, i) => (
                                <p key={i} style={{ color: '#aaa', fontSize: '13px' }}>
                                    {item.product_name} x{item.quantity} — {item.line_total} ₺
                                </p>
                            ))}
                        </div>
                    </div>
                ))
            )}
        </div>
    );
}

export default Orders;