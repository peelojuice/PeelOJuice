import { Tag } from 'lucide-react';
import { useState } from 'react';

export default function CouponSection({ 
  appliedCoupon, 
  onApplyCoupon, 
  onRemoveCoupon,
  isApplying 
}) {
  const [couponCode, setCouponCode] = useState('');

  const handleApply = () => {
    onApplyCoupon(couponCode);
  };

  const handleRemove = () => {
    setCouponCode('');
    onRemoveCoupon();
  };

  return (
    <div className="bg-gray-50 p-4 rounded-lg">
      <h3 className="font-semibold mb-3 flex items-center gap-2">
        <Tag className="w-5 h-5 text-primary" />
        Apply Coupon
      </h3>
      
      {appliedCoupon ? (
        <div className="flex items-center justify-between bg-green-50 border border-green-300 rounded-lg p-3">
          <div>
            <p className="font-semibold text-green-700">{appliedCoupon.code}</p>
            <p className="text-sm text-green-600">Coupon applied successfully!</p>
          </div>
          <button
            onClick={handleRemove}
            className="text-red-500 hover:text-red-700 font-semibold text-sm"
          >
            Remove
          </button>
        </div>
      ) : (
        <div className="flex gap-2">
          <input
            type="text"
            value={couponCode}
            onChange={(e) => setCouponCode(e.target.value.toUpperCase())}
            placeholder="Enter coupon code"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary"
          />
          <button
            onClick={handleApply}
            disabled={isApplying || !couponCode.trim()}
            className="bg-primary text-white px-6 py-2 rounded-lg font-semibold hover:bg-primary/90 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
          >
            {isApplying ? 'Applying...' : 'Apply'}
          </button>
        </div>
      )}
    </div>
  );
}


