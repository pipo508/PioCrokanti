// src/components/Navbar.jsx

import { Link } from 'react-router-dom';
import styles from './Navbar.module.css';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { cartItems } = useCart();
  const { isAuthenticated, logout } = useAuth();

  const totalItems = cartItems.reduce((total, item) => total + item.quantity, 0);

  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        <Link to={isAuthenticated ? "/admin/dashboard" : "/"}>
          Pio<span>Crokanti</span>
        </Link>
      </div>
      <ul className={styles.navLinks}>
        {isAuthenticated ? (
          // Links para el Admin
          <>
            <li className={styles.navLink}>
              <Link to="/admin/dashboard">Pedidos</Link>
            </li>
            <li className={styles.navLink}>
              <Link to="/admin/products">Productos</Link>
            </li>
            <li className={styles.navLink}>
              <button onClick={logout} className={styles.logoutButton}>Logout</button>
            </li>
          </>
        ) : (
          // Links para el Cliente
          <>
            <li className={styles.navLink}>
              <Link to="/menu">Menú</Link>
            </li>
            <li className={styles.navLink}>
              <Link to="/carrito">Carrito ({totalItems})</Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
}