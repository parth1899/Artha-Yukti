import React, { useState, useRef } from 'react';
import { ChevronLeft, ChevronRight, ExternalLink } from 'lucide-react';

const ValidationCarousel: React.FC = () => {
  const [scrollPosition, setScrollPosition] = useState(0);
  const carouselRef = useRef<HTMLDivElement>(null);

  // Sample validation sources
  const validationSources = [
    {
      title: 'MoneyControl Financial Data',
      url: 'https://www.moneycontrol.com/india/stockpricequote',
      description: 'Comprehensive financial data and stock quotes'
    },
    {
      title: 'NSE India Market Data',
      url: 'https://www.nseindia.com',
      description: 'Official market data from National Stock Exchange of India'
    },
    {
      title: 'LiveMint Financial News',
      url: 'https://www.livemint.com/market',
      description: 'Latest financial news and market analysis'
    },
    {
      title: 'Economic Times Markets',
      url: 'https://economictimes.indiatimes.com/markets',
      description: 'Market news, analysis and stock recommendations'
    },
    {
      title: 'Bloomberg Quint',
      url: 'https://www.bloombergquint.com',
      description: 'Business and financial news with focus on Indian markets'
    },
    {
      title: 'Yahoo Finance India',
      url: 'https://in.finance.yahoo.com',
      description: 'Stock data, charts, and financial news'
    }
  ];

  const scroll = (direction: 'left' | 'right') => {
    if (carouselRef.current) {
      const { scrollWidth, clientWidth } = carouselRef.current;
      const scrollAmount = clientWidth / 2;
      
      let newPosition;
      if (direction === 'left') {
        newPosition = Math.max(0, scrollPosition - scrollAmount);
      } else {
        newPosition = Math.min(scrollWidth - clientWidth, scrollPosition + scrollAmount);
      }
      
      carouselRef.current.scrollTo({
        left: newPosition,
        behavior: 'smooth'
      });
      
      setScrollPosition(newPosition);
    }
  };

  return (
    <div className="relative">
      <div className="flex items-center">
        <button 
          className="absolute left-0 z-10 bg-white rounded-full p-2 shadow-md hover:bg-gray-100 transition-colors duration-300"
          onClick={() => scroll('left')}
          aria-label="Scroll left"
        >
          <ChevronLeft className="h-5 w-5 text-gray-600" />
        </button>
        
        <div 
          ref={carouselRef}
          className="flex overflow-x-auto scrollbar-hide py-4 px-10 space-x-4 scroll-smooth"
          style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
        >
          {validationSources.map((source, index) => (
            <div 
              key={index}
              className="flex-shrink-0 w-72 bg-white rounded-lg shadow-md p-4 border border-gray-200 hover:border-indigo-300 transition-colors duration-300"
            >
              <h3 className="font-medium text-lg mb-2 text-indigo-600">{source.title}</h3>
              <p className="text-gray-600 mb-3 text-sm">{source.description}</p>
              <a 
                href={source.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center text-indigo-500 hover:text-indigo-700 text-sm font-medium"
              >
                Visit Source <ExternalLink className="h-4 w-4 ml-1" />
              </a>
            </div>
          ))}
        </div>
        
        <button 
          className="absolute right-0 z-10 bg-white rounded-full p-2 shadow-md hover:bg-gray-100 transition-colors duration-300"
          onClick={() => scroll('right')}
          aria-label="Scroll right"
        >
          <ChevronRight className="h-5 w-5 text-gray-600" />
        </button>
      </div>
    </div>
  );
};

export default ValidationCarousel;