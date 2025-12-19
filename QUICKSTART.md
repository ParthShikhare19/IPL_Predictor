# IPL Match Predictor - Quick Setup Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Backend Setup

```powershell
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Train the model (first time only - takes 2-3 minutes)
cd model
python train.py
cd ..

# Start Flask server
python app.py
```

✅ Backend running on http://localhost:5000

### Step 2: Frontend Setup

```powershell
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start React dev server
npm run dev
```

✅ Frontend running on http://localhost:5173

### Step 3: Use the Application

1. Open http://localhost:5173 in your browser
2. Fill in the match details
3. Click "Predict Match Outcome"
4. View prediction results!

## 📝 What Each Script Does

### Backend Scripts

**feature_engineering.py**
- Loads IPL.csv
- Aggregates ball-by-ball data to match-level
- Creates ML-ready features
- Saves cleaned data

**train.py**
- Loads processed data
- Builds preprocessing pipeline (OneHotEncoder + StandardScaler)
- Trains RandomForest classifier (300 estimators)
- Saves model to model.pkl
- Prints accuracy, precision, recall

**predict.py**
- Loads trained model
- Makes predictions on new data
- Returns win/loss probabilities

**app.py**
- Flask REST API server
- POST /api/predict endpoint
- CORS enabled for React
- Input validation

### Frontend Components

**App.jsx**
- Main application component
- Handles state management
- Displays results

**PredictionForm.jsx**
- Input form with validation
- Auto-calculates run rate
- Submits to backend API

**predict.js**
- Axios API wrapper
- Makes HTTP requests to Flask

## 🧪 Test the API Directly

```powershell
# Test prediction endpoint
curl -X POST http://localhost:5000/api/predict `
  -H "Content-Type: application/json" `
  -d '{
    "batting_team": "Mumbai Indians",
    "bowling_team": "Chennai Super Kings",
    "venue": "Wankhede Stadium",
    "city": "Mumbai",
    "total_runs": 180,
    "total_wickets": 5,
    "overs_played": 20.0,
    "extras_total": 12,
    "run_rate": 9.0
  }'
```

## 🔍 Troubleshooting

**Model not found error?**
- Make sure you ran `python train.py` first
- Check that `model.pkl` exists in `backend/model/`

**CORS error?**
- Ensure Flask backend is running
- Check Flask CORS is installed: `pip install flask-cors`

**Connection refused?**
- Verify Flask is running on port 5000
- Verify React is running on port 5173

**Import errors?**
- Install all requirements: `pip install -r requirements.txt`
- Activate virtual environment if using one

## 📊 Expected Model Performance

After training, you should see:
- Training Accuracy: ~75-85%
- Test Accuracy: ~70-80%
- Precision: ~70-80%
- Recall: ~70-80%

## 🎯 Next Steps

1. ✅ Train model with your IPL dataset
2. ✅ Start backend server
3. ✅ Start frontend server
4. ✅ Make predictions
5. 📈 Improve model with more features
6. 🚀 Deploy to production

Happy predicting! 🏏
