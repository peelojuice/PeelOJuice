import { Tag, X, CheckCircle } from 'lucide-react';
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
    <div className="bg-[#F9F9F9] p-6 rounded-[32px] border border-[#F0F0F0] shadow-sm">
      <h3 className="text-xs font-black mb-6 flex items-center gap-2 text-gray-400 uppercase tracking-widest">
        <Tag className="w-4 h-4 text-[#FF6B35]" />
        Special Offers & Coupons
      </h3>
      
      {appliedCoupon ? (
        <div className="flex items-center justify-between bg-[#F4FFF0] border border-[#D1F0C4] rounded-2xl p-4 shadow-sm animate-in fade-in zoom-in duration-300">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center text-green-500 shadow-sm">
              <CheckCircle className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-black text-green-700 tracking-tight uppercase">{appliedCoupon.code}</p>
              <p className="text-[10px] font-bold text-green-600 uppercase tracking-widest leading-none">Coupon Active</p>
            </div>
          </div>
          <button
            onClick={handleRemove}
            className="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-red-500 hover:bg-white rounded-full transition-all"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      ) : (
        <div className="flex gap-2 p-1.5 bg-white rounded-[24px] border border-[#F0F0F0] shadow-inner">
          <input
            type="text"
            value={couponCode}
            onChange={(e) => setCouponCode(e.target.value.toUpperCase())}
            placeholder="Enter promo code"
            className="flex-1 px-5 py-3 bg-transparent text-sm font-black text-[#1A1A1A] placeholder:text-gray-300 focus:outline-none uppercase tracking-widest"
          />
          <button
            onClick={handleApply}
            disabled={isApplying || !couponCode.trim()}
            className="bg-[#1A1A1A] text-white px-8 py-3 rounded-[18px] text-[10px] font-black uppercase tracking-widest hover:bg-black disabled:bg-gray-100 disabled:text-gray-300 disabled:cursor-not-allowed transition-all active:scale-95"
          >
            {isApplying ? '...' : 'Apply'}
          </button>
        </div>
      )}
    </div>
  );
}


