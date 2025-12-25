import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, Package, Clock, CheckCircle, XCircle, Truck, ChefHat,
  MapPin, Phone, Mail, CreditCard, Banknote, AlertTriangle
} from 'lucide-react';
import api from '../services/api';
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
      fetchOrderDetail(); // Refresh data
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Failed to cancel order';
      showToast(errorMsg, 'error');
    } finally {
      setCancelling(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'pending':
        return <Clock className="w-6 h-6 text-yellow-600" />;
      case 'confirmed':
        return <CheckCircle className="w-6 h-6 text-blue-600" />;
      case 'preparing':
        return <ChefHat className="w-6 h-6 text-orange-600" />;
      case 'out_for_delivery':
        return <Truck className="w-6 h-6 text-purple-600" />;
      case 'delivered':
        return <CheckCircle className="w-6 h-6 text-green-600" />;
      case 'cancelled':
        return <XCircle className="w-6 h-6 text-red-600" />;
      default:
        return <Clock className="w-6 h-6 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-700 border-yellow-300';
      case 'confirmed':
        return 'bg-blue-100 text-blue-700 border-blue-300';
      case 'preparing':
        return 'bg-orange-100 text-orange-700 border-orange-300';
      case 'out_for_delivery':
        return 'bg-purple-100 text-purple-700 border-purple-300';
      case 'delivered':
        return 'bg-green-100 text-green-700 border-green-300';
      case 'cancelled':
        return 'bg-red-100 text-red-700 border-red-300';
      default:
        return 'bg-gray-100 text-gray-700 border-gray-300';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-2xl font-semibold text-primary">Loading...</div>
      </div>
    );
  }

  if (!order) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-orange-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <button
          onClick={() => navigate('/orders')}
          className="flex items-center gap-2 text-gray-600 hover:text-primary mb-6 transition"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Orders
        </button>

        {/* Order Header Card */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Order <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">{order.order_number || `#${order.id}`}</span>
              </h1>
              <p className="text-gray-600">
                Placed on {new Date(order.created_at).toLocaleString('en-IN', {
                  dateStyle: 'long',
                  timeStyle: 'short'
                })}
              </p>
            </div>
            <div className={`px-6 py-3 rounded-full border-2 flex items-center gap-3 ${getStatusColor(order.status)}`}>
              {getStatusIcon(order.status)}
              <span className="font-bold capitalize">{order.status_display || order.status.replace('_', ' ')}</span>
            </div>
          </div>

          {/* Payment Info */}
          <div className="grid md:grid-cols-2 gap-4">
            <div className="flex items-center gap-3 text-gray-700">
              {order.payment_method === 'Cash on Delivery' ? (
                <Banknote className="w-5 h-5 text-green-600" />
              ) : (
                <CreditCard className="w-5 h-5 text-blue-600" />
              )}
              <div>
                <p className="text-sm text-gray-500">Payment Method</p>
                <p className="font-semibold">{order.payment_method || 'N/A'}</p>
              </div>
            </div>
            <div className="flex items-center gap-3 text-gray-700">
              <Package className="w-5 h-5 text-purple-600" />
              <div>
                <p className="text-sm text-gray-500">Payment Status</p>
                <p className="font-semibold capitalize">{order.payment_status || 'N/A'}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Order Items */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Package className="w-6 h-6 text-primary" />
            Order Items
          </h2>
          <div className="space-y-4">
            {(order.items || []).map((item) => (
              <div key={item.id} className="flex gap-4 p-4 bg-gray-50 rounded-xl">
                <img
                  src={item.juice_image ? `http://localhost:8000${item.juice_image}` : '/placeholder-juice.jpg'}
                  alt={item.juice_name}
                  className="w-20 h-20 object-cover rounded-lg"
                  onError={(e) => { e.target.src = '/placeholder-juice.jpg'; }}
                />
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900">{item.juice_name}</h3>
                  <p className="text-sm text-gray-600">Quantity: {item.quantity}</p>
                  <p className="text-sm text-gray-600">Price: ₹{item.price_per_item} each</p>
                </div>
                <div className="text-right">
                  <p className="font-bold text-lg text-primary">₹{item.subtotal}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Price Breakdown */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">Price Details</h2>
          <div className="space-y-3">
            <div className="flex justify-between text-gray-700">
              <span>Food Subtotal</span>
              <span className="font-semibold">₹{Number(order.food_subtotal || 0).toFixed(2)}</span>
            </div>
            {order.discount > 0 && (
              <div className="flex justify-between text-green-600">
                <span>Discount</span>
                <span className="font-semibold">-₹{Number(order.discount).toFixed(2)}</span>
              </div>
            )}
            <div className="flex justify-between text-gray-700">
              <span>Food GST (5%)</span>
              <span className="font-semibold">₹{Number(order.food_gst || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-gray-700">
              <span>Delivery Fee</span>
              <span className="font-semibold">₹{Number(order.delivery_fee_base || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-gray-700">
              <span>Delivery GST (18%)</span>
              <span className="font-semibold">₹{Number(order.delivery_gst || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-gray-700">
              <span>Platform Fee</span>
              <span className="font-semibold">₹{Number(order.platform_fee || 0).toFixed(2)}</span>
            </div>
            <div className="border-t pt-3 flex justify-between text-xl font-bold text-gray-900">
              <span>Total Amount</span>
              <span className="text-primary">₹{Number(order.total_amount).toFixed(2)}</span>
            </div>
          </div>
        </div>

        {/* Cancel Order Button - Only show if can_cancel is true */}
        {order.can_cancel && (
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <button
              onClick={() => setShowCancelModal(true)}
              disabled={cancelling}
              className="w-full bg-red-500 hover:bg-red-600 disabled:bg-gray-400 text-white font-bold py-3 px-6 rounded-lg transition transform hover:scale-105"
            >
              {cancelling ? 'Cancelling...' : 'Cancel Order'}
            </button>
            <p className="text-sm text-gray-500 text-center mt-2">
              You can cancel this order before it's delivered
            </p>
          </div>
        )}

        {/* Cancel Confirmation Modal */}
        {showCancelModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                  <AlertTriangle className="w-6 h-6 text-red-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900">Cancel Order?</h3>
              </div>
              
              <p className="text-gray-600 mb-6">
                Are you sure you want to cancel this order? This action cannot be undone.
              </p>

              <div className="flex gap-3">
                <button
                  onClick={() => setShowCancelModal(false)}
                  className="flex-1 px-4 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition"
                >
                  No, Keep Order
                </button>
                <button
                  onClick={handleCancelOrder}
                  className="flex-1 px-4 py-3 bg-red-500 text-white rounded-lg font-semibold hover:bg-red-600 transition"
                >
                  Yes, Cancel Order
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
