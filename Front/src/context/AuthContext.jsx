// src/context/AuthContext.jsx

import { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Función de login (harcodeada por ahora)
  const login = (username, password) => {
    // En un futuro, aquí llamarías a tu API de autenticación.
    if (username === 'admin' && password === '1234') {
      setIsAuthenticated(true);
      return true; // Login exitoso
    }
    setIsAuthenticated(false);
    return false; // Login fallido
  };

  // Función para cerrar sesión
  const logout = () => {
    setIsAuthenticated(false);
  };

  const value = {
    isAuthenticated,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Hook personalizado para acceder fácilmente al contexto
export function useAuth() {
  return useContext(AuthContext);
}   