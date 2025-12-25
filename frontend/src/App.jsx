import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { BranchProvider } from './context/BranchContext';
import { CartProvider } from './context/CartContext';
import { ToastProvider } from './context/ToastContext';
import Toast from './components/Toast';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Menu from './pages/Menu';
import JuiceDetail from './pages/JuiceDetail';
import Cart from './pages/Cart';
import Checkout from './pages/Checkout';
import Orders from './pages/Orders';
import OrderDetail from './pages/OrderDetail';
import OrderSuccess from './pages/OrderSuccess';
import Login from './pages/Login';
import Register from './pages/Register';
import VerifyEmail from './pages/VerifyEmail';
import VerifyPhone from './pages/VerifyPhone';
import ProtectedRoute from './components/ProtectedRoute';
import MyAddresses from './pages/MyAddresses';
import MyProfile from './pages/MyProfile';

function App() {
  return (
    <AuthProvider>
      <BranchProvider>
        <ToastProvider>
          <CartProvider>
            <Router>
            <div className="min-h-screen bg-[#F5F2ED]">
              <Navbar />
              <Toast />
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/menu" element={<Menu />} />
                <Route path="/juice/:id" element={<JuiceDetail />} />
                <Route path="/cart" element={<Cart />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/verify-email" element={<VerifyEmail />} />
                <Route path="/verify-phone" element={<VerifyPhone />} />
                
                <Route path="/checkout" element={
                  <ProtectedRoute>
                    <Checkout />
                  </ProtectedRoute>
                } />
                <Route path="/order-success" element={
                  <ProtectedRoute>
                    <OrderSuccess />
                  </ProtectedRoute>
                } />
                <Route path="/orders" element={
                  <ProtectedRoute>
                    <Orders />
                  </ProtectedRoute>
                } />
                <Route path="/orders/:id" element={
                  <ProtectedRoute>
                    <OrderDetail />
                  </ProtectedRoute>
                } />
                <Route path="/my-addresses" element={
                  <ProtectedRoute>
                    <MyAddresses />
                  </ProtectedRoute>
                } />
                <Route path="/my-profile" element={
                  <ProtectedRoute>
                    <MyProfile />
                  </ProtectedRoute>
                } />
              </Routes>
            </div>
          </Router>
        </CartProvider>
      </ToastProvider>
      </BranchProvider>
    </AuthProvider>
  );
}

export default App;
