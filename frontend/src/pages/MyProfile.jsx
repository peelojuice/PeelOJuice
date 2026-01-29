import { useState, useEffect } from 'react';
import { User, Mail, Phone, Edit2, Save, X, CheckCircle, Shield, Zap, Package, MapPin, TrendingUp } from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';

export default function MyProfile() {
  const { showToast } = useToast();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({ full_name: '' });
  const [stats, setStats] = useState({ totalOrders: 0, totalSpent: 0, savedAddresses: 0 });

  useEffect(() => {
    fetchProfile();
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const ordersResponse = await api.get('/orders/my-orders/');
      const orders = ordersResponse.data.orders || [];
      const addressesResponse = await api.get('/addresses/');
      const addresses = addressesResponse.data || [];
      setStats({
        totalOrders: orders.length,
        totalSpent: orders.reduce((sum, order) => sum + parseFloat(order.total_amount || 0), 0),
        savedAddresses: addresses.length
      });
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const fetchProfile = async () => {
    try {
      const response = await api.get('/users/profile/');
      setProfile(response.data);
      setFormData({ full_name: response.data.full_name || '' });
    } catch (error) {
      showToast('Failed to load profile', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      const response = await api.put('/users/profile/', formData);
      setProfile(response.data);
      setEditing(false);
      showToast('Profile updated successfully', 'success');
    } catch (error) {
      showToast('Failed to update profile', 'error');
    }
  };

  const handleCancel = () => {
    setFormData({ full_name: profile.full_name || '' });
    setEditing(false);
  };

  if (loading) {
    return (
      <div className="flex flex-col justify-center items-center min-h-screen bg-white gap-4">
        <div className="w-12 h-12 border-4 border-[#FF6B35] border-t-transparent rounded-full animate-spin"></div>
        <div className="text-lg font-black text-[#1A1A1A] tracking-tighter uppercase">Preparing your workspace...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white pb-20">
      <div className="max-w-5xl mx-auto px-6 py-10">
        <div className="flex items-center gap-4 mb-12">
          <div className="w-12 h-12 bg-[#1A1A1A] rounded-2xl flex items-center justify-center shadow-lg transform rotate-3">
            <User className="w-6 h-6 text-[#FF6B35]" />
          </div>
          <div>
            <h1 className="text-4xl font-black text-[#1A1A1A] tracking-tighter uppercase leading-none">Your Identity</h1>
            <p className="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mt-1">Personalized wellness dashboard</p>
          </div>
        </div>

        <div className="grid lg:grid-cols-[1fr_350px] gap-12 items-start">
          <div className="space-y-10">
            {/* Profile Overview Card */}
            <div className="bg-[#1A1A1A] rounded-[40px] p-10 text-white shadow-2xl relative overflow-hidden group">
               <div className="absolute top-0 right-0 w-64 h-64 bg-[#FF6B35] opacity-10 rounded-full -mr-32 -mt-32 transition-transform duration-1000 group-hover:scale-110"></div>
               
               <div className="flex flex-col md:flex-row items-center gap-8 relative z-10">
                  <div className="w-32 h-32 rounded-[40px] bg-white/10 backdrop-blur-md border border-white/20 flex items-center justify-center shadow-2xl relative">
                     <User className="w-16 h-16 text-white opacity-50" />
                     <div className="absolute -bottom-2 -right-2 w-10 h-10 bg-[#FF6B35] rounded-xl flex items-center justify-center border-4 border-[#1A1A1A]">
                        <Zap className="w-4 h-4 text-white" fill="currentColor" />
                     </div>
                  </div>
                  <div className="text-center md:text-left">
                     {editing ? (
                        <input
                           type="text"
                           value={formData.full_name}
                           onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                           className="bg-white/10 border border-white/20 rounded-2xl px-6 py-3 text-2xl font-black uppercase tracking-tighter focus:outline-none focus:bg-white/20 transition-all w-full md:w-auto"
                           placeholder="Your Name"
                        />
                     ) : (
                        <h2 className="text-4xl font-black uppercase tracking-tighter leading-none mb-2">{profile.full_name || 'PeelOJuice User'}</h2>
                     )}
                     <p className="text-[10px] font-black text-gray-400 tracking-[0.2em] uppercase">Joined {new Date(profile.created_at).toLocaleDateString('en-IN', { month: 'long', year: 'numeric' })}</p>
                  </div>
               </div>

               <div className="mt-12 flex flex-wrap justify-center md:justify-start gap-4">
                  {editing ? (
                     <>
                        <button onClick={handleSave} className="bg-white text-[#1A1A1A] px-8 py-4 rounded-[20px] font-black uppercase tracking-widest text-[10px] hover:bg-[#FF6B35] hover:text-white transition-all shadow-xl flex items-center gap-2">
                           <Save className="w-4 h-4" /> Save
                        </button>
                        <button onClick={handleCancel} className="bg-white/10 backdrop-blur-md border border-white/20 text-white px-8 py-4 rounded-[20px] font-black uppercase tracking-widest text-[10px] hover:bg-white/20 transition-all">
                           <X className="w-4 h-4" />
                        </button>
                     </>
                  ) : (
                    <button onClick={() => setEditing(true)} className="bg-white text-[#1A1A1A] px-10 py-5 rounded-[24px] font-black uppercase tracking-widest text-[10px] hover:bg-[#FF6B35] hover:text-white transition-all shadow-xl flex items-center gap-3">
                       <Edit2 className="w-4 h-4" /> Edit Profile
                    </button>
                  )}
               </div>
            </div>

            {/* Account Details */}
            <div className="grid md:grid-cols-2 gap-6">
               <div className="bg-[#F9F9F9] rounded-[32px] p-8 border border-[#F0F0F0] hover:bg-white transition-all group">
                  <div className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center shadow-sm border border-[#F0F0F0] text-[#FF6B35] mb-6 group-hover:scale-110 transition-transform">
                     <Mail className="w-5 h-5" />
                  </div>
                  <p className="text-[8px] font-black text-gray-400 uppercase tracking-widest mb-1">Email Address</p>
                  <p className="text-sm font-black text-[#1A1A1A] uppercase tracking-tighter break-all mb-4">{profile.email}</p>
                  <div className="flex">
                     <span className={`px-4 py-1.5 rounded-full text-[8px] font-black uppercase tracking-[0.2em] ${profile.is_email_verified ? 'bg-[#F4FFF0] text-green-600 border border-[#D1F0C4]' : 'bg-[#FFF5F8] text-red-500 border border-[#FED7E2]'}`}>
                        {profile.is_email_verified ? 'Verified' : 'Unverified'}
                     </span>
                  </div>
               </div>

               <div className="bg-[#F9F9F9] rounded-[32px] p-8 border border-[#F0F0F0] hover:bg-white transition-all group">
                  <div className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center shadow-sm border border-[#F0F0F0] text-[#FF6B35] mb-6 group-hover:scale-110 transition-transform">
                     <Phone className="w-5 h-5" />
                  </div>
                  <p className="text-[8px] font-black text-gray-400 uppercase tracking-widest mb-1">Phone Number</p>
                  <p className="text-sm font-black text-[#1A1A1A] uppercase tracking-tighter mb-4">{profile.phone_number || 'STILL FRESH'}</p>
                  <div className="flex">
                     <span className={`px-4 py-1.5 rounded-full text-[8px] font-black uppercase tracking-[0.2em] ${profile.is_phone_verified ? 'bg-[#F4FFF0] text-green-600 border border-[#D1F0C4]' : 'bg-[#FFF5F8] text-red-500 border border-[#FED7E2]'}`}>
                        {profile.is_phone_verified ? 'Verified' : 'Action Needed'}
                     </span>
                  </div>
               </div>
            </div>
          </div>

          <aside className="space-y-6 lg:mt-0">
             <div className="bg-white rounded-[40px] border border-[#F0F0F0] p-10 shadow-[0_20px_50px_rgba(0,0,0,0.03)]">
                <h3 className="text-lg font-black text-[#1A1A1A] uppercase tracking-tighter mb-10 flex items-center gap-3">
                   <TrendingUp className="w-5 h-5 text-[#FF6B35]" />
                   Wellness Stats
                </h3>
                
                <div className="space-y-8">
                   <div className="flex items-center gap-6">
                      <div className="w-16 h-16 bg-[#F9F9F9] rounded-2xl flex items-center justify-center border border-[#F0F0F0] text-[#FF6B35]">
                         <Package className="w-7 h-7" />
                      </div>
                      <div>
                         <p className="text-[24px] font-black text-[#1A1A1A] tracking-tighter leading-none">{stats.totalOrders}</p>
                         <p className="text-[9px] font-black text-gray-400 uppercase tracking-widest">Total Orders</p>
                      </div>
                   </div>

                   <div className="flex items-center gap-6">
                      <div className="w-16 h-16 bg-[#F9F9F9] rounded-2xl flex items-center justify-center border border-[#F0F0F0] text-green-500">
                         <TrendingUp className="w-7 h-7" />
                      </div>
                      <div>
                         <p className="text-[24px] font-black text-[#1A1A1A] tracking-tighter leading-none">₹{stats.totalSpent.toFixed(0)}</p>
                         <p className="text-[9px] font-black text-gray-400 uppercase tracking-widest">Total Spent</p>
                      </div>
                   </div>

                   <div className="flex items-center gap-6">
                      <div className="w-16 h-16 bg-[#F9F9F9] rounded-2xl flex items-center justify-center border border-[#F0F0F0] text-blue-500">
                         <MapPin className="w-7 h-7" />
                      </div>
                      <div>
                         <p className="text-[24px] font-black text-[#1A1A1A] tracking-tighter leading-none">{stats.savedAddresses}</p>
                         <p className="text-[9px] font-black text-gray-400 uppercase tracking-widest">Addresses</p>
                      </div>
                   </div>
                </div>
             </div>

             <div className="bg-[#FFF9F0] rounded-3xl p-8 border border-[#FEEBC8]">
                <div className="flex items-center gap-3 mb-6">
                   <Shield className="w-6 h-6 text-[#FF6B35]" />
                   <span className="text-[10px] font-black text-[#1A1A1A] uppercase tracking-widest">Privacy Shield</span>
                </div>
                <p className="text-[10px] font-bold text-gray-500 uppercase leading-relaxed tracking-tight">
                   Your personal data is encrypted and never shared. Wellness is private.
                </p>
             </div>
          </aside>
        </div>
      </div>
    </div>
  );
}
