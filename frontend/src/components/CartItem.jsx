import { Minus, Plus, Trash2 } from 'lucide-react';
import { BASE_URL } from '../services/api';

export default function CartItem({ item, onUpdateQuantity, onRemove }) {
  const imageUrl = item.juice_image 
    ? (item.juice_image.startsWith('http') ? item.juice_image : `${BASE_URL}${item.juice_image}`)
    : '/placeholder-juice.jpg';

  return (
    <div className="bg-white rounded-[24px] p-4 flex flex-col sm:flex-row items-center gap-6 border border-[#F0F0F0] hover:shadow-md transition-shadow">
      {/* Product Image */}
      <div className="w-24 h-24 flex-shrink-0 bg-[#F9F9F9] rounded-[20px] overflow-hidden border border-[#F0F0F0]">
        <img
          src={imageUrl}
          alt={item.juice_name}
          className="w-full h-full object-cover"
          onError={(e) => { e.target.src = '/placeholder-juice.jpg'; }}
        />
      </div>

      {/* Info Container */}
      <div className="flex-1 text-center sm:text-left">
        <h3 className="text-lg font-black text-[#1A1A1A] tracking-tighter uppercase mb-1">
          {item.juice_name}
        </h3>
        <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">
          ₹{Number(item.price_at_added || 0).toFixed(0)} each
        </p>
      </div>

      {/* Controls Container */}
      <div className="flex flex-col items-center sm:items-end gap-3 min-w-[120px]">
        {/* Quantity Selector */}
        <div className="flex items-center gap-4 bg-[#F9F9F9] px-4 py-2 rounded-full border border-[#F0F0F0]">
          <button
            onClick={() => onUpdateQuantity(item.juice, 'decrement')}
            className={`w-6 h-6 flex items-center justify-center transition-all ${
              item.quantity <= 1 ? 'text-gray-200' : 'text-[#FF6B35] hover:scale-125'
            }`}
            disabled={item.quantity <= 1}
          >
            <Minus className="w-4 h-4" />
          </button>
          <span className="font-extrabold text-[#1A1A1A] w-6 text-center">{item.quantity}</span>
          <button
            onClick={() => onUpdateQuantity(item.juice, 'increment')}
            className="w-6 h-6 flex items-center justify-center text-[#FF6B35] hover:scale-125 transition-all"
          >
            <Plus className="w-4 h-4" />
          </button>
        </div>
        
        {/* Price & Remove */}
        <div className="flex items-center gap-3">
          <span className="text-lg font-black text-[#1A1A1A] tracking-tight">
            ₹{(Number(item.price_at_added || 0) * item.quantity).toFixed(0)}
          </span>
          <button
            onClick={() => onRemove(item.juice)}
            className="w-8 h-8 flex items-center justify-center text-red-400 hover:bg-red-50 rounded-full transition-colors"
            title="Remove item"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}


