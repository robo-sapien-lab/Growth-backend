import React, { useEffect, useState } from 'react';
import { View, FlatList } from 'react-native';
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
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => <StoryCircle avatarUrl={item.avatar_url} />}
      />
    </View>
  );
}
