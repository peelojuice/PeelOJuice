import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../services/api';
import { Key, Star, Zap, ChevronLeft } from 'lucide-react';

const ForgotPassword = () => {
  const navigate = useNavigate();
  const [emailOrPhone, setEmailOrPhone] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await authAPI.requestPasswordReset({ email_or_phone: emailOrPhone });
      navigate('/verify-reset-otp', { state: { email_or_phone: emailOrPhone } });
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to send security code');
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
              <Key className="w-10 h-10" />
            </div>
            <h2 className="text-2xl font-black text-[#1A1A1A] tracking-tighter uppercase mb-2">Access Recovery</h2>
            <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Enter your identity to reset access</p>
          </div>

          {error && (
            <div className="bg-[#FFF5F8] border border-[#FED7E2] text-red-500 px-6 py-4 rounded-2xl mb-8 text-[10px] font-black uppercase tracking-widest text-center animate-in fade-in slide-in-from-top-2">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-8">
            <div>
              <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3 ml-1">Account Connection</label>
              <input
                type="text"
                value={emailOrPhone}
                onChange={(e) => setEmailOrPhone(e.target.value)}
                placeholder="Email or Phone Number"
                className="w-full px-8 py-5 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[24px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all placeholder:text-gray-300 placeholder:font-bold text-center"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-[#1A1A1A] text-white py-6 rounded-[24px] font-black uppercase tracking-[0.2em] text-[10px] hover:bg-black transition-all shadow-xl active:scale-95 disabled:opacity-30 flex items-center justify-center gap-3"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
              ) : (
                <>Dispatch Code <Zap className="w-4 h-4 text-[#FF6B35]" fill="currentColor" /></>
              )}
            </button>

            <div className="text-center">
              <Link to="/login" className="inline-flex items-center gap-2 text-[9px] font-black text-gray-400 uppercase tracking-widest hover:text-[#FF6B35] transition-colors">
                <ChevronLeft className="w-3 h-3" /> Back to Login
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
