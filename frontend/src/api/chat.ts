import api from './client';

export async function sendMessage(
  senderId: number,
  receiverId: number,
  message: string
) {
  await api.post('/chat/send', { sender_id: senderId, receiver_id: receiverId, message });
}

export async function fetchChatHistory(user1: number, user2: number) {
  const res = await api.get(`/chat/history/${user1}/${user2}`);
  return res.data;
}
