import api from './client';

export async function uploadImage(userId: number, caption: string, uri: string) {
  const form = new FormData();
  form.append('user_id', String(userId));
  form.append('caption', caption);
  // @ts-ignore
  form.append('image', { uri, name: 'image.jpg', type: 'image/jpeg' });

  const res = await api.post('/feed/upload-image', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
}

export async function fetchPosts(userId: number) {
  const res = await api.get('/feed/all', { params: { user_id: userId } });
  return res.data.posts as any[];
}

export async function reactToPost(postId: number, userId: number, emoji: string) {
  await api.post('/feed/react', { post_id: postId, user_id: userId, emoji });
}

export async function commentOnPost(postId: number, userId: number, comment: string) {
  await api.post('/feed/comment', { post_id: postId, user_id: userId, comment });
}
