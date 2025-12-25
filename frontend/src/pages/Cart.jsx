import { useEffect, useState } from 'react';
import { ShoppingBag } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useToast } from '../context/ToastContext';
import api from '../services/api';
import addressAPI from '../services/addressAPI';
import CartItem from '../components/CartItem';
import CouponSection from '../components/CouponSection';
import CartSummary from '../components/CartSummary';

export default function Cart() {
  const { cart, loading, updateQuantity, removeItem, fetchCart } = useCart();
  const { showToast } = useToast();
  const navigate = useNavigate();
  const [applyingCoupon, setApplyingCoupon] = useState(false);
  const [addresses, setAddresses] = useState([]);
  const [addressesLoading, setAddressesLoading] = useState(true);

  useEffect(() => {
    fetchCart();
    fetchAddresses();
  }, []);

  const fetchAddresses = async () => {
    try {
      const response = await addressAPI.getAddresses();
      setAddresses(response.data);
    } catch (error) {
      // User might not be logged in or no addresses
      setAddresses([]);
    } finally {
      setAddressesLoading(false);
    }
  };

  const handleUpdateQuantity = async (juiceId, action) => {
    const result = await updateQuantity(juiceId, action);
    if (!result.success) {
      showToast(result.message || 'Failed to update quantity', 'error');
    }
  };

  const handleRemoveItem = async (juiceId) => {
    const result = await removeItem(juiceId);
    if (!result.success) {
      showToast(result.message || 'Failed to remove item', 'error');
    } else {
      showToast('Item removed from cart', 'success');
    }
  };

  const handleApplyCoupon = async (couponCode) => {
    if (!couponCode.trim()) {
      showToast('Please enter a coupon code', 'error');
      return;
    }

    setApplyingCoupon(true);
    try {
      const response = await api.post('/cart/apply-coupon/', { code: couponCode });
      showToast(response.data.message, 'success');
      await fetchCart();
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Failed to apply coupon';
      showToast(errorMessage, 'error');
    } finally {
      setApplyingCoupon(false);
    }
  };

  const handleRemoveCoupon = async () => {
    try {
      await api.post('/cart/remove-coupon/', {});
      showToast('Coupon removed', 'success');
      await fetchCart();
    } catch (error) {
      showToast('Failed to remove coupon', 'error');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-2xl font-semibold text-primary">Loading...</div>
      </div>
    );
  }

  if (!cart || cart.items.length === 0) {
    return (
      <div className="min-h-screen bg-[#F5F2ED] flex items-center justify-center px-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-sm p-12 text-center">
          <div className="w-20 h-20 bg-[#8BA888]/10 rounded-full flex items-center justify-center mx-auto mb-6">
            <ShoppingBag className="w-10 h-10 text-[#8BA888]" />
          </div>
          <h2 className="text-2xl font-semibold text-gray-800 mb-3">Your Cart is Empty</h2>
          <p className="text-gray-600 mb-8">
            Add some delicious juices to get started!
          </p>
          <button
            onClick={() => navigate('/menu')}
            className="w-full bg-[#8BA888] text-white px-8 py-3 rounded-lg font-semibold hover:bg-[#7a9677] transition shadow-md"
          >
            Browse Menu
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Shopping Cart</h1>
      
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Cart Items */}
        <div className="lg:col-span-2 space-y-6">
          {/* Products Table */}
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <table className="w-full">
              <thead className="bg-black text-white">
                <tr>
                  <th className="p-4 text-left">Product</th>
                  <th className="p-4 text-center">Quantity</th>
                  <th className="p-4 text-right">Subtotal</th>
                  <th className="p-4 text-center">Remove</th>
                </tr>
              </thead>
              <tbody>
                {cart.items.map((item) => (
                  <CartItem
                    key={item.id}
                    item={item}
                    onUpdateQuantity={handleUpdateQuantity}
                    onRemove={handleRemoveItem}
                  />
                ))}
              </tbody>
            </table>
          </div>

          {/* Coupon Section */}
          <CouponSection
            appliedCoupon={cart.applied_coupon}
            onApplyCoupon={handleApplyCoupon}
            onRemoveCoupon={handleRemoveCoupon}
            isApplying={applyingCoupon}
          />

          {/* Address Validation Section */}
          {!addressesLoading && addresses.length === 0 && (
            <div className="bg-yellow-50 border-2 border-yellow-400 rounded-xl p-6">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0">
                  <svg className="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-yellow-800 mb-2">
                    No Delivery Address Found
                  </h3>
                  <p className="text-yellow-700 mb-4">
                    Please add a delivery address before proceeding to checkout. We need to know where to deliver your delicious juices!
                  </p>
                  <button
                    onClick={() => navigate('/my-addresses')}
                    className="bg-yellow-600 hover:bg-yellow-700 text-white px-6 py-2 rounded-lg font-semibold transition"
                  >
                    Add Delivery Address
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Cart Summary */}
        <div>
          <CartSummary cart={cart} hasAddresses={addresses.length > 0} />
        </div>
      </div>
    </div>
  );
}
