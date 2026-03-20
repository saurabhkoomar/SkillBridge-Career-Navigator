/**
 * API client for Skill-Bridge Career Navigator backend.
 */
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || error.message || 'Something went wrong';
    console.error('API Error:', message);
    return Promise.reject(error);
  }
);

export const healthCheck = () => api.get('/health');
export const getProfiles = (search) => api.get('/profiles', { params: { search } });
export const getProfile = (id) => api.get(`/profiles/${id}`);
export const createProfile = (data) => api.post('/profiles', data);
export const updateProfile = (id, data) => api.put(`/profiles/${id}`, data);
export const deleteProfile = (id) => api.delete(`/profiles/${id}`);
export const analyzeSkills = (data) => api.post('/analysis/analyze', data);
export const getSampleAnalysis = (resumeId, roleId) => api.get(`/analysis/sample/${resumeId}/${roleId}`);
export const getRoles = (filters = {}) => api.get('/roles', { params: filters });
export const getRole = (id) => api.get(`/roles/${id}`);
export const getCourses = (filters = {}) => api.get('/courses', { params: filters });
export const getRecommendedCourses = (skills) =>
  api.get('/courses/recommend', { params: { skills: skills.join(',') } });
export const getSampleResumes = () => api.get('/data/resumes');
