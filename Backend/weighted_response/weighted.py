import os
import sys
import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime, timedelta
import tensorflow as tf
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# ==============================
# LSTM Prediction Functionality
# ==============================
def run_lstm_forecast(stock_symbol: str, target_date_str: str):
    # ---- Step 1: Load the Cleaned Dataset ----
    file_path = "weighted_response/NIFTY50_cleaned.csv"
    df = pd.read_csv(file_path, parse_dates=['Date'])

    # ---- Parse Target Forecast Date ----
    try:
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format! Please use YYYY-MM-DD.")
        exit()

    # ---- Step 2: Filter Data for the Selected Stock ----
    stock_df = df[df['Symbol'] == stock_symbol].sort_values(by='Date')
    if stock_df.empty:
        print(f"No data found for stock symbol {stock_symbol}")
        exit()

    # ---- Step 3: Verify Target Date is After the Last Available Date ----
    last_date = stock_df['Date'].max().date()
    if target_date <= last_date:
        print(f"Target date must be after the last available date in the dataset: {last_date}")
        exit()

    # ---- Step 4: Load the Saved Model and Scaler from 'models' Directory ----
    models_dir = "lstm_models/models"
    model_filename = os.path.join(models_dir, f"{stock_symbol}_lstm_model.h5")
    scaler_filename = os.path.join(models_dir, f"{stock_symbol}_scaler.pkl")

    if not (os.path.exists(model_filename) and os.path.exists(scaler_filename)):
        print(f"Model or scaler for '{stock_symbol}' not found. Please train the model first.")
        exit()

    model = tf.keras.models.load_model(model_filename)
    scaler = joblib.load(scaler_filename)

    # ---- Step 5: Prepare Input Data for Forecasting ----
    seq_length = 60  # Must match training sequence length
    if len(stock_df) < seq_length:
        print("Not enough data to create input sequence.")
        exit()

    last_60 = stock_df['Close'].values[-seq_length:]
    scaled_seq = scaler.transform(last_60.reshape(-1, 1))

    # ---- Step 6: Forecast for the Next 7 Days ----
    forecast_horizon = 7
    predictions = []
    confidence_scores = []
    input_seq = scaled_seq.copy()

    # Compute historical volatility for confidence estimation
    historical_volatility = stock_df['Close'].rolling(60).std().iloc[-1]

    for _ in range(forecast_horizon):
        input_seq_reshaped = np.reshape(input_seq, (1, seq_length, 1))
        pred_scaled = model.predict(input_seq_reshaped)
        # Convert predicted price back to original scale
        pred_price = scaler.inverse_transform([[pred_scaled[0][0]]])[0][0]
        predictions.append(pred_price)
        # Use last 5 predictions (or available ones) to estimate confidence
        window = predictions[-5:] if len(predictions) >= 5 else predictions
        confidence_score = max(0.0, min(1.0, 1 - (np.std(window) / (historical_volatility + 1e-6))))
        confidence_scores.append(confidence_score)
        # Update input sequence with the predicted value
        input_seq = np.append(input_seq, [[pred_scaled[0][0]]], axis=0)[1:]

    # Calculate average LSTM prediction and confidence over 7 days
    avg_lstm_prediction = np.mean(predictions)
    avg_lstm_confidence = np.mean(confidence_scores)

    print("\nLSTM 7-day Predictions:")
    for i, (pred, conf) in enumerate(zip(predictions, confidence_scores), 1):
        print(f"Day {i}: Predicted Price: {pred:.2f}, Confidence: {conf:.2f}")

    print(f"\nAverage LSTM Prediction: {avg_lstm_prediction:.2f}")
    print(f"Average LSTM Confidence: {avg_lstm_confidence:.2f}\n")

    return stock_symbol, avg_lstm_prediction, avg_lstm_confidence

# ==============================
# Sentiment Analysis Functionality
# ==============================
def analyze_sentiment(text: str):
    model_name = "StephanAkkerman/FinTwitBERT-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    result = sentiment_pipeline(text)
    return result

