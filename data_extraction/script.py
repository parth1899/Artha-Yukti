import yfinance as yf
import pandas as pd
import os

# List of your stock symbols (as used in your dataset)
stock_symbols = [
    "ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV",
    "BAJFINANCE", "BHARTIARTL", "BPCL", "BRITANNIA", "CIPLA", "COALINDIA",
    "DRREDDY", "EICHERMOT", "GAIL", "GRASIM", "HCLTECH", "HDFC", "HDFCBANK",
    "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "INDUSINDBK",
    "INFRATEL", "INFY", "IOC", "ITC", "JSWSTEEL", "KOTAKBANK", "LT",
    "MARUTI", "MM", "NESTLEIND", "NTPC", "ONGC", "POWERGRID", "RELIANCE",
    "SBIN", "SHREECEM", "SUNPHARMA", "TATAMOTORS", "TATASTEEL", "TCS",
    "TECHM", "TITAN", "ULTRACEMCO", "UPL", "VEDL", "WIPRO", "ZEEL"
]

# Convert your stock symbols to Yahoo Finance tickers (assuming NSE stocks)
tickers = [f"{sym}.NS" for sym in stock_symbols]

# Define the new data period (day after April 30, 2021 to Feb 28, 2025)
start_date = "2014-01-01"
end_date = "2025-02-28"

# Directory where your CSV files are stored
data_dir = "datasets"  # Change this to your actual directory

# Loop through each ticker, download data, and save/append to CSV
for ticker, symbol in zip(tickers, stock_symbols):
    print(f"Downloading data for {symbol}...")
    
    # Download historical data using yfinance
    df_new = yf.download(ticker, start=start_date, end=end_date)
    
    if df_new.empty:
        print(f"No data found for {ticker}.")
        continue

    # Reset index to make the Date a column
    df_new.reset_index(inplace=True)
    
    # Optionally, add any columns that are not provided by Yahoo Finance.
    # For example, if you want a constant "Series" column (e.g., "EQ"):
    df_new["Series"] = "EQ"
    
    # You can compute 'Prev Close' by shifting the 'Close' column by one day
    df_new["Prev Close"] = df_new["Close"].shift(1)
    
    # 'Last' price might be assumed as the 'Close' price (or you could adjust as needed)
    df_new["Last"] = df_new["Close"]
    
    # VWAP is not directly provided by Yahoo Finance for daily data.
    # One simple approximation (not a true intraday VWAP) is to use the average of High, Low, and Close:
    df_new["VWAP"] = (df_new["High"] + df_new["Low"] + df_new["Close"]) / 3

    # Reorder or select columns to match your dataset format.
    # Example order: Date, Symbol, Series, Prev Close, Open, High, Low, Last, Close, VWAP
    df_new["Symbol"] = symbol  # add the symbol column
    df_new = df_new[["Date", "Symbol", "Series", "Prev Close", "Open", "High", "Low", "Last", "Close", "VWAP"]]

    # Define the CSV file path for the stock
    file_path = os.path.join(data_dir, f"{symbol}.csv")
    
    # If file exists, append the new data (ensuring no overlapping dates)
    if os.path.exists(file_path):
        df_existing = pd.read_csv(file_path, parse_dates=["Date"])
        # Keep only new dates that are not already in the existing dataset
        new_data = df_new[~df_new["Date"].isin(df_existing["Date"])]
        if not new_data.empty:
            df_updated = pd.concat([df_existing, new_data], ignore_index=True)
            # Optionally, sort by Date if needed
            df_updated.sort_values("Date", inplace=True)
            df_updated.to_csv(file_path, index=False)
            print(f"Appended {len(new_data)} rows to {symbol}.csv")
        else:
            print(f"No new data for {symbol}.")
    else:
        # If no file exists, create a new one
        df_new.to_csv(file_path, index=False)
        print(f"Created new file for {symbol} with {len(df_new)} rows.")
