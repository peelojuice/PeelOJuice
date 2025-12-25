import { useState, useEffect } from 'react';
import { MapPin, ChevronDown } from 'lucide-react';
import api from '../services/api';

export default function BranchSelector({ onBranchSelect, selectedBranch }) {
  const [branches, setBranches] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBranches();
  }, []);

  const fetchBranches = async () => {
    setLoading(true);
    try {
      const response = await api.get('/products/branches/');
      const fetchedBranches = response.data.results || response.data;
      setBranches(fetchedBranches);
      
      // Auto-select first branch
      if (fetchedBranches.length > 0 && onBranchSelect) {
        onBranchSelect(fetchedBranches[0]);
      }
    } catch (error) {
      console.error('Error loading branches:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBranchSelect = (branch) => {
    selectBranch(branch);
    setIsOpen(false);
  };

  if (loading) {
    return <div className="text-sm text-gray-500">Loading...</div>;
  }

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 text-gray-700 hover:text-[#8BA888] transition font-medium"
      >
        <MapPin className="w-5 h-5" />
        <span>{selectedBranch ? selectedBranch.name : 'Select Branch'}</span>
        <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
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
                <span className="font-medium">{branch.name}</span>
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
