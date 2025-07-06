import api from './client';

export async function fetchLeaderboard(schoolId: number) {
  const res = await api.get(`/leaderboard/leaderboard/${schoolId}`);
  return res.data;
}
