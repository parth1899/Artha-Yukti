import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface SentimentMeterProps {
  sentiment: 'bullish' | 'bearish' | 'neutral';
}

const SentimentMeter: React.FC<SentimentMeterProps> = ({ sentiment }) => {
  const getSentimentColor = () => {
    switch (sentiment) {
      case 'bullish':
        return 'text-green-500';
      case 'bearish':
        return 'text-red-500';
      case 'neutral':
        return 'text-yellow-500';
      default:
        return 'text-gray-500';
    }
  };

  const getSentimentIcon = () => {
    switch (sentiment) {
      case 'bullish':
        return <TrendingUp className="h-12 w-12 text-green-500" />;
      case 'bearish':
        return <TrendingDown className="h-12 w-12 text-red-500" />;
      case 'neutral':
        return <Minus className="h-12 w-12 text-yellow-500" />;
      default:
        return null;
    }
  };

  const getRotationDegree = () => {
    switch (sentiment) {
      case 'bullish':
        return 45;
      case 'bearish':
        return -45;
      case 'neutral':
        return 0;
      default:
        return 0;
    }
  };

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-64 h-32 mb-8">
        {/* Speedometer background */}
        <div className="absolute w-full h-full bg-gray-200 rounded-t-full"></div>
        
        {/* Sentiment zones */}
        <div className="absolute w-full h-full">
          <div className="absolute top-0 left-0 w-1/3 h-full bg-red-200 rounded-tl-full"></div>
          <div className="absolute top-0 left-1/3 w-1/3 h-full bg-yellow-200"></div>
          <div className="absolute top-0 right-0 w-1/3 h-full bg-green-200 rounded-tr-full"></div>
        </div>
        
        {/* Needle */}
        <div 
          className="absolute top-full left-1/2 w-1 h-32 bg-gray-800 origin-bottom transform -translate-x-1/2"
          style={{ transform: `translateX(-50%) rotate(${getRotationDegree()}deg)` }}
        ></div>
        
        {/* Center point */}
        <div className="absolute bottom-0 left-1/2 w-6 h-6 bg-gray-800 rounded-full transform -translate-x-1/2 translate-y-1/2"></div>
        
        {/* Labels */}
        <div className="absolute bottom-4 left-4 text-red-700 font-medium">Bearish</div>
        <div className="absolute bottom-4 left-1/2 text-yellow-700 font-medium transform -translate-x-1/2">Neutral</div>
        <div className="absolute bottom-4 right-4 text-green-700 font-medium">Bullish</div>
      </div>
      
      <div className="flex items-center justify-center mt-4">
        {getSentimentIcon()}
        <span className={`text-2xl font-bold ml-2 ${getSentimentColor()}`}>
          {sentiment.charAt(0).toUpperCase() + sentiment.slice(1)}
        </span>
      </div>
    </div>
  );
};

export default SentimentMeter;