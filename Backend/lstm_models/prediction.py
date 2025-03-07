import os
import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime, timedelta
import tensorflow as tf

# ---- Step 1: Load the Cleaned Dataset ----
file_path = "NIFTY50_cleaned.csv"  # Ensure this file exists
df = pd.read_csv(file_path, parse_dates=['Date'])

# ---- Step 2: Ask for Stock Symbol and Target Forecast Date ----
stock_symbol = input("Enter stock symbol (e.g., TCS, RELIANCE): ").strip().upper()
target_date_str = input("Enter target forecast date (YYYY-MM-DD): ").strip()

try:
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
except ValueError:
    print("Invalid date format! Please use YYYY-MM-DD.")
    exit()

# ---- Step 3: Filter Data for the Selected Stock ----
stock_df = df[df['Symbol'] == stock_symbol].sort_values(by='Date')
if stock_df.empty:
    print(f"No data found for stock symbol {stock_symbol}")
    exit()

# ---- Step 4: Verify Target Date is After the Last Available Date ----
last_date = stock_df['Date'].max().date()
if target_date <= last_date:
    print("Target date must be after the last available date in the dataset:", last_date)
    exit()

# ---- Step 5: Load the Saved Model and Scaler from 'models' Directory ----
models_dir = "models"
model_filename = os.path.join(models_dir, f"{stock_symbol}_lstm_model.h5")
scaler_filename = os.path.join(models_dir, f"{stock_symbol}_scaler.pkl")

if not (os.path.exists(model_filename) and os.path.exists(scaler_filename)):
    print(f"Model or scaler for '{stock_symbol}' not found. Please train the models first.")
    exit()

model = tf.keras.models.load_model(model_filename)
scaler = joblib.load(scaler_filename)

# ---- Step 6: Prepare Input Data for Forecasting ----
seq_length = 60  # Must match training sequence length
if len(stock_df) < seq_length:
    print("Not enough data to create input sequence.")
    exit()

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

# ---- Step 8: Build CSV Rows and JSON Forecast Results ----
series_val = stock_df['Series'].iloc[-1]
last_actual_price = stock_df['Close'].values[-1]
csv_rows = []
json_forecasts = []
prev_price = last_actual_price

for d, pred in zip(forecast_dates, predictions):
    # Build CSV row
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

# ---- Step 9: Save the 7-Day Forecast to CSV ----
output_df = pd.DataFrame(csv_rows, columns=["Date", "Symbol", "Series", "Prev Close", "Open", "High", "Low", "Last", "Close", "VWAP"])
output_csv_filename = f"{stock_symbol}_7_day_forecast.csv"
output_df.to_csv(output_csv_filename, index=False)
print(f"7-day forecast saved to {output_csv_filename}")

# ---- Step 10: Prepare and Print JSON Output for the Target Forecast Date ----
target_forecast = next((item for item in json_forecasts if item["date"] == target_date_str), None)
output_json = {
    "target_date_forecast": target_forecast,
    "7_day_forecast": json_forecasts
}
print(json.dumps(output_json, indent=4))
