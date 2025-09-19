// src/context/CartContext.jsx

import { createContext, useState, useContext } from 'react';

const CartContext = createContext();

export function CartProvider({ children }) {
  const [cartItems, setCartItems] = useState([]);

  const addToCart = (product) => {
    setCartItems((prevItems) => {
      const existingItem = prevItems.find((item) => item.id === product.id);
      if (existingItem) {
        return prevItems.map((item) =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prevItems, { ...product, quantity: 1 }];
    });
  };

  // --- NUEVA FUNCIÓN ---
  const decreaseQuantity = (productId) => {
    setCartItems((prevItems) => {
      const existingItem = prevItems.find((item) => item.id === productId);
      // Si la cantidad es 1, al disminuir se elimina el producto
      if (existingItem.quantity === 1) {
        return prevItems.filter((item) => item.id !== productId);
      }
      // Si es mayor a 1, solo restamos la cantidad
      return prevItems.map((item) =>
        item.id === productId
          ? { ...item, quantity: item.quantity - 1 }
          : item
      );
    });
  };

  // --- NUEVA FUNCIÓN ---
  const removeFromCart = (productId) => {
    setCartItems((prevItems) => prevItems.filter((item) => item.id !== productId));
  };
  
  const value = {
    cartItems,
    addToCart,
    decreaseQuantity, // <-- Exportar nueva función
    removeFromCart,   // <-- Exportar nueva función
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart() {
  return useContext(CartContext);
}