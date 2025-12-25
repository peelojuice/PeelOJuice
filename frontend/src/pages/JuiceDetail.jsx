import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Minus, Plus } from 'lucide-react';
import api from '../services/api';
import { useCart } from '../context/CartContext';
import { useToast } from '../context/ToastContext';
import BenefitsPanel from '../components/BenefitsPanel';
import FeatureBadges from '../components/FeatureBadges';
import ProductInfoTabs from '../components/ProductInfoTabs';

export default function JuiceDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const { showToast } = useToast();
  const [juice, setJuice] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [adding, setAdding] = useState(false);

  useEffect(() => {
    fetchJuiceDetail();
  }, [id]);

  const fetchJuiceDetail = async () => {
    try {
      const response = await api.get(`/products/juices/${id}/`);
      setJuice(response.data);
    } catch (error) {
      console.error('Error fetching juice:', error);
      showToast('Failed to load juice details', 'error');
      navigate('/menu');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = async () => {
    const accessToken = sessionStorage.getItem('accessToken');
    if (!accessToken) {
      showToast('Please login to add items to cart', 'warning');
      navigate('/login');
      return;
    }

    setAdding(true);
    const result = await addToCart(juice.id, quantity);
    if (result.success) {
      showToast(`Added ${quantity} ${juice.name} to cart!`, 'success');
      setQuantity(1);
    } else {
      showToast('Failed to add to cart', 'error');
    }
    setAdding(false);
  };

  const increaseQuantity = () => setQuantity(prev => prev + 1);
  const decreaseQuantity = () => setQuantity(prev => prev > 1 ? prev - 1 : 1);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-white">
        <div className="text-lg font-medium text-gray-900">Loading...</div>
      </div>
    );
  }

  if (!juice) return null;

  const pricePerMl = (juice.price / (juice.net_quantity_ml || 300)).toFixed(2);
  
  // Construct full image URL
  const imageUrl = juice.image ? 
    (juice.image.startsWith('http') ? juice.image : `http://localhost:8000${juice.image}`) 
    : null;

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Back Button */}
        <button
          onClick={() => navigate('/menu')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition mb-6"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Menu
        </button>

        {/* Main Product Container */}
        <div className="grid md:grid-cols-[30%_70%] gap-8 mb-8">
          {/* Left: Product Image - Sticky */}
          <div className="relative">
            {imageUrl ? (
              <img
                src={imageUrl}
                alt={juice.name}
                className="w-full h-auto object-cover rounded-2xl shadow-lg sticky top-4"
                onError={(e) => { e.target.src = '/placeholder-juice.jpg'; }}
              />
            ) : (
              <div className="bg-white rounded-2xl border border-gray-200 shadow-lg p-8 flex items-center justify-center h-full">
                <div className="text-9xl text-center">🧃</div>
              </div>
            )}
          </div>

          {/* Right: Product Details + Benefits - Scrollable */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-lg">
            <div className="p-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">{juice.name}</h1>
              
              {(juice.long_description || juice.description) && (
                <p className="text-gray-600 leading-relaxed mb-6">
                  {juice.long_description || juice.description}
                </p>
              )}

              {/* Net Quantity */}
              <div className="mb-3">
                <div className="text-sm font-semibold text-gray-700">
                  Net Qty: <span className="font-bold">{juice.net_quantity_ml || 300} ml</span>
                  <span className="text-gray-500 ml-2">(USP ₹{pricePerMl}/ml)</span>
                </div>
              </div>

              {/* MRP */}
              <div className="mb-6">
                <div className="text-sm font-semibold text-gray-700 mb-1">MRP:</div>
                <div className="text-4xl font-bold text-gray-900">
                  ₹{juice.price}
                  <span className="text-sm text-gray-500 ml-2 font-normal">(Inclusive of All Taxes)</span>
                </div>
              </div>

              {/* Quantity Selector */}
              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-3">Qty</label>
                <div className="flex items-center gap-3">
                  <button
                    onClick={decreaseQuantity}
                    className={`w-10 h-10 rounded-full border-2 border-gray-300 flex items-center justify-center hover:bg-gray-100 transition ${
                      quantity === 1 ? 'cursor-not-allowed opacity-50' : ''
                    }`}
                  >
                    <Minus className="w-4 h-4" />
                  </button>
                  <span className="font-bold text-2xl w-16 text-center">{quantity}</span>
                  <button
                    onClick={increaseQuantity}
                    className="w-10 h-10 rounded-full border-2 border-black bg-black text-white flex items-center justify-center hover:bg-gray-800 transition"
                  >
                    <Plus className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3 mb-6">
                <button
                  onClick={handleAddToCart}
                  disabled={!juice.is_available || adding}
                  className="w-48 bg-black text-white py-3 px-6 rounded-lg font-semibold hover:bg-gray-800 transition disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  {adding ? 'Adding...' : 'Add to Cart'}
                </button>
                <button
                  onClick={handleAddToCart}
                  disabled={!juice.is_available || adding}
                  className="w-48 bg-gray-800 text-white py-3 px-6 rounded-lg font-semibold hover:bg-gray-700 transition disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  Buy Now
                </button>
              </div>

              {/* Feature Badges */}
              <FeatureBadges features={juice.features} />

              {/* Benefits Panel - Integrated */}
              {juice.benefits && juice.benefits.length > 0 && (
                <div className="mt-8 pt-8 border-t border-gray-200">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Juice Benefits</h2>
                  <div className="grid grid-cols-1 gap-3">
                    {juice.benefits.map((benefit, index) => (
                      <div key={index} className="bg-gray-100 rounded-lg p-4 border border-gray-200">
                        <h3 className="font-semibold text-gray-900 text-sm mb-1">{benefit.title}</h3>
                        <p className="text-xs text-gray-600 leading-relaxed">{benefit.description}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Product Info Tabs */}
        <div className="mt-12">
          <ProductInfoTabs
            nutrition={{
              calories: juice.nutrition_calories,
              total_fat: juice.nutrition_total_fat,
              carbohydrate: juice.nutrition_carbohydrate,
              dietary_fiber: juice.nutrition_dietary_fiber,
              total_sugars: juice.nutrition_total_sugars,
              protein: juice.nutrition_protein
            }}
            ingredients={juice.ingredients}
            allergenInfo={juice.allergen_info}
          />
        </div>
      </div>
    </div>
  );
}
