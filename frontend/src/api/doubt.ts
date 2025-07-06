import axios from 'axios';

const api = axios.create({ baseURL: 'http://localhost:8000' });

export async function askDoubt(token: string, question: string) {
  const res = await api.post(
    '/doubt/ask',
    { question },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return res.data;
}
