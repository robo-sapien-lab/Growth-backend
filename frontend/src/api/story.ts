import axios from 'axios';

const api = axios.create({ baseURL: 'http://localhost:8000' });

export async function postStory(token: string, data: FormData) {
  const res = await api.post('/story/post', data, {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'multipart/form-data',
    },
  });
  return res.data;
}

export async function fetchAllStories() {
  const res = await api.get('/story/active/all');
  return res.data;
}
