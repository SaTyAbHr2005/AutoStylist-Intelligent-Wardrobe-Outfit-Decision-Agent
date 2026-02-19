import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export const uploadItem = async (file, category, style = 'casual') => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('category', category);
    formData.append('style', style);

    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Upload failed' };
  }
};

export const getRecommendations = async (occasion) => {
  try {
    const formData = new FormData();
    formData.append('occasion', occasion);

    const response = await axios.post(`${API_BASE_URL}/recommend`, formData);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to get recommendations' };
  }
};

export const sendFeedback = async (feedback) => {
  try {
    const formData = new FormData();
    Object.keys(feedback).forEach((key) => {
      formData.append(key, feedback[key]);
    });

    const response = await axios.post(`${API_BASE_URL}/feedback`, formData);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to send feedback' };
  }
};

export const getContext = async (occasion) => {
  try {
    const formData = new FormData();
    formData.append('occasion', occasion);

    const response = await axios.post(`${API_BASE_URL}/context`, formData);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to get context' };
  }
};
