import api from './client';

export async function askDoubt(token: string, question: string) {
  const res = await api.post(
    '/doubt/ask',
    { question },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return res.data;
}
