import { useState, useEffect } from 'react';
import { MapPin, ChevronDown, Lock } from 'lucide-react';
import { useBranch } from '../context/BranchContext';
import { useCart } from '../context/CartContext';
import api from '../services/api';

export default function BranchSelector() {
  const { selectedBranch, selectBranch, branches, setBranches } = useBranch();
  const { cart } = useCart();
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  // Check if cart has items to lock branch selection
  const hasCartItems = cart?.items?.length > 0;
  const canSwitchBranch = !hasCartItems;

  useEffect(() => {
    loadBranches();
  }, []);

  const loadBranches = async () => {
    setLoading(true);
    try {
      const response = await api.get('/products/branches/');
      setBranches(response.data);
      
      // Auto-select first branch if none selected
      if (!selectedBranch && response.data.length > 0) {
        selectBranch(response.data[0]);
      }
    } catch (error) {
      console.error('Error loading branches:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBranchSelect = (branch) => {
    if (!canSwitchBranch) {
      return; // Don't allow switching when cart has items
    }
    selectBranch(branch);
    setIsOpen(false);
  };

  if (loading) {
    return <div className="text-sm text-gray-500">Loading...</div>;
  }

  return (
    <div className="relative group">
      <button
        onClick={() => canSwitchBranch && setIsOpen(!isOpen)}
        disabled={!canSwitchBranch}
        className={`flex items-center gap-2 transition font-medium ${
          canSwitchBranch 
            ? 'text-gray-700 hover:text-[#8BA888] cursor-pointer' 
            : 'text-gray-400 cursor-not-allowed'
        }`}
      >
        {hasCartItems ? (
          <Lock className="w-5 h-5" />
        ) : (
          <MapPin className="w-5 h-5" />
        )}
        <span>{selectedBranch ? selectedBranch.name : 'Select Branch'}</span>
        {canSwitchBranch && (
          <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
        )}
      </button>

      {/* Tooltip when locked */}
      {!canSwitchBranch && (
        <div className="absolute left-0 top-full mt-2 w-64 bg-gray-800 text-white text-xs px-3 py-2 rounded-lg shadow-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-30">
          <p className="font-semibold mb-1">Branch locked</p>
          <p>Empty your cart to switch branches. Items from different branches cannot be mixed in one order.</p>
        </div>
      )}

      {isOpen && canSwitchBranch && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />
          
          {/* Dropdown Menu */}
          <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg border border-gray-100 py-2 z-20">
            <div className="px-4 py-3 border-b border-gray-100">
              <p className="text-sm font-semibold text-gray-800">Select Branch</p>
              <p className="text-xs text-gray-500 mt-1">Choose your preferred branch</p>
            </div>
            
            {branches.map((branch) => (
              <button
                key={branch.id}
                onClick={() => handleBranchSelect(branch)}
                className={`w-full text-left flex items-center gap-3 px-4 py-3 transition ${
                  selectedBranch?.id === branch.id
                    ? 'bg-[#8BA888]/10 text-[#8BA888]'
                    : 'hover:bg-[#8BA888]/10 text-gray-700'
                }`}
              >
                <MapPin className="w-5 h-5" />
                <div className="flex-1">
                  <span className="font-medium block">{branch.name}</span>
                  <span className="text-xs text-gray-500">{branch.city}</span>
                </div>
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
