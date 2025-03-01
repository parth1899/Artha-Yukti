import React, { useState } from 'react';
import { Search, TrendingUp, TrendingDown, Minus, ChevronLeft, ChevronRight, ExternalLink } from 'lucide-react';
import StockSearch from './components/StockSearch';
import SentimentMeter from './components/SentimentMeter';
import StockChart from './components/StockChart';
import ValidationCarousel from './components/ValidationCarousel';
import InvestmentSummary from './components/InvestmentSummary';
import ChatOutput from './components/ChatOutput';

function App() {
  const [searchedCompany, setSearchedCompany] = useState('');
  const [sentiment, setSentiment] = useState<'bullish' | 'bearish' | 'neutral'>('neutral');
  const [showResults, setShowResults] = useState(false);
  const [chatMessages, setChatMessages] = useState<Array<{text: string, type: 'system' | 'analysis'}>>([]);

  const handleSearch = (company: string) => {
    setSearchedCompany(company);
    // Simulate sentiment analysis result
    const sentiments: Array<'bullish' | 'bearish' | 'neutral'> = ['bullish', 'bearish', 'neutral'];
    const newSentiment = sentiments[Math.floor(Math.random() * sentiments.length)];
    setSentiment(newSentiment);
    setShowResults(true);
    
    // Add chat messages
    setChatMessages([
      { text: `Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. `, type: 'system' }
    ]);
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm py-4">
        <div className="max-w-5xl mx-auto px-4 flex items-center">
          <TrendingUp className="h-6 w-6 text-indigo-600 mr-2" />
          <h1 className="text-xl font-semibold text-indigo-600">indoVate Real Time Stock Analysis</h1>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-6 flex-grow">
        {/* Search Section */}
        <section className="mb-6">
          <StockSearch onSearch={handleSearch} />
        </section>

        {/* Validation Carousel - Now below search bar */}
        <section className="mb-6">
          <h2 className="text-xl font-semibold mb-4">Validation Sources</h2>
          <ValidationCarousel />
        </section>

        {showResults && (
          <>
            {/* Chat Output and Sentiment Meter */}
            <section className="mb-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Left Panel - Chat Output */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-lg font-medium mb-4">Analysis Process</h3>
                  <ChatOutput messages={chatMessages} />
                </div>

                {/* Right Panel - Sentiment Meter */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-lg font-medium mb-4">Market Sentiment</h3>
                  <SentimentMeter sentiment={sentiment} />
                </div>
              </div>
            </section>

            {/* Stock Chart - Full Width */}
            <section className="mb-6">
              <h2 className="text-xl font-semibold mb-4">Stock Performance for {searchedCompany}</h2>
              <div className="bg-white rounded-lg shadow-md p-6">
                <StockChart company={searchedCompany} />
              </div>
            </section>

            {/* Investment Recommendation Summary */}
            <section className="mb-6">
              <h2 className="text-xl font-semibold mb-4">Investment Recommendation Summary</h2>
              <InvestmentSummary company={searchedCompany} sentiment={sentiment} />
            </section>
          </>
        )}
      </main>

      <footer className="bg-white shadow-inner py-4 mt-auto">
        <div className="max-w-5xl mx-auto px-4 text-center text-sm text-gray-500">
          © 2025 indoVate Real Time Stock Analysis. All data is for informational purposes only.
        </div>
      </footer>
    </div>
  );
}

export default App;