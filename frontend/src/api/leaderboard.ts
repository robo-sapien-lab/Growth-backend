import axios from 'axios';

const api = axios.create({ baseURL: 'http://localhost:8000' });

export async function fetchLeaderboard(schoolId: number) {
  const res = await api.get(`/leaderboard/leaderboard/${schoolId}`);
  return res.data;
}
