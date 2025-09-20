// src/pages/CheckoutPage.jsx

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import api from '../services/api';
import styles from './CheckoutPage.module.css';

function CheckoutPage() {
  const { cartItems, clearCart } = useCart();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    telefono: '',
    direccion: '',
  });

  const [paymentMethod, setPaymentMethod] = useState('efectivo'); // Estado para el método de pago

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handlePaymentChange = (e) => {
    setPaymentMethod(e.target.value);
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

    const orderData = {
      user: userData,
      items: items,
      payment_method: paymentMethod, // Incluir método de pago
    };

    try {
      await api.post('/orders/', orderData);
      alert('¡Pedido realizado con éxito!');
      clearCart(); 
      navigate('/'); 
    } catch (error) {
      console.error('Error al crear el pedido:', error);
      const errorMessage = error.response?.data?.error || 'Hubo un error al realizar el pedido.';
      alert(errorMessage);
    }
  };

  return (
    <div className={styles.checkoutContainer}>
      <h1 className={styles.title}>Datos de Entrega y Pago</h1>
      <form onSubmit={handleSubmit} className={styles.form}>
        {/* --- Datos del Cliente --- */}
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

        {/* --- Método de Pago --- */}
        <div className={styles.paymentMethod}>
          <h2>Método de Pago</h2>
          <div className={styles.paymentOptions}>
            <div className={styles.option}>
              <input type="radio" id="efectivo" name="paymentMethod" value="efectivo" checked={paymentMethod === 'efectivo'} onChange={handlePaymentChange} />
              <label htmlFor="efectivo">Efectivo en el local</label>
            </div>
            <div className={styles.option}>
              <input type="radio" id="transferencia" name="paymentMethod" value="transferencia" checked={paymentMethod === 'transferencia'} onChange={handlePaymentChange} />
              <label htmlFor="transferencia">Transferencia Bancaria</label>
            </div>
            <div className={styles.option}>
              <input type="radio" id="mp" name="paymentMethod" value="mp" checked={paymentMethod === 'mp'} onChange={handlePaymentChange} />
              <label htmlFor="mp">Link de Pago (Mercado Pago)</label>
            </div>
          </div>
        </div>

        <button type="submit" className={styles.submitButton}>
          Finalizar Pedido
        </button>
      </form>
    </div>
  );
}

export default CheckoutPage;
