import React from 'react';

interface InvestmentSummaryProps {
  company: string;
  sentiment: 'bullish' | 'bearish' | 'neutral';
}

const InvestmentSummary: React.FC<InvestmentSummaryProps> = ({ company, sentiment }) => {
  // Generate random financial data for demonstration
  const generateFinancialData = () => {
    const revenue = (Math.random() * 100 + 20).toFixed(2);
    const growthRate = (Math.random() * 10 - 2).toFixed(2);
    const quarter = ['March 31', 'June 30', 'September 30', 'December 31'][Math.floor(Math.random() * 4)];
    const year = 2024;
    
    return {
      revenue,
      growthRate,
      quarter,
      year
    };
  };
  
  const financialData = generateFinancialData();
  
  // Determine recommendation based on sentiment
  const getRecommendation = () => {
    switch (sentiment) {
      case 'bullish':
        return {
          action: 'Buy',
          description: `Based on our analysis, we recommend investing in ${company} as it shows strong growth potential and positive market sentiment. The company demonstrates solid financial performance and favorable market conditions.`
        };
      case 'bearish':
        return {
          action: 'Sell',
          description: `Based on our analysis, we recommend caution with ${company} as it shows concerning trends and negative market sentiment. Consider reducing exposure or waiting for more favorable conditions before investing.`
        };
      case 'neutral':
        return {
          action: 'Hold',
          description: `Based on our analysis, we recommend a neutral stance on ${company}. While the company shows some positive indicators, there are also potential concerns. Consider your investment goals and risk tolerance before making a decision.`
        };
      default:
        return {
          action: 'Research',
          description: 'Insufficient data to make a clear recommendation. Further research is advised.'
        };
    }
  };
  
  const recommendation = getRecommendation();
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {/* Financial Health */}
      <div className="bg-white rounded-lg shadow-md p-6 border-t-4 border-blue-500">
        <h3 className="text-lg font-medium mb-4 text-blue-700">Financial Health</h3>
        
        <div className="mb-4">
          <h4 className="font-medium text-gray-700 mb-2">Revenue Growth</h4>
          <p className="text-sm text-gray-600">
            {company} reported a revenue of {financialData.revenue}B INR in the quarter ending {financialData.quarter}, {financialData.year}, 
            with a {parseFloat(financialData.growthRate) >= 0 ? 'growth' : 'decline'} rate of {Math.abs(parseFloat(financialData.growthRate))}%.
          </p>
        </div>
        
        <div className="mb-4">
          <h4 className="font-medium text-gray-700 mb-2">Profit & Loss</h4>
          <p className="text-sm text-gray-600">
            Detailed profit and loss data is accessible from sources like Moneycontrol, Stockanalysis, and Livemint.
          </p>
        </div>
        
        <div>
          <h4 className="font-medium text-gray-700 mb-2">Income Statement</h4>
          <p className="text-sm text-gray-600">
            Comprehensive annual and quarterly income statements are available from official company filings.
          </p>
        </div>
      </div>
      
      {/* Market Sentiment */}
      <div className="bg-white rounded-lg shadow-md p-6 border-t-4 border-purple-500">
        <h3 className="text-lg font-medium mb-4 text-purple-700">Market Sentiment</h3>
        
        <div className="mb-4">
          <h4 className="font-medium text-gray-700 mb-2">Trend Analysis</h4>
          <p className="text-sm text-gray-600">
            {sentiment === 'bullish' && 'Positive trends observed in recent trading sessions with strong buying interest.'}
            {sentiment === 'bearish' && 'Negative trends observed in recent trading sessions with increased selling pressure.'}
            {sentiment === 'neutral' && 'Mixed trends observed in recent trading sessions with balanced buying and selling activity.'}
          </p>
        </div>
        
        <div className="mb-4">
          <h4 className="font-medium text-gray-700 mb-2">Investor Interest</h4>
          <p className="text-sm text-gray-600">
            {sentiment === 'bullish' && 'Strong interest in the company\'s financial performance with positive outlook from institutional investors.'}
            {sentiment === 'bearish' && 'Declining interest in the company\'s financial performance with cautious outlook from institutional investors.'}
            {sentiment === 'neutral' && 'Moderate interest in the company\'s financial performance with mixed outlook from institutional investors.'}
          </p>
        </div>
        
        <div>
          <h4 className="font-medium text-gray-700 mb-2">Transparency</h4>
          <p className="text-sm text-gray-600">
            The company maintains transparency in financial reporting with regular updates to stakeholders.
          </p>
        </div>
      </div>
      
      {/* Recommendation */}
      <div className={`bg-white rounded-lg shadow-md p-6 border-t-4 
        ${sentiment === 'bullish' ? 'border-green-500' : 
          sentiment === 'bearish' ? 'border-red-500' : 'border-yellow-500'}`}>
        <h3 className={`text-lg font-medium mb-4 
          ${sentiment === 'bullish' ? 'text-green-700' : 
            sentiment === 'bearish' ? 'text-red-700' : 'text-yellow-700'}`}>
          Recommendation: {recommendation.action}
        </h3>
        
        <p className="text-sm text-gray-600 mb-4">
          {recommendation.description}
        </p>
        
        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-medium text-gray-700 mb-2">Additional Considerations</h4>
          <ul className="text-sm text-gray-600 list-disc pl-5 space-y-1">
            <li>Industry trends and competitive landscape</li>
            <li>Regulatory environment and compliance</li>
            <li>Global economic factors</li>
            <li>Your personal investment goals and risk tolerance</li>
          </ul>
        </div>
        
        <div className="mt-4 text-xs text-gray-500 italic">
          This recommendation is based on current data and analysis. Always conduct your own due diligence before making investment decisions.
        </div>
      </div>
    </div>
  );
};

export default InvestmentSummary;