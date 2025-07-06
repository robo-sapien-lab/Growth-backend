import React, { useEffect, useState } from 'react';
import { View, Text, FlatList } from 'react-native';
import { fetchLeaderboard } from '../api/leaderboard';

export default function LeaderboardScreen({ route }: any) {
  const { schoolId } = route.params;
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const load = async () => {
      const res = await fetchLeaderboard(schoolId);
      setData(res);
    };
    load();
  }, [schoolId]);

  if (!data) return null;

  return (
    <View style={{ flex: 1, padding: 16 }}>
      <Text style={{ fontSize: 20, marginBottom: 12 }}>Top Contributors</Text>
      <FlatList
        data={data.top_contributors}
        keyExtractor={(item) => item.user_id.toString()}
        renderItem={({ item }) => (
          <Text>{item.name} - Posts: {item.post_count}</Text>
        )}
      />
    </View>
  );
}
