// src/pages/CategoryProductsPage.jsx

import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import ProductCard from '../components/ProductCard'; // <-- 1. IMPORTAR ProductCard
import styles from './MenuPage.module.css'; 

export default function CategoryProductsPage() {
  const { categoryId } = useParams();
  const [products, setProducts] = useState([]);
  const [categoryName, setCategoryName] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // La lógica para obtener los datos se mantiene igual
    const fetchProducts = async () => {
      try {
        const [productsResponse, categoryResponse] = await Promise.all([
          api.get('/products'),
          api.get(`/categories/${categoryId}`)
        ]);
        
        const filteredProducts = productsResponse.data.filter(
          (product) => product.category_id === parseInt(categoryId)
        );
        
        setProducts(filteredProducts);
        setCategoryName(categoryResponse.data.nombre);

      } catch (err) {
        setError('No se pudieron cargar los productos.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, [categoryId]);

  if (loading) return <div className={styles.loading}>Cargando productos...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles.menuContainer}>
      <Link to="/menu">← Volver a Categorías</Link>
      <h1 className={styles.title}>{categoryName}</h1>
      <div className={styles.categoriesGrid}>
        {products.length > 0 ? (
          // 👇 --- 2. USAR ProductCard AQUÍ --- 👇
          products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))
        ) : (
          <p>No hay productos en esta categoría.</p>
        )}
      </div>
    </div>
  );
}