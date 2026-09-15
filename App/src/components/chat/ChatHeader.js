import React from 'react';
import { View, Text, TouchableOpacity, Image } from 'react-native';
import { ArrowLeft, BadgeCheck, MoreVertical } from 'lucide-react-native';
import { styles } from '../../constants/styles';

export const ChatHeader = ({ chat, goBack, openProfile }) => {
  return (
    <View style={styles.header}>
      <TouchableOpacity
        style={styles.headerLeft}
        activeOpacity={0.7}
        onPress={openProfile}
      >
        <TouchableOpacity style={styles.backButton} onPress={goBack}>
          <ArrowLeft size={24} color="#fff" />
        </TouchableOpacity>
        {chat.avatar ? (
          <Image source={chat.avatar} style={styles.avatarImage} />
        ) : (
          <View style={[styles.avatarImage, { backgroundColor: '#ccc', justifyContent: 'center', alignItems: 'center' }]}>
            <Text style={{ fontSize: 18, color: '#fff' }}>{chat.name.charAt(0)}</Text>
          </View>
        )}
        <View style={styles.headerTitleContainer}>
          <View style={{ flexDirection: 'row', alignItems: 'center' }}>
            <Text style={styles.headerName}>{chat.name}</Text>
            {chat.isOfficial && <BadgeCheck size={16} color="#53BDEB" style={{ marginLeft: 4 }} fill="#fff" />}
          </View>
          <Text style={styles.headerStatus}>{chat.status}</Text>
        </View>
      </TouchableOpacity>
      <View style={styles.headerRight}>
        <TouchableOpacity style={styles.iconButton}>
          <MoreVertical size={22} color="#fff" />
        </TouchableOpacity>
      </View>
    </View>
  );
};
