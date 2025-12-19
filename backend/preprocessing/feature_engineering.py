"""
Feature Engineering Module for IPL Match Prediction
Converts ball-by-ball data to match-level aggregated features
"""

import pandas as pd
import numpy as np


def load_data(path):
    """
    Load IPL ball-by-ball CSV data
    
    Args:
        path (str): Path to IPL.csv file
        
    Returns:
        pd.DataFrame: Raw IPL data
    """
    try:
        df = pd.read_csv(path, low_memory=False)
        print(f"✓ Data loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        raise


def aggregate_features(df):
    """
    Aggregate ball-by-ball data to match-level features
    
    Args:
        df (pd.DataFrame): Raw ball-by-ball data
        
    Returns:
        pd.DataFrame: Aggregated match-level features
    """
    # Create is_wicket column from wicket_kind (not null means wicket occurred)
    df['is_wicket'] = df['wicket_kind'].notna().astype(int)
    
    # Group by match_id, innings, and batting_team
    aggregated = df.groupby(['match_id', 'innings', 'batting_team']).agg({
        'runs_batter': 'sum',
        'runs_extras': 'sum',
        'is_wicket': 'sum',
        'ball': 'count',  # Total balls faced
        'season': 'first',
        'venue': 'first',
        'city': 'first',
        'bowling_team': 'first',
        'match_won_by': 'first'
    }).reset_index()
    
    # Rename columns
    aggregated.rename(columns={
        'runs_batter': 'runs_off_bat_total',
        'runs_extras': 'extras_total',
        'is_wicket': 'total_wickets',
        'ball': 'balls_faced',
        'match_won_by': 'winner'
    }, inplace=True)
    
    # Calculate derived features
    aggregated['total_runs'] = aggregated['runs_off_bat_total'] + aggregated['extras_total']
    aggregated['overs_played'] = aggregated['balls_faced'] / 6
    aggregated['run_rate'] = aggregated['total_runs'] / aggregated['overs_played']
    
    # Handle division by zero
    aggregated['run_rate'] = aggregated['run_rate'].replace([np.inf, -np.inf], 0)
    aggregated['run_rate'] = aggregated['run_rate'].fillna(0)
    
    # Create target variable: 1 if batting team won, 0 otherwise
    aggregated['target'] = (aggregated['batting_team'] == aggregated['winner']).astype(int)
    
    # Select final features
    final_features = aggregated[[
        'match_id',
        'innings',
        'season',
        'venue',
        'city',
        'batting_team',
        'bowling_team',
        'total_runs',
        'total_wickets',
        'balls_faced',
        'overs_played',
        'run_rate',
        'extras_total',
        'target'
    ]]
    
    print(f"✓ Features aggregated: {final_features.shape[0]} match innings")
    return final_features


def clean_data(df):
    """
    Clean aggregated data for ML training
    
    Args:
        df (pd.DataFrame): Aggregated features
        
    Returns:
        pd.DataFrame: Cleaned ML-ready data
    """
    # Remove rows with missing critical values
    df_clean = df.dropna(subset=['batting_team', 'bowling_team', 'venue', 'target'])
    
    # Remove rows with zero overs (no meaningful data)
    df_clean = df_clean[df_clean['overs_played'] > 0]
    
    # Remove outliers (e.g., run_rate > 50 is unrealistic)
    df_clean = df_clean[df_clean['run_rate'] <= 50]
    
    # Fill remaining NaN values
    df_clean = df_clean.copy()
    df_clean['city'] = df_clean['city'].fillna('Unknown')
    df_clean['extras_total'] = df_clean['extras_total'].fillna(0)
    
    # Remove duplicate rows
    df_clean = df_clean.drop_duplicates()
    
    print(f"✓ Data cleaned: {df_clean.shape[0]} valid records")
    print(f"  - Removed {df.shape[0] - df_clean.shape[0]} invalid/duplicate rows")
    
    return df_clean


def prepare_ml_data(csv_path):
    """
    Complete pipeline: Load → Aggregate → Clean
    
    Args:
        csv_path (str): Path to raw IPL.csv
        
    Returns:
        pd.DataFrame: ML-ready dataset
    """
    print("="*60)
    print("IPL FEATURE ENGINEERING PIPELINE")
    print("="*60)
    
    # Step 1: Load
    print("\n[1/3] Loading data...")
    df_raw = load_data(csv_path)
    
    # Step 2: Aggregate
    print("\n[2/3] Aggregating features...")
    df_agg = aggregate_features(df_raw)
    
    # Step 3: Clean
    print("\n[3/3] Cleaning data...")
    df_clean = clean_data(df_agg)
    
    print("\n" + "="*60)
    print("✓ FEATURE ENGINEERING COMPLETE")
    print("="*60)
    print(f"Final dataset shape: {df_clean.shape}")
    print(f"Features: {df_clean.columns.tolist()}")
    print(f"Target distribution:\n{df_clean['target'].value_counts()}")
    
    return df_clean


if __name__ == "__main__":
    # Example usage
    csv_path = "../Data/Raw/IPL.csv"
    ml_data = prepare_ml_data(csv_path)
    
    # Save processed data
    output_path = "../Data/Cleaned/IPL_features.csv"
    ml_data.to_csv(output_path, index=False)
    print(f"\n✓ Processed data saved to: {output_path}")
