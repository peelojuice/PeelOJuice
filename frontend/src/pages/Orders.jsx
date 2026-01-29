import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Package, Clock, CheckCircle, XCircle, Eye, Search, Filter, ChevronRight, Zap } from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [filteredOrders, setFilteredOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const navigate = useNavigate();
  const { showToast } = useToast();

  useEffect(() => {
    fetchOrders();
  }, []);

  useEffect(() => {
    filterOrders();
  }, [orders, searchQuery, statusFilter]);

  const fetchOrders = async () => {
    try {
      const response = await api.get('/orders/my-orders/');
      const ordersData = response.data.orders || [];
      setOrders(ordersData);
    } catch (error) {
      showToast('Failed to load orders', 'error');
    } finally {
      setLoading(false);
    }
  };

  const filterOrders = () => {
    let filtered = [...orders];
    if (statusFilter !== 'all') {
      filtered = filtered.filter(order => order.status.toLowerCase() === statusFilter);
    }
    if (searchQuery) {
      filtered = filtered.filter(order =>
        order.id.toString().includes(searchQuery) ||
        (order.items && order.items.some(item => 
          item.juice_name?.toLowerCase().includes(searchQuery.toLowerCase())
        ))
      );
    }
    setFilteredOrders(filtered);
  };

  const getStatusConfig = (status) => {
    switch (status.toLowerCase()) {
      case 'pending': return { icon: Clock, color: 'text-yellow-500', bg: 'bg-[#FFF9F0]', border: 'border-[#FEEBC8]' };
      case 'delivered': return { icon: CheckCircle, color: 'text-green-500', bg: 'bg-[#F4FFF0]', border: 'border-[#D1F0C4]' };
      case 'cancelled': return { icon: XCircle, color: 'text-red-500', bg: 'bg-[#FFF5F8]', border: 'border-[#FED7E2]' };
      default: return { icon: Package, color: 'text-blue-500', bg: 'bg-[#F0F5FF]', border: 'border-[#D1E9FF]' };
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col justify-center items-center min-h-screen bg-white gap-4">
        <div className="w-12 h-12 border-4 border-[#FF6B35] border-t-transparent rounded-full animate-spin"></div>
        <div className="text-lg font-black text-[#1A1A1A] tracking-tighter uppercase">Tracking Wellness...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white pb-20">
      <div className="max-w-6xl mx-auto px-6 py-10">
        <div className="mb-12">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-12 h-12 bg-[#1A1A1A] rounded-2xl flex items-center justify-center shadow-lg">
              <Zap className="w-6 h-6 text-yellow-400" fill="currentColor" />
            </div>
            <div>
              <h1 className="text-4xl font-black text-[#1A1A1A] tracking-tighter uppercase leading-none">Your Orders</h1>
              <p className="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mt-1">Journey of your freshness</p>
            </div>
          </div>
        </div>

        {/* Search & Filter Bar */}
        <div className="flex flex-col md:flex-row gap-4 mb-10">
          <div className="relative flex-1 group">
            <Search className="absolute left-6 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-300 group-focus-within:text-[#FF6B35] transition-colors" />
            <input
              type="text"
              placeholder="Search by ID or product..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-14 pr-6 py-5 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[24px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all placeholder:text-gray-300 placeholder:font-bold"
            />
          </div>

          <div className="flex gap-2 overflow-x-auto pb-2 md:pb-0 scrollbar-hide">
            {['all', 'pending', 'delivered', 'cancelled'].map((status) => (
              <button
                key={status}
                onClick={() => setStatusFilter(status)}
                className={`px-8 py-4 rounded-[20px] text-[10px] font-black uppercase tracking-widest whitespace-nowrap transition-all ${
                  statusFilter === status 
                    ? 'bg-[#1A1A1A] text-white shadow-xl scale-105' 
                    : 'bg-[#F9F9F9] text-gray-400 border border-[#F0F0F0] hover:bg-white'
                }`}
              >
                {status}
              </button>
            ))}
          </div>
        </div>

        {/* Orders List */}
        {filteredOrders.length === 0 ? (
          <div className="text-center py-24 bg-[#F9F9F9] rounded-[40px] border border-[#F0F0F0]">
            <Package className="w-20 h-20 mx-auto text-gray-200 mb-6 opacity-20" />
            <h2 className="text-2xl font-black text-[#1A1A1A] tracking-tighter uppercase mb-2">No results</h2>
            <p className="text-gray-400 font-bold text-xs uppercase tracking-widest mb-10">Try a different filter or check back later</p>
            <button
              onClick={() => navigate('/menu')}
              className="bg-[#1A1A1A] text-white px-10 py-5 rounded-[24px] font-black uppercase tracking-[0.2em] text-[10px] hover:bg-black transition-all shadow-xl active:scale-95"
            >
              Browse Menu
            </button>
          </div>
        ) : (
          <div className="grid gap-6">
            {filteredOrders.map((order) => {
              const cfg = getStatusConfig(order.status);
              return (
                <div
                  key={order.id}
                  onClick={() => navigate(`/orders/${order.id}`)}
                  className="bg-white rounded-[32px] border border-[#F0F0F0] p-8 hover:shadow-[0_20px_60px_rgba(0,0,0,0.05)] hover:border-[#E0E0E0] transition-all cursor-pointer group"
                >
                  <div className="flex flex-col md:flex-row justify-between gap-8">
                    <div className="flex-1">
                      <div className="flex items-center gap-4 mb-4">
                        <div className={`px-4 py-2 rounded-xl border ${cfg.bg} ${cfg.border} ${cfg.color} flex items-center gap-2`}>
                          <cfg.icon className="w-4 h-4" />
                          <span className="text-[10px] font-black uppercase tracking-widest">{order.status}</span>
                        </div>
                        <span className="text-[10px] font-black text-gray-300 uppercase tracking-widest">
                          #{order.order_number || order.id}
                        </span>
                      </div>
                      
                      <div className="flex flex-wrap gap-2 mb-6">
                        {(order.items || []).map((item, idx) => (
                           <div key={idx} className="flex items-center gap-2 bg-[#F9F9F9] px-4 py-2.5 rounded-xl border border-[#F0F0F0]">
                             <span className="text-[10px] font-black text-[#1A1A1A] uppercase tracking-tight">{item.juice_name}</span>
                             <span className="text-[9px] font-black text-[#FF6B35]">x{item.quantity}</span>
                           </div>
                        ))}
                      </div>

                      <div className="flex items-center gap-6">
                        <div>
                          <p className="text-[8px] font-black text-gray-400 uppercase tracking-widest mb-1">Total</p>
                          <p className="text-2xl font-black text-[#1A1A1A] tracking-tighter">₹{Number(order.total_amount).toFixed(0)}</p>
                        </div>
                        <div className="w-px h-8 bg-gray-100"></div>
                        <div>
                          <p className="text-[8px] font-black text-gray-400 uppercase tracking-widest mb-1">Date</p>
                          <p className="text-xs font-black text-[#1A1A1A] uppercase tracking-tighter">
                            {new Date(order.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center justify-end">
                       <div className="w-12 h-12 rounded-2xl bg-[#F9F9F9] flex items-center justify-center border border-[#F0F0F0] group-hover:bg-[#1A1A1A] group-hover:text-white transition-all">
                          <Eye className="w-5 h-5" />
                       </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
