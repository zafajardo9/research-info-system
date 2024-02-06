import axios from 'axios';

export const risApi = axios.create({
  baseURL: process.env.RIS_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
