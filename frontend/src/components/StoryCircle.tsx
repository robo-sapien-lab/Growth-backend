import React from 'react';
import { View, Image, StyleSheet } from 'react-native';

interface Props {
  avatarUrl: string;
}

export default function StoryCircle({ avatarUrl }: Props) {
  return (
    <View style={styles.circle}>
      <Image source={{ uri: avatarUrl }} style={styles.avatar} />
    </View>
  );
}

const styles = StyleSheet.create({
  circle: {
    width: 60,
    height: 60,
    borderRadius: 30,
    overflow: 'hidden',
    marginHorizontal: 8,
  },
  avatar: { width: '100%', height: '100%' },
});
