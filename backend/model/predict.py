"""
Prediction Utility for IPL Match Prediction
Loads trained model and makes predictions on new data
"""

import os
import joblib
import pandas as pd
import numpy as np


# Global variable to cache loaded model
_cached_model = None
_model_path = None


def load_model(model_path='model.pkl'):
    """
    Load trained model from disk (with caching)
    
    Args:
        model_path (str): Path to saved model pickle file
        
    Returns:
        Pipeline: Trained sklearn pipeline
    """
    global _cached_model, _model_path
    
    # Return cached model if already loaded and path matches
    if _cached_model is not None and _model_path == model_path:
        return _cached_model
    
    try:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        _cached_model = joblib.load(model_path)
        _model_path = model_path
        print(f"✓ Model loaded successfully from: {model_path}")
        return _cached_model
    
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        raise


def predict_match(input_dict, model_path='model.pkl'):
    """
    Predict match outcome based on input features
    
    Args:
        input_dict (dict): Dictionary containing input features:
            - batting_team (str)
            - bowling_team (str)
            - venue (str)
            - city (str)
            - total_runs (int/float)
            - total_wickets (int)
            - overs_played (float)
            - extras_total (int/float)
            - run_rate (float)
            
        model_path (str): Path to trained model
        
    Returns:
        dict: Prediction results
            - prediction_label (int): 0 (loss) or 1 (win)
            - win_probability (float): Probability of batting team winning
            - loss_probability (float): Probability of batting team losing
    """
    try:
        # Load model
        model = load_model(model_path)
        
        # Validate input
        required_fields = [
            'batting_team', 'bowling_team', 'venue', 'city',
            'total_runs', 'total_wickets', 'overs_played', 
            'extras_total', 'run_rate'
        ]
        
        for field in required_fields:
            if field not in input_dict:
                raise ValueError(f"Missing required field: {field}")
        
        # Convert input to DataFrame (model expects DataFrame)
        input_df = pd.DataFrame([input_dict])
        
        # Ensure correct column order
        feature_columns = [
            'batting_team', 'bowling_team', 'venue', 'city',
            'total_runs', 'total_wickets', 'run_rate', 
            'extras_total', 'overs_played'
        ]
        input_df = input_df[feature_columns]
        
        # Make prediction
        prediction_label = model.predict(input_df)[0]
        prediction_proba = model.predict_proba(input_df)[0]
        
        # Extract probabilities
        loss_probability = float(prediction_proba[0])
        win_probability = float(prediction_proba[1])
        
        result = {
            'prediction_label': int(prediction_label),
            'win_probability': round(win_probability, 4),
            'loss_probability': round(loss_probability, 4),
            'prediction_text': 'Batting Team Wins' if prediction_label == 1 else 'Batting Team Loses'
        }
        
        print(f"✓ Prediction made: {result['prediction_text']} (confidence: {max(win_probability, loss_probability)*100:.2f}%)")
        
        return result
    
    except Exception as e:
        print(f"✗ Prediction error: {e}")
        raise


def batch_predict(input_list, model_path='model.pkl'):
    """
    Make predictions for multiple inputs
    
    Args:
        input_list (list): List of input dictionaries
        model_path (str): Path to trained model
        
    Returns:
        list: List of prediction results
    """
    try:
        model = load_model(model_path)
        
        # Convert to DataFrame
        input_df = pd.DataFrame(input_list)
        
        # Ensure correct column order
        feature_columns = [
            'batting_team', 'bowling_team', 'venue', 'city',
            'total_runs', 'total_wickets', 'run_rate', 
            'extras_total', 'overs_played'
        ]
        input_df = input_df[feature_columns]
        
        # Make predictions
        predictions = model.predict(input_df)
        probabilities = model.predict_proba(input_df)
        
        results = []
        for i, (pred, proba) in enumerate(zip(predictions, probabilities)):
            result = {
                'prediction_label': int(pred),
                'win_probability': round(float(proba[1]), 4),
                'loss_probability': round(float(proba[0]), 4),
                'prediction_text': 'Batting Team Wins' if pred == 1 else 'Batting Team Loses'
            }
            results.append(result)
        
        print(f"✓ Batch prediction complete: {len(results)} predictions made")
        return results
    
    except Exception as e:
        print(f"✗ Batch prediction error: {e}")
        raise


if __name__ == "__main__":
    # Example usage
    print("="*60)
    print("IPL MATCH PREDICTION - INFERENCE EXAMPLE")
    print("="*60)
    
    # Sample input
    sample_input = {
        'batting_team': 'Mumbai Indians',
        'bowling_team': 'Chennai Super Kings',
        'venue': 'Wankhede Stadium',
        'city': 'Mumbai',
        'total_runs': 180,
        'total_wickets': 5,
        'overs_played': 20.0,
        'extras_total': 12,
        'run_rate': 9.0
    }
    
    print("\nInput:")
    for key, value in sample_input.items():
        print(f"  {key}: {value}")
    
    # Make prediction
    print("\nMaking prediction...")
    try:
        result = predict_match(sample_input)
        
        print("\n" + "="*60)
        print("PREDICTION RESULT")
        print("="*60)
        print(f"Prediction: {result['prediction_text']}")
        print(f"Win Probability: {result['win_probability']*100:.2f}%")
        print(f"Loss Probability: {result['loss_probability']*100:.2f}%")
        print("="*60)
    
    except FileNotFoundError:
        print("\n⚠ Model file not found. Please train the model first by running:")
        print("  python train.py")
    except Exception as e:
        print(f"\n✗ Error: {e}")
