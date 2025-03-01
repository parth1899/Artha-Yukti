import React, { useState } from 'react';
import { TrendingUp } from 'lucide-react';
import StockSearch from './components/StockSearch';
import SentimentMeter from './components/SentimentMeter';
import StockChart from './components/StockChart';
import ValidationCarousel from './components/ValidationCarousel';
import InvestmentSummary from './components/InvestmentSummary';
import ChatOutput from './components/ChatOutput';

function App() {
  const [searchedCompany, setSearchedCompany] = useState('');
  const [sentimentLabel, setSentimentLabel] = useState<'bullish' | 'bearish' | 'neutral'>('neutral');
  const [sentimentValue, setSentimentValue] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [chatMessages, setChatMessages] = useState<Array<{ text: string, type: 'system' }>>([]);
  // Recommendation will now be an object with three keys from the backend.
  const [recommendation, setRecommendation] = useState<{
    "Financial Health": string;
    "Market Sentiment": string;
    "Recommendation": string;
  } | null>(null);

  const handleSearch = async (company: string) => {
    setSearchedCompany(company);
    setShowResults(true);

    // This endpoint must be called so that sentiment analysis can work (if applicable)
    try {
      await fetch("http://127.0.0.1:5000/query_concurrent");
    } catch (error) {
      console.error("Error calling query_concurrent:", error);
    }

    try {
      // Fetch sentiment from backend
      const sentimentRes = await fetch("http://127.0.0.1:5000/sentiment");
      const sentimentData = await sentimentRes.json();
      const sentimentResult = sentimentData.result[0];
      if (sentimentResult) {
        const label = sentimentResult.label.toLowerCase();
        const score = sentimentResult.score;
        if (label === "bullish") {
          setSentimentLabel('bullish');
          setSentimentValue(score);
        } else if (label === "bearish") {
          setSentimentLabel('bearish');
          setSentimentValue(-score);
        } else {
          setSentimentLabel('neutral');
          setSentimentValue(0);
        }
      }
    } catch (error) {
      console.error("Error fetching sentiment:", error);
    }

    try {
      // Fetch chat output text from backend
      const outputRes = await fetch("http://127.0.0.1:5000/output_text");
      const outputData = await outputRes.json();
      setChatMessages([{ text: outputData.insights, type: 'system' }]);
    } catch (error) {
      console.error("Error fetching output text:", error);
    }

    try {
      // Fetch investment recommendation from backend
      const recommendationRes = await fetch("http://127.0.0.1:5000/recommendation");
      const recommendationData = await recommendationRes.json();
      // Extract the nested result so the keys match what the component expects
      setRecommendation(recommendationData.result);
      // Update the sentiment label using the backend sentiment if needed
      setSentimentLabel(
        recommendationData.sentiment.toLowerCase() as 'bullish' | 'bearish' | 'neutral'
      );
    } catch (error) {
      console.error("Error fetching recommendation:", error);
    }
    
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

      <main className="max-w-5xl w-full mx-auto px-4 py-6 flex-grow">
      {/* Search Section */}
        <section className="mb-6">
          <StockSearch onSearch={handleSearch} />
        </section>

        {/* Validation Carousel */}
        <section className="mb-6">
          <h2 className="text-xl font-semibold mb-4">Validation Sources</h2>
          <ValidationCarousel />
        </section>

        {showResults && (
          <>
            {/* Chat Output and Sentiment Meter */}
            <section className="mb-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Chat Output */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-lg font-medium mb-4">Analysis Process</h3>
                  <ChatOutput messages={chatMessages} />
                </div>
                {/* Sentiment Meter */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-lg font-medium mb-4">Market Sentiment</h3>
                  <SentimentMeter value={sentimentValue} />
                </div>
              </div>
            </section>

            {/* Stock Chart */}
            <section className="mb-6">
              <h2 className="text-xl font-semibold mb-4">Stock Performance for {searchedCompany}</h2>
              <div className="bg-white rounded-lg shadow-md p-6">
                <StockChart company={searchedCompany} />
              </div>
            </section>

            {/* Investment Recommendation */}
            {recommendation && (
              <section className="mb-6">
                <h2 className="text-xl font-semibold mb-4">Investment Recommendation Summary</h2>
                <InvestmentSummary 
                  company={searchedCompany} 
                  sentiment={sentimentLabel} 
                  recommendation={recommendation} 
                />
              </section>
            )}
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