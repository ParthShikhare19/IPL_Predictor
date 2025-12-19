/**
 * PredictionForm Component
 * Form for inputting match data and getting predictions
 */

import { useState, useEffect } from 'react';
import './PredictionForm.css';

// IPL teams
const IPL_TEAMS = [
  'Mumbai Indians',
  'Chennai Super Kings',
  'Royal Challengers Bangalore',
  'Kolkata Knight Riders',
  'Delhi Capitals',
  'Punjab Kings',
  'Rajasthan Royals',
  'Sunrisers Hyderabad',
  'Gujarat Titans',
  'Lucknow Super Giants'
];

// Popular venues
const VENUES = [
  'Wankhede Stadium',
  'M. A. Chidambaram Stadium',
  'Eden Gardens',
  'Feroz Shah Kotla',
  'M. Chinnaswamy Stadium',
  'Rajiv Gandhi International Stadium',
  'Punjab Cricket Association Stadium',
  'Sawai Mansingh Stadium',
  'Arun Jaitley Stadium',
  'Narendra Modi Stadium'
];

// Cities
const CITIES = [
  'Mumbai',
  'Chennai',
  'Bangalore',
  'Kolkata',
  'Delhi',
  'Hyderabad',
  'Mohali',
  'Jaipur',
  'Ahmedabad',
  'Lucknow',
  'Pune',
  'Indore',
  'Dharamsala'
];

