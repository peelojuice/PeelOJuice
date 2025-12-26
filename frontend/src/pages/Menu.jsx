import { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import api, { BASE_URL } from '../services/api';
import { useCart } from '../context/CartContext';
import { useToast } from '../context/ToastContext';
import { useBranch } from '../context/BranchContext';
import CategoryFilter from '../components/CategoryFilter';

export default function Menu() {
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const { showToast } = useToast();
  const { selectedBranch } = useBranch();
  const [juices, setJuices] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const observer = useRef();

  useEffect(() => {
    fetchCategories();
    // Fetch juices on initial load
    fetchJuices(1, true);
  }, []);

  useEffect(() => {
    if (selectedBranch) {
      setJuices([]);
      setPage(1);
      setHasMore(true);
      fetchJuices(1, true);
    }
  }, [selectedCategory, selectedBranch]); // Added selectedBranch to dependencies

  const fetchCategories = async () => {
    try {
      const response = await api.get('/products/categories/');
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };


  const fetchJuices = async (pageNum, reset = false) =>{
    if (!hasMore && !reset) return;
    
    setLoadingMore(true);
    try {
      const params = { page: pageNum };
      if (selectedCategory !== 'all') {
        params.category_id = selectedCategory;
      }
      
      let response;
      // If branch is selected, use branch-specific endpoint
      // Otherwise, fallback to general juices endpoint
      if (selectedBranch) {
        response = await api.get(`/products/branches/${selectedBranch.id}/products/`, { params });
      } else {
        response = await api.get(`/products/juices/`, { params });
      }
      
      const newJuices = response.data.results || response.data;
      
      if (reset) {
        setJuices(newJuices);
      } else {
        setJuices(prev => [...prev, ...newJuices]);
      }
      
      setHasMore(!!response.data.next);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching juices:', error);
      showToast('Failed to load juices', 'error');
      setLoading(false);
    } finally {
      setLoadingMore(false);
    }
  };

  const lastJuiceElementRef = useCallback(node => {
    if (loadingMore) return;
    if (observer.current) observer.current.disconnect();
    
    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && hasMore) {
        setPage(prevPage => {
          const nextPage = prevPage + 1;
          fetchJuices(nextPage);
          return nextPage;
        });
      }
    });
    
    if (node) observer.current.observe(node);
  }, [loadingMore, hasMore]);

  // Scroll-based zoom animation
  useEffect(() => {
    const scrollObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('scale-100', 'opacity-100');
            entry.target.classList.remove('scale-90', 'opacity-0');
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      }
    );

    // Observe all product cards
    const cards = document.querySelectorAll('.product-card');
    cards.forEach((card) => scrollObserver.observe(card));

    return () => scrollObserver.disconnect();
  }, [juices]);

  const handleAddToCart = async (juice) => {
    const accessToken = sessionStorage.getItem('accessToken');
    if (!accessToken) {
      showToast('Please login to add items to cart', 'warning');
      navigate('/login');
      return;
    }

    const result = await addToCart(juice.id, 1);
    if (result.success) {
      showToast('Added to cart!', 'success');
    } else {
      showToast('Failed to add to cart', 'error');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-[#F5F2ED]">
        <div className="text-lg font-medium text-gray-700">Loading menu...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white px-4 py-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-semibold text-gray-800 mb-2">
            Our Menu
          </h1>
          <p className="text-gray-600">
            Fresh pressed wellness delivered with care
          </p>
        </div>

        {/* Category Filter */}
        <CategoryFilter 
          categories={categories}
          selectedCategory={selectedCategory}
          onSelectCategory={setSelectedCategory}
        />

        {/* Products Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
          {juices.map((juice, index) => {
            const isLast = juices.length === index + 1;
            return (
              <div 
                key={juice.id} 
                ref={isLast ? lastJuiceElementRef : null}
                onClick={() => navigate(`/juice/${juice.id}`)}
                className="product-card bg-white rounded-2xl shadow-sm overflow-hidden hover:-translate-y-2 hover:shadow-lg transition-all duration-500 cursor-pointer scale-90 opacity-0"
              >
                {/* Product Image - Static, no zoom */}
                <div className="aspect-[4/3] bg-gray-100 overflow-hidden">
                  <img
                    src={juice.image ? (juice.image.startsWith('http') ? juice.image : `${BASE_URL}${juice.image}`) : '/carrot-juice.png'}
                    alt={juice.name}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.target.src = '/carrot-juice.png';
                    }}
                  />
                </div>

                {/* Product Info */}
                <div className="p-5">
                  <div className="text-xs text-gray-500 mb-1">{juice.category?.name || 'Juice'}</div>
                  <h3 className="text-lg font-semibold text-gray-800 mb-2">{juice.name}</h3>
                  <p className="text-sm text-gray-600 mb-4 line-clamp-2">
                    {juice.description || 'Fresh and delicious juice made with premium ingredients.'}
                  </p>

                  {/* Price and Add Button */}
                  <div className="flex items-center justify-between">
                    <div className="text-xl font-semibold text-gray-800">
                      ₹{juice.price}
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleAddToCart(juice);
                      }}
                      className="px-6 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition font-medium text-sm flex items-center gap-2"
                    >
                      <span>+</span>
                      <span>Add</span>
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Loading More */}
        {loadingMore && (
          <div className="text-center py-8">
            <div className="text-gray-600">Loading more...</div>
          </div>
        )}

        {/* No Results */}
        {!loading && juices.length === 0 && (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">🥤</div>
            <h3 className="text-2xl font-semibold text-gray-800 mb-2">No juices found</h3>
            <p className="text-gray-600">Try selecting a different category</p>
          </div>
        )}
      </div>
    </div>
  );
}
