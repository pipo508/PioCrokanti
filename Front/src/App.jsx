// src/App.jsx

import { Routes, Route } from 'react-router-dom';

// Importación de componentes principales
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ProtectedRoute from './components/ProtectedRoute';

// Importación de todas las páginas
import HomePage from './pages/HomePage';
import MenuPage from './pages/MenuPage';
import CartPage from './pages/CartPage';
import CheckoutPage from './pages/CheckoutPage';
import LoginPage from './pages/LoginPage';
import AdminDashboard from './pages/AdminDashboard';
import NotFoundPage from './pages/NotFoundPage';
import CategoryProductsPage from './pages/CategoryProductsPage';
import ProductManagementPage from './pages/ProductManagementPage';
import EditProductPage from './pages/EditProductPage'; // Importar la página de edición de producto

function App() {
  return (
    <>
      <Navbar />
      <main>
        <Routes>
          {/* Rutas Públicas */}
          <Route path="/" element={<HomePage />} />
          <Route path="/menu" element={<MenuPage />} />
          <Route path="/menu/:categoryId" element={<CategoryProductsPage />} />
          <Route path="/carrito" element={<CartPage />} />
          <Route path="/checkout" element={<CheckoutPage />} />
          <Route path="/admin/login" element={<LoginPage />} />

          {/* Rutas de Administrador Protegidas */}
          <Route
            path="/admin/dashboard"
            element={<ProtectedRoute><AdminDashboard /></ProtectedRoute>}
          />
          <Route
            path="/admin/products"
            element={<ProtectedRoute><ProductManagementPage /></ProtectedRoute>}
          />
          <Route
            path="/admin/products/:productId/edit"
            element={<ProtectedRoute><EditProductPage /></ProtectedRoute>}
          />

          {/* Ruta para páginas no encontradas */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </main>
      <Footer />
    </>
  );
}

export default App;