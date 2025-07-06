import React, { useEffect, useState } from 'react';
import { View, FlatList, Text } from 'react-native';
import { fetchAllStories } from '../api/story';
import StoryCircle from '../components/StoryCircle';

export default function StoryViewer() {
  const [stories, setStories] = useState<any[]>([]);

  useEffect(() => {
    const load = async () => {
      const data = await fetchAllStories();
      setStories(data);
    };
    load();
  }, []);

  return (
    <View style={{ padding: 16 }}>
      <FlatList
        horizontal
        data={stories}
        keyExtractor={(item) => item.user}
        renderItem={({ item }) => (
          <View style={{ alignItems: 'center' }}>
            <StoryCircle avatarUrl={''} />
            <Text>{item.user}</Text>
          </View>
        )}
      />
    </View>
  );
}
