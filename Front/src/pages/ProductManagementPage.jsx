// src/pages/ProductManagementPage.jsx

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Importar useNavigate
import api from '../services/api';
import styles from './AdminDashboard.module.css'; // Reutilizamos los estilos
import CreateProductForm from '../components/CreateProductForm';

export default function ProductManagementPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Inicializar useNavigate

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const response = await api.get('/products');
      setProducts(response.data);
    } catch (err) {
      setError('No se pudieron cargar los productos.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleDeactivate = async (productId) => {
    if (window.confirm('¿Estás seguro de que quieres desactivar este producto?')) {
      try {
        await api.delete(`/products/${productId}`);
        setProducts(products.map(p => p.id === productId ? { ...p, activo: false } : p));
        alert('Producto desactivado con éxito.');
      } catch (err) {
        alert('Error al desactivar el producto.');
        console.error(err);
      }
    }
  };

  const handleActivate = async (productId) => {
    if (window.confirm('¿Estás seguro de que quieres activar este producto?')) {
      try {
        await api.put(`/products/${productId}/activate`);
        setProducts(products.map(p => p.id === productId ? { ...p, activo: true } : p));
        alert('Producto activado con éxito.');
      } catch (err) {
        alert('Error al activar el producto.');
        console.error(err);
      }
    }
  };

  const handleEdit = (productId) => {
    navigate(`/admin/products/${productId}/edit`); // Navegar a la página de edición
  };

  if (loading) {
    return <div className={styles.loading}>Cargando productos...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  return (
    <div className={styles.dashboardContainer}>
      <h1 className={styles.title}>Gestión de Productos</h1>
      
      <CreateProductForm onProductCreated={fetchProducts} />

      <h2>Lista de Productos</h2>
      <table className={styles.ordersTable}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Precio</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.id}>
              <td>{product.id}</td>
              <td>{product.nombre}</td>
              <td>${product.precio.toFixed(2)}</td>
              <td>
                <span className={product.activo ? styles.statusActivo : styles.statusInactivo}>
                  {product.activo ? 'Activo' : 'Inactivo'}
                </span>
              </td>
              <td>
                <button onClick={() => handleEdit(product.id)} className={styles.editButton}>
                  Editar
                </button>
                {product.activo ? (
                  <button onClick={() => handleDeactivate(product.id)} className={styles.deactivateButton}>
                    Desactivar
                  </button>
                ) : (
                  <button onClick={() => handleActivate(product.id)} className={styles.activateButton}>
                    Activar
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

