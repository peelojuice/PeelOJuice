import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { CheckCircle, Package, CreditCard, Clock, Star, Zap, ShoppingBag } from 'lucide-react';

export default function OrderSuccess() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [orderDetails] = useState({
    orderId: searchParams.get('orderId'),
    method: searchParams.get('method'),
    success: searchParams.get('success') === 'true'
  });

  useEffect(() => {
    if (!orderDetails.success) {
      const timer = setTimeout(() => navigate('/orders'), 2000);
      return () => clearTimeout(timer);
    }
  }, [orderDetails.success, navigate]);

  if (!orderDetails.success) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white px-6">
        <div className="bg-white rounded-[40px] border border-[#F0F0F0] p-12 max-w-md w-full text-center shadow-2xl animate-in fade-in slide-in-from-top-4">
          <div className="w-24 h-24 bg-[#FFF5F8] border border-[#FED7E2] rounded-[30px] flex items-center justify-center mx-auto mb-8 text-red-500">
             <div className="w-12 h-12 border-4 border-red-500 rounded-full flex items-center justify-center font-black text-2xl">!</div>
          </div>
          <h1 className="text-3xl font-black text-[#1A1A1A] tracking-tighter uppercase mb-4 leading-none">Entry Denied</h1>
          <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest leading-relaxed mb-8">Security check failed or payment was interrupted. Redirecting to your command center...</p>
        </div>
      </div>
    );
  }

  const paymentMethodDisplay = orderDetails.method === 'cod' ? 'Cash Collective' : 'Digital Transfer';

  return (
    <div className="min-h-screen bg-white flex items-center justify-center px-6 py-12">
      <div className="max-w-2xl w-full">
        {/* Success Header */}
        <div className="text-center mb-16 relative">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-[#FF6B35]/5 rounded-full blur-3xl -z-10 animate-pulse"></div>
          <div className="inline-flex items-center justify-center w-28 h-28 bg-[#FF6B35] rounded-[36px] shadow-2xl shadow-[#FF6B35]/40 mb-10 transform scale-110 rotate-3">
             <Star className="w-14 h-14 text-white" fill="currentColor" />
          </div>
          <h1 className="text-5xl font-black text-[#1A1A1A] tracking-tighter uppercase mb-2 leading-none">Mission Success</h1>
          <p className="text-[10px] font-black text-[#FF6B35] uppercase tracking-[0.4em]">Energy Is On Its Way</p>
        </div>

        {/* Order Intel Card */}
        <div className="bg-white rounded-[48px] border-2 border-[#1A1A1A] p-10 md:p-14 shadow-[0_40px_100px_rgba(0,0,0,0.1)] relative overflow-hidden mb-12">
           <div className="absolute top-0 right-0 w-32 h-32 bg-[#FF6B35]/5 rounded-bl-[100px]"></div>
           
           <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-8 mb-12 border-b border-[#F0F0F0] pb-10">
              <div>
                <p className="text-[8px] font-black text-gray-400 uppercase tracking-widest mb-1">Authorization ID</p>
                <h2 className="text-3xl font-black text-[#1A1A1A] tracking-tighter">#{orderDetails.orderId}</h2>
              </div>
              <div className="flex flex-col items-end">
                <p className="text-[8px] font-black text-gray-400 uppercase tracking-widest mb-2">Operational Status</p>
                <span className="px-6 py-2 bg-[#1A1A1A] text-white rounded-full text-[10px] font-black uppercase tracking-[0.2em]">Confirmed</span>
              </div>
           </div>

           <div className="grid md:grid-cols-2 gap-12">
              <div className="flex gap-6">
                 <div className="w-14 h-14 bg-[#F9F9F9] border border-[#F0F0F0] rounded-2xl flex items-center justify-center text-[#FF6B35]">
                    <CreditCard className="w-6 h-6" />
                 </div>
                 <div>
                    <p className="text-[8px] font-black text-gray-400 uppercase tracking-widest mb-1">Transfer Method</p>
                    <p className="text-sm font-black text-[#1A1A1A] uppercase tracking-tighter">{paymentMethodDisplay}</p>
                 </div>
              </div>
              <div className="flex gap-6">
                 <div className="w-14 h-14 bg-[#F9F9F9] border border-[#F0F0F0] rounded-2xl flex items-center justify-center text-[#FF6B35]">
                    <Clock className="w-6 h-6" />
                 </div>
                 <div>
                    <p className="text-[8px] font-black text-gray-400 uppercase tracking-widest mb-1">Estimated Dispatch</p>
                    <p className="text-sm font-black text-[#1A1A1A] uppercase tracking-tighter">Under 30 Minutes</p>
                 </div>
              </div>
           </div>

           <div className="mt-14 pt-10 border-t border-[#F0F0F0] flex items-center justify-between">
              <div className="flex items-center gap-3">
                 <Zap className="w-5 h-5 text-[#FF6B35]" fill="currentColor" />
                 <span className="text-[9px] font-black text-[#1A1A1A] uppercase tracking-widest">Priority Processing Active</span>
              </div>
              <p className="text-[9px] font-black text-gray-300 uppercase tracking-widest">Licensed Wellness</p>
           </div>
        </div>

        {/* Tactical Actions */}
        <div className="flex flex-col md:flex-row gap-6">
           <button
              onClick={() => navigate('/orders')}
              className="flex-1 bg-[#1A1A1A] text-white py-8 rounded-[32px] font-black uppercase tracking-[0.3em] text-[10px] hover:bg-black transition-all shadow-2xl active:scale-95 flex items-center justify-center gap-4"
           >
              <Package className="w-5 h-5 text-[#FF6B35]" />
              Track Intel
           </button>
           <button
              onClick={() => navigate('/menu')}
              className="flex-1 bg-white text-[#1A1A1A] border-2 border-[#1A1A1A] py-8 rounded-[32px] font-black uppercase tracking-[0.3em] text-[10px] hover:bg-[#F9F9F9] transition-all active:scale-95 flex items-center justify-center gap-4"
           >
              <ShoppingBag className="w-5 h-5 text-[#FF6B35]" />
              Deploy More
           </button>
        </div>

        <p className="text-center mt-12 text-[8px] font-black text-gray-300 uppercase tracking-[0.5em]">Electronic confirmation dispatched to your communication channel</p>
      </div>
    </div>
  );
}
