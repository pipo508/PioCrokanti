// src/pages/MenuPage.jsx

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom'; // Se importa <Link> para la navegación
import api from '../services/api';
import styles from './MenuPage.module.css';

export default function MenuPage() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await api.get('/categories/active');
        setCategories(response.data);
      } catch (err) {
        setError('No se pudieron cargar las categorías.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchCategories();
  }, []);

  if (loading) {
    return <div className={styles.loading}>Cargando categorías...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  return (
    <div className={styles.menuContainer}>
      <h1 className={styles.title}>Nuestro Menú</h1>
      <div className={styles.categoriesGrid}>
        {categories.map((category) => (
          // Cada tarjeta de categoría ahora es un enlace a su página de productos
          <Link to={`/menu/${category.id}`} key={category.id} className={styles.categoryCard}>
            <h3>{category.nombre}</h3>
          </Link>
        ))}
      </div>
    </div>
  );
}