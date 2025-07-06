import React, { useEffect, useState, useContext } from 'react';
import { View, Text, Image, StyleSheet } from 'react-native';
import AuthContext from '../context/AuthContext';

export default function ProfileScreen() {
  const { token } = useContext(AuthContext);
  const [profile, setProfile] = useState<any>(null);

  useEffect(() => {
    const load = async () => {
      if (!token) return;
      const res = await fetch('http://localhost:8000/user/me', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setProfile(await res.json());
    };
    load();
  }, [token]);

  if (!profile) return null;

  return (
    <View style={styles.container}>
      <Image source={{ uri: profile.avatar_url }} style={styles.avatar} />
      <Text style={styles.name}>{profile.name}</Text>
      <Text>{profile.email}</Text>
      <Text>XP: {profile.xp}</Text>
      <Text>Streak: {profile.streak}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', padding: 16 },
  avatar: { width: 120, height: 120, borderRadius: 60, marginBottom: 16 },
  name: { fontSize: 24, fontWeight: 'bold' },
});
