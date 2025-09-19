// src/pages/CartPage.jsx

import { Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import styles from './CartPage.module.css';

export default function CartPage() {
  const { cartItems, addToCart, decreaseQuantity, removeFromCart } = useCart();

  // Calculamos el total de la compra
  const orderTotal = cartItems.reduce(
    (total, item) => total + item.precio * item.quantity,
    0
  );

  // Si el carrito está vacío, mostramos un mensaje
  if (cartItems.length === 0) {
    return (
      <div className={styles.cartContainer}>
        <h1 className={styles.title}>Tu Carrito</h1>
        <p className={styles.emptyCart}>Tu carrito está vacío.</p>
        <Link to="/menu" className={styles.checkoutButton}>Ver Menú</Link>
      </div>
    );
  }

  return (
    <div className={styles.cartContainer}>
      <h1 className={styles.title}>Tu Carrito</h1>
      
      {/* Listamos los productos del carrito */}
      <div className={styles.cartItemsList}>
        {cartItems.map((item) => (
          <div key={item.id} className={styles.cartItem}>
            <div className={styles.itemDetails}>
              <h3>{item.nombre}</h3>
              <p>Precio: ${item.precio}</p>
            </div>
            
            <div className={styles.quantityControls}>
              <button onClick={() => decreaseQuantity(item.id)} className={styles.quantityButton}>-</button>
              <span>{item.quantity}</span>
              <button onClick={() => addToCart(item)} className={styles.quantityButton}>+</button>
            </div>

            <p>Subtotal: ${item.precio * item.quantity}</p>

            <button onClick={() => removeFromCart(item.id)} className={styles.removeButton}>×</button>
          </div>
        ))}
      </div>

      {/* Mostramos el resumen de la compra */}
      <div className={styles.cartSummary}>
        <h2 className={styles.total}>Total: ${orderTotal.toFixed(2)}</h2>
        <Link to="/checkout" className={styles.checkoutButton}>
          Proceder al Pago
        </Link>
      </div>
    </div>
  );
}