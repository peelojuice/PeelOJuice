import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { CreditCard, Banknote, MapPin, Plus } from 'lucide-react';
import api from '../services/api';
import addressAPI from '../services/addressAPI';
import { useCart } from '../context/CartContext';
import { useToast } from '../context/ToastContext';
import AddressForm from '../components/AddressForm';

export default function Checkout() {
  const [paymentMethod, setPaymentMethod] = useState('cod');
  const [loading, setLoading] = useState(false);
  const [addresses, setAddresses] = useState([]);
  const [selectedAddress, setSelectedAddress] = useState(null);
  const [showAddressForm, setShowAddressForm] = useState(false);
  const [submittingAddress, setSubmittingAddress] = useState(false);
  const navigate = useNavigate();
  const { clearCart } = useCart();
  const { showToast } = useToast();

  useEffect(() => {
    fetchAddresses();
  }, []);

  const fetchAddresses = async () => {
    try {
      const response = await addressAPI.getAddresses();
      setAddresses(response.data);
      // Auto-select default address
      const defaultAddr = response.data.find(addr => addr.is_default);
      if (defaultAddr) {
        setSelectedAddress(defaultAddr.id);
      }
    } catch (error) {
      showToast('Failed to load addresses', 'error');
    }
  };

  const handleAddAddress = async (formData) => {
    setSubmittingAddress(true);
    try {
      await addressAPI.createAddress(formData);
      showToast('Address added successfully', 'success');
      await fetchAddresses();
      setShowAddressForm(false);
    } catch (error) {
      showToast('Failed to add address', 'error');
    } finally {
      setSubmittingAddress(false);
    }
  };

  const handleCheckout = async () => {
    if (!selectedAddress) {
      showToast('Please select a delivery address', 'error');
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/orders/checkout/', {
        payment_method: paymentMethod,
        address_id: selectedAddress
      });

      if (paymentMethod === 'online') {
        // Razorpay payment flow
        if (!window.Razorpay) {
          showToast('Payment gateway not loaded. Please refresh and try again.', 'error');
          setLoading(false);
          return;
        }

        const orderData = response.data.order;
        const paymentRes = await api.post('/payments/razorpay/create-order/', {
          order_id: orderData.id
        });

        const options = {
          key: paymentRes.data.key_id,
          amount: paymentRes.data.amount,
          currency: paymentRes.data.currency,
          order_id: paymentRes.data.razorpay_order_id,
          name: "PeelOJuice",
          description: `Order #${orderData.id}`,
          handler: async function(paymentResponse) {
            try {
              await api.post('/payments/razorpay/verify/', {
                razorpay_order_id: paymentResponse.razorpay_order_id,
                razorpay_payment_id: paymentResponse.razorpay_payment_id,
                razorpay_signature: paymentResponse.razorpay_signature
              });
              clearCart();
              navigate(`/order-success?success=true&orderId=${orderData.id}&method=online`);
            } catch (error) {
              navigate(`/order-success?success=false`);
            }
          },
          modal: {
            ondismiss: function() {
              showToast('Payment cancelled', 'info');
              setLoading(false);
            }
          },
          theme: {
            color: "#8B5CF6"
          }
        };

        const razorpay = new window.Razorpay(options);
        razorpay.on('payment.failed', function (response) {
          showToast('Payment failed: ' + response.error.description, 'error');
          setLoading(false);
        });
        razorpay.open();
      } else {
        // COD order
        const orderData = response.data.order;
        clearCart();
        navigate(`/order-success?success=true&orderId=${orderData.id}&method=cod`);
      }
    } catch (error) {
      console.error('Checkout error:', error);
      const errorMessage = error.response?.data?.detail || 'Failed to place order';
      showToast(errorMessage, 'error');
      setLoading(false);
    }
  };

  const selectedAddressData = addresses.find(addr => addr.id === selectedAddress);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-8">Checkout</h1>

        <div className="space-y-6">
          {/* Delivery Address Section */}
          <div className="bg-white rounded-2xl shadow-md p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold flex items-center gap-2">
                <MapPin className="w-6 h-6 text-purple-500" />
                Delivery Address
              </h2>
              <button
                onClick={() => setShowAddressForm(true)}
                className="flex items-center gap-1 text-purple-600 hover:text-purple-700 font-semibold text-sm"
              >
                <Plus className="w-4 h-4" />
                Add New
              </button>
            </div>

            {addresses.length === 0 ? (
              <div className="text-center py-8 border-2 border-dashed border-gray-300 rounded-xl">
                <MapPin className="w-16 h-16 mx-auto text-gray-300 mb-3" />
                <p className="text-gray-600 mb-4">No delivery address found</p>
                <button
                  onClick={() => setShowAddressForm(true)}
                  className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-2 rounded-full font-semibold hover:from-purple-600 hover:to-pink-600 transition"
                >
                  Add Address
                </button>
              </div>
            ) : (
              <div className="space-y-3">
                {addresses.map((address) => (
                  <div
                    key={address.id}
                    onClick={() => setSelectedAddress(address.id)}
                    className={`p-4 border-2 rounded-xl cursor-pointer transition ${
                      selectedAddress === address.id
                        ? 'border-purple-500 bg-purple-50'
                        : 'border-gray-200 hover:border-purple-300'
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <input
                        type="radio"
                        checked={selectedAddress === address.id}
                        onChange={() => setSelectedAddress(address.id)}
                        className="mt-1 w-4 h-4 text-purple-500"
                      />
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-bold text-gray-800">{address.label}</span>
                          {address.is_default && (
                            <span className="text-xs bg-purple-500 text-white px-2 py-0.5 rounded-full">
                              DEFAULT
                            </span>
                          )}
                        </div>
                        <p className="text-sm text-gray-700">{address.full_name} | {address.phone_number}</p>
                        <p className="text-sm text-gray-600">
                          {address.address_line1}, {address.address_line2 && `${address.address_line2}, `}
                          {address.city}, {address.state} - {address.pincode}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Payment Method Section */}
          <div className="bg-white rounded-2xl shadow-md p-6">
            <h2 className="text-xl font-bold mb-4">Payment Method</h2>
            <div className="space-y-3">
              <div
                onClick={() => setPaymentMethod('cod')}
                className={`p-4 border-2 rounded-xl cursor-pointer transition flex items-center gap-3 ${
                  paymentMethod === 'cod'
                    ? 'border-green-500 bg-green-50'
                    : 'border-gray-200 hover:border-green-300'
                }`}
              >
                <input
                  type="radio"
                  checked={paymentMethod === 'cod'}
                  onChange={() => setPaymentMethod('cod')}
                  className="w-4 h-4 text-green-500"
                />
                <Banknote className="w-6 h-6 text-green-600" />
                <div>
                  <p className="font-semibold text-gray-800">Cash on Delivery</p>
                  <p className="text-sm text-gray-600">Pay when you receive</p>
                </div>
              </div>

              <div
                onClick={() => setPaymentMethod('online')}
                className={`p-4 border-2 rounded-xl cursor-pointer transition flex items-center gap-3 ${
                  paymentMethod === 'online'
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-blue-300'
                }`}
              >
                <input
                  type="radio"
                  checked={paymentMethod === 'online'}
                  onChange={() => setPaymentMethod('online')}
                  className="w-4 h-4 text-blue-500"
                />
                <CreditCard className="w-6 h-6 text-blue-600" />
                <div>
                  <p className="font-semibold text-gray-800">Online Payment</p>
                  <p className="text-sm text-gray-600">UPI, Cards, Net Banking</p>
                </div>
              </div>
            </div>
          </div>

          {/* Place Order Button */}
          <button
            onClick={handleCheckout}
            disabled={loading || addresses.length === 0 || !selectedAddress}
            className="w-full bg-gradient-to-r from-green-500 to-green-600 text-white py-4 px-6 rounded-full font-bold text-lg shadow-lg hover:from-green-600 hover:to-green-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Processing...' : addresses.length === 0 ? 'Add Address to Continue' : 'Place Order'}
          </button>

          {addresses.length === 0 && (
            <p className="text-center text-sm text-gray-500">
              Please add a delivery address to proceed with checkout
            </p>
          )}
        </div>

        {/* Address Form Modal */}
        {showAddressForm && (
          <AddressForm
            onSubmit={handleAddAddress}
            onCancel={() => setShowAddressForm(false)}
            isSubmitting={submittingAddress}
          />
        )}
      </div>
    </div>
  );
}
