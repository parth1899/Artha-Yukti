import React, { useEffect, useState } from 'react';

interface StockChartProps {
  company: string;
  sessionId: string;
}

const StockChart: React.FC<StockChartProps> = ({ company, sessionId }) => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading delay (or remove if not needed)
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1500);
    return () => clearTimeout(timer);
  }, [company]);

  return (
    <div className="h-80 w-full flex items-center justify-center border border-gray-300 rounded">
      {loading ? (
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      ) : (
        <iframe 
          src={`http://127.0.0.1:5000/graphs?session_id=${sessionId}`} 
          width="100%" 
          height="100%" 
          frameBorder="0"
          title="Stock Graph"
        />
      )}
    </div>
  );
};

export default StockChart;
