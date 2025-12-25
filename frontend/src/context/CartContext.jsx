import { createContext, useState, useContext, useEffect, useCallback } from 'react';
import api from '../services/api';

const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState(null);
  const [cartCount, setCartCount] = useState(0);
  const [loading, setLoading] = useState(true);

  const fetchCart = useCallback(async () => {
    try {
      const response = await api.get('/cart/');
      setCart(response.data);
      setCartCount(response.data.items.length);
    } catch (error) {
      console.error('Error fetching cart:', error);
      setCart(null);
      setCartCount(0);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const accessToken = sessionStorage.getItem('accessToken');
    if (accessToken) {
      fetchCart();
    } else {
      // Set loading to false immediately if not logged in
      setLoading(false);
    }
  }, [fetchCart]);

  const addToCart = async (juiceId, quantity = 1) => {
    try {
      await api.post('/cart/add/', { juice_id: juiceId, quantity });
      await fetchCart();
      return { success: true };
    } catch (error) {
      console.error('Error adding to cart:', error);
      return { success: false, error };
    }
  };

  const updateQuantity = async (juiceId, action) => {
    try {
      // Backend expects juice_id, not item_id
      await api.post('/cart/update/', { juice_id: juiceId, action });
      await fetchCart();
      return { success: true };
    } catch (error) {
      console.error('Error updating cart:', error);
      const errorMsg = error.response?.data?.message || 'Failed to update cart';
      return { success: false, error, message: errorMsg };
    }
  };

  const removeItem = async (juiceId) => {
    try {
      // Backend expects juice_id, not item_id
      console.log('Removing item with juice_id:', juiceId);
      await api.delete('/cart/remove/', { data: { juice_id: juiceId } });
      await fetchCart();
      return { success: true };
    } catch (error) {
      console.error('Error removing item:', error);
      console.error('Error response:', error.response?.data);
      const errorMsg = error.response?.data?.message || 'Failed to remove item';
      return { success: false, error, message: errorMsg };
    }
  };

  const clearCart = () => {
    setCart(null);
    setCartCount(0);
  };

  const value = {
    cart,
    cartCount,
    loading,
    fetchCart,
    addToCart,
    updateQuantity,
    removeItem,
    clearCart,
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};
