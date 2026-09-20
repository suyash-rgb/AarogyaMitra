import React from 'react';
import { View, Text } from 'react-native';

export const Toast = ({ text }) => {
  if (!text) return null;

  return (
    <View style={{
      position: 'absolute',
      bottom: 90,
      alignSelf: 'center',
      backgroundColor: '#202C33',
      paddingHorizontal: 16,
      paddingVertical: 10,
      borderRadius: 20,
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.3,
      shadowRadius: 4,
      elevation: 5,
      zIndex: 999
    }}>
      <Text style={{ color: '#E9EDEF', fontSize: 13, fontWeight: '600' }}>{text}</Text>
    </View>
  );
};
