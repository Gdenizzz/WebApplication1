import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Monitoring({ token }) {
  const [stats, setStats] = useState(null);
  const [services, setServices] = useState([]);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await axios.get('http://localhost:8003/logs', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const logs = res.data;
        const uniqueUsers = [...new Set(logs.map((l) => l.user))].length;
        const errors = logs.filter((l) => l.status !== 200).length;
        setStats({ total: logs.length, uniqueUsers, errors });
      } catch (err) {
        console.error(err);
      }
    };

    const checkServices = async () => {
      const serviceList = [
        { name: 'Dispatcher', url: 'http://localhost:8003/health' },
      ];
      const results = await Promise.all(
        serviceList.map(async (s) => {
          try {
            const res = await axios.get(s.url);
            return {
              name: s.name,
              status: res.data.status === 'ok' ? 'online' : 'offline',
            };
          } catch {
            return { name: s.name, status: 'offline' };
          }
        })
      );
      setServices(results);
    };

    fetchStats();
    checkServices();
  }, [token]);

  return (
    <div>
      <div className="card">
        <h3>Servis Durumlari</h3>
        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', marginTop: '8px' }}>
          {services.map((s, i) => (
            <div key={i} style={{
              background: '#0f0f1a',
              border: s.status === 'online' ? '1px solid #5ce05c' : '1px solid #e05c5c',
              borderRadius: '8px',
              padding: '12px 20px',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
            }}>
              <div style={{
                width: '10px',
                height: '10px',
                borderRadius: '50%',
                background: s.status === 'online' ? '#5ce05c' : '#e05c5c',
              }} />
              <span>{s.name}</span>
              <span style={{ color: s.status === 'online' ? '#5ce05c' : '#e05c5c', fontSize: '12px' }}>
                {s.status}
              </span>
            </div>
          ))}
        </div>
      </div>

      {stats && (
        <div className="card">
          <h3>Trafik Istatistikleri</h3>
          <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', marginTop: '8px' }}>
            <div style={{ background: '#0f0f1a', borderRadius: '8px', padding: '16px 24px', border: '1px solid #2a2a4a', textAlign: 'center' }}>
              <p style={{ color: '#7c83fd', fontSize: '28px', fontWeight: 'bold' }}>{stats.total}</p>
              <p style={{ color: '#aaa', fontSize: '13px' }}>Toplam Istek</p>
            </div>
            <div style={{ background: '#0f0f1a', borderRadius: '8px', padding: '16px 24px', border: '1px solid #2a2a4a', textAlign: 'center' }}>
              <p style={{ color: '#f5a623', fontSize: '28px', fontWeight: 'bold' }}>{stats.uniqueUsers}</p>
              <p style={{ color: '#aaa', fontSize: '13px' }}>Benzersiz Kullanici</p>
            </div>
            <div style={{ background: '#0f0f1a', borderRadius: '8px', padding: '16px 24px', border: '1px solid #2a2a4a', textAlign: 'center' }}>
              <p style={{ color: '#e05c5c', fontSize: '28px', fontWeight: 'bold' }}>{stats.errors}</p>
              <p style={{ color: '#aaa', fontSize: '13px' }}>Hatali Istek</p>
            </div>
          </div>
        </div>
      )}

      <div className="card">
        <h3>Izleme Araclari</h3>
        <div style={{ display: 'flex', gap: '12px', marginTop: '8px' }}>
          <a href="http://localhost:3000" target="_blank" rel="noreferrer"
            style={{ background: '#f5a623', color: '#0f0f1a', padding: '12px 24px', borderRadius: '8px', textDecoration: 'none', fontWeight: 'bold', fontSize: '14px' }}>
            Grafana Dashboard
          </a>
          <a href="http://localhost:8089" target="_blank" rel="noreferrer"
            style={{ background: '#5ce05c', color: '#0f0f1a', padding: '12px 24px', borderRadius: '8px', textDecoration: 'none', fontWeight: 'bold', fontSize: '14px' }}>
            Locust Yuk Testi
          </a>
        </div>
      </div>
    </div>
  );
}

export default Monitoring;