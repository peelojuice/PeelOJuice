import { Plus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { BASE_URL } from '../services/api';

export default function JuiceCard({ juice, onAddToCart }) {
  const navigate = useNavigate();

  const imageUrl = juice.image 
    ? (juice.image.startsWith('http') ? juice.image : `${BASE_URL}${juice.image}`)
    : '/placeholder-juice.jpg';

  return (
    <div 
      onClick={() => navigate(`/juice/${juice.id}`)}
      className="bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 cursor-pointer overflow-hidden group border border-gray-100"
    >
      {/* Image Container */}
      <div className="relative overflow-hidden bg-gradient-to-br from-orange-50 to-pink-50">
        <img
          src={imageUrl}
          alt={juice.name}
          className="w-full h-56 object-contain group-hover:scale-110 transition-transform duration-300"
          onError={(e) => { e.target.src = '/placeholder-juice.jpg'; }}
        />
        {juice.is_available === false && (
          <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <span className="text-white font-bold text-lg">Out of Stock</span>
          </div>
        )}
      </div>

      {/* Juice Info */}
      <div className="text-center p-6">
        <h3 className="font-bold text-xl text-gray-800 mb-2">{juice.name}</h3>
        <div className="flex items-center justify-center gap-2 mb-4">
          <span className="text-2xl font-bold text-gray-900">₹{juice.price}</span>
          <span className="text-gray-500">| 250 ml</span>
        </div>

        {/* Add to Cart Button */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            onAddToCart(juice.id);
          }}
          disabled={!juice.is_available}
          className={`w-full py-3 rounded-full font-bold text-sm uppercase tracking-wide transition-all duration-300 flex items-center justify-center gap-2 ${
            juice.is_available
              ? 'bg-gradient-to-r from-green-500 to-green-600 text-white hover:shadow-lg hover:scale-105'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
        >
          <Plus className="w-5 h-5" />
          {juice.is_available ? 'Add to Cart' : 'Out of Stock'}
        </button>

        {/* Read More Link */}
        <button 
          onClick={(e) => {
            e.stopPropagation();
            navigate(`/juice/${juice.id}`);
          }}
          className="text-green-600 hover:text-green-700 text-sm mt-3 font-medium underline"
        >
          Read More
        </button>
      </div>
    </div>
  );
}
