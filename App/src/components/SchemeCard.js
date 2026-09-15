import React, { useState } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { schemeCardStyles as styles } from '../constants/schemeStyles';
import { SchemeDetailsModal } from './SchemeDetailsModal';

export const SchemeCard = ({ scheme }) => {
  const [modalVisible, setModalVisible] = useState(false);

  return (
    <View style={styles.card}>
      <View style={styles.header}>
        <Text style={styles.title} numberOfLines={2}>
          {scheme.scheme_name}
        </Text>
        {scheme.level && (
          <View style={styles.badge}>
            <Text style={styles.badgeText}>{scheme.level.toUpperCase()}</Text>
          </View>
        )}
      </View>

      <View style={styles.content}>
        <Text style={styles.department} numberOfLines={1}>
          {scheme.department || 'Govt of India'}
        </Text>
        
        <Text style={styles.description} numberOfLines={3}>
          {scheme.brief_description}
        </Text>

        <TouchableOpacity 
          onPress={() => setModalVisible(true)} 
          style={{ 
            marginTop: 12, 
            paddingVertical: 8, 
            paddingHorizontal: 16, 
            backgroundColor: '#128C7E', 
            borderRadius: 8, 
            alignSelf: 'flex-start' 
          }}
        >
          <Text style={{ color: '#fff', fontWeight: 'bold', fontSize: 13 }}>
            View Details
          </Text>
        </TouchableOpacity>
      </View>

      <SchemeDetailsModal 
        visible={modalVisible} 
        onClose={() => setModalVisible(false)} 
        schemeId={scheme.id || scheme.slug} 
      />
    </View>
  );
};
