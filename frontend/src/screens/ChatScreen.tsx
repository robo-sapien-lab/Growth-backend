import React, { useState, useEffect } from 'react';
import { View, TextInput, Button, FlatList } from 'react-native';
import ChatBubble from '../components/ChatBubble';

export default function ChatScreen({ route }: any) {
  const { user1, user2 } = route.params;
  const [messages, setMessages] = useState<any[]>([]);
  const [text, setText] = useState('');

  useEffect(() => {
    const load = async () => {
      const res = await fetch(`http://localhost:8000/chat/history/${user1}/${user2}`);
      setMessages(await res.json());
    };
    load();
  }, [user1, user2]);

  const send = async () => {
    await fetch('http://localhost:8000/chat/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sender_id: user1, receiver_id: user2, message: text }),
    });
    setText('');
    const res = await fetch(`http://localhost:8000/chat/history/${user1}/${user2}`);
    setMessages(await res.json());
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
