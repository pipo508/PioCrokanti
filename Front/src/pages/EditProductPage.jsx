// src/pages/EditProductPage.jsx

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import styles from './AdminDashboard.module.css'; // Reutilizamos los estilos
import formStyles from '../components/CreateProductForm.module.css'; // Reutilizamos estilos de formulario

export default function EditProductPage() {
  const { productId } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    precio: '',
    cantidad_personas: '',
    category_id: '',
    imagen_url: ''
  });
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch product data
        const productResponse = await api.get(`/products/${productId}`);
        const productData = productResponse.data;
        setFormData({
          nombre: productData.nombre,
          descripcion: productData.descripcion || '',
          precio: productData.precio,
          cantidad_personas: productData.cantidad_personas,
          category_id: productData.category_id,
          imagen_url: productData.imagen_url || ''
        });

        // Fetch categories
        const categoriesResponse = await api.get('/categories/active');
        setCategories(categoriesResponse.data);

      } catch (err) {
        setError('No se pudo cargar el producto o las categorías.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [productId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const productData = {
        ...formData,
        precio: parseFloat(formData.precio),
        cantidad_personas: parseInt(formData.cantidad_personas),
        category_id: parseInt(formData.category_id)
      };
      await api.put(`/products/${productId}`, productData);
      alert('Producto actualizado con éxito');
      navigate('/admin/products'); // Volver a la gestión de productos
    } catch (err) {
      alert('Error al actualizar el producto.');
      console.error(err);
    }
  };

  if (loading) {
    return <div className={styles.loading}>Cargando producto...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  return (
    <div className={styles.dashboardContainer}>
      <h1 className={styles.title}>Editar Producto</h1>
      <form onSubmit={handleSubmit} className={formStyles.form}>
        <div className={formStyles.formGroup}>
          <label>Nombre</label>
          <input type="text" name="nombre" value={formData.nombre} onChange={handleChange} required />
        </div>
        <div className={formStyles.formGroup}>
          <label>Descripción</label>
          <textarea name="descripcion" value={formData.descripcion} onChange={handleChange}></textarea>
        </div>
        <div className={formStyles.formGroup}>
          <label>Precio</label>
          <input type="number" name="precio" value={formData.precio} onChange={handleChange} required step="0.01" />
        </div>
        <div className={formStyles.formGroup}>
          <label>Cantidad de Personas</label>
          <input type="number" name="cantidad_personas" value={formData.cantidad_personas} onChange={handleChange} required min="1" />
        </div>
        <div className={formStyles.formGroup}>
          <label>Categoría</label>
          <select name="category_id" value={formData.category_id} onChange={handleChange} required>
            {categories.map(cat => (
              <option key={cat.id} value={cat.id}>{cat.nombre}</option>
            ))}
          </select>
        </div>
        <div className={formStyles.formGroup}>
          <label>URL de la Imagen (Opcional)</label>
          <input type="text" name="imagen_url" value={formData.imagen_url} onChange={handleChange} />
        </div>
        <button type="submit" className={formStyles.submitButton}>Guardar Cambios</button>
      </form>
    </div>
  );
}
