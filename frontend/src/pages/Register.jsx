import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Mail, Lock, User, Phone, Star, Zap, ChevronRight } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Register() {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    password: '',
    confirm_password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [phoneOTP, setPhoneOTP] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (formData.password !== formData.confirm_password) {
      setError('Passwords do not match');
      return;
    }
    setLoading(true);
    try {
      const response = await register(formData);
      if (response.data.phone_otp) setPhoneOTP(response.data.phone_otp);
      navigate('/verify-email', { state: { email: formData.email, phone: formData.phone_number } });
    } catch (err) {
      setError(err.response?.data?.message || 'Joining failed. Please check your data.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex items-center justify-center px-6 py-12">
      <div className="w-full max-w-[540px]">
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

        {/* Register Card */}
        <div className="bg-white rounded-[40px] border border-[#F0F0F0] p-12 shadow-[0_30px_70px_rgba(0,0,0,0.05)]">
          <div className="mb-10 text-center">
            <h2 className="text-2xl font-black text-[#1A1A1A] tracking-tighter uppercase mb-2">Create Identity</h2>
            <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Join the fresh revolution today</p>
          </div>

          {error && (
            <div className="bg-[#FFF5F8] border border-[#FED7E2] text-red-500 px-6 py-4 rounded-2xl mb-8 text-[10px] font-black uppercase tracking-widest text-center animate-in fade-in slide-in-from-top-2">
              {error}
            </div>
          )}

          {phoneOTP && (
            <div className="bg-[#FFF9F0] border border-[#FEEBC8] p-6 rounded-[24px] mb-8 flex items-center justify-between">
              <div>
                <p className="text-[8px] font-black text-[#FF6B35] uppercase tracking-widest mb-1">Dev Environment OTP</p>
                <p className="text-2xl font-black text-[#1A1A1A] tracking-tighter">{phoneOTP}</p>
              </div>
              <Zap className="w-8 h-8 text-[#FF6B35] opacity-20" />
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3 ml-1">First Name</label>
                <input
                  type="text"
                  name="first_name"
                  placeholder="John"
                  value={formData.first_name}
                  onChange={handleChange}
                  className="w-full px-8 py-5 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[24px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all placeholder:text-gray-300 placeholder:font-bold"
                  required
                />
              </div>
              <div>
                <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3 ml-1">Last Name</label>
                <input
                  type="text"
                  name="last_name"
                  placeholder="Doe"
                  value={formData.last_name}
                  onChange={handleChange}
                  className="w-full px-8 py-5 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[24px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all placeholder:text-gray-300 placeholder:font-bold"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3 ml-1">Email Connection</label>
              <div className="relative group">
                <Mail className="absolute left-6 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-300 group-focus-within:text-[#FF6B35] transition-colors" />
                <input
                  type="email"
                  name="email"
                  placeholder="name@energy.com"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full pl-16 pr-6 py-5 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[24px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all placeholder:text-gray-300 placeholder:font-bold"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3 ml-1">Contact Number</label>
              <div className="relative group">
                <Phone className="absolute left-6 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-300 group-focus-within:text-[#FF6B35] transition-colors" />
                <input
                  type="tel"
                  name="phone_number"
                  placeholder="+91 ••••• •••••"
                  value={formData.phone_number}
                  onChange={handleChange}
                  className="w-full pl-16 pr-6 py-5 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[24px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all placeholder:text-gray-300 placeholder:font-bold"
                  required
                />
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3 ml-1">Password</label>
                <input
                  type="password"
                  name="password"
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full px-8 py-5 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[24px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all placeholder:text-gray-300 placeholder:font-bold"
                  required
                />
              </div>
              <div>
                <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3 ml-1">Confirm</label>
                <input
                  type="password"
                  name="confirm_password"
                  placeholder="••••••••"
                  value={formData.confirm_password}
                  onChange={handleChange}
                  className="w-full px-8 py-5 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[24px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all placeholder:text-gray-300 placeholder:font-bold"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-[#1A1A1A] text-white py-6 rounded-[24px] font-black uppercase tracking-[0.2em] text-[10px] hover:bg-black transition-all shadow-xl active:scale-95 disabled:opacity-50 disabled:scale-100 flex items-center justify-center gap-3"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
              ) : (
                <>Join Revolution <ChevronRight className="w-4 h-4 text-[#FF6B35]" /></>
              )}
            </button>

            <div className="text-center pt-4">
              <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Returning warrior?</span>
              <Link to="/login" className="ml-2 text-[10px] font-black text-[#FF6B35] uppercase tracking-widest hover:underline">
                Sign In
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
