import React, { useState, useContext } from 'react';
import { View, TextInput, Button, Text, StyleSheet } from 'react-native';
import AuthContext from '../context/AuthContext';
import { askDoubt } from '../api/doubt';

export default function AskDoubtScreen() {
  const { token } = useContext(AuthContext);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const handleAsk = async () => {
    if (!token) return;
    const data = await askDoubt(token, question);
    setAnswer(data.answer);
  };

  return (
    <View style={styles.container}>
      <TextInput
        placeholder="Ask a question"
        value={question}
        onChangeText={setQuestion}
        style={styles.input}
      />
      <Button title="Ask" onPress={handleAsk} />
      <Text>{answer}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 8,
    marginBottom: 12,
  },
});
