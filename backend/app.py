"""
Flask Backend API for IPL Match Prediction
Provides REST API endpoint for match predictions
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Add model directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from model.predict import predict_match, load_model

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for React frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'model.pkl')

# Load model at startup
try:
    load_model(MODEL_PATH)
    print("✓ Model loaded successfully at startup")
except Exception as e:
    print(f"⚠ Warning: Could not load model at startup: {e}")
    print("  Model will be loaded on first prediction request")


@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'IPL Match Prediction API is running',
        'version': '1.0.0',
        'endpoints': {
            '/api/predict': 'POST - Make match prediction',
            '/api/health': 'GET - Health check'
        }
    }), 200


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    model_exists = os.path.exists(MODEL_PATH)
    return jsonify({
        'status': 'healthy' if model_exists else 'degraded',
        'model_loaded': model_exists,
        'model_path': MODEL_PATH
    }), 200


@app.route('/api/predict', methods=['POST', 'OPTIONS'])
def predict():
    """
    Predict match outcome endpoint
    
    Expected JSON payload:
    {
        "batting_team": "Mumbai Indians",
        "bowling_team": "Chennai Super Kings",
        "venue": "Wankhede Stadium",
        "city": "Mumbai",
        "total_runs": 180,
        "total_wickets": 5,
        "overs_played": 20.0,
        "extras_total": 12,
        "run_rate": 9.0
    }
    
    Returns:
    {
        "status": "success",
        "prediction": "Batting Team Wins" or "Batting Team Loses",
        "win_probability": 0.82,
        "loss_probability": 0.18,
        "input_data": {...}
    }
    """
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Parse JSON request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided'
            }), 400
        
        # Validate required fields
        required_fields = [
            'batting_team', 'bowling_team', 'venue', 'city',
            'total_runs', 'total_wickets', 'overs_played',
            'extras_total', 'run_rate'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}',
                'required_fields': required_fields
            }), 400
        
        # Validate numeric fields
        numeric_fields = ['total_runs', 'total_wickets', 'overs_played', 'extras_total', 'run_rate']
        for field in numeric_fields:
            try:
                data[field] = float(data[field])
                if data[field] < 0:
                    return jsonify({
                        'status': 'error',
                        'message': f'{field} cannot be negative'
                    }), 400
            except (ValueError, TypeError):
                return jsonify({
                    'status': 'error',
                    'message': f'{field} must be a valid number'
                }), 400
        
        # Additional validation
        if data['overs_played'] > 20:
            return jsonify({
                'status': 'error',
                'message': 'overs_played cannot exceed 20 in T20 cricket'
            }), 400
        
        if data['total_wickets'] > 10:
            return jsonify({
                'status': 'error',
                'message': 'total_wickets cannot exceed 10'
            }), 400
        
        if data['batting_team'] == data['bowling_team']:
            return jsonify({
                'status': 'error',
                'message': 'batting_team and bowling_team must be different'
            }), 400
        
        # Make prediction
        result = predict_match(data, MODEL_PATH)
        
        # Return response
        return jsonify({
            'status': 'success',
            'prediction': result['prediction_text'],
            'win_probability': result['win_probability'],
            'loss_probability': result['loss_probability'],
            'confidence': round(max(result['win_probability'], result['loss_probability']) * 100, 2),
            'input_data': data
        }), 200
    
    except FileNotFoundError:
        return jsonify({
            'status': 'error',
            'message': 'Model file not found. Please train the model first.',
            'details': f'Expected model at: {MODEL_PATH}'
        }), 500
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Prediction failed',
            'details': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'available_endpoints': {
            '/': 'GET - API info',
            '/api/health': 'GET - Health check',
            '/api/predict': 'POST - Make prediction'
        }
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'details': str(error)
    }), 500


if __name__ == '__main__':
    print("="*70)
    print("IPL MATCH PREDICTION API SERVER")
    print("="*70)
    print(f"Model path: {MODEL_PATH}")
    print(f"Model exists: {os.path.exists(MODEL_PATH)}")
    print("\nStarting Flask server...")
    print("API will be available at: http://localhost:5000")
    print("\nEndpoints:")
    print("  GET  /              - API information")
    print("  GET  /api/health    - Health check")
    print("  POST /api/predict   - Make prediction")
    print("\nPress Ctrl+C to stop the server")
    print("="*70)
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
