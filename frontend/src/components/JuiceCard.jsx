import { Plus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { BASE_URL } from '../services/api';

// Muted colors for categories inspired by mobile app
const getCategoryColor = (categoryName) => {
  const colors = {
    'Citrus Juices': 'bg-[#FFF9F0] text-[#D97706]', // Muted Cream/Amber
    'Vegetable Juices': 'bg-[#F0FFF4] text-[#166534]', // Muted Mint/Green
    'Berry Juices': 'bg-[#FFF5F8] text-[#9D174D]', // Muted Rose/Pink
    'Tropical Juices': 'bg-[#FFF9E5] text-[#854D0E]', // Muted Gold/Brown
    'Green Juices': 'bg-[#F4FFF0] text-[#166534]', // Muted Lime/Green
    'Root Juices': 'bg-[#F9F5F0] text-[#78350F]', // Muted Sand/Brown
    'Mixed Fruit': 'bg-[#FFF0F0] text-[#991B1B]', // Muted Coral/Red
  };
  return colors[categoryName] || 'bg-gray-50 text-gray-600';
};

export default function JuiceCard({ juice, onAddToCart }) {
  const navigate = useNavigate();

  const imageUrl = juice.image 
    ? (juice.image.startsWith('http') ? juice.image : `${BASE_URL}${juice.image}`)
    : '/placeholder-juice.jpg';

  const categoryColorClass = getCategoryColor(juice.category?.name);

  return (
    <div 
      onClick={() => navigate(`/juice/${juice.id}`)}
      className="bg-white rounded-[28px] shadow-[0_12px_15px_rgba(0,0,0,0.05)] hover:shadow-[0_20px_30px_rgba(0,0,0,0.1)] transition-all duration-500 cursor-pointer overflow-hidden group border border-[#F0F0F0] flex flex-col h-full"
    >
      {/* Image Container */}
      <div className="relative h-48 overflow-hidden bg-white">
        <img
          src={imageUrl}
          alt={juice.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
          onError={(e) => { e.target.src = '/placeholder-juice.jpg'; }}
        />
        {juice.is_available === false && (
          <div className="absolute inset-0 bg-black/40 backdrop-blur-[2px] flex items-center justify-center">
            <span className="text-white font-black text-sm uppercase tracking-wider bg-black/20 px-4 py-2 rounded-full">Out of Stock</span>
          </div>
        )}
      </div>

      {/* Juice Info */}
      <div className="p-5 flex flex-col flex-1">
        <h3 className="font-extrabold text-lg text-gray-900 mb-2 truncate group-hover:text-[#FF6B35] transition-colors duration-300">
          {juice.name}
        </h3>
        
        <div className={`self-start px-3 py-1 rounded-xl text-[10px] font-extrabold uppercase tracking-widest mb-4 ${categoryColorClass}`}>
          {juice.category?.name || 'Juice'}
        </div>

        {juice.description && (
          <p className="text-gray-500 text-xs leading-relaxed mb-4 line-clamp-2 font-medium">
            {juice.description}
          </p>
        )}

        <div className="mt-auto flex items-center justify-between">
          <div className="flex flex-col">
            <span className="text-[#FF6B35] text-2xl font-black">₹{juice.price}</span>
            {juice.net_quantity_ml && (
              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-tighter">
                {juice.net_quantity_ml} ml
              </span>
            )}
          </div>

          {/* Add to Cart Button */}
          <button
            onClick={(e) => {
              e.stopPropagation();
              onAddToCart(juice);
            }}
            disabled={!juice.is_available}
            className={`w-10 h-10 rounded-xl shadow-lg flex items-center justify-center transition-all duration-300 transform group-hover:scale-110 ${
              juice.is_available
                ? 'bg-[#1E1E1E] text-white hover:bg-black active:scale-95'
                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
            }`}
          >
            <Plus className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
