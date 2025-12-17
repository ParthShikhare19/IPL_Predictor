import pandas as pd
import os

# Read the CSV file
print("Reading IPL.csv...")
# Use absolute path relative to script location
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, '..', 'Data', 'Raw', 'IPL.csv')
df = pd.read_csv(csv_path)

# Display initial information
print(f"\nDataset shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")

# Remove specified columns
columns_to_remove = ['match_id', 'date', 'match_type', 'event_name', 'gender', 'team_type', 'method', 'match_number']
df = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors='ignore')
print(f"\nDataset shape after removing columns: {df.shape}")
print(f"\nRemaining columns: {df.columns.tolist()}")

# Check for null values
print("\nNull values per column:")
null_counts = df.isnull().sum()
print(null_counts[null_counts > 0])

# Replace all null/NaN values with the string "None"
df = df.fillna("None")

# Verify no null values remain
print("\nNull values after replacement:")
print(df.isnull().sum().sum())

# Save the modified dataframe back to CSV
output_path = os.path.join(script_dir, '..', 'Data', 'Cleaned', 'IPL_cleaned.csv')
df.to_csv(output_path, index=False)
print(f"\nCleaned data saved to {output_path}")
