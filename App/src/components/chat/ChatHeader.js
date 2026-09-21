import React from 'react';
import { View, Text, TouchableOpacity, Image } from 'react-native';
import { ArrowLeft, BadgeCheck, MoreVertical } from 'lucide-react-native';
import { useStyles } from '../../constants/styles';
import { useTheme } from '../../context/ThemeContext';

export const ChatHeader = ({ chat, goBack, openProfile }) => {
  const styles = useStyles();
  const { colors } = useTheme();
  return (
    <View style={styles.header}>
      <TouchableOpacity
        style={styles.headerLeft}
        activeOpacity={0.7}
        onPress={openProfile}
      >
        <TouchableOpacity style={styles.backButton} onPress={goBack}>
          <ArrowLeft size={24} color={colors.textInverse} />
        </TouchableOpacity>
        {chat.avatar ? (
          <Image source={chat.avatar} style={styles.avatarImage} />
        ) : (
          <View style={[styles.avatarImage, { backgroundColor: colors.border, justifyContent: 'center', alignItems: 'center' }]}>
            <Text style={{ fontSize: 18, color: colors.textInverse }}>{chat.name.charAt(0)}</Text>
          </View>
        )}
        <View style={styles.headerTitleContainer}>
          <View style={{ flexDirection: 'row', alignItems: 'center' }}>
            <Text style={styles.headerName}>{chat.name}</Text>
            {chat.isOfficial && <BadgeCheck size={16} color="#53BDEB" style={{ marginLeft: 4 }} fill={colors.headerBg} />}
          </View>
          <Text style={styles.headerStatus}>{chat.status}</Text>
        </View>
      </TouchableOpacity>
      <View style={styles.headerRight}>
        <TouchableOpacity style={styles.iconButton}>
          <MoreVertical size={22} color={colors.textInverse} />
        </TouchableOpacity>
      </View>
    </View>
  );
};
