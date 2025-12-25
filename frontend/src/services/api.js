import axios from 'axios';

// Use environment variable for API URL (localhost in dev, Railway in production)
const API_BASE_URL = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api`;

// Export base URL for use in image paths
export const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add access token
api.interceptors.request.use(
  (config) => {
    const accessToken = sessionStorage.getItem('accessToken');
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 and not already retried, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          throw new Error('No refresh token');
        }

        const response = await axios.post(`${API_BASE_URL}/users/token/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        sessionStorage.setItem('accessToken', access);

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('refreshToken');
        sessionStorage.removeItem('accessToken');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  register: (data) => api.post('/users/register/', data),
  verifyEmail: (data) => api.post('/users/verify-email/', data),
  verifyPhone: (data) => api.post('/users/verify-phone/', data),
  login: (data) => api.post('/users/login/', data),
  logout: (refreshToken) => api.post('/users/logout/', { refresh_token: refreshToken }),
  
  requestPasswordReset: (data) => api.post('/users/password-reset/request/', data),
  verifyResetOTP: (data) => api.post('/users/password-reset/verify/', data),
  confirmPasswordReset: (data) => api.post('/users/password-reset/confirm/', data),
  
  resendEmailOTP: (email) => api.post('/users/resend-email-otp/', { email }),
  resendPhoneOTP: (phone_number) => api.post('/users/resend-phone-otp/', { phone_number }),
};

export default api;
