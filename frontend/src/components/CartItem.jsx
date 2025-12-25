import { Minus, Plus, Trash2 } from 'lucide-react';
import { BASE_URL } from '../services/api';

export default function CartItem({ item, onUpdateQuantity, onRemove }) {
  const imageUrl = item.juice_image 
    ? (item.juice_image.startsWith('http') ? item.juice_image : `${BASE_URL}${item.juice_image}`)
    : '/placeholder-juice.jpg';

  return (
    <tr className="border-b hover:bg-gray-50 transition">
      <td className="p-4">
        <div className="flex items-center gap-4">
          <img
            src={imageUrl}
            alt={item.juice_name}
            className="w-20 h-20 object-cover rounded-lg shadow"
            onError={(e) => { e.target.src = '/placeholder-juice.jpg'; }}
          />
          <div>
            <h3 className="font-semibold text-gray-900">{item.juice_name}</h3>
            <p className="text-sm text-gray-500">₹{Number(item.price_at_added || 0).toFixed(2)} each</p>
          </div>
        </div>
      </td>
      <td className="p-4">
        <div className="flex items-center gap-2">
          <button
            onClick={() => onUpdateQuantity(item.juice, 'decrement')}
            className="p-1 rounded-full hover:bg-gray-200 transition"
            disabled={item.quantity <= 1}
          >
            <Minus className="w-5 h-5 text-gray-600" />
          </button>
          <span className="w-12 text-center font-semibold">{item.quantity}</span>
          <button
            onClick={() => onUpdateQuantity(item.juice, 'increment')}
            className="p-1 rounded-full hover:bg-gray-200 transition"
          >
            <Plus className="w-5 h-5 text-gray-600" />
          </button>
        </div>
      </td>
      <td className="p-4 text-right font-semibold text-gray-900">
        ₹{(Number(item.price_at_added || 0) * item.quantity).toFixed(2)}
      </td>
      <td className="p-4 text-center">
        <button
          onClick={() => onRemove(item.juice)}
          className="p-2 text-red-500 hover:bg-red-50 rounded-full transition"
          title="Remove item"
        >
          <Trash2 className="w-5 h-5" />
        </button>
      </td>
    </tr>
  );
}


