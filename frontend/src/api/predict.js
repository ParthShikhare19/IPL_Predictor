/**
 * API utility for making prediction requests to Flask backend
 */

import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Make a match prediction
 * @param {Object} predictionData - The match data for prediction
 * @returns {Promise} - API response
 */
export const makePrediction = async (predictionData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/predict`, predictionData, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with error
      throw new Error(error.response.data.message || 'Prediction failed');
    } else if (error.request) {
      // No response received
      throw new Error('Unable to connect to server. Please ensure the Flask backend is running.');
    } else {
      // Other errors
      throw new Error('An unexpected error occurred');
    }
  }
};

/**
 * Check API health
 * @returns {Promise} - Health status
 */
export const checkHealth = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  } catch (error) {
    throw new Error('Unable to connect to server');
  }
};
