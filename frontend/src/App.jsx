import { useState } from 'react';
import PredictionForm from './components/PredictionForm';
import { makePrediction } from './api/predict';
import './App.css';

function App() {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePrediction = async (formData) => {
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const result = await makePrediction(formData);
      setPrediction(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleNewPrediction = () => {
    setPrediction(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🏏 IPL Match Predictor</h1>
          <p className="subtitle">Predict match outcomes using Machine Learning</p>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          {/* Info Banner */}
          <div className="info-banner">
            <h3>How it works</h3>
            <p>
              Enter the match details below to predict whether the batting team will win or lose.
              Our ML model analyzes team performance, venue statistics, and match conditions to provide accurate predictions.
            </p>
          </div>

          {/* Prediction Form */}
          <PredictionForm onPrediction={handlePrediction} loading={loading} />

          {/* Error Display */}
          {error && (
            <div className="result-card error-card">
              <div className="error-icon">⚠️</div>
              <h2>Prediction Failed</h2>
              <p className="error-message">{error}</p>
              <button onClick={handleNewPrediction} className="btn-retry">
                Try Again
              </button>
            </div>
          )}

          {/* Prediction Result */}
          {prediction && (
            <div className="result-card success-card">
              <div className="result-header">
                <h2>Prediction Result</h2>
                <span className="confidence-badge">
                  {prediction.confidence}% Confidence
                </span>
              </div>

              <div className="prediction-outcome">
                <div className={`outcome-icon ${prediction.prediction === 'Batting Team Wins' ? 'win' : 'loss'}`}>
                  {prediction.prediction === 'Batting Team Wins' ? '🎉' : '😔'}
                </div>
                <h3 className="prediction-text">{prediction.prediction}</h3>
              </div>

              <div className="probability-section">
                <div className="probability-item">
                  <span className="probability-label">Win Probability</span>
                  <div className="probability-bar-container">
                    <div 
                      className="probability-bar win" 
                      style={{ width: `${prediction.win_probability * 100}%` }}
                    ></div>
                  </div>
                  <span className="probability-value">
                    {(prediction.win_probability * 100).toFixed(2)}%
                  </span>
                </div>

                <div className="probability-item">
                  <span className="probability-label">Loss Probability</span>
                  <div className="probability-bar-container">
                    <div 
                      className="probability-bar loss" 
                      style={{ width: `${prediction.loss_probability * 100}%` }}
                    ></div>
                  </div>
                  <span className="probability-value">
                    {(prediction.loss_probability * 100).toFixed(2)}%
                  </span>
                </div>
              </div>

              <div className="input-summary">
                <h4>Match Details</h4>
                <div className="summary-grid">
                  <div className="summary-item">
                    <span className="label">Batting Team:</span>
                    <span className="value">{prediction.input_data.batting_team}</span>
                  </div>
                  <div className="summary-item">
                    <span className="label">Bowling Team:</span>
                    <span className="value">{prediction.input_data.bowling_team}</span>
                  </div>
                  <div className="summary-item">
                    <span className="label">Venue:</span>
                    <span className="value">{prediction.input_data.venue}</span>
                  </div>
                  <div className="summary-item">
                    <span className="label">Score:</span>
                    <span className="value">
                      {prediction.input_data.total_runs}/{prediction.input_data.total_wickets} 
                      ({prediction.input_data.overs_played} overs)
                    </span>
                  </div>
                </div>
              </div>

              <button onClick={handleNewPrediction} className="btn-new-prediction">
                Make Another Prediction
              </button>
            </div>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>Built with Flask + Scikit-Learn + React | IPL Match Prediction System</p>
      </footer>
    </div>
  );
}

export default App;