def get_sentiment(sentiment_text: str):
    analysis_result = analyze_sentiment(sentiment_text)
    # Extract the first result
    finbert_sentiment = analysis_result[0]['label']
    finbert_confidence = analysis_result[0]['score']
    print("\nSentiment Analysis Result:")
    print(f"Label: {finbert_sentiment} | Score: {finbert_confidence:.4f}\n")
    return finbert_sentiment, finbert_confidence

# ==============================
# Dynamic Weight Adjustment
# ==============================
def adjust_weights(finbert_sentiment, finbert_confidence, lstm_prediction, lstm_confidence, sentiment_match_rate, market_impact_factor=1.0):
    """
    Adjusts weight dynamically while ensuring LSTM always has at least 50% weight.
    
    Parameters:
    - finbert_sentiment (str): "Bullish", "Bearish", or "Neutral"
    - finbert_confidence (float): Confidence score (0 to 1) from FinBERT
    - lstm_prediction (float): LSTM predicted close price (average over 7 days)
    - lstm_confidence (float): Average confidence score from LSTM
    - sentiment_match_rate (float): Historical accuracy of sentiment (0 to 1)
    - market_impact_factor (float): External event impact (1.0 = neutral, >1 increases sentiment weight, <1 reduces sentiment weight)
    
    Returns:
    - adjusted_price (float): Final adjusted close price prediction
    - weight_distribution (dict): Assigned weights for FinBERT and LSTM
    """
    # Base weight for LSTM is always 50%
    lstm_weight = 0.50

    # Adjust FinBERT weight based on its confidence, historical accuracy, and market impact
    if finbert_confidence >= 0.7:
        finbert_weight = min(0.50, finbert_confidence * sentiment_match_rate * market_impact_factor)
    else:
        finbert_weight = max(0.0, finbert_confidence * 0.5)  # Reduce weight if confidence < 0.7

    # Ensure total weight is 1 with LSTM at least 50%
    lstm_weight = max(0.50, 1.0 - finbert_weight)

    # In this example, the adjusted price is a weighted average.
    # (Note: As written, both weights multiply the LSTM prediction; modify if you have a separate sentiment-based price.)
    adjusted_price = (finbert_weight * lstm_prediction) + (lstm_weight * lstm_prediction)
    return adjusted_price, {"FinBERT": round(finbert_weight * 100, 2), "LSTM": round(lstm_weight * 100, 2)}

# ==============================
# Main Combined Execution
# ==============================
def weighted_main(stock_symbol: str, target_date_str: str, sentiment_text: str):
    # Run LSTM forecast and compute averages using provided inputs
    stock_symbol, avg_lstm_prediction, avg_lstm_confidence = run_lstm_forecast(stock_symbol, target_date_str)
    
    # Perform sentiment analysis on the input text
    finbert_sentiment, finbert_confidence = get_sentiment(sentiment_text)
    
    # Set additional parameters (can be adjusted as needed)
    sentiment_match_rate = 0.75    # Historical accuracy of sentiment analysis
    market_impact_factor = 1.2     # Factor to amplify/reduce sentiment impact based on market conditions
    
    # Run dynamic weight adjustment using averaged LSTM values and sentiment analysis results
    adjusted_price, weight_distribution = adjust_weights(
        finbert_sentiment,
        finbert_confidence,
        avg_lstm_prediction,
        avg_lstm_confidence,
        sentiment_match_rate,
        market_impact_factor
    )
    
    # print("🔹 Adjusted Predicted Close Price:", round(adjusted_price, 2))
    # print("🔹 Weight Distribution:", weight_distribution)

    return adjusted_price, weight_distribution

# if __name__ == "__main__":
#     if len(sys.argv) != 4:
#         print("Usage: python script.py <stock_symbol> <target_date: YYYY-MM-DD> <sentiment_text>")
#         sys.exit(1)
#     stock_symbol_input = sys.argv[1]
#     target_date_input = sys.argv[2]
#     sentiment_text_input = sys.argv[3]
#     main(stock_symbol_input, target_date_input, sentiment_text_input)
