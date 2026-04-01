import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Logs({ token }) {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const res = await axios.get('http://localhost:8003/logs', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setLogs(res.data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchLogs();
    }, [token]);

    if (loading) return <p className="loading">Yükleniyor...</p>;

    return (
        <div className="card">
            <h3>Trafik Logları</h3>
            {logs.length === 0 ? (
                <p style={{ color: '#888' }}>Henüz log yok.</p>
            ) : (
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px' }}>
                    <thead>
                        <tr style={{ borderBottom: '1px solid #2a2a4a', color: '#aaa' }}>
                            <th style={{ padding: '8px', textAlign: 'left' }}>Zaman</th>
                            <th style={{ padding: '8px', textAlign: 'left' }}>Method</th>
                            <th style={{ padding: '8px', textAlign: 'left' }}>Path</th>
                            <th style={{ padding: '8px', textAlign: 'left' }}>Kullanıcı</th>
                            <th style={{ padding: '8px', textAlign: 'left' }}>Rol</th>
                            <th style={{ padding: '8px', textAlign: 'left' }}>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {logs.map((log, i) => (
                            <tr key={i} style={{ borderBottom: '1px solid #1a1a2e' }}>
                                <td style={{ padding: '8px', color: '#888' }}>
                                    {new Date(log.timestamp).toLocaleString('tr-TR')}
                                </td>
                                <td style={{ padding: '8px' }}>
                                    <span style={{
                                        color: log.method === 'GET' ? '#7c83fd' : '#f5a623',
                                        fontWeight: 'bold'
                                    }}>
                                        {log.method}
                                    </span>
                                </td>
                                <td style={{ padding: '8px', color: '#e0e0e0' }}>{log.path}</td>
                                <td style={{ padding: '8px', color: '#aaa' }}>{log.user}</td>
                                <td style={{ padding: '8px', color: log.role === 'admin' ? '#f5a623' : '#7c83fd' }}>
                                    {log.role}
                                </td>
                                <td style={{ padding: '8px' }}>
                                    <span style={{ color: log.status === 200 ? '#5ce05c' : '#e05c5c' }}>
                                        {log.status}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default Logs;