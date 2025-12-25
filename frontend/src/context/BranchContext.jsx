import { createContext, useState, useContext, useEffect } from 'react';

const BranchContext = createContext(null);

export const BranchProvider = ({ children }) => {
  const [selectedBranch, setSelectedBranch] = useState(null);
  const [branches, setBranches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load saved branch from localStorage
    const saved = localStorage.getItem('selectedBranch');
    if (saved) {
      try {
        setSelectedBranch(JSON.parse(saved));
      } catch (e) {
        console.error('Error loading saved branch:', e);
      }
    }
    setLoading(false);
  }, []);

  const selectBranch = (branch) => {
    setSelectedBranch(branch);
    if (branch) {
      localStorage.setItem('selectedBranch', JSON.stringify(branch));
    } else {
      localStorage.removeItem('selectedBranch');
    }
  };

  return (
    <BranchContext.Provider value={{ 
      selectedBranch, 
      selectBranch, 
      branches, 
      setBranches,
      loading 
    }}>
      {children}
    </BranchContext.Provider>
  );
};

export const useBranch = () => {
  const context = useContext(BranchContext);
  if (!context) {
    throw new Error('useBranch must be used within BranchProvider');
  }
  return context;
};
