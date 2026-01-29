import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Phone, Zap, Star } from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';

export default function VerifyPhone() {
  const navigate = useNavigate();
  const location = useLocation();
  const { showToast } = useToast();
  const phone = location.state?.phone;
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post('/users/verify-phone/', { phone_number: phone, otp });
      showToast('Phone verified successfully!', 'success');
      navigate('/');
    } catch (error) {
      showToast(error.response?.data?.message || 'Verification failed', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex items-center justify-center px-6 py-12">
      <div className="w-full max-w-[480px]">
        {/* Logo Section */}
        <div className="text-center mb-12">
           <div className="inline-flex items-center gap-4 mb-6 group cursor-pointer" onClick={() => navigate('/')}>
             <div className="w-16 h-16 bg-[#FF6B35] rounded-3xl flex items-center justify-center shadow-2xl transform transition-transform group-hover:rotate-12">
                <Star className="w-10 h-10 text-white" fill="currentColor" />
             </div>
             <div className="text-left">
                <h1 className="text-3xl font-black text-[#1A1A1A] tracking-tighter uppercase leading-none">
                  Peel<span className="text-[#FF6B35]">O</span>Juice
                </h1>
                <p className="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mt-1">Nature's purest energy</p>
             </div>
           </div>
        </div>

        <div className="bg-white rounded-[40px] border border-[#F0F0F0] p-10 shadow-[0_30px_70px_rgba(0,0,0,0.05)]">
          <div className="text-center mb-10">
            <div className="w-20 h-20 bg-[#F9F9F9] border border-[#F0F0F0] rounded-[30px] flex items-center justify-center mx-auto mb-6 text-[#FF6B35]">
              <Phone className="w-10 h-10" />
            </div>
            <h2 className="text-2xl font-black text-[#1A1A1A] tracking-tighter uppercase mb-2">Check Your Device</h2>
            <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest leading-relaxed">
              We've dispatched a secure code to<br />
              <span className="text-[#1A1A1A] font-black">{phone}</span>
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-8">
            <div>
              <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3 ml-1 text-center">Enter 6-Digit Gateway Code</label>
              <input
                type="text"
                placeholder="000 000"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                maxLength={6}
                className="w-full px-6 py-5 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[24px] text-3xl font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all text-center tracking-[0.5em] placeholder:text-gray-200"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading || otp.length !== 6}
              className="w-full bg-[#1A1A1A] text-white py-6 rounded-[24px] font-black uppercase tracking-[0.2em] text-[10px] hover:bg-black transition-all shadow-xl active:scale-95 disabled:opacity-30 disabled:scale-100 flex items-center justify-center gap-3"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
              ) : (
                <>Scale Access <Zap className="w-4 h-4 text-[#FF6B35]" fill="currentColor" /></>
              )}
            </button>

            <div className="text-center">
              <button
                type="button"
                className="text-[9px] font-black text-[#FF6B35] uppercase tracking-widest hover:underline"
              >
                Request Fresh Dispatch
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
