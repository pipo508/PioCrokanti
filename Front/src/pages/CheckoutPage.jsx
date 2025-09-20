// src/pages/CheckoutPage.jsx

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import api from '../services/api';
import styles from './CheckoutPage.module.css';

export default function CheckoutPage() {
  const { cartItems } = useCart();
  const navigate = useNavigate();
  
  const [paymentMethod, setPaymentMethod] = useState('efectivo');
  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    telefono: '',
    direccion: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const userData = {
      nombre: formData.nombre,
      apellido: formData.apellido,
      telefono: formData.telefono,
      direccion: formData.direccion,
    };
    const items = cartItems.map(item => ({
      product_id: item.id,
      cantidad: item.quantity,
    }));
    
    const payload = { json: { user: userData, items: items } };

    try {
      if (paymentMethod === 'efectivo') {
        // --- FLUJO PARA PAGO EN EFECTIVO ---
        await api.post('/orders/cash-order', payload);
        alert('¡Pedido realizado con éxito! Pagarás al recibirlo.');
        // clearCart(); // Futura mejora
        navigate('/');
      } else {
        // --- FLUJO PARA MERCADO PAGO ---
        const response = await api.post('/orders/initiate-payment', payload);
        const preference = response.data;
        console.log("Respuesta del backend (preference):", preference); 

        // Redirigimos al usuario al checkout de Mercado Pago
        window.location.href = preference.init_point;
      }
    } catch (error) {
      console.error('Error al procesar el pedido:', error);
      alert('Hubo un error al procesar el pedido.');
    }
  };

  return (
    <div className={styles.checkoutContainer}>
      <h1 className={styles.title}>Datos y Método de Pago</h1>
      <form onSubmit={handleSubmit} className={styles.form}>
        {/* ... (Tus inputs para nombre, apellido, etc. se mantienen igual) ... */}
        <div className={styles.formGroup}>
          <label htmlFor="nombre">Nombre</label>
          <input type="text" id="nombre" name="nombre" value={formData.nombre} onChange={handleChange} required />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="apellido">Apellido</label>
          <input type="text" id="apellido" name="apellido" value={formData.apellido} onChange={handleChange} required />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="telefono">Teléfono</label>
          <input type="tel" id="telefono" name="telefono" value={formData.telefono} onChange={handleChange} required />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="direccion">Dirección de Entrega</label>
          <input type="text" id="direccion" name="direccion" value={formData.direccion} onChange={handleChange} required />
        </div>
        
        {/* --- NUEVA SECCIÓN DE PAGO --- */}
        <div className={styles.paymentOptions}>
          <h3>Selecciona un método de pago</h3>
          <div 
            onClick={() => setPaymentMethod('efectivo')} 
            className={`${styles.paymentOption} ${paymentMethod === 'efectivo' ? styles.selected : ''}`}
          >
            <input type="radio" id="efectivo" name="paymentMethod" value="efectivo" checked={paymentMethod === 'efectivo'} readOnly />
            <label htmlFor="efectivo">Efectivo (Pagas al recibir)</label>
          </div>
          <br/>
          <div 
            onClick={() => setPaymentMethod('mp')}
            className={`${styles.paymentOption} ${paymentMethod === 'mp' ? styles.selected : ''}`}
          >
            <input type="radio" id="mp" name="paymentMethod" value="mp" checked={paymentMethod === 'mp'} readOnly />
            <label htmlFor="mp">Mercado Pago (Tarjeta de débito/crédito, etc.)</label>
          </div>
        </div>
        
        <button type="submit" className={styles.submitButton}>
          {paymentMethod === 'efectivo' ? 'Finalizar Pedido' : 'Pagar con Mercado Pago'}
        </button>
      </form>
    </div>
  );
}