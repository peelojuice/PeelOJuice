import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { CheckCircle, Package, CreditCard, Clock } from 'lucide-react';

export default function OrderSuccess() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [orderDetails, setOrderDetails] = useState({
    orderId: searchParams.get('orderId'),
    method: searchParams.get('method'),
    success: searchParams.get('success') === 'true'
  });

  useEffect(() => {
    // If not successful, redirect to orders page
    if (!orderDetails.success) {
      setTimeout(() => navigate('/orders'), 2000);
    }
  }, [orderDetails.success, navigate]);

  if (!orderDetails.success) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-50 to-orange-50">
        <div className="bg-white rounded-3xl shadow-2xl p-12 max-w-md text-center">
          <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg className="w-12 h-12 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-3">Payment Failed</h1>
          <p className="text-gray-600 mb-6">Something went wrong with your payment. Redirecting...</p>
        </div>
      </div>
    );
  }

  const paymentMethodDisplay = orderDetails.method === 'cod' ? 'Cash on Delivery' : 'Online Payment';

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 via-pink-50 to-orange-50 py-12 px-4">
      <div className="bg-white rounded-3xl shadow-2xl max-w-lg w-full overflow-hidden">
        {/* Success Animation */}
        <div className="bg-gradient-to-r from-green-400 to-emerald-500 p-8 text-center">
          <div className="inline-block">
            <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce">
              <CheckCircle className="w-16 h-16 text-green-500" strokeWidth={3} />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">
            Order Placed Successfully!
          </h1>
          <p className="text-2xl">🎉</p>
        </div>

        {/* Content */}
        <div className="p-8">
          <p className="text-center text-gray-600 mb-8 text-lg">
            Thank you for your order. We've received your request and it's being processed.
          </p>

          {/* Order Details Card */}
          <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6 mb-8">
            <div className="flex items-center gap-2 mb-4">
              <Package className="w-6 h-6 text-purple-600" />
              <h2 className="text-xl font-bold text-gray-900">Order Details</h2>
            </div>
            
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-600 font-medium">Order Number:</span>
                <span className="text-gray-900 font-bold text-lg">{orderDetails.orderId}</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-gray-600 font-medium flex items-center gap-2">
                  <CreditCard className="w-4 h-4" />
                  Payment:
                </span>
                <span className="text-gray-900 font-semibold">{paymentMethodDisplay}</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-gray-600 font-medium flex items-center gap-2">
                  <Clock className="w-4 h-4" />
                  Status:
                </span>
                <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-bold">
                  Confirmed
                </span>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="space-y-3">
            <button
              onClick={() => navigate('/orders')}
              className="w-full bg-gradient-to-r from-purple-500 via-pink-500 to-orange-500 text-white py-4 px-6 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-105 flex items-center justify-center gap-2"
            >
              <Package className="w-5 h-5" />
              View My Orders
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
            
            <button
              onClick={() => navigate('/menu')}
              className="w-full bg-white border-2 border-gray-300 text-gray-700 py-4 px-6 rounded-xl font-semibold text-lg hover:bg-gray-50 transition-all"
            >
              Continue Shopping
            </button>
          </div>

          {/* Additional Info */}
          <div className="mt-6 p-4 bg-blue-50 rounded-xl">
            <p className="text-sm text-blue-800 text-center">
              <span className="font-semibold">📧 Confirmation sent!</span>
              <br />
              Check your email for order details
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
