import api from './client';

export async function getMe(token: string) {
  const res = await api.get('/user/me', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}

export async function uploadAvatar(token: string, fileUri: string) {
  const form = new FormData();
  // @ts-ignore
  form.append('file', { uri: fileUri, name: 'avatar.jpg', type: 'image/jpeg' });
  const res = await api.post('/user/upload-avatar', form, {
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
}
