import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft, Package, Clock, CheckCircle, XCircle, Truck, ChefHat,
  MapPin, CreditCard, Banknote, AlertTriangle, ShieldCheck
} from 'lucide-react';
import api, { BASE_URL } from '../services/api';
import { useToast } from '../context/ToastContext';

export default function OrderDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [cancelling, setCancelling] = useState(false);
  const [showCancelModal, setShowCancelModal] = useState(false);

  useEffect(() => {
    fetchOrderDetail();
  }, [id]);

  const fetchOrderDetail = async () => {
    try {
      const response = await api.get(`/orders/my-orders/${id}/`);
      setOrder(response.data);
    } catch (error) {
      showToast('Failed to load order details', 'error');
      navigate('/orders');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelOrder = async () => {
    setCancelling(true);
    setShowCancelModal(false);
    try {
      await api.post(`/orders/my-orders/${id}/cancel/`);
      showToast('Order cancelled successfully', 'success');
      fetchOrderDetail();
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Failed to cancel order';
      showToast(errorMsg, 'error');
    } finally {
      setCancelling(false);
    }
  };

  const getStatusConfig = (status) => {
    switch (status) {
      case 'pending': return { icon: Clock, color: 'text-yellow-600', bg: 'bg-[#FFF9F0]', border: 'border-[#FEEBC8]' };
      case 'confirmed': return { icon: CheckCircle, color: 'text-blue-600', bg: 'bg-[#F0F5FF]', border: 'border-[#D1E9FF]' };
      case 'preparing': return { icon: ChefHat, color: 'text-orange-600', bg: 'bg-[#FFF2E5]', border: 'border-[#FFDAB3]' };
      case 'out_for_delivery': return { icon: Truck, color: 'text-purple-600', bg: 'bg-[#F6F0FF]', border: 'border-[#E6D4FF]' };
      case 'delivered': return { icon: CheckCircle, color: 'text-green-600', bg: 'bg-[#F4FFF0]', border: 'border-[#D1F0C4]' };
      case 'cancelled': return { icon: XCircle, color: 'text-red-600', bg: 'bg-[#FFF5F8]', border: 'border-[#FED7E2]' };
      default: return { icon: Clock, color: 'text-gray-500', bg: 'bg-gray-50', border: 'border-gray-200' };
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col justify-center items-center min-h-screen bg-white gap-4">
        <div className="w-12 h-12 border-4 border-[#FF6B35] border-t-transparent rounded-full animate-spin"></div>
        <div className="text-lg font-black text-[#1A1A1A] tracking-tighter uppercase">Finding your juice...</div>
      </div>
    );
  }

  if (!order) return null;
  const cfg = getStatusConfig(order.status);

  return (
    <div className="min-h-screen bg-white pb-20">
      <div className="max-w-4xl mx-auto px-6 py-10">
        <button
          onClick={() => navigate('/orders')}
          className="w-12 h-12 bg-[#F9F9F9] rounded-2xl flex items-center justify-center border border-[#F0F0F0] hover:bg-white transition-colors group mb-10"
        >
          <ArrowLeft className="w-5 h-5 text-[#1A1A1A] group-hover:-translate-x-1 transition-transform" />
        </button>

        <div className="grid lg:grid-cols-[1fr_320px] gap-12 items-start">
          <div className="space-y-10">
            {/* Header Content */}
            <div className="flex flex-col md:flex-row justify-between items-start gap-6">
              <div>
                <h1 className="text-4xl font-black text-[#1A1A1A] tracking-tighter uppercase leading-none mb-2">
                  Order Details
                </h1>
                <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">
                  #{order.order_number || order.id} • {new Date(order.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}
                </p>
              </div>
              <div className={`px-6 py-3 rounded-2xl border ${cfg.bg} ${cfg.border} ${cfg.color} flex items-center gap-3`}>
                <cfg.icon className="w-5 h-5" />
                <span className="text-[10px] font-black uppercase tracking-widest">{order.status_display || order.status.replace('_', ' ')}</span>
              </div>
            </div>

            {/* Items Summary */}
            <section>
               <div className="flex items-center gap-3 mb-6">
                  <div className="w-8 h-8 bg-[#F9F9F9] rounded-xl flex items-center justify-center text-[#FF6B35] border border-[#F0F0F0]">
                     <Package className="w-4 h-4" />
                  </div>
                  <h2 className="text-lg font-black text-[#1A1A1A] tracking-tighter uppercase">Purchased Items</h2>
               </div>
               <div className="space-y-4">
                  {(order.items || []).map((item) => (
                    <div key={item.id} className="flex gap-6 p-6 bg-white rounded-[28px] border border-[#F0F0F0] hover:shadow-md transition-shadow">
                      <div className="w-20 h-20 bg-[#F9F9F9] rounded-2xl overflow-hidden shadow-sm border border-[#F0F0F0] flex-shrink-0">
                        <img
                          src={item.juice_image ? (item.juice_image.startsWith('http') ? item.juice_image : `${BASE_URL}${item.juice_image}`) : '/placeholder-juice.jpg'}
                          alt={item.juice_name}
                          className="w-full h-full object-cover"
                          onError={(e) => { e.target.src = '/placeholder-juice.jpg'; }}
                        />
                      </div>
                      <div className="flex-1">
                        <h3 className="text-sm font-black text-[#1A1A1A] uppercase tracking-tighter mb-1">{item.juice_name}</h3>
                        <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest leading-none mb-4">QTY: {item.quantity}</p>
                        <p className="text-sm font-black text-[#FF6B35]">₹{item.subtotal}</p>
                      </div>
                    </div>
                  ))}
               </div>
            </section>
          </div>

          <aside className="space-y-6">
             {/* Payment Summary */}
             <div className="bg-[#1A1A1A] rounded-[32px] p-8 text-white shadow-2xl">
                <p className="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-6">Payment Info</p>
                <div className="space-y-4 mb-10">
                   <div className="flex justify-between items-center text-[10px] font-black uppercase tracking-widest">
                      <span className="text-gray-500">Method</span>
                      <span className="flex items-center gap-2">
                         {order.payment_method === 'Cash on Delivery' ? <Banknote className="w-3.5 h-3.5" /> : <CreditCard className="w-3.5 h-3.5" />}
                         {order.payment_method}
                      </span>
                   </div>
                   <div className="flex justify-between items-center text-[10px] font-black uppercase tracking-widest">
                      <span className="text-gray-500">Status</span>
                      <span className="text-green-400">{order.payment_status}</span>
                   </div>
                </div>
                
                <div className="pt-6 border-t border-white/10">
                   <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Total Amount Paid</p>
                   <p className="text-4xl font-black tracking-tighter">₹{Number(order.total_amount).toFixed(0)}</p>
                </div>
             </div>

             {/* Cancel Order */}
             {order.can_cancel && (
               <button
                  onClick={() => setShowCancelModal(true)}
                  disabled={cancelling}
                  className="w-full bg-[#FFF5F8] border border-[#FED7E2] text-red-500 py-6 rounded-2xl font-black uppercase text-[10px] tracking-widest hover:bg-red-50 transition-all active:scale-95"
               >
                  {cancelling ? '...' : 'Cancel Order'}
               </button>
             )}

             <div className="bg-[#F9F9F9] rounded-3xl p-6 border border-[#F0F0F0]">
                <div className="flex items-center gap-3 mb-4">
                   <ShieldCheck className="w-5 h-5 text-[#FF6B35]" />
                   <span className="text-[10px] font-black text-[#1A1A1A] uppercase tracking-widest">Customer Support</span>
                </div>
                <p className="text-[9px] font-bold text-gray-400 uppercase leading-relaxed tracking-tight">
                   Need help with this order? Our team is available 24/7. Just reach out via the help section.
                </p>
             </div>
          </aside>
        </div>

        {/* Cancel Confirmation Modal */}
        {showCancelModal && (
          <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-6 animate-in fade-in duration-300">
            <div className="bg-white rounded-[40px] shadow-2xl max-w-md w-full p-10 text-center">
              <div className="w-20 h-20 bg-red-50 rounded-[30px] flex items-center justify-center mx-auto mb-8">
                <AlertTriangle className="w-10 h-10 text-red-500" />
              </div>
              <h3 className="text-2xl font-black text-[#1A1A1A] tracking-tighter uppercase mb-2">Cancel Order?</h3>
              <p className="text-gray-400 font-bold text-xs uppercase tracking-widest leading-relaxed mb-10">
                Are you sure? This freshness journey will be cut short and cannot be undone.
              </p>
              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={() => setShowCancelModal(false)}
                  className="px-6 py-5 bg-[#F9F9F9] text-[#1A1A1A] rounded-2xl font-black uppercase text-[10px] tracking-widest hover:bg-white border border-[#F0F0F0] transition-all"
                >
                  Keep It
                </button>
                <button
                  onClick={handleCancelOrder}
                  className="px-6 py-5 bg-[#1A1A1A] text-white rounded-2xl font-black uppercase text-[10px] tracking-widest hover:bg-black transition-all shadow-xl"
                >
                  Yes, Cancel
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
