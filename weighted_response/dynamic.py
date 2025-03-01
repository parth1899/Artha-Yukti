import numpy as np

def adjust_weights(finbert_sentiment, finbert_confidence, lstm_prediction, lstm_confidence, sentiment_match_rate, market_impact_factor=1.0):
    """
    Adjusts weight dynamically while ensuring LSTM always has at least 50% weight.
    
    Parameters:
    - finbert_sentiment (str): "Bullish", "Bearish", or "Neutral"
    - finbert_confidence (float): Confidence score (0 to 1) from FinBERT
    - lstm_prediction (float): LSTM predicted close price
    - lstm_confidence (float): Confidence score (0 to 1) from LSTM
    - sentiment_match_rate (float): Historical accuracy of sentiment (0 to 1)
    - market_impact_factor (float): External event impact (1.0 = neutral, >1 increases sentiment weight, <1 reduces sentiment weight)

    Returns:
    - adjusted_price (float): Final adjusted close price prediction
    - weight_distribution (dict): Assigned weights for FinBERT and LSTM
    """

    # Base weight for LSTM is always 50%
    lstm_weight = 0.50

    # Adjust FinBERT weight based on confidence, historical accuracy, and market impact
    if finbert_confidence >= 0.7:
        finbert_weight = min(0.50, finbert_confidence * sentiment_match_rate * market_impact_factor)
    else:
        finbert_weight = max(0.0, finbert_confidence * 0.5)  # Reduce weight if confidence < 0.7

    # Adjust LSTM weight dynamically to ensure total weight is 1
    lstm_weight = max(0.50, 1.0 - finbert_weight)

    # Adjust final price based on weights
    adjusted_price = (finbert_weight * lstm_prediction) + (lstm_weight * lstm_prediction)

    return adjusted_price, {"FinBERT": round(finbert_weight * 100, 2), "LSTM": round(lstm_weight * 100, 2)}

# ---- Example Inputs ----
finbert_sentiment = "Bullish"
finbert_confidence = 0.65  # Below 0.7, so weight will be reduced
lstm_prediction = 2540.75
lstm_confidence = 0.85
sentiment_match_rate = 0.50  # Historical accuracy of sentiment
market_impact_factor = 1.2  # Higher if sentiment is more reliable in current market conditions

# ---- Run Weight Adjustment ----
adjusted_price, weight_distribution = adjust_weights(finbert_sentiment, finbert_confidence, lstm_prediction, lstm_confidence, sentiment_match_rate, market_impact_factor)

# ---- Output Result ----
print("\n🔹 Adjusted Predicted Close Price:", round(adjusted_price, 2))
print("🔹 Weight Distribution:", weight_distribution)

