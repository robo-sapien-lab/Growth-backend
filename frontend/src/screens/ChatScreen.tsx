import React, { useState, useEffect } from 'react';
import { View, TextInput, Button, FlatList } from 'react-native';
import ChatBubble from '../components/ChatBubble';
import { fetchChatHistory, sendMessage } from '../api/chat';

export default function ChatScreen({ route }: any) {
  const { user1, user2 } = route.params;
  const [messages, setMessages] = useState<any[]>([]);
  const [text, setText] = useState('');

  useEffect(() => {
    const load = async () => {
      const res = await fetchChatHistory(user1, user2);
      setMessages(res);
    };
    load();
  }, [user1, user2]);

  const send = async () => {
    await sendMessage(user1, user2, text);
    setText('');
    const res = await fetchChatHistory(user1, user2);
    setMessages(res);
  };

  return (
    <View style={{ flex: 1, padding: 16 }}>
      <FlatList
        data={messages}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <ChatBubble message={item.message} isMe={item.sender_id === user1} />
        )}
      />
      <TextInput value={text} onChangeText={setText} style={{ borderWidth: 1 }} />
      <Button title="Send" onPress={send} />
    </View>
  );
}
