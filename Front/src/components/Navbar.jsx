// src/components/Navbar.jsx

import { Link } from 'react-router-dom';
import styles from './Navbar.module.css';
import { useCart } from '../context/CartContext'; // <-- 1. IMPORTAR useCart

export default function Navbar() {
  const { cartItems } = useCart(); // <-- 2. OBTENER los items del carrito

  // Calculamos la cantidad total de productos en el carrito
  const totalItems = cartItems.reduce((total, item) => total + item.quantity, 0);

  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        <Link to="/">
          Pio<span>Crokanti</span>
        </Link>
      </div>
      <ul className={styles.navLinks}>
        <li className={styles.navLink}>
          <Link to="/menu">Menú</Link>
        </li>
        <li className={styles.navLink}>
          {/* 3. MOSTRAR el total de items */}
          <Link to="/carrito">
            Carrito ({totalItems})
          </Link>
        </li>
        <li className={styles.adminLink}>
          <Link to="/login">Admin</Link>
        </li>
      </ul>
    </nav>
  );
}