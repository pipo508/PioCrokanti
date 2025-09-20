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
// --- AÑADIR IMPORTACIONES ---
import OrderSuccessPage from './pages/OrderSuccessPage';
import OrderFailurePage from './pages/OrderFailurePage';

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
          <Route path="/login" element={<LoginPage />} />

          {/* --- AÑADIR RUTAS DE RESPUESTA DE PAGO --- */}
          <Route path="/order/success" element={<OrderSuccessPage />} />
          <Route path="/order/failure" element={<OrderFailurePage />} />

          {/* Ruta de Administrador Protegida */}
          <Route
            path="/admin/dashboard"
            element={
              <ProtectedRoute>
                <AdminDashboard />
              </ProtectedRoute>
            }
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