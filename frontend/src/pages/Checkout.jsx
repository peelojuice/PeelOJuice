import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { CreditCard, Banknote, MapPin, Plus, ArrowLeft, ShieldCheck, ChevronRight } from 'lucide-react';
import api from '../services/api';
import addressAPI from '../services/addressAPI';
import { useCart } from '../context/CartContext';
import { useToast } from '../context/ToastContext';
import { useBranch } from '../context/BranchContext';
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
  const { selectedBranch } = useBranch();

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
    if (!selectedBranch) {
      showToast('Please select a branch from the top navigation', 'error');
      return;
    }

    if (!selectedAddress) {
      showToast('Please select a delivery address', 'error');
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/orders/checkout/', {
        payment_method: paymentMethod,
        address_id: selectedAddress,
        branch_id: selectedBranch.id
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
            color: "#FF6B35"
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
    <div className="min-h-screen bg-white pb-20">
      <div className="max-w-4xl mx-auto px-6 py-10">
        <div className="flex items-center gap-4 mb-10">
          <button 
            onClick={() => navigate('/cart')}
            className="w-12 h-12 bg-[#F9F9F9] rounded-2xl flex items-center justify-center border border-[#F0F0F0] hover:bg-white transition-colors group"
          >
            <ArrowLeft className="w-5 h-5 text-[#1A1A1A] group-hover:-translate-x-1 transition-transform" />
          </button>
          <div>
            <h1 className="text-3xl font-black text-[#1A1A1A] tracking-tighter uppercase">Finalize Order</h1>
            <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Secure Checkout</p>
          </div>
        </div>

        <div className="grid md:grid-cols-[1fr_350px] gap-12 items-start">
          <div className="space-y-10">
            {/* Delivery Address Section */}
            <section>
              <div className="flex justify-between items-center mb-6">
                <div className="flex items-center gap-3">
                   <div className="w-8 h-8 bg-[#F9F9F9] rounded-xl flex items-center justify-center text-[#FF6B35] border border-[#F0F0F0]">
                      <MapPin className="w-4 h-4" />
                   </div>
                   <h2 className="text-lg font-black text-[#1A1A1A] tracking-tighter uppercase">Delivery Address</h2>
                </div>
                <button
                  onClick={() => setShowAddressForm(true)}
                  className="bg-[#F9F9F9] text-[#1A1A1A] px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-white border border-[#F0F0F0] transition-all flex items-center gap-2"
                >
                  <Plus className="w-3.5 h-3.5" />
                  Add New
                </button>
              </div>

              {addresses.length === 0 ? (
                <div className="text-center py-12 bg-[#F9F9F9] border-2 border-dashed border-[#F0F0F0] rounded-[32px]">
                  <MapPin className="w-12 h-12 mx-auto text-gray-200 mb-4" />
                  <p className="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-6">No address on file</p>
                  <button
                    onClick={() => setShowAddressForm(true)}
                    className="bg-[#2D2D2D] text-white px-8 py-3 rounded-2xl font-black uppercase text-[10px] tracking-widest hover:bg-black transition-all"
                  >
                    Add Delivery Address
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  {addresses.map((address) => (
                    <div
                      key={address.id}
                      onClick={() => setSelectedAddress(address.id)}
                      className={`group p-6 rounded-[28px] border-2 cursor-pointer transition-all relative overflow-hidden ${
                        selectedAddress === address.id
                          ? 'border-[#FF6B35] bg-[#FFF9F0]'
                          : 'border-[#F0F0F0] hover:border-gray-200'
                      }`}
                    >
                      <div className="flex items-start gap-4">
                        <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center mt-1 transition-colors ${
                          selectedAddress === address.id ? 'border-[#FF6B35] bg-[#FF6B35]' : 'border-gray-200'
                        }`}>
                          {selectedAddress === address.id && <div className="w-2 h-2 bg-white rounded-full"></div>}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="text-xs font-black text-[#1A1A1A] uppercase tracking-widest">{address.label}</span>
                            {address.is_default && (
                              <span className="text-[8px] bg-[#1A1A1A] text-white px-2 py-0.5 rounded-full font-black uppercase tracking-widest">
                                DEFAULT
                              </span>
                            )}
                          </div>
                          <p className="text-[10px] font-bold text-gray-500 uppercase tracking-tight mb-1">{address.full_name} • {address.phone_number}</p>
                          <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest leading-relaxed">
                            {address.address_line1}, {address.address_line2 && `${address.address_line2}, `}
                            {address.city}, {address.state} - {address.pincode}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>

            {/* Payment Method Section */}
            <section>
              <div className="flex items-center gap-3 mb-6">
                 <div className="w-8 h-8 bg-[#F9F9F9] rounded-xl flex items-center justify-center text-[#FF6B35] border border-[#F0F0F0]">
                    <ShieldCheck className="w-4 h-4" />
                 </div>
                 <h2 className="text-lg font-black text-[#1A1A1A] tracking-tighter uppercase">Payment Options</h2>
              </div>
              <div className="grid md:grid-cols-2 gap-4">
                <div
                  onClick={() => setPaymentMethod('cod')}
                  className={`p-6 rounded-[28px] border-2 cursor-pointer transition-all flex items-center gap-4 ${
                    paymentMethod === 'cod'
                      ? 'border-[#FF6B35] bg-[#FFF9F0]'
                      : 'border-[#F0F0F0] hover:border-gray-200'
                  }`}
                >
                  <div className={`w-12 h-12 rounded-2xl flex items-center justify-center shadow-sm border ${
                    paymentMethod === 'cod' ? 'bg-white border-[#FFE082] text-green-500' : 'bg-[#F9F9F9] border-[#F0F0F0] text-gray-300'
                  }`}>
                    <Banknote className="w-6 h-6" />
                  </div>
                  <div>
                    <p className="text-xs font-black text-[#1A1A1A] uppercase tracking-widest">COD</p>
                    <p className="text-[9px] font-bold text-gray-400 uppercase tracking-tight">Pay on arrival</p>
                  </div>
                </div>

                <div
                  onClick={() => setPaymentMethod('online')}
                  className={`p-6 rounded-[28px] border-2 cursor-pointer transition-all flex items-center gap-4 ${
                    paymentMethod === 'online'
                      ? 'border-[#FF6B35] bg-[#FFF9F0]'
                      : 'border-[#F0F0F0] hover:border-gray-200'
                  }`}
                >
                  <div className={`w-12 h-12 rounded-2xl flex items-center justify-center shadow-sm border ${
                    paymentMethod === 'online' ? 'bg-white border-[#FFE082] text-blue-500' : 'bg-[#F9F9F9] border-[#F0F0F0] text-gray-300'
                  }`}>
                    <CreditCard className="w-6 h-6" />
                  </div>
                  <div>
                    <p className="text-xs font-black text-[#1A1A1A] uppercase tracking-widest">Online</p>
                    <p className="text-[9px] font-bold text-gray-400 uppercase tracking-tight">Cards & UPI</p>
                  </div>
                </div>
              </div>
            </section>
          </div>

          {/* Right Column: Checkout Summary info or small cards */}
          <div className="md:sticky md:top-28 space-y-6">
            <div className="bg-[#1A1A1A] rounded-[32px] p-8 text-white shadow-2xl relative overflow-hidden group">
               <div className="absolute top-0 right-0 w-32 h-32 bg-[#FF6B35] opacity-10 rounded-full -mr-16 -mt-16 group-hover:scale-150 transition-transform duration-1000"></div>
               <p className="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-2">Order Ready?</p>
               <h3 className="text-3xl font-black tracking-tighter uppercase mb-10 leading-none">Confirm<br />& Pay</h3>
               
               <button
                  onClick={handleCheckout}
                  disabled={loading || addresses.length === 0 || !selectedAddress}
                  className="w-full bg-[#FF6B35] text-white py-5 rounded-2xl font-black uppercase text-xs tracking-widest flex items-center justify-center gap-2 hover:scale-[1.02] active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:grayscale"
                >
                  {loading ? '...' : 'Complete Order'}
                  <ChevronRight className="w-4 h-4" />
                </button>
            </div>
            
            <div className="bg-[#F9F9F9] rounded-3xl p-6 border border-[#F0F0F0]">
               <div className="flex items-center gap-3 mb-4">
                  <ShieldCheck className="w-5 h-5 text-green-500" />
                  <span className="text-[10px] font-black text-[#1A1A1A] uppercase tracking-widest">Safe & Secure</span>
               </div>
               <p className="text-[10px] font-bold text-gray-400 uppercase leading-relaxed tracking-tight">
                  Your payment information is encrypted. We don't store card details.
               </p>
            </div>
          </div>
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
