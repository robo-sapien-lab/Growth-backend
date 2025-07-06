import axios from 'axios';

const api = axios.create({ baseURL: 'http://localhost:8000' });

export async function signup(data: {
  name: string;
  email: string;
  password: string;
  grade: string;
  school_code: string;
}) {
  await api.post('/auth/signup', data);
}

export async function login(email: string, password: string) {
  const res = await api.post('/auth/login', { email, password });
  return res.data.access_token as string;
}
