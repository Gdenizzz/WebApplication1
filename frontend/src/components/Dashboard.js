import React, { useState, useEffect } from 'react';
import Products from './Products';
import Orders from './Orders';
import CreateOrder from './CreateOrder';
import AddProduct from './AddProduct';
import { jwtDecode } from 'jwt-decode';

function Dashboard({ token, onLogout }) {
    const [page, setPage] = useState('products');
    const [role, setRole] = useState('customer');
    const [email, setEmail] = useState('');

    useEffect(() => {
        try {
            const decoded = jwtDecode(token);
            setRole(decoded.role);
            setEmail(decoded.email);
        } catch (e) {
            setRole('customer');
        }
    }, [token]);

    return (
        <div className="dashboard">
            <div className="navbar">
                <h2>Microservices App</h2>
                <div className="nav-buttons">
                    <button
                        className={page === 'products' ? 'active' : ''}
                        onClick={() => setPage('products')}
                    >
                        Urunler
                    </button>
                    {role === 'admin' && (
                        <button
                            className={page === 'add-product' ? 'active' : ''}
                            onClick={() => setPage('add-product')}
                        >
                            Urun Ekle
                        </button>
                    )}
                    <button
                        className={page === 'orders' ? 'active' : ''}
                        onClick={() => setPage('orders')}
                    >
                        Siparislerim
                    </button>
                    <button
                        className={page === 'create-order' ? 'active' : ''}
                        onClick={() => setPage('create-order')}
                    >
                        Siparis Olustur
                    </button>
                    <div style={{ color: '#aaa', fontSize: '13px', display: 'flex', flexDirection: 'column', alignItems: 'flex-end', marginRight: '8px' }}>
                        <span style={{ color: '#e0e0e0' }}>{email}</span>
                        <span style={{ color: role === 'admin' ? '#f5a623' : '#7c83fd' }}>{role}</span>
                    </div>
                    <button className="btn-danger" onClick={onLogout}>
                        Cikis
                    </button>
                </div>
            </div>
            <div className="content">
                {page === 'products' && <Products token={token} />}
                {page === 'add-product' && role === 'admin' && <AddProduct token={token} onSuccess={() => setPage('products')} />}
                {page === 'orders' && <Orders token={token} />}
                {page === 'create-order' && <CreateOrder token={token} onSuccess={() => setPage('orders')} />}
            </div>
        </div>
    );
}

export default Dashboard;