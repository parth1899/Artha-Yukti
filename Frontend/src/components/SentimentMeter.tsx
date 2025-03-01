import React from 'react';
import ReactSpeedometer from 'react-d3-speedometer';
import "../index.css";

interface SentimentMeterProps {
  // Numeric sentiment between -1 (fully bearish) and 1 (fully bullish)
  value?: number;
}

const SentimentMeter: React.FC<SentimentMeterProps> = ({ value = 0 }) => {
  const sentimentLabel = value > 0 ? "Bullish" : value < 0 ? "Bearish" : "Neutral";
  const sentimentColor = value > 0 ? 'text-green-500' : value < 0 ? 'text-red-500' : 'text-yellow-500';

  return (
    <div className="flex flex-col items-center">
      <ReactSpeedometer
        minValue={-1}
        maxValue={1}
        value={value}
        // Softer pastel segments: light red for bearish and light green for bullish
        customSegmentStops={[-1, 0, 1]}
        segmentColors={['#ffcdd2', '#c8e6c9']}
        needleColor="gray"
        // Configure the arc to span from -90° to 90°
        startAngle={-90}
        endAngle={90}
        needleTransitionDuration={400}
        needleTransition="easeElastic"
        height={200}
        width={400}
        // Remove the built-in numeric display
        currentValueText=""
      />
      <div className="flex items-center justify-center mt-4">
        <span className={`text-2xl font-bold ${sentimentColor}`}>
          {sentimentLabel} ({value.toFixed(2)})
        </span>
      </div>
    </div>
  );
};

export default SentimentMeter;