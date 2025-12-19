"""
Model Training Script for IPL Match Prediction
Uses RandomForestClassifier with preprocessing pipeline
"""

import sys
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report, confusion_matrix
import joblib

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocessing.feature_engineering import prepare_ml_data


def build_preprocessing_pipeline(categorical_features, numerical_features):
    """
    Build preprocessing pipeline with OneHotEncoder and StandardScaler
    
    Args:
        categorical_features (list): List of categorical column names
        numerical_features (list): List of numerical column names
        
    Returns:
        ColumnTransformer: Preprocessing pipeline
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features),
            ('num', StandardScaler(), numerical_features)
        ],
        remainder='drop'
    )
    
    return preprocessor


def train_model(csv_path, save_path='model.pkl'):
    """
    Complete model training pipeline
    
    Args:
        csv_path (str): Path to raw IPL.csv
        save_path (str): Path to save trained model
        
    Returns:
        Pipeline: Trained model pipeline
    """
    print("="*70)
    print("IPL MATCH PREDICTION - MODEL TRAINING")
    print("="*70)
    
    # Step 1: Prepare data
    print("\n[STEP 1] Preparing ML-ready data...")
    df = prepare_ml_data(csv_path)
    
    # Step 2: Define features
    print("\n[STEP 2] Defining features...")
    categorical_features = ['batting_team', 'bowling_team', 'venue', 'city']
    numerical_features = ['total_runs', 'total_wickets', 'run_rate', 'extras_total', 'overs_played']
    
    feature_columns = categorical_features + numerical_features
    target_column = 'target'
    
    print(f"  Categorical features: {categorical_features}")
    print(f"  Numerical features: {numerical_features}")
    
    # Step 3: Split features and target
    X = df[feature_columns]
    y = df[target_column]
    
    print(f"\n  Feature matrix shape: {X.shape}")
    print(f"  Target shape: {y.shape}")
    print(f"  Target distribution:\n{y.value_counts()}")
    
    # Step 4: Train-test split
    print("\n[STEP 3] Splitting data (80-20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"  Training set: {X_train.shape[0]} samples")
    print(f"  Test set: {X_test.shape[0]} samples")
    
    # Step 5: Build pipeline
    print("\n[STEP 4] Building ML pipeline...")
    preprocessor = build_preprocessing_pipeline(categorical_features, numerical_features)
    
    model_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', RandomForestClassifier(
            n_estimators=300,
            max_depth=20,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1,
            verbose=0
        ))
    ])
    
    print("  ✓ Pipeline created:")
    print(f"    - Preprocessor: ColumnTransformer (OneHotEncoder + StandardScaler)")
    print(f"    - Model: RandomForestClassifier (n_estimators=300)")
    
    # Step 6: Train model
    print("\n[STEP 5] Training model...")
    print("  (This may take a few minutes...)")
    model_pipeline.fit(X_train, y_train)
    print("  ✓ Model training complete!")
    
    # Step 7: Evaluate model
    print("\n[STEP 6] Evaluating model...")
    y_pred_train = model_pipeline.predict(X_train)
    y_pred_test = model_pipeline.predict(X_test)
    
    train_accuracy = accuracy_score(y_train, y_pred_train)
    test_accuracy = accuracy_score(y_test, y_pred_test)
    test_precision = precision_score(y_test, y_pred_test, zero_division=0)
    test_recall = recall_score(y_test, y_pred_test, zero_division=0)
    
    print("\n" + "="*70)
    print("MODEL PERFORMANCE METRICS")
    print("="*70)
    print(f"Training Accuracy:   {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
    print(f"Test Accuracy:       {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    print(f"Test Precision:      {test_precision:.4f} ({test_precision*100:.2f}%)")
    print(f"Test Recall:         {test_recall:.4f} ({test_recall*100:.2f}%)")
    print("="*70)
    
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred_test, target_names=['Loss', 'Win']))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred_test)
    print(cm)
    print(f"  True Negatives:  {cm[0][0]}")
    print(f"  False Positives: {cm[0][1]}")
    print(f"  False Negatives: {cm[1][0]}")
    print(f"  True Positives:  {cm[1][1]}")
    
    # Step 8: Save model
    print(f"\n[STEP 7] Saving model to: {save_path}")
    joblib.dump(model_pipeline, save_path)
    print(f"  ✓ Model saved successfully!")
    
    # Save feature information for inference
    feature_info = {
        'categorical_features': categorical_features,
        'numerical_features': numerical_features,
        'feature_columns': feature_columns
    }
    feature_info_path = save_path.replace('.pkl', '_features.pkl')
    joblib.dump(feature_info, feature_info_path)
    print(f"  ✓ Feature info saved to: {feature_info_path}")
    
    print("\n" + "="*70)
    print("✓ TRAINING PIPELINE COMPLETE")
    print("="*70)
    
    return model_pipeline


if __name__ == "__main__":
    # Configuration
    RAW_DATA_PATH = "../Data/Raw/IPL.csv"
    MODEL_SAVE_PATH = "model.pkl"
    
    # Train model
    trained_model = train_model(RAW_DATA_PATH, MODEL_SAVE_PATH)
    
    print("\n✓ Model is ready for production use!")
    print(f"  Load with: joblib.load('{MODEL_SAVE_PATH}')")
