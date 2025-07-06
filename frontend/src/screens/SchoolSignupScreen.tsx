import React, { useState } from 'react';
import { View, TextInput, Button, StyleSheet } from 'react-native';
import { createSchool } from '../api/school';

export default function SchoolSignupScreen() {
  const [name, setName] = useState('');
  const [code, setCode] = useState('');

  const handleCreate = async () => {
    await createSchool(name, code);
    setName('');
    setCode('');
  };

  return (
    <View style={styles.container}>
      <TextInput placeholder="School Name" value={name} onChangeText={setName} style={styles.input} />
      <TextInput placeholder="School Code" value={code} onChangeText={setCode} style={styles.input} />
      <Button title="Create" onPress={handleCreate} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 16 },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 8, marginBottom: 12 },
});
