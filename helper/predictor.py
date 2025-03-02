import os
import sys
import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime, timedelta
import tensorflow as tf

def predict_main(stock_symbol, target_date_str):
    # ---- Step 1: Load the Cleaned Dataset ----
    # print("HI")
    file_path = "lstm_models/NIFTY50_cleaned.csv"  # Ensure this file exists
    df = pd.read_csv(file_path, parse_dates=['Date'])
    
    # ---- Process Input Parameters ----
    stock_symbol = stock_symbol.strip().upper()
    try:
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format! Please use YYYY-MM-DD.")
        return

    # ---- Step 3: Filter Data for the Selected Stock ----
    stock_df = df[df['Symbol'] == stock_symbol].sort_values(by='Date')
    if stock_df.empty:
        print(f"No data found for stock symbol {stock_symbol}")
        return

    # ---- Step 4: Verify Target Date is After the Last Available Date ----
    last_date = stock_df['Date'].max().date()
    if target_date <= last_date:
        print("Target date must be after the last available date in the dataset:", last_date)
        return

    # ---- Step 5: Load the Saved Model and Scaler from 'models' Directory ----
    models_dir = "lstm_models/models"
    model_filename = os.path.join(models_dir, f"{stock_symbol}_lstm_model.h5")
    scaler_filename = os.path.join(models_dir, f"{stock_symbol}_scaler.pkl")

    if not (os.path.exists(model_filename) and os.path.exists(scaler_filename)):
        print(f"Model or scaler for '{stock_symbol}' not found. Please train the models first.")
        return

    model = tf.keras.models.load_model(model_filename)
    scaler = joblib.load(scaler_filename)

    # ---- Step 6: Prepare Input Data for Forecasting ----
    seq_length = 60  # Must match training sequence length
    if len(stock_df) < seq_length:
        print("Not enough data to create input sequence.")
        return

    last_60 = stock_df['Close'].values[-seq_length:]
    scaled_seq = scaler.transform(last_60.reshape(-1, 1))

    # ---- Step 7: Recursive Forecast for the Next 7 Days ----
    forecast_horizon = 7
    predictions = []
    input_seq = scaled_seq.copy()  # shape: (seq_length, 1)

    for _ in range(forecast_horizon):
        input_seq_reshaped = np.reshape(input_seq, (1, seq_length, 1))
        pred_scaled = model.predict(input_seq_reshaped)
        pred = scaler.inverse_transform(pred_scaled)[0][0]
        predictions.append(pred)
        input_seq = np.append(input_seq, pred_scaled, axis=0)[1:]

    forecast_dates = [(last_date + timedelta(days=i+1)) for i in range(forecast_horizon)]

    # ---- Step 8: Build CSV Rows and JSON Forecast Results for Predicted Data ----
    series_val = stock_df['Series'].iloc[-1]
    last_actual_price = stock_df['Close'].values[-1]
    csv_rows = []
    json_forecasts = []
    prev_price = last_actual_price

    for d, pred in zip(forecast_dates, predictions):
        # Build CSV row for forecasted data
        row = {
            "Date": d.strftime("%Y-%m-%d"),
            "Symbol": stock_symbol,
            "Series": series_val,
            "Prev Close": round(prev_price, 2),
            "Open": round(pred, 2),
            "High": round(pred, 2),
            "Low": round(pred, 2),
            "Last": round(pred, 2),
            "Close": round(pred, 2),
            "VWAP": round(pred, 2)
        }
        csv_rows.append(row)
        
        # Build JSON forecast info
        trend = "UP" if pred > prev_price else "DOWN"
        percent_change = ((pred - prev_price) / prev_price) * 100
        json_forecasts.append({
            "date": d.strftime("%Y-%m-%d"),
            "predicted_close_price": float(round(pred, 2)),
            "trend": trend,
            "percent_change": f"{float(percent_change):+.2f}%"
        })
        prev_price = pred

    # ---- Step 9: Create DataFrames for Historical and Predicted Data ----
    # Predicted DataFrame with a new 'predicted' column set to 1
    predicted_df = pd.DataFrame(csv_rows, columns=["Date", "Symbol", "Series", "Prev Close", "Open", "High", "Low", "Last", "Close", "VWAP"])
    predicted_df['predicted'] = 1

    # Take the last 7 days from the historical data
    historical_df = stock_df.tail(7).copy()
    # If 'Prev Close' or 'Last' do not exist in historical data, create/compute them
    if "Prev Close" not in historical_df.columns:
        historical_df["Prev Close"] = historical_df["Close"].shift(1)
        historical_df["Prev Close"].fillna(historical_df["Close"], inplace=True)
    if "Last" not in historical_df.columns:
        historical_df["Last"] = historical_df["Close"]

    # Reorder columns to match the predicted data structure
    historical_df = historical_df[["Date", "Symbol", "Series", "Prev Close", "Open", "High", "Low", "Last", "Close", "VWAP"]]
    historical_df['predicted'] = 0

    # ---- Step 10: Append Predicted Data to Historical Data and Save ----
    combined_df = pd.concat([historical_df, predicted_df], ignore_index=True)
    combined_csv_filename = f"temp.csv"
    combined_df.to_csv(combined_csv_filename, index=False)
    print(f"Forecast appended with historical data saved to {combined_csv_filename}")

    # ---- Step 11: Prepare and Print JSON Output for the Target Forecast Date ----
    target_forecast = next((item for item in json_forecasts if item["date"] == target_date_str), None)
    output_json = {
        "target_date_forecast": target_forecast,
        "7_day_forecast": json_forecasts
    }
    print(json.dumps(output_json, indent=4))
