import api from './api';

// Address API service
const addressAPI = {
  // Get all user addresses
  getAddresses: () => api.get('/addresses/'),

  // Get single address
  getAddress: (id) => api.get(`/addresses/${id}/`),

  // Create new address
  createAddress: (data) => api.post('/addresses/', data),

  // Update address
  updateAddress: (id, data) => api.put(`/addresses/${id}/`, data),

  // Delete address
  deleteAddress: (id) => api.delete(`/addresses/${id}/`),

  // Set address as default
  setDefaultAddress: (id) => api.post(`/addresses/${id}/set_default/`),
};

export default addressAPI;
