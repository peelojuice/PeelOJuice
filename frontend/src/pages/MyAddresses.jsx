import { useState, useEffect } from 'react';
import { Plus, MapPin, Edit, Trash2, Star, Zap, Map } from 'lucide-react';
import addressAPI from '../services/addressAPI';
import { useToast } from '../context/ToastContext';
import AddressForm from '../components/AddressForm';

export default function MyAddresses() {
  const [addresses, setAddresses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingAddress, setEditingAddress] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const { showToast } = useToast();

  useEffect(() => {
    fetchAddresses();
  }, []);

  const fetchAddresses = async () => {
    try {
      const response = await addressAPI.getAddresses();
      setAddresses(response.data);
    } catch (error) {
      showToast('Failed to load addresses', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (formData) => {
    setSubmitting(true);
    try {
      if (editingAddress) {
        await addressAPI.updateAddress(editingAddress.id, formData);
        showToast('Address updated successfully', 'success');
      } else {
        await addressAPI.createAddress(formData);
        showToast('Address added successfully', 'success');
      }
      fetchAddresses();
      setShowForm(false);
      setEditingAddress(null);
    } catch (error) {
      showToast(error.response?.data?.message || 'Failed to save address', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this address?')) return;
    try {
      await addressAPI.deleteAddress(id);
      showToast('Address deleted successfully', 'success');
      fetchAddresses();
    } catch (error) {
      showToast('Failed to delete address', 'error');
    }
  };

  const handleSetDefault = async (id) => {
    try {
      await addressAPI.setDefaultAddress(id);
      showToast('Default address updated', 'success');
      fetchAddresses();
    } catch (error) {
      showToast('Failed to set default address', 'error');
    }
  };

  const handleEdit = (address) => {
    setEditingAddress(address);
    setShowForm(true);
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingAddress(null);
  };

  if (loading) {
    return (
      <div className="flex flex-col justify-center items-center min-h-screen bg-white gap-4">
        <div className="w-12 h-12 border-4 border-[#FF6B35] border-t-transparent rounded-full animate-spin"></div>
        <div className="text-lg font-black text-[#1A1A1A] tracking-tighter uppercase">Locating your spots...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white pb-20">
      <div className="max-w-6xl mx-auto px-6 py-10">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-12">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-[#1A1A1A] rounded-2xl flex items-center justify-center shadow-lg">
              <Map className="w-6 h-6 text-[#FF6B35]" />
            </div>
            <div>
              <h1 className="text-4xl font-black text-[#1A1A1A] tracking-tighter uppercase leading-none">Saved Locations</h1>
              <p className="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mt-1">Manage where we bring your health</p>
            </div>
          </div>
          <button
            onClick={() => setShowForm(true)}
            className="group flex items-center gap-3 bg-[#FF6B35] text-white px-8 py-5 rounded-[24px] font-black uppercase tracking-widest text-[10px] hover:bg-black transition-all shadow-xl active:scale-95"
          >
            <Plus className="w-4 h-4 group-hover:rotate-90 transition-transform" />
            Add New Address
          </button>
        </div>

        {addresses.length === 0 ? (
          <div className="text-center py-24 bg-[#F9F9F9] rounded-[40px] border border-[#F0F0F0]">
            <MapPin className="w-20 h-20 mx-auto text-gray-200 mb-6 opacity-20" />
            <h2 className="text-2xl font-black text-[#1A1A1A] tracking-tighter uppercase mb-2">No addresses yet</h2>
            <p className="text-gray-400 font-bold text-xs uppercase tracking-widest mb-10">Save your favorite spots for faster checkout</p>
            <button
              onClick={() => setShowForm(true)}
              className="bg-[#1A1A1A] text-white px-10 py-5 rounded-[24px] font-black uppercase tracking-[0.2em] text-[10px] hover:bg-black transition-all shadow-xl"
            >
              Add First Address
            </button>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {addresses.map((address) => (
              <div
                key={address.id}
                className={`bg-white rounded-[32px] border transition-all p-8 relative group ${
                  address.is_default ? 'border-[#FF6B35] shadow-lg bg-[#FFF9F0]' : 'border-[#F0F0F0] hover:border-[#E0E0E0] hover:shadow-md'
                }`}
              >
                {address.is_default && (
                  <div className="absolute top-8 right-8 bg-[#FF6B35] text-white px-4 py-2 rounded-xl text-[8px] font-black flex items-center gap-2 uppercase tracking-widest">
                    <Star className="w-3 h-3" fill="currentColor" />
                    Default
                  </div>
                )}

                <div className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center border border-[#F0F0F0] shadow-sm text-[#FF6B35] mb-6">
                  <MapPin className="w-6 h-6" />
                </div>

                <h3 className="text-xl font-black text-[#1A1A1A] uppercase tracking-tighter mb-4">{address.label}</h3>
                
                <div className="text-gray-500 space-y-2 mb-8">
                  <p className="text-[10px] font-black text-[#1A1A1A] uppercase tracking-widest">{address.full_name}</p>
                  <p className="text-[10px] font-bold text-gray-400 uppercase tracking-tighter leading-relaxed">
                    {address.address_line1}, {address.address_line2 && `${address.address_line2}, `}
                    {address.city}, {address.state} - {address.pincode}
                  </p>
                  <p className="text-[10px] font-black text-[#FF6B35] uppercase tracking-widest">{address.phone_number}</p>
                </div>

                <div className="flex gap-2 pt-6 border-t border-[#F0F0F0]">
                  {!address.is_default && (
                    <button
                      onClick={() => handleSetDefault(address.id)}
                      className="flex-1 px-4 py-3 bg-white text-[#1A1A1A] rounded-xl font-black uppercase tracking-widest text-[8px] hover:bg-[#F9F9F9] border border-[#F0F0F0] transition-all"
                    >
                      Make Default
                    </button>
                  )}
                  <button
                    onClick={() => handleEdit(address)}
                    className="flex items-center justify-center gap-2 px-4 py-3 bg-[#F9F9F9] text-[#1A1A1A] rounded-xl font-black uppercase tracking-widest text-[8px] hover:bg-white border border-[#F0F0F0] transition-all"
                  >
                    <Edit className="w-3 h-3" />
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(address.id)}
                    className="flex items-center justify-center gap-2 px-4 py-3 bg-red-50 text-red-500 rounded-xl font-black uppercase tracking-widest text-[8px] hover:bg-red-100 border border-red-100 transition-all"
                  >
                    <Trash2 className="w-3 h-3" />
                    Trash
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {showForm && (
          <AddressForm
            address={editingAddress}
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            isSubmitting={submitting}
          />
        )}
      </div>
    </div>
  );
}
