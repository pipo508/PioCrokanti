// src/components/ProductCard.jsx

import styles from './ProductCard.module.css';
import { useCart } from '../context/CartContext'; // <-- 1. IMPORTAR useCart

export default function ProductCard({ product }) {
  const { addToCart } = useCart(); // <-- 2. OBTENER la función del contexto

  const handleAddToCart = () => {
    // 3. USAR la función real
    addToCart(product); 
    console.log(`Añadiendo ${product.nombre} al carrito.`);
  };

  return (
    <div className={styles.card}>
      {product.imagen_url ? (
        <img src={product.imagen_url} alt={product.nombre} />
      ) : (
        <div className={styles.imagePlaceholder}>Imagen no disponible</div>
      )}
      
      <h3 className={styles.name}>{product.nombre}</h3>
      <p className={styles.description}>{product.descripcion}</p>
      
      <div className={styles.footer}>
        <span className={styles.price}>${product.precio}</span>
        <button className={styles.addButton} onClick={handleAddToCart}>
          Añadir
        </button>
      </div>
    </div>
  );
}