import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Phone, Hash, Leaf } from 'lucide-react';
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
    <div className="min-h-screen bg-[#F5F2ED] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Branding */}
        <div className="text-center mb-8">
          <div className="mb-2">
            <div className="text-4xl font-bold">
              <span className="text-[#F5A623]">Peel</span>
              <span className="text-[#FF6B35]">O</span>
              <span className="text-gray-800">JUICE</span>
            </div>
          </div>
          <p className="text-sm text-gray-500">Verify Your Phone</p>
        </div>

        {/* Verify Card */}
        <div className="bg-white rounded-2xl shadow-sm p-8">
          <div className="text-center mb-6">
            <div className="w-16 h-16 bg-[#8BA888]/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Phone className="w-8 h-8 text-[#8BA888]" />
            </div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-2">Check Your Phone</h2>
            <p className="text-gray-600 text-sm">
              We've sent a verification code to<br />
              <span className="font-semibold text-gray-800">{phone}</span>
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* OTP Input */}
            <div>
              <label className="block text-sm text-gray-600 mb-2">Enter Code</label>
              <input
                type="text"
                placeholder="000000"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                maxLength={6}
                className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:border-[#8BA888] focus:ring-1 focus:ring-[#8BA888] transition text-gray-700 text-center text-xl tracking-widest font-semibold"
                required
              />
            </div>

            {/* Verify Button */}
            <button
              type="submit"
              disabled={loading || otp.length !== 6}
              className="w-full bg-[#8BA888] text-white font-medium py-3 rounded-lg hover:bg-[#7a9677] transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Verifying...' : 'Verify Phone'}
            </button>

            {/* Resend Link */}
            <div className="text-center">
              <button
                type="button"
                className="text-gray-600 hover:text-gray-800 font-medium text-sm underline"
              >
                Didn't receive code? Resend
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
