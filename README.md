# 🏏 IPL Match Predictor

A production-ready machine learning application that predicts IPL (Indian Premier League) match outcomes using a Flask backend, Scikit-Learn ML models, and React frontend.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Dataset](#dataset)
- [ML Pipeline](#ml-pipeline)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)

## 🎯 Overview

This application analyzes ball-by-ball IPL cricket data to predict match outcomes. It features:

- **Backend**: Flask REST API with ML inference
- **ML Model**: Random Forest Classifier with preprocessing pipeline
- **Frontend**: React application with modern UI
- **Model Persistence**: Pickle/Joblib for model serialization

The system converts ball-by-ball data into match-level features and uses ensemble learning to predict whether the batting team will win or lose.

## ✨ Features

- ✅ Complete feature engineering pipeline
- ✅ Production-ready ML model training
- ✅ RESTful API for predictions
- ✅ Interactive React frontend
- ✅ Real-time prediction with confidence scores
- ✅ Input validation and error handling
- ✅ Auto-calculated run rates
- ✅ Responsive design

## 🏗️ Architecture

```
┌─────────────┐      HTTP POST      ┌──────────────┐
│   React     │ ──────────────────> │  Flask API   │
│  Frontend   │ <────────────────── │   (Python)   │
└─────────────┘      JSON           └──────────────┘
                                             │
                                             │ load_model()
                                             ▼
                                    ┌──────────────────┐
                                    │ Scikit-Learn     │
                                    │ RandomForest     │
                                    │ Pipeline         │
                                    └──────────────────┘
```

## 📊 Dataset

The project uses IPL ball-by-ball CSV data with the following key columns:

- `match_id` - Unique identifier for each match
- `innings` - Innings number (1 or 2)
- `batting_team` - Team batting
- `bowling_team` - Team bowling
- `runs_off_bat` - Runs scored off the bat
- `extras` - Extra runs (wides, no-balls, etc.)
- `is_wicket` - Whether a wicket fell
- `venue` - Match venue
- `city` - City where match was played
- `season` - IPL season year
- `winner` - Winning team

## 🤖 ML Pipeline

### 1. Feature Engineering

**Script**: `backend/preprocessing/feature_engineering.py`

Converts ball-by-ball data to match-level aggregated features:

**Aggregated Features**:
- `total_runs` = runs_off_bat + extras
- `total_wickets` = sum of wickets
- `balls_faced` = count of balls
- `overs_played` = balls_faced / 6
- `run_rate` = total_runs / overs_played
- `extras_total` = sum of extras

**Context Features**:
- Team names (batting_team, bowling_team)
- Venue and city
- Season
- Innings number

**Target**:
- `target` = 1 if batting_team won, else 0

### 2. Model Training

**Script**: `backend/model/train.py`

**Preprocessing Pipeline**:
```python
ColumnTransformer([
    ('cat', OneHotEncoder, ['batting_team', 'bowling_team', 'venue', 'city']),
    ('num', StandardScaler, ['total_runs', 'total_wickets', 'run_rate', 
                             'extras_total', 'overs_played'])
])
```

**Model**: RandomForestClassifier
- n_estimators: 300
- max_depth: 20
- min_samples_split: 10
- min_samples_leaf: 5
- random_state: 42

**Training/Test Split**: 80/20 with stratification

**Evaluation Metrics**:
- Accuracy
- Precision
- Recall
- Confusion Matrix

### 3. Model Inference

**Script**: `backend/model/predict.py`

- Loads trained model from `model.pkl`
- Accepts JSON input
- Returns prediction with probabilities

## 📥 Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**:
```powershell
cd backend
```

2. **Create virtual environment** (recommended):
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. **Install Python dependencies**:
```powershell
pip install flask flask-cors scikit-learn pandas numpy joblib
```

4. **Train the model** (first time only):
```powershell
cd model
python train.py
```

This will:
- Load and process `Data/Raw/IPL.csv`
- Train the RandomForest model
- Save `model.pkl` and `model_features.pkl`
- Display performance metrics

5. **Start Flask server**:
```powershell
cd ..
python app.py
```

Server will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**:
```powershell
cd frontend
```

2. **Install npm dependencies**:
```powershell
npm install
```

This will install:
- React
- Axios (for API calls)
- Vite (dev server)
- ESLint

3. **Start development server**:
```powershell
npm run dev
```

Frontend will run on `http://localhost:5173`

## 🚀 Usage

### Training the Model

```powershell
cd backend/model
python train.py
```

**Output**:
- Feature engineering progress
- Training metrics
- Model saved to `model.pkl`

### Running the Backend

```powershell
cd backend
python app.py
```

**Endpoints**:
- `GET /` - API info
- `GET /api/health` - Health check
- `POST /api/predict` - Make prediction

### Running the Frontend

```powershell
cd frontend
npm run dev
```

**Features**:
- Input form with dropdowns for teams, venues, cities
- Numeric inputs for match statistics
- Auto-calculated run rate
- Real-time validation
- Prediction results with confidence scores

### Making Predictions

1. Open `http://localhost:5173` in browser
2. Fill in match details:
   - Batting Team
   - Bowling Team
   - Venue
   - City
   - Total Runs
   - Total Wickets
   - Overs Played
   - Extras
3. Click "Predict Match Outcome"
4. View results with win/loss probabilities

## 📡 API Documentation

### POST /api/predict

**Request**:
```json
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
```

**Response** (Success):
```json
{
  "status": "success",
  "prediction": "Batting Team Wins",
  "win_probability": 0.82,
  "loss_probability": 0.18,
  "confidence": 82.0,
  "input_data": { ... }
}
```

**Response** (Error):
```json
{
  "status": "error",
  "message": "Missing required fields: venue",
  "required_fields": [ ... ]
}
```

**Validation Rules**:
- All fields required
- Numeric fields must be ≥ 0
- `overs_played` must be between 0.1 and 20
- `total_wickets` must be between 0 and 10
- `batting_team` ≠ `bowling_team`

## 📁 Project Structure

```
IPL_Predictor/
│
├── backend/
│   ├── app.py                          # Flask API server
│   │
│   ├── preprocessing/
│   │   └── feature_engineering.py      # Data preprocessing
│   │
│   ├── model/
│   │   ├── train.py                    # Model training script
│   │   ├── predict.py                  # Prediction utility
│   │   ├── model.pkl                   # Trained model (generated)
│   │   └── model_features.pkl          # Feature metadata (generated)
│   │
│   └── Data/
│       ├── Raw/
│       │   └── IPL.csv                 # Original dataset
│       └── Cleaned/
│           └── IPL_features.csv        # Processed features (generated)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                     # Main React component
│   │   ├── App.css                     # App styles
│   │   │
│   │   ├── components/
│   │   │   ├── PredictionForm.jsx      # Prediction form component
│   │   │   └── PredictionForm.css      # Form styles
│   │   │
│   │   └── api/
│   │       └── predict.js              # API utility functions
│   │
│   ├── package.json                    # npm dependencies
│   └── vite.config.js                  # Vite configuration
│
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## 🔧 Dependencies

### Backend (Python)
```
flask>=2.3.0
flask-cors>=4.0.0
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
joblib>=1.3.0
```

### Frontend (npm)
```json
{
  "dependencies": {
    "react": "^19.2.0",
    "react-dom": "^19.2.0",
    "axios": "^1.6.0"
  }
}
```

## 🎨 Frontend Features

- **Dropdowns**: Pre-populated with IPL teams, venues, and cities
- **Auto-calculation**: Run rate calculated automatically
- **Validation**: Real-time form validation with error messages
- **Responsive**: Mobile-friendly design
- **Animations**: Smooth transitions and loading states
- **Error Handling**: User-friendly error messages

## 🧪 Testing the API

### Using cURL

```powershell
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

### Using Python

```python
import requests

url = "http://localhost:5000/api/predict"
data = {
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

response = requests.post(url, json=data)
print(response.json())
```

## 🚀 Future Improvements

### Model Enhancements
- [ ] Add XGBoost/LightGBM models
- [ ] Hyperparameter tuning with GridSearchCV
- [ ] Feature importance analysis
- [ ] Player-level statistics
- [ ] Weather data integration
- [ ] Head-to-head team statistics

### Application Features
- [ ] User authentication
- [ ] Prediction history
- [ ] Model performance dashboard
- [ ] Real-time match updates
- [ ] Mobile app version
- [ ] Batch prediction upload

### Technical Improvements
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] API rate limiting
- [ ] Caching layer (Redis)
- [ ] Database integration (PostgreSQL)
- [ ] Logging and monitoring
- [ ] Unit and integration tests
- [ ] API documentation (Swagger)

### Data Enhancements
- [ ] Live data scraping
- [ ] Data augmentation
- [ ] Feature engineering automation
- [ ] Time-series analysis
- [ ] Player form tracking

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Authors

IPL Match Predictor Team

## 🙏 Acknowledgments

- IPL data source
- Scikit-Learn documentation
- Flask documentation
- React documentation

---

**Built with ❤️ using Flask, Scikit-Learn, and React**