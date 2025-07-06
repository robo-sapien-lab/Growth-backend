import api from './client';

export async function createSchool(name: string, code: string) {
  await api.post('/school/create', { name, code });
}
