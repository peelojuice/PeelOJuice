import { useState } from 'react';
import { X, MapPin, CheckCircle, Zap } from 'lucide-react';

export default function AddressForm({ address, onSubmit, onCancel, isSubmitting }) {
  const [formData, setFormData] = useState({
    label: address?.label || '',
    full_name: address?.full_name || '',
    phone_number: address?.phone_number || '',
    address_line1: address?.address_line1 || '',
    address_line2: address?.address_line2 || '',
    city: address?.city || '',
    state: address?.state || '',
    pincode: address?.pincode || '',
    landmark: address?.landmark || '',
    is_default: address?.is_default || false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-6 animate-in fade-in duration-300">
      <div className="bg-white rounded-[40px] shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto scrollbar-hide border border-[#F0F0F0]">
        {/* Header */}
        <div className="sticky top-0 bg-white/80 backdrop-blur-md z-10 px-10 py-8 border-b border-[#F0F0F0] flex justify-between items-center">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 bg-[#1A1A1A] rounded-2xl flex items-center justify-center text-[#FF6B35]">
              <MapPin className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-xl font-black text-[#1A1A1A] tracking-tighter uppercase leading-none">
                {address ? 'Modify Spot' : 'New Destination'}
              </h2>
              <p className="text-[8px] font-black text-gray-400 uppercase tracking-widest mt-1">Configure your delivery zone</p>
            </div>
          </div>
          <button
            onClick={onCancel}
            className="w-10 h-10 bg-[#F9F9F9] border border-[#F0F0F0] rounded-2xl flex items-center justify-center text-[#1A1A1A] hover:bg-white transition-all active:scale-95"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form Content */}
        <form onSubmit={handleSubmit} className="p-10 space-y-8">
          <div>
            <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3 ml-1">Location Label</label>
            <input
              type="text"
              name="label"
              value={formData.label}
              onChange={handleChange}
              placeholder="Home / Office / Gym"
              className="w-full px-6 py-4 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[20px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all placeholder:text-gray-300 placeholder:font-bold"
              required
            />
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3 ml-1">Receiver Name</label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                placeholder="Full Legal Name"
                className="w-full px-6 py-4 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[20px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all placeholder:text-gray-300 placeholder:font-bold"
                required
              />
            </div>
            <div>
              <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3 ml-1">Direct Contact</label>
              <input
                type="tel"
                name="phone_number"
                value={formData.phone_number}
                onChange={handleChange}
                placeholder="+91 ••••• •••••"
                className="w-full px-6 py-4 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[20px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all placeholder:text-gray-300 placeholder:font-bold"
                required
              />
            </div>
          </div>

          <div className="space-y-4">
            <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-1 ml-1">Exact Address Details</label>
            <input
              type="text"
              name="address_line1"
              value={formData.address_line1}
              onChange={handleChange}
              placeholder="House/Flat No., Building Name"
              className="w-full px-6 py-4 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[20px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all placeholder:text-gray-300 placeholder:font-bold"
              required
            />
            <input
              type="text"
              name="address_line2"
              value={formData.address_line2}
              onChange={handleChange}
              placeholder="Street, Area, Colony (Optional)"
              className="w-full px-6 py-4 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[20px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all placeholder:text-gray-300 placeholder:font-bold"
            />
          </div>

          <div className="grid grid-cols-3 gap-6">
            <div>
              <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3 ml-1">City</label>
              <input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleChange}
                className="w-full px-6 py-4 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[20px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all"
                required
              />
            </div>
            <div>
              <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3 ml-1">State</label>
              <input
                type="text"
                name="state"
                value={formData.state}
                onChange={handleChange}
                className="w-full px-6 py-4 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[20px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all"
                required
              />
            </div>
            <div>
              <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3 ml-1">Zipcode</label>
              <input
                type="text"
                name="pincode"
                value={formData.pincode}
                onChange={handleChange}
                className="w-full px-6 py-4 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[20px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-[8px] font-black text-gray-400 uppercase tracking-[0.2em] mb-3 ml-1">Landmark</label>
            <input
              type="text"
              name="landmark"
              value={formData.landmark}
              onChange={handleChange}
              placeholder="e.g. Near Rose Garden (Optional)"
              className="w-full px-6 py-4 bg-[#F9F9F9] border-2 border-[#F0F0F0] rounded-[20px] text-sm font-black text-[#1A1A1A] focus:bg-white focus:border-[#FF6B35] focus:outline-none transition-all placeholder:text-gray-300 placeholder:font-bold"
            />
          </div>

          <div className="flex items-center gap-4 bg-[#F9F9F9] p-6 rounded-[24px] border border-[#F0F0F0]">
            <div className="relative flex items-center">
              <input
                type="checkbox"
                name="is_default"
                id="is_default"
                checked={formData.is_default}
                onChange={handleChange}
                className="peer w-6 h-6 opacity-0 absolute cursor-pointer"
              />
              <div className="w-6 h-6 border-2 border-[#F0F0F0] rounded-lg peer-checked:bg-[#FF6B35] peer-checked:border-[#FF6B35] transition-all flex items-center justify-center">
                <CheckCircle className="w-4 h-4 text-white opacity-0 peer-checked:opacity-100" />
              </div>
            </div>
            <label htmlFor="is_default" className="text-[10px] font-black text-[#1A1A1A] uppercase tracking-widest cursor-pointer">
              Mark as Primary Destination
            </label>
          </div>

          <div className="flex gap-4 pt-4">
            <button
              type="button"
              onClick={onCancel}
              className="flex-1 px-8 py-5 bg-[#F9F9F9] text-[#1A1A1A] rounded-[24px] font-black uppercase text-[10px] tracking-widest hover:bg-white border border-[#F0F0F0] transition-all"
            >
              Discard Changes
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 px-8 py-5 bg-[#1A1A1A] text-white rounded-[24px] font-black uppercase text-[10px] tracking-[0.2em] hover:bg-black transition-all shadow-xl active:scale-95 disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {isSubmitting ? (
                <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
              ) : (
                <>Scale Destination <Zap className="w-3.5 h-3.5 text-[#FF6B35]" fill="currentColor" /></>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
