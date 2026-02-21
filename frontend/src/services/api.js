import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

export const setAuthToken = (token) => {
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete axios.defaults.headers.common['Authorization'];
    delete apiClient.defaults.headers.common['Authorization'];
  }
};

// Initialize token from localStorage to prevent race conditions on page reload
const initialToken = localStorage.getItem('token');
if (initialToken) {
  setAuthToken(initialToken);
}

export const uploadItem = async (file, category, style = 'casual', gender = 'male') => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('category', category);
    formData.append('style', style);
    formData.append('gender', gender);

    const response = await apiClient.post(`/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Upload failed' };
  }
};

export const getRecommendations = async (occasion, gender = 'male') => {
  try {
    const formData = new FormData();
    formData.append('occasion', occasion);
    formData.append('gender', gender);

    const response = await axios.post(`${API_BASE_URL}/recommend`, formData);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to get recommendations' };
  }
};

export const sendFeedback = async (feedbackData) => {
  try {
    const response = await apiClient.post('/feedback', feedbackData);
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

// Wardrobe endpoints
export const getWardrobe = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/wardrobe`);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to get wardrobe' };
  }
};

export const getWardrobeByCategory = async (category) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/wardrobe/${category}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: `Failed to get ${category} items` };
  }
};

export const getWardrobeStats = async () => {
  try {
    const response = await apiClient.get(`/stats`);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to get wardrobe stats' };
  }
};

export const deleteWardrobeItem = async (itemId) => {
  try {
    const response = await apiClient.delete(`/wardrobe/${itemId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to delete item' };
  }
};

// Authentication
export const registerUser = async ({ full_name, email, password }) => {
  try {
    const response = await apiClient.post('/auth/register', { full_name, email, password });
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Registration failed' };
  }
};

export const loginUser = async (email, password) => {
  try {
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);

    const response = await apiClient.post('/auth/login', params.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });

    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Login failed' };
  }
};

export const getMe = async () => {
  try {
    const response = await apiClient.get('/auth/me');
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to fetch user' };
  }
};

export const logoutUser = async () => {
  try {
    const response = await apiClient.post('/auth/logout');
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Logout failed' };
  }
};

