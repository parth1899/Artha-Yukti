import React, { useState } from 'react';
import { Search } from 'lucide-react';

const SAMPLE_QUERIES = [
  "Should i buy HDFCBANK stock today?",
  "Will the price for WIPRO shares increase or decrease?"
];

interface StockSearchProps {
  onSearch: (query: string) => void;
}

const StockSearch: React.FC<StockSearchProps> = ({ onSearch }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);
  const [filteredSuggestions, setFilteredSuggestions] = useState<string[]>(SAMPLE_QUERIES);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchTerm(value);

    // Filter sample queries based on input value
    const filtered = SAMPLE_QUERIES.filter(query =>
      query.toLowerCase().includes(value.toLowerCase())
    );
    setFilteredSuggestions(filtered);
    setShowDropdown(true);
  };

  const handleSuggestionSelect = (suggestion: string) => {
    setSearchTerm(suggestion);
    setShowDropdown(false);
  };

  const handleSearch = async () => {
    if (searchTerm.trim()) {
      try {
        await fetch("http://127.0.0.1:5000/query", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ query: searchTerm })
        });
      } catch (error) {
        console.error("Error sending query:", error);
      }
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
            placeholder="Enter your query..."
            className="w-full px-4 py-3 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            value={searchTerm}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            onFocus={() => setShowDropdown(true)}
          />
          {showDropdown && (
            <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
              {filteredSuggestions.length > 0 ? (
                filteredSuggestions.map((suggestion, index) => (
                  <div
                    key={index}
                    className="px-4 py-2 cursor-pointer hover:bg-indigo-50"
                    onClick={() => handleSuggestionSelect(suggestion)}
                  >
                    {suggestion}
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
