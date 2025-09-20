// src/pages/AdminDashboard.jsx

import { useState, useEffect } from 'react';
import api from '../services/api';
import styles from './AdminDashboard.module.css';

export default function AdminDashboard() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await api.get('/orders/');
        setOrders(response.data);
      } catch (err) {
        setError('No se pudieron cargar los pedidos.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, []);

  if (loading) {
    return <div className={styles.loading}>Cargando pedidos...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  return (
    <div className={styles.dashboardContainer}>
      <h1 className={styles.title}>Panel de Pedidos</h1>
      <table className={styles.ordersTable}>
        <thead>
          <tr>
            <th>ID Pedido</th>
            <th>Cliente</th>
            <th>Dirección</th>
            <th>Total</th>
            <th>Estado</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order) => (
            <tr key={order.id}>
              <td>{order.id}</td>
              <td>{order.user ? order.user.nombre_completo : 'Usuario no disponible'}</td>
              <td>{order.direccion_entrega}</td>
              <td>${order.total.toFixed(2)}</td>
              <td>
                <span className={styles.statusRecibido}>{order.estado}</span>
              </td>
              <td>
                {new Date(order.created_at).toLocaleDateString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
