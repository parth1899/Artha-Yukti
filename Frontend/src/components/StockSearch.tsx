import React, { useState } from 'react';
import { Search } from 'lucide-react';

// NIFTY 50 companies list
const NIFTY50_COMPANIES = [
  'Adani Ports and Special Economic Zone Ltd',
  'Asian Paints Ltd',
  'Axis Bank Ltd',
  'Bajaj Auto Ltd',
  'Bajaj Finance Ltd',
  'Bajaj Finserv Ltd',
  'Bharti Airtel Ltd',
  'BPCL Ltd',
  'Britannia Industries Ltd',
  'Cipla Ltd',
  'Coal India Ltd',
  'Divis Laboratories Ltd',
  'Dr Reddys Laboratories Ltd',
  'Eicher Motors Ltd',
  'Grasim Industries Ltd',
  'HCL Technologies Ltd',
  'HDFC Bank Ltd',
  'Hero MotoCorp Ltd',
  'Hindalco Industries Ltd',
  'Hindustan Unilever Ltd',
  'ICICI Bank Ltd',
  'IndusInd Bank Ltd',
  'Infosys Ltd',
  'ITC Ltd',
  'JSW Steel Ltd',
  'Kotak Mahindra Bank Ltd',
  'Larsen & Toubro Ltd',
  'Mahindra & Mahindra Ltd',
  'Maruti Suzuki India Ltd',
  'Nestle India Ltd',
  'NTPC Ltd',
  'Oil & Natural Gas Corporation Ltd',
  'Power Grid Corporation of India Ltd',
  'Reliance Industries Ltd',
  'SBI Life Insurance Company Ltd',
  'State Bank of India',
  'Sun Pharmaceutical Industries Ltd',
  'Tata Consumer Products Ltd',
  'Tata Motors Ltd',
  'Tata Steel Ltd',
  'Tech Mahindra Ltd',
  'Titan Company Ltd',
  'UltraTech Cement Ltd',
  'UPL Ltd',
  'Wipro Ltd'
];

interface StockSearchProps {
  onSearch: (company: string) => void;
}

const StockSearch: React.FC<StockSearchProps> = ({ onSearch }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);
  const [filteredCompanies, setFilteredCompanies] = useState<string[]>([]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchTerm(value);
    
    if (value.length > 0) {
      const filtered = NIFTY50_COMPANIES.filter(company => 
        company.toLowerCase().includes(value.toLowerCase())
      );
      setFilteredCompanies(filtered);
      setShowDropdown(true);
    } else {
      setShowDropdown(false);
    }
  };

  const handleCompanySelect = (company: string) => {
    setSearchTerm(company);
    setShowDropdown(false);
  };

  const handleSearch = () => {
    if (searchTerm.trim()) {
      onSearch(searchTerm);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="relative">
      <div className="flex items-center">
        <div className="relative flex-grow">
          <input
            type="text"
            placeholder="Search for a company..."
            className="w-full px-4 py-3 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            value={searchTerm}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            onFocus={() => searchTerm && setShowDropdown(true)}
          />
          {showDropdown && (
            <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
              {filteredCompanies.length > 0 ? (
                filteredCompanies.map((company, index) => (
                  <div
                    key={index}
                    className="px-4 py-2 cursor-pointer hover:bg-indigo-50"
                    onClick={() => handleCompanySelect(company)}
                  >
                    {company}
                  </div>
                ))
              ) : (
                <div className="px-4 py-2 text-gray-500">No matches found</div>
              )}
            </div>
          )}
        </div>
        <button
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-r-lg flex items-center transition-colors duration-300"
          onClick={handleSearch}
        >
          <Search className="h-5 w-5 mr-2" />
          Search
        </button>
      </div>
    </div>
  );
};

export default StockSearch;