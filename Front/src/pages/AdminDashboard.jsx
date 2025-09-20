// src/pages/AdminDashboard.jsx

import { useState, useEffect } from 'react';
import api from '../services/api';
import styles from './AdminDashboard.module.css';

export default function AdminDashboard() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const response = await api.get('/orders/');
      // Ordenamos los pedidos para que los más nuevos aparezcan primero
      setOrders(response.data.sort((a, b) => b.id - a.id));
    } catch (err) {
      setError('No se pudieron cargar los pedidos.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // --- FUNCIÓN NUEVA ---
  const handleStatusChange = async (orderId, newStatus) => {
    try {
      // Llamamos al nuevo endpoint del backend
      await api.put(`/orders/${orderId}/status`, { estado: newStatus });

      // Actualizamos el estado localmente para que el cambio se vea al instante
      setOrders((prevOrders) =>
        prevOrders.map((order) =>
          order.id === orderId ? { ...order, estado: newStatus } : order
        )
      );
    } catch (err) {
      console.error("Error al actualizar el estado:", err);
      alert("No se pudo actualizar el estado del pedido.");
    }
  };

  if (loading) return <div className={styles.loading}>Cargando pedidos...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles.dashboardContainer}>
      <h1 className={styles.title}>Panel de Pedidos</h1>
      <table className={styles.ordersTable}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>Dirección</th>
            <th>Total</th>
            <th>Fecha</th>
            <th>Estado</th>
            <th>Acciones</th> {/* <-- Nueva columna */}
          </tr>
        </thead>
        <tbody>
          {orders.map((order) => (
            <tr key={order.id}>
              <td>{order.id}</td>
              <td>{order.user.nombre_completo}</td>
              <td>{order.direccion_entrega}</td>
              <td>${order.total.toFixed(2)}</td>
              <td>{new Date(order.created_at).toLocaleDateString()}</td>
              <td>
                <span className={styles[`status${order.estado.replace(' ', '')}`] || styles.statusRecibido}>
                  {order.estado}
                </span>
              </td>
              {/* --- NUEVO TD CON EL SELECT --- */}
              <td>
                <select 
                  value={order.estado} 
                  onChange={(e) => handleStatusChange(order.id, e.target.value)}
                >
                  <option value="Recibido">Recibido</option>
                  <option value="En preparación">En preparación</option>
                  <option value="Entregado">Entregado</option>
                  <option value="Cancelado">Cancelado</option>
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}