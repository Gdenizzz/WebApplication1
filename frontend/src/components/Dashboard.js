import React, { useState } from 'react';
import Products from './Products';
import Orders from './Orders';
import CreateOrder from './CreateOrder';

function Dashboard({ token, onLogout }) {
    const [page, setPage] = useState('products');

    return (
        <div className="dashboard">
            <div className="navbar">
                <h2>🛒 Microservices App</h2>
                <div className="nav-buttons">
                    <button
                        className={page === 'products' ? 'active' : ''}
                        onClick={() => setPage('products')}
                    >
                        Ürünler
                    </button>
                    <button
                        className={page === 'orders' ? 'active' : ''}
                        onClick={() => setPage('orders')}
                    >
                        Siparişlerim
                    </button>
                    <button
                        className={page === 'create-order' ? 'active' : ''}
                        onClick={() => setPage('create-order')}
                    >
                        Sipariş Oluştur
                    </button>
                    <button className="btn-danger" onClick={onLogout}>
                        Çıkış
                    </button>
                </div>
            </div>
            <div className="content">
                {page === 'products' && <Products token={token} />}
                {page === 'orders' && <Orders token={token} />}
                {page === 'create-order' && <CreateOrder token={token} onSuccess={() => setPage('orders')} />}
            </div>
        </div>
    );
}

export default Dashboard;