// src/pages/CheckoutPage.jsx

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import api from '../services/api';
import styles from './CheckoutPage.module.css';

// The function is declared here
function CheckoutPage() {
  const { cartItems } = useCart();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    telefono: '',
    direccion: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
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
    };

    try {
      const response = await api.post('/orders/', orderData);
      alert('¡Pedido realizado con éxito!');
      // clearCart(); 
      navigate('/'); 
    } catch (error) {
      console.error('Error al crear el pedido:', error);
      const errorMessage = error.response?.data?.error || 'Hubo un error al realizar el pedido.';
      alert(errorMessage);
    }
  };

  return (
    <div className={styles.checkoutContainer}>
      <h1 className={styles.title}>Datos de Entrega</h1>
      <form onSubmit={handleSubmit} className={styles.form}>
        {/* Form groups go here... */}
        <div className={styles.formGroup}>
          <label htmlFor="nombre">Nombre</label>
          <input
            type="text"
            id="nombre"
            name="nombre"
            value={formData.nombre}
            onChange={handleChange}
            required
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="apellido">Apellido</label>
          <input
            type="text"
            id="apellido"
            name="apellido"
            value={formData.apellido}
            onChange={handleChange}
            required
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="telefono">Teléfono</label>
          <input
            type="tel"
            id="telefono"
            name="telefono"
            value={formData.telefono}
            onChange={handleChange}
            required
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="direccion">Dirección de Entrega</label>
          <input
            type="text"
            id="direccion"
            name="direccion"
            value={formData.direccion}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className={styles.submitButton}>
          Finalizar Pedido
        </button>
      </form>
    </div>
  );
}

// And the export statement is at the end
export default CheckoutPage;