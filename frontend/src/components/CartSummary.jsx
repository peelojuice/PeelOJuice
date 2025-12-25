import { useNavigate } from 'react-router-dom';

export default function CartSummary({ cart, hasAddresses = true }) {
  const navigate = useNavigate();

  // Calculate values safely
  const foodSubtotal = Number(cart.total_amount) || 0;
  const couponDiscount = Number(cart.coupon_discount) || 0;
  const foodGST = Number(cart.food_gst) || 0;
  const deliveryFee = Number(cart.delivery_fee_base) || 0;
  const deliveryGST = Number(cart.delivery_gst) || 0;
  const platformFee = Number(cart.platform_fee) || 0;
  const grandTotal = Number(cart.grand_total) || 0;

  return (
    <div className="bg-white rounded-lg shadow-md p-6 sticky top-4">
      <h2 className="text-2xl font-bold mb-6">Order Summary</h2>
      
      {/* Free Delivery Progress */}
      {!cart.free_delivery && foodSubtotal < 99 && (
        <div className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
          <div className="flex justify-between text-sm text-blue-700 mb-1">
            <span className="font-semibold">Add ₹{(99 - foodSubtotal).toFixed(2)} for FREE delivery!</span>
            <span className="font-bold">🚚</span>
          </div>
          <div className="w-full bg-blue-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full transition-all"
              style={{ width: `${Math.min((foodSubtotal / 99) * 100, 100)}%` }}
            ></div>
          </div>
        </div>
      )}
      
      <div className="space-y-3 mb-6">
        <div className="flex justify-between text-gray-700">
          <span>Subtotal</span>
          <span className="font-semibold">₹{foodSubtotal.toFixed(2)}</span>
        </div>
        
        {couponDiscount > 0 && (
          <div className="flex justify-between text-green-600">
            <span>Coupon Discount</span>
            <span className="font-semibold">-₹{couponDiscount.toFixed(2)}</span>
          </div>
        )}
        
        <div className="flex justify-between text-gray-700">
          <span>GST (5%)</span>
          <span className="font-semibold">₹{foodGST.toFixed(2)}</span>
        </div>
        
        {/* Delivery Fee with Free Delivery Indicator */}
        <div className="flex justify-between text-gray-700">
          <span>Delivery Fee</span>
          <div className="flex items-center gap-2">
            {cart.free_delivery ? (
              <>
                <span className="line-through text-gray-400">₹{cart.original_delivery_fee}</span>
                <span className="font-semibold text-green-600">FREE</span>
              </>
            ) : (
              <span className="font-semibold">₹{deliveryFee.toFixed(2)}</span>
            )}
          </div>
        </div>
        
        {/* Show free delivery badge */}
        {cart.free_delivery && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-2 flex items-center gap-2">
            <span className="text-green-700 text-sm font-semibold">🎉 Free Delivery Applied! (Orders above ₹99)</span>
          </div>
        )}
        
        <div className="flex justify-between text-gray-700">
          <span>Delivery GST (18%)</span>
          <span className="font-semibold">₹{deliveryGST.toFixed(2)}</span>
        </div>
        
        <div className="flex justify-between text-gray-700">
          <span>Platform Fee</span>
          <span className="font-semibold">₹{platformFee.toFixed(2)}</span>
        </div>
        
        <div className="border-t pt-3 flex justify-between text-lg font-bold text-gray-900">
          <span>Total</span>
          <span className="text-primary">₹{grandTotal.toFixed(2)}</span>
        </div>
      </div>
      
      <div className="relative group">
        <button
          onClick={() => hasAddresses && navigate('/checkout')}
          disabled={!hasAddresses}
          className={`w-full py-3 px-6 rounded-lg font-semibold text-lg transition ${
            hasAddresses
              ? 'bg-black text-white hover:bg-gray-800'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
        >
          {hasAddresses ? 'Proceed to Checkout' : 'Add Address to Checkout'}
        </button>
        {!hasAddresses && (
          <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">
            Please add a delivery address first
          </div>
        )}
      </div>
    </div>
  );
}


