import React, { useState } from 'react';
import { View, Text, TouchableOpacity, FlatList, Image, Modal, TouchableWithoutFeedback } from 'react-native';
import { Search, MoreVertical, Camera, BadgeCheck } from 'lucide-react-native';
import { useStyles } from '../constants/styles';
import { useTheme } from '../context/ThemeContext';

export default function ChatListScreen({ chats, onSelectChat, openSettings }) {
  const styles = useStyles();
  const { colors } = useTheme();
  const [showDropdown, setShowDropdown] = useState(false);

  const renderItem = ({ item }) => {
    const lastMessage = item.messages.length > 0 ? item.messages[item.messages.length - 1] : null;

    return (
      <TouchableOpacity style={styles.chatListItem} onPress={() => onSelectChat(item)}>
        {item.avatar ? (
          <Image source={item.avatar} style={styles.chatListAvatar} />
        ) : (
          <View style={[styles.chatListAvatar, { backgroundColor: item.isMetaAI ? '#25D366' : colors.border, justifyContent: 'center', alignItems: 'center' }]}>
            {item.isMetaAI ? (
               <Text style={{ fontSize: 24 }}>🤖</Text>
            ) : (
               <Text style={{ fontSize: 20, color: colors.textInverse }}>{item.name.charAt(0)}</Text>
            )}
          </View>
        )}
        
        <View style={styles.chatListDetails}>
          <View style={{ flex: 1 }}>
            <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 4 }}>
              <Text style={styles.chatListName} numberOfLines={1}>{item.name}</Text>
              {item.isOfficial && <BadgeCheck size={14} color="#53BDEB" style={{ marginLeft: 4 }} fill={colors.surface} />}
            </View>
            {lastMessage && (
              <Text style={styles.chatListLastMessage} numberOfLines={1}>
                {lastMessage.type === 'audio' ? '🎵 Audio message' : 
                 lastMessage.type === 'image' ? '📷 Photo' : 
                 lastMessage.type === 'document' ? '📄 Document' : 
                 lastMessage.text}
              </Text>
            )}
          </View>

          <View style={{ alignItems: 'flex-end', justifyContent: 'center', marginLeft: 8 }}>
            {lastMessage && (
              <Text style={[styles.chatListTime, item.unreadCount > 0 && { color: '#00A884', fontWeight: 'bold' }]}>
                {lastMessage.time}
              </Text>
            )}
            {item.unreadCount > 0 && (
              <View style={styles.unreadBadge}>
                <Text style={styles.unreadBadgeText}>{item.unreadCount}</Text>
              </View>
            )}
          </View>
        </View>
      </TouchableOpacity>
    );
  };

  return (
    <View style={styles.container}>
      {/* WhatsApp Home Header */}
      <View style={styles.homeHeader}>
        <Text style={styles.homeTitle}>WhatsApp</Text>
        <View style={styles.homeIcons}>
          <TouchableOpacity style={styles.iconButton}>
            <Camera size={24} color={colors.textInverse} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.iconButton}>
            <Search size={24} color={colors.textInverse} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.iconButton} onPress={() => setShowDropdown(true)}>
            <MoreVertical size={24} color={colors.textInverse} />
          </TouchableOpacity>
        </View>
      </View>

      <Modal visible={showDropdown} transparent animationType="fade" onRequestClose={() => setShowDropdown(false)}>
        <TouchableWithoutFeedback onPress={() => setShowDropdown(false)}>
          <View style={{ flex: 1 }}>
            <View style={{ position: 'absolute', top: 50, right: 10, backgroundColor: colors.surface, borderRadius: 8, paddingVertical: 8, elevation: 4, minWidth: 150, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.2, shadowRadius: 4 }}>
              <TouchableOpacity style={{ paddingHorizontal: 16, paddingVertical: 12 }} onPress={() => { setShowDropdown(false); openSettings(); }}>
                <Text style={{ fontSize: 16, color: colors.text }}>Settings</Text>
              </TouchableOpacity>
            </View>
          </View>
        </TouchableWithoutFeedback>
      </Modal>
      
      {/* Tabs */}
      <View style={styles.homeTabs}>
        <View style={[styles.tabItem, styles.activeTab]}>
          <Text style={styles.activeTabText}>Chats</Text>
        </View>
        <View style={styles.tabItem}>
          <Text style={styles.tabText}>Updates</Text>
        </View>
        <View style={styles.tabItem}>
          <Text style={styles.tabText}>Calls</Text>
        </View>
      </View>

      <FlatList
        data={chats}
        keyExtractor={item => item.id}
        renderItem={renderItem}
        contentContainerStyle={styles.chatListContainer}
      />
    </View>
  );
}
