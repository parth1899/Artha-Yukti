import React, { useState, useRef, useEffect } from 'react';
import { ChevronLeft, ChevronRight, ExternalLink } from 'lucide-react';

interface ValidationSource {
  snippet: string;
  title: string;
  url: string;
}

const ValidationCarousel: React.FC = () => {
  const [scrollPosition, setScrollPosition] = useState(0);
  const [validationSources, setValidationSources] = useState<ValidationSource[]>([]);
  const carouselRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchValidations = async () => {
      try {
        const res = await fetch("http://127.0.0.1:5000/validations");
        const data = await res.json();
        setValidationSources(data.result);
      } catch (error) {
        console.error("Error fetching validations:", error);
      }
    };
    fetchValidations();
  }, []);

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
              className="relative flex-shrink-0 w-72 h-56 bg-white rounded-lg shadow-md p-4 border border-gray-200 overflow-hidden hover:border-indigo-300 transition-colors duration-300"
            >
              <div className="pb-10">
                <h3 className="font-medium text-lg mb-2 text-indigo-600">{source.title}</h3>
                <p className="text-gray-600 mb-3 text-sm overflow-hidden line-clamp-3">
                  {source.snippet}
                </p>
              </div>
              <a 
                href={source.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="absolute bottom-4 left-4 flex items-center text-indigo-500 hover:text-indigo-700 text-sm font-medium"
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