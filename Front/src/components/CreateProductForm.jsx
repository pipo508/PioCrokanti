// src/components/CreateProductForm.jsx

import { useState, useEffect } from 'react';
import api from '../services/api';
import styles from './CreateProductForm.module.css';

export default function CreateProductForm({ onProductCreated }) {
  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    precio: '',
    cantidad_personas: 1,
    category_id: '',
    imagen_url: ''
  });
  const [categories, setCategories] = useState([]);
  const [loadingCategories, setLoadingCategories] = useState(true);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await api.get('/categories/active');
        setCategories(response.data);
        if (response.data.length > 0) {
          setFormData(prev => ({ ...prev, category_id: response.data[0].id }));
        }
      } catch (error) {
        console.error("Error al cargar categorías", error);
      } finally {
        setLoadingCategories(false);
      }
    };
    fetchCategories();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.category_id) {
      alert('Por favor, crea una categoría activa antes de añadir un producto.');
      return;
    }
    try {
      const productData = { 
        ...formData, 
        precio: parseFloat(formData.precio), 
        cantidad_personas: parseInt(formData.cantidad_personas),
        category_id: parseInt(formData.category_id)
      };
      await api.post('/products', productData);
      alert('Producto creado con éxito');
      setFormData({
        nombre: '',
        descripcion: '',
        precio: '',
        cantidad_personas: 1,
        category_id: categories.length > 0 ? categories[0].id : '',
        imagen_url: ''
      });
      onProductCreated();
    } catch (error) {
      alert('Error al crear el producto.');
      console.error(error);
    }
  };

  return (
    <div className={styles.formContainer}>
      <h2>Crear Nuevo Producto</h2>
      <form onSubmit={handleSubmit} className={styles.form}>
        {/* Form fields... */}
        <div className={styles.formGroup}>
          <label>Categoría</label>
          <select name="category_id" value={formData.category_id} onChange={handleChange} required disabled={loadingCategories || categories.length === 0}>
            {loadingCategories ? (
              <option>Cargando categorías...</option>
            ) : categories.length === 0 ? (
              <option>No hay categorías activas</option>
            ) : (
              categories.map(cat => (
                <option key={cat.id} value={cat.id}>{cat.nombre}</option>
              ))
            )}
          </select>
        </div>
        {/* Other form fields... */}
        <div className={styles.formGroup}>
          <label>Nombre</label>
          <input type="text" name="nombre" value={formData.nombre} onChange={handleChange} required />
        </div>
        <div className={styles.formGroup}>
          <label>Descripción</label>
          <textarea name="descripcion" value={formData.descripcion} onChange={handleChange}></textarea>
        </div>
        <div className={styles.formGroup}>
          <label>Precio</label>
          <input type="number" name="precio" value={formData.precio} onChange={handleChange} required step="0.01" />
        </div>
        <div className={styles.formGroup}>
          <label>Cantidad de Personas</label>
          <input type="number" name="cantidad_personas" value={formData.cantidad_personas} onChange={handleChange} required min="1" />
        </div>
        <div className={styles.formGroup}>
          <label>URL de la Imagen (Opcional)</label>
          <input type="text" name="imagen_url" value={formData.imagen_url} onChange={handleChange} />
        </div>
        <button type="submit" className={styles.submitButton} disabled={loadingCategories || categories.length === 0}>
          Crear Producto
        </button>
      </form>
    </div>
  );
}