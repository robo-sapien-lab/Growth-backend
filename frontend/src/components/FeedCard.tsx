import React from 'react';
import { View, Text, Image, StyleSheet } from 'react-native';

interface Props {
  caption: string;
  imageUrl: string;
}

export default function FeedCard({ caption, imageUrl }: Props) {
  return (
    <View style={styles.card}>
      <Image source={{ uri: imageUrl }} style={styles.image} />
      <Text style={styles.caption}>{caption}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: { marginBottom: 16 },
  image: { width: '100%', height: 200 },
  caption: { marginTop: 8, fontSize: 16 },
});
