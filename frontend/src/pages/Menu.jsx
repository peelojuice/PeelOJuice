import { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, X, Star } from 'lucide-react';
import api from '../services/api';
import { useCart } from '../context/CartContext';
import { useToast } from '../context/ToastContext';
import { useBranch } from '../context/BranchContext';
import CategoryFilter from '../components/CategoryFilter';
import JuiceCard from '../components/JuiceCard';

export default function Menu() {
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const { showToast } = useToast();
  const { selectedBranch } = useBranch();
  const [juices, setJuices] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const observer = useRef();

  useEffect(() => {
    fetchCategories();
    fetchJuices(1, true);
  }, []);

  useEffect(() => {
    setJuices([]);
    setPage(1);
    setHasMore(true);
    fetchJuices(1, true);
  }, [selectedCategory, selectedBranch]);

  const fetchCategories = async () => {
    try {
      const response = await api.get('/products/categories/');
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchJuices = async (pageNum, reset = false) => {
    if (!hasMore && !reset) return;
    
    setLoadingMore(true);
    try {
      const params = { page: pageNum };
      if (selectedCategory !== 'all') {
        params.category_id = selectedCategory;
      }
      
      let response;
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

  const handleAddToCart = async (juice) => {
    const accessToken = sessionStorage.getItem('accessToken');
    if (!accessToken) {
      showToast('Please login to add items to cart', 'warning');
      navigate('/login');
      return;
    }

    const result = await addToCart(juice.id, 1);
    if (result.success) {
      showToast(`${juice.name} added!`, 'success');
    } else {
      showToast('Failed to add to cart', 'error');
    }
  };

  // Filter juices by search query for current page
  const filteredJuices = useMemo(() => {
    if (!searchQuery) return juices;
    return juices.filter(juice => 
      juice.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      juice.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      juice.category?.name?.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [juices, searchQuery]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-white">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-[#FF6B35] border-t-transparent rounded-full animate-spin"></div>
          <div className="text-lg font-extrabold text-[#1A1A1A] tracking-tight">Refreshing Menu...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white pb-24">
      {/* Header Section */}
      <div className="bg-white pt-10 pb-4">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
            <div className="flex items-center gap-3">
              <div className="bg-[#FFF9F0] p-2 rounded-2xl">
                <Star className="w-8 h-8 text-[#FF6B35]" fill="#FF6B35" />
              </div>
              <div>
                <h1 className="text-3xl font-black text-[#1A1A1A] tracking-tighter uppercase">
                  Our Menu
                </h1>
                <p className="text-gray-400 font-bold text-xs uppercase tracking-widest mt-0.5">
                  Freshness in every sip
                </p>
              </div>
            </div>

            {/* Premium Search Bar */}
            <div className="relative group flex-1 max-w-md">
              <div className="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-gray-400 group-focus-within:text-[#FF6B35] transition-colors" />
              </div>
              <input
                type="text"
                className="block w-full pl-12 pr-12 py-4 bg-[#F9F9F9] border border-[#F0F0F0] rounded-[24px] text-gray-800 font-bold text-sm focus:outline-none focus:ring-2 focus:ring-[#FF6B35]/20 focus:border-[#FF6B35] transition-all placeholder:text-gray-400 placeholder:font-medium"
                placeholder="Search juices, categories..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              {searchQuery && (
                <button 
                  onClick={() => setSearchQuery('')}
                  className="absolute inset-y-0 right-0 pr-5 flex items-center text-gray-400 hover:text-gray-600"
                >
                  <X className="h-5 w-5" />
                </button>
              )}
            </div>
          </div>

          {/* Category Filter */}
          <CategoryFilter 
            categories={categories}
            selectedCategory={selectedCategory}
            onSelectCategory={setSelectedCategory}
          />
        </div>
      </div>

      {/* Products Grid */}
      <div className="max-w-7xl mx-auto px-6">
        {filteredJuices.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {filteredJuices.map((juice, index) => {
              const isLast = filteredJuices.length === index + 1;
              return (
                <div 
                  key={juice.id} 
                  ref={isLast ? lastJuiceElementRef : null}
                  className="animate-in fade-in slide-in-from-bottom-4 duration-500 fill-mode-both"
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  <JuiceCard 
                    juice={juice} 
                    onAddToCart={handleAddToCart} 
                  />
                </div>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-32 flex flex-col items-center">
            <div className="w-24 h-24 bg-[#F9F9F9] rounded-full flex items-center justify-center mb-6 border border-[#F0F0F0]">
              <Search className="w-10 h-10 text-[#FF6B35] opacity-20" />
            </div>
            <h3 className="text-2xl font-black text-[#1A1A1A] tracking-tighter uppercase mb-2">
              No juices found
            </h3>
            <p className="text-gray-400 font-bold text-sm uppercase tracking-widest">
              Try a different search or category
            </p>
          </div>
        )}

        {/* Loading More Spinner */}
        {loadingMore && (
          <div className="flex justify-center mt-16 pb-10">
            <div className="w-8 h-8 border-3 border-[#FF6B35] border-t-transparent rounded-full animate-spin"></div>
          </div>
        )}
      </div>
    </div>
  );
}
