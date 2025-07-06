import api from './client';

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
  const obj = res.data.active_stories as Record<string, any[]>;
  return Object.keys(obj).map((user) => ({ user, stories: obj[user] }));
}