const PredictionForm = ({ onPrediction, loading }) => {
  const [formData, setFormData] = useState({
    batting_team: '',
    bowling_team: '',
    venue: '',
    city: '',
    total_runs: '',
    total_wickets: '',
    overs_played: '',
    extras_total: '',
    run_rate: ''
  });

  const [errors, setErrors] = useState({});

  // Auto-calculate run rate when total_runs or overs_played changes
  useEffect(() => {
    if (formData.total_runs && formData.overs_played && parseFloat(formData.overs_played) > 0) {
      const runRate = (parseFloat(formData.total_runs) / parseFloat(formData.overs_played)).toFixed(2);
      setFormData(prev => ({ ...prev, run_rate: runRate }));
    }
  }, [formData.total_runs, formData.overs_played]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Required fields
    if (!formData.batting_team) newErrors.batting_team = 'Batting team is required';
    if (!formData.bowling_team) newErrors.bowling_team = 'Bowling team is required';
    if (!formData.venue) newErrors.venue = 'Venue is required';
    if (!formData.city) newErrors.city = 'City is required';
    if (!formData.total_runs) newErrors.total_runs = 'Total runs is required';
    if (!formData.total_wickets) newErrors.total_wickets = 'Total wickets is required';
    if (!formData.overs_played) newErrors.overs_played = 'Overs played is required';
    if (!formData.extras_total) newErrors.extras_total = 'Extras is required';

    // Same team validation
    if (formData.batting_team && formData.bowling_team && formData.batting_team === formData.bowling_team) {
      newErrors.bowling_team = 'Bowling team must be different from batting team';
    }

    // Numeric validations
    const totalRuns = parseFloat(formData.total_runs);
    if (formData.total_runs && (isNaN(totalRuns) || totalRuns < 0)) {
      newErrors.total_runs = 'Must be a positive number';
    }

    const totalWickets = parseInt(formData.total_wickets);
    if (formData.total_wickets && (isNaN(totalWickets) || totalWickets < 0 || totalWickets > 10)) {
      newErrors.total_wickets = 'Must be between 0 and 10';
    }

    const oversPlayed = parseFloat(formData.overs_played);
    if (formData.overs_played && (isNaN(oversPlayed) || oversPlayed <= 0 || oversPlayed > 20)) {
      newErrors.overs_played = 'Must be between 0.1 and 20';
    }

    const extrasTotal = parseFloat(formData.extras_total);
    if (formData.extras_total && (isNaN(extrasTotal) || extrasTotal < 0)) {
      newErrors.extras_total = 'Must be a positive number';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      // Convert numeric fields to numbers
      const submissionData = {
        ...formData,
        total_runs: parseFloat(formData.total_runs),
        total_wickets: parseInt(formData.total_wickets),
        overs_played: parseFloat(formData.overs_played),
        extras_total: parseFloat(formData.extras_total),
        run_rate: parseFloat(formData.run_rate)
      };
      
      onPrediction(submissionData);
    }
  };

  const handleReset = () => {
    setFormData({
      batting_team: '',
      bowling_team: '',
      venue: '',
      city: '',
      total_runs: '',
      total_wickets: '',
      overs_played: '',
      extras_total: '',
      run_rate: ''
    });
    setErrors({});
  };

  return (
    <form className="prediction-form" onSubmit={handleSubmit}>
      <div className="form-grid">
        {/* Team Selection */}
        <div className="form-group">
          <label htmlFor="batting_team">Batting Team *</label>
          <select
            id="batting_team"
            name="batting_team"
            value={formData.batting_team}
            onChange={handleChange}
            className={errors.batting_team ? 'error' : ''}
          >
            <option value="">Select batting team</option>
            {IPL_TEAMS.map(team => (
              <option key={team} value={team}>{team}</option>
            ))}
          </select>
          {errors.batting_team && <span className="error-message">{errors.batting_team}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="bowling_team">Bowling Team *</label>
          <select
            id="bowling_team"
            name="bowling_team"
            value={formData.bowling_team}
            onChange={handleChange}
            className={errors.bowling_team ? 'error' : ''}
          >
            <option value="">Select bowling team</option>
            {IPL_TEAMS.map(team => (
              <option key={team} value={team}>{team}</option>
            ))}
          </select>
          {errors.bowling_team && <span className="error-message">{errors.bowling_team}</span>}
        </div>

        {/* Venue & City */}
        <div className="form-group">
          <label htmlFor="venue">Venue *</label>
          <select
            id="venue"
            name="venue"
            value={formData.venue}
            onChange={handleChange}
            className={errors.venue ? 'error' : ''}
          >
            <option value="">Select venue</option>
            {VENUES.map(venue => (
              <option key={venue} value={venue}>{venue}</option>
            ))}
          </select>
          {errors.venue && <span className="error-message">{errors.venue}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="city">City *</label>
          <select
            id="city"
            name="city"
            value={formData.city}
            onChange={handleChange}
            className={errors.city ? 'error' : ''}
          >
            <option value="">Select city</option>
            {CITIES.map(city => (
              <option key={city} value={city}>{city}</option>
            ))}
          </select>
          {errors.city && <span className="error-message">{errors.city}</span>}
        </div>

        {/* Match Statistics */}
        <div className="form-group">
          <label htmlFor="total_runs">Total Runs *</label>
          <input
            type="number"
            id="total_runs"
            name="total_runs"
            value={formData.total_runs}
            onChange={handleChange}
            placeholder="e.g., 180"
            min="0"
            className={errors.total_runs ? 'error' : ''}
          />
          {errors.total_runs && <span className="error-message">{errors.total_runs}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="total_wickets">Total Wickets *</label>
          <input
            type="number"
            id="total_wickets"
            name="total_wickets"
            value={formData.total_wickets}
            onChange={handleChange}
            placeholder="e.g., 5"
            min="0"
            max="10"
            className={errors.total_wickets ? 'error' : ''}
          />
          {errors.total_wickets && <span className="error-message">{errors.total_wickets}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="overs_played">Overs Played *</label>
          <input
            type="number"
            id="overs_played"
            name="overs_played"
            value={formData.overs_played}
            onChange={handleChange}
            placeholder="e.g., 20.0"
            step="0.1"
            min="0.1"
            max="20"
            className={errors.overs_played ? 'error' : ''}
          />
          {errors.overs_played && <span className="error-message">{errors.overs_played}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="extras_total">Extras *</label>
          <input
            type="number"
            id="extras_total"
            name="extras_total"
            value={formData.extras_total}
            onChange={handleChange}
            placeholder="e.g., 12"
            min="0"
            className={errors.extras_total ? 'error' : ''}
          />
          {errors.extras_total && <span className="error-message">{errors.extras_total}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="run_rate">Run Rate (Auto-calculated)</label>
          <input
            type="number"
            id="run_rate"
            name="run_rate"
            value={formData.run_rate}
            readOnly
            placeholder="Auto-calculated"
            className="readonly"
          />
          <span className="help-text">Calculated as: Total Runs / Overs Played</span>
        </div>
      </div>

      <div className="form-actions">
        <button type="button" onClick={handleReset} className="btn-secondary" disabled={loading}>
          Reset
        </button>
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Predicting...' : 'Predict Match Outcome'}
        </button>
      </div>
    </form>
  );
};

export default PredictionForm;
