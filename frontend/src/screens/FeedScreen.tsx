import React, { useEffect, useState, useContext } from 'react';
import { View, FlatList } from 'react-native';
import AuthContext from '../context/AuthContext';
import { fetchPosts } from '../api/feed';
import FeedCard from '../components/FeedCard';

export default function FeedScreen() {
  const { userId } = useContext(AuthContext);
  const [posts, setPosts] = useState<any[]>([]);

  useEffect(() => {
    const load = async () => {
      if (!userId) return;
      const data = await fetchPosts(userId);
      setPosts(data);
    };
    load();
  }, [userId]);

  return (
    <View style={{ flex: 1, padding: 16 }}>
      <FlatList
        data={posts}
        keyExtractor={(item) => item.post_id.toString()}
        renderItem={({ item }) => (
          <FeedCard
            caption={item.caption}
            imageUrl={item.image_url}
            timestamp={item.created_at}
          />
        )}
      />
    </View>
  );
}
