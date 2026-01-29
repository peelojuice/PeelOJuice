import { useEffect, useState } from 'react';
import { ShoppingBag, ArrowLeft, MapPin, AlertCircle } from 'lucide-react';
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
      <div className="flex flex-col justify-center items-center min-h-screen bg-white gap-4">
        <div className="w-12 h-12 border-4 border-[#FF6B35] border-t-transparent rounded-full animate-spin"></div>
        <div className="text-lg font-black text-[#1A1A1A] tracking-tighter uppercase">Processing Cart...</div>
      </div>
    );
  }

  if (!cart || cart.items.length === 0) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center px-6">
        <div className="max-w-md w-full text-center">
          <div className="w-32 h-32 bg-[#F9F9F9] rounded-[40px] flex items-center justify-center mx-auto mb-8 border border-[#F0F0F0] shadow-sm">
            <ShoppingBag className="w-12 h-12 text-[#FF6B35] opacity-20" />
          </div>
          <h2 className="text-3xl font-black text-[#1A1A1A] tracking-tighter uppercase mb-2">Cart is empty</h2>
          <p className="text-gray-400 font-bold text-xs uppercase tracking-widest mb-10">
            Time to fill your bag with some wellness!
          </p>
          <button
            onClick={() => navigate('/menu')}
            className="w-full bg-[#1A1A1A] text-white px-8 py-5 rounded-[24px] font-black uppercase tracking-[0.2em] text-xs hover:bg-black transition-all shadow-xl active:scale-95"
          >
            Explore Full Menu
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white min-h-screen pb-24">
      <div className="max-w-7xl mx-auto px-6 py-10">
        <div className="flex items-center gap-4 mb-10">
          <button 
            onClick={() => navigate('/menu')}
            className="w-12 h-12 bg-[#F9F9F9] rounded-2xl flex items-center justify-center border border-[#F0F0F0] hover:bg-white transition-colors group"
          >
            <ArrowLeft className="w-5 h-5 text-[#1A1A1A] group-hover:-translate-x-1 transition-transform" />
          </button>
          <div>
            <h1 className="text-3xl font-black text-[#1A1A1A] tracking-tighter uppercase">Checkout Bag</h1>
            <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">{cart.items.length} Items Selected</p>
          </div>
        </div>
        
        <div className="grid lg:grid-cols-[1fr_400px] gap-12 items-start">
          {/* Left Column: Items & Options */}
          <div className="space-y-8">
            {/* Address Warning */}
            {!addressesLoading && addresses.length === 0 && (
              <div className="bg-[#FFF9E5] border border-[#FFE082] rounded-[32px] p-8 flex items-start gap-6 shadow-sm">
                <div className="w-14 h-14 bg-white rounded-2xl flex items-center justify-center text-[#F57C00] shadow-sm flex-shrink-0">
                  <MapPin className="w-7 h-7" />
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-black text-[#1A1A1A] tracking-tight mb-2 uppercase">No Delivery Address</h3>
                  <p className="text-gray-500 font-medium text-sm leading-relaxed mb-6">
                    Please provide your delivery details so we can bring your fresh items to your doorstep!
                  </p>
                  <button
                    onClick={() => navigate('/my-addresses')}
                    className="bg-white border-2 border-[#1A1A1A] text-[#1A1A1A] px-6 py-3 rounded-2xl font-black uppercase text-[10px] tracking-widest hover:bg-[#1A1A1A] hover:text-white transition-all active:scale-95"
                  >
                    Set Delivery Address
                  </button>
                </div>
              </div>
            )}

            {/* Cart Items List */}
            <div className="space-y-4">
               {cart.items.map((item) => (
                <CartItem
                  key={item.id}
                  item={item}
                  onUpdateQuantity={handleUpdateQuantity}
                  onRemove={handleRemoveItem}
                />
              ))}
            </div>

            {/* Coupon Section */}
            <CouponSection
              appliedCoupon={cart.applied_coupon}
              onApplyCoupon={handleApplyCoupon}
              onRemoveCoupon={handleRemoveCoupon}
              isApplying={applyingCoupon}
            />
          </div>

          {/* Right Column: Summary */}
          <div className="lg:sticky lg:top-8">
            <CartSummary cart={cart} hasAddresses={addresses.length > 0} />
            <div className="mt-6 flex items-center gap-3 px-4 py-3 bg-[#F9F9F9] rounded-2xl border border-[#F0F0F0]">
              <AlertCircle className="w-4 h-4 text-gray-300" />
              <p className="text-[9px] font-bold text-gray-400 uppercase tracking-tight leading-snug">
                Items are fresh and perishable. Please ensure someone is available for delivery.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
