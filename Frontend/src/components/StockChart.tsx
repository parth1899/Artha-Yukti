import React, { useEffect, useState } from 'react';

interface StockChartProps {
  company: string;
}

const StockChart: React.FC<StockChartProps> = ({ company }) => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading time for chart data
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1500);
    
    return () => clearTimeout(timer);
  }, [company]);

  // Generate random data points for demonstration
  const generateChartData = () => {
    const data = [];
    let value = 100 + Math.random() * 50;
    
    for (let i = 0; i < 30; i++) {
      // Add some randomness to the data
      value = value + (Math.random() * 10 - 5);
      data.push(value);
    }
    
    return data;
  };
  
  const chartData = generateChartData();
  const maxValue = Math.max(...chartData);
  const minValue = Math.min(...chartData);
  const range = maxValue - minValue;

  return (
    <div className="h-80 w-full"> {/* Increased height for better visibility */}
      {loading ? (
        <div className="h-full w-full flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
      ) : (
        <div className="h-full w-full relative">
          {/* Y-axis labels */}
          <div className="absolute left-0 top-0 h-full flex flex-col justify-between text-xs text-gray-500">
            <span>{Math.round(maxValue)}</span>
            <span>{Math.round(minValue + range/2)}</span>
            <span>{Math.round(minValue)}</span>
          </div>
          
          {/* Chart */}
          <div className="absolute left-8 right-0 top-0 h-full flex items-end">
            {chartData.map((value, index) => {
              const height = ((value - minValue) / range) * 100;
              const isPositive = index > 0 && value >= chartData[index - 1];
              
              return (
                <div 
                  key={index}
                  className="flex-1 flex flex-col justify-end mx-px"
                >
                  <div 
                    className={`${isPositive ? 'bg-green-500' : 'bg-red-500'} rounded-t`}
                    style={{ height: `${height}%` }}
                  ></div>
                </div>
              );
            })}
          </div>
          
          {/* X-axis labels */}
          <div className="absolute left-8 right-0 bottom-0 flex justify-between text-xs text-gray-500 mt-2">
            <span>30d</span>
            <span>20d</span>
            <span>10d</span>
            <span>Now</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default StockChart;