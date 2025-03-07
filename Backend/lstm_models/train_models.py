import os
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Load the cleaned dataset (ensure this file exists in your working directory)
file_path = "NIFTY50_cleaned.csv"
df = pd.read_csv(file_path, parse_dates=['Date'])

# Create a directory for models if it doesn't exist
models_dir = "models"
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

# Get unique stock symbols
unique_symbols = df['Symbol'].unique()
print("Training models for the following stocks:", unique_symbols)

def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

seq_length = 60  # Use past 60 days to predict the next day

# Iterate over each stock symbol
for symbol in unique_symbols:
    stock_df = df[df['Symbol'] == symbol].sort_values(by='Date')
    
    # Skip stocks with insufficient data
    if len(stock_df) < seq_length:
        print(f"Not enough data for {symbol}, skipping.")
        continue

    print(f"Training model for {symbol}...")
    data = stock_df[['Close']].values  # use closing price for forecasting
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    # Create sequences for LSTM input
    X, y = create_sequences(scaled_data, seq_length)
    if len(X) == 0:
        print(f"Not enough sequences for {symbol}, skipping.")
        continue

    # Use 80% of data for training
    train_size = int(len(X) * 0.8)
    X_train, y_train = X[:train_size], y[:train_size]
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))

    # Build LSTM model
    model = Sequential([
        LSTM(100, return_sequences=True, input_shape=(seq_length, 1)),
        Dropout(0.2),
        LSTM(100, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)

    # Save the model and scaler using the stock symbol in the filename
    model_filename = os.path.join(models_dir, f"{symbol}_lstm_model.h5")
    scaler_filename = os.path.join(models_dir, f"{symbol}_scaler.pkl")
    model.save(model_filename)
    joblib.dump(scaler, scaler_filename)
    print(f"Trained and saved model for {symbol} as {model_filename} and scaler as {scaler_filename}\n")
