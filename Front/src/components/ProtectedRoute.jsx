// src/components/ProtectedRoute.jsx

import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();

  // Si el usuario NO está autenticado, lo redirigimos a la página de login.
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  // Si SÍ está autenticado, mostramos el componente que está protegiendo.
  return children;
}