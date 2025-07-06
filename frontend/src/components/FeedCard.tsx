import React from 'react';
import { View, Text, Image, StyleSheet } from 'react-native';

interface Props {
  caption: string;
  imageUrl: string;
  timestamp?: string;
}

export default function FeedCard({ caption, imageUrl, timestamp }: Props) {
  return (
    <View style={styles.card}>
      <Image source={{ uri: imageUrl }} style={styles.image} />
      {timestamp && (
        <Text style={styles.time}>{new Date(timestamp).toLocaleString()}</Text>
      )}
      <Text style={styles.caption}>{caption}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: { marginBottom: 16 },
  image: { width: '100%', height: 200 },
  time: { marginTop: 4, color: '#666' },
  caption: { marginTop: 8, fontSize: 16 },
});
