import { useState, useEffect } from 'react';
import { Plus, MapPin, Edit, Trash2, Star } from 'lucide-react';
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
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-2xl font-semibold text-primary">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">My Addresses</h1>
            <p className="text-gray-600 mt-1">Manage your delivery addresses</p>
          </div>
          <button
            onClick={() => setShowForm(true)}
            className="flex items-center gap-2 bg-black text-white px-6 py-3 rounded-lg font-semibold hover:bg-gray-800 transition shadow-lg"
          >
            <Plus className="w-5 h-5" />
            Add New Address
          </button>
        </div>

        {/* Addresses Grid */}
        {addresses.length === 0 ? (
          <div className="text-center py-16">
            <MapPin className="w-24 h-24 mx-auto text-gray-300 mb-4" />
            <h2 className="text-2xl font-bold text-gray-800 mb-2">No addresses yet</h2>
            <p className="text-gray-600 mb-6">Add your first delivery address</p>
            <button
              onClick={() => setShowForm(true)}
              className="bg-black text-white px-8 py-3 rounded-lg font-semibold hover:bg-gray-800 transition"
            >
              Add Address
            </button>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {addresses.map((address) => (
              <div
                key={address.id}
                className={`bg-white rounded-2xl shadow-md hover:shadow-xl transition-all p-6 relative ${
                  address.is_default ? 'ring-2 ring-black' : ''
                }`}
              >
                {/* Default Badge */}
                {address.is_default && (
                  <div className="absolute top-4 right-4 bg-black text-white px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1">
                    <Star className="w-3 h-3" />
                    DEFAULT
                  </div>
                )}

                {/* Label */}
                <div className="mb-4">
                  <h3 className="text-lg font-bold text-gray-800 flex items-center gap-2">
                    <MapPin className="w-5 h-5 text-black" />
                    {address.label}
                  </h3>
                </div>

                {/* Address Details */}
                <div className="text-gray-600 space-y-1 mb-4">
                  <p className="font-semibold text-gray-800">{address.full_name}</p>
                  <p>{address.phone_number}</p>
                  <p>{address.address_line1}</p>
                  {address.address_line2 && <p>{address.address_line2}</p>}
                  <p>{address.city}, {address.state} - {address.pincode}</p>
                  {address.landmark && <p className="text-sm text-gray-500">Near: {address.landmark}</p>}
                </div>

                {/* Actions */}
                <div className="flex gap-2 pt-4 border-t">
                  {!address.is_default && (
                    <button
                      onClick={() => handleSetDefault(address.id)}
                      className="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-semibold hover:bg-gray-200 transition text-sm"
                    >
                      Set Default
                    </button>
                  )}
                  <button
                    onClick={() => handleEdit(address)}
                    className="flex items-center justify-center gap-1 px-4 py-2 bg-blue-50 text-blue-600 rounded-lg font-semibold hover:bg-blue-100 transition text-sm"
                  >
                    <Edit className="w-4 h-4" />
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(address.id)}
                    className="flex items-center justify-center gap-1 px-4 py-2 bg-red-50 text-red-600 rounded-lg font-semibold hover:bg-red-100 transition text-sm"
                  >
                    <Trash2 className="w-4 h-4" />
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Address Form Modal */}
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
