import os
import pandas as pd

# Directory where your CSV files are stored
data_dir = "datasets"  # Adjust this path if needed

# List all CSV files in the directory
csv_files = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith(".csv")]

# Initialize an empty list to store each DataFrame
dfs = []

# Loop through each CSV file and read it
for file in csv_files:
    df = pd.read_csv(file, parse_dates=["Date"])
    dfs.append(df)

# Concatenate all DataFrames into one merged DataFrame
merged_df = pd.concat(dfs, ignore_index=True)

# Optionally, sort the merged DataFrame by Date (or any other column)
merged_df.sort_values("Date", inplace=True)

# Save the merged DataFrame to merged.csv
merged_df.to_csv("merged.csv", index=False)

print(f"Merged {len(csv_files)} files into merged.csv with {len(merged_df)} rows.")
