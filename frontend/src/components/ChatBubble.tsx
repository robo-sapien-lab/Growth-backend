import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface Props {
  message: string;
  isMe: boolean;
}

export default function ChatBubble({ message, isMe }: Props) {
  return (
    <View style={[styles.bubble, isMe ? styles.me : styles.them]}>
      <Text style={styles.text}>{message}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  bubble: {
    padding: 10,
    borderRadius: 8,
    marginVertical: 4,
    maxWidth: '70%',
  },
  me: {
    backgroundColor: '#dcf8c6',
    alignSelf: 'flex-end',
  },
  them: {
    backgroundColor: '#f0f0f0',
    alignSelf: 'flex-start',
  },
  text: { fontSize: 16 },
});
