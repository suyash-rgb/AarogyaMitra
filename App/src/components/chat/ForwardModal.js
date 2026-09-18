import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Modal, ScrollView, Image } from 'react-native';
import { X, Send, CornerUpRight, BadgeCheck } from 'lucide-react-native';
import { styles } from '../../constants/styles';

export const ForwardModal = ({ visible, onClose, chats = [], onForward }) => {
  const [selectedChatId, setSelectedChatId] = useState(null);

  const handleSendForward = () => {
    if (!selectedChatId) return;
    const targetChat = chats.find(c => c.id === selectedChatId);
    if (targetChat) {
      onForward(targetChat);
      setSelectedChatId(null);
    }
  };

  return (
    <Modal
      visible={visible}
      transparent={true}
      animationType="slide"
      onRequestClose={onClose}
    >
      <TouchableOpacity
        style={styles.modalOverlay}
        activeOpacity={1}
        onPress={onClose}
      >
        <TouchableOpacity
          activeOpacity={1}
          style={[styles.modalContentContainer, { maxHeight: '75%' }]}
        >
          <View style={styles.modalHeader}>
            <View style={{ flexDirection: 'row', alignItems: 'center' }}>
              <CornerUpRight size={20} color="#00A884" style={{ marginRight: 8 }} />
              <Text style={styles.modalTitle}>Forward message to...</Text>
            </View>
            <TouchableOpacity onPress={onClose}>
              <X size={24} color="#111B21" />
            </TouchableOpacity>
          </View>

          <ScrollView style={{ marginTop: 10 }}>
            {chats.map((chatItem) => {
              const isSelected = selectedChatId === chatItem.id;
              return (
                <TouchableOpacity
                  key={chatItem.id}
                  style={[
                    styles.langOption,
                    isSelected ? { backgroundColor: '#E6F4FE', borderColor: '#00A884' } : null
                  ]}
                  onPress={() => setSelectedChatId(chatItem.id)}
                >
                  <View style={{ flexDirection: 'row', alignItems: 'center', flex: 1 }}>
                    {chatItem.avatar ? (
                      <Image source={chatItem.avatar} style={{ width: 40, height: 40, borderRadius: 20, marginRight: 12 }} />
                    ) : (
                      <View style={{ width: 40, height: 40, borderRadius: 20, backgroundColor: '#00A884', justifyContent: 'center', alignItems: 'center', marginRight: 12 }}>
                        <Text style={{ color: '#fff', fontWeight: 'bold', fontSize: 16 }}>{chatItem.name.charAt(0)}</Text>
                      </View>
                    )}
                    <View style={{ flex: 1 }}>
                      <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                        <Text style={[styles.langOptionText, { fontSize: 16 }]}>{chatItem.name}</Text>
                        {chatItem.isOfficial && <BadgeCheck size={14} color="#53BDEB" style={{ marginLeft: 4 }} fill="#fff" />}
                      </View>
                      <Text style={{ fontSize: 12, color: '#667781', marginTop: 2 }}>{chatItem.status || 'Available'}</Text>
                    </View>
                  </View>
                  {isSelected && (
                    <View style={{ width: 22, height: 22, borderRadius: 11, backgroundColor: '#00A884', justifyContent: 'center', alignItems: 'center' }}>
                      <Text style={{ color: '#fff', fontSize: 12, fontWeight: 'bold' }}>✓</Text>
                    </View>
                  )}
                </TouchableOpacity>
              );
            })}
          </ScrollView>

          {selectedChatId && (
            <TouchableOpacity
              style={{
                backgroundColor: '#00A884',
                paddingVertical: 12,
                borderRadius: 24,
                flexDirection: 'row',
                justifyContent: 'center',
                alignItems: 'center',
                marginTop: 14
              }}
              onPress={handleSendForward}
            >
              <Send size={18} color="#fff" style={{ marginRight: 8 }} />
              <Text style={{ color: '#fff', fontWeight: 'bold', fontSize: 15 }}>Send Forward</Text>
            </TouchableOpacity>
          )}
        </TouchableOpacity>
      </TouchableOpacity>
    </Modal>
  );
};
