import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Products({ token }) {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const res = await axios.get('http://localhost:8003/products', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setProducts(res.data.products || []);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchProducts();
    }, [token]);

    if (loading) return <p className="loading">Yükleniyor...</p>;

    return (
        <div className="card">
            <h3>Ürünler</h3>
            {products.length === 0 ? (
                <p style={{ color: '#888' }}>Henüz ürün yok.</p>
            ) : (
                <div className="product-grid">
                    {products.map((p) => (
                        <div className="product-card" key={p.id}>
                            <h4>{p.name}</h4>
                            <p style={{ color: '#aaa', fontSize: '12px', marginBottom: '8px' }}>{p.description}</p>
                            <p className="price">{p.price} ₺</p>
                            <p className="stock">Stok: {p.stock}</p>
                            <p style={{ color: '#888', fontSize: '11px' }}>{p.category}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default Products;