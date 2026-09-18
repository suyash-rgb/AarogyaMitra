import React from 'react';
import { View, Text, TouchableOpacity, Modal } from 'react-native';
import { Copy, CornerUpRight, Share2, X } from 'lucide-react-native';
import { styles } from '../../constants/styles';

export const MessageActionModal = ({ visible, onClose, selectedMessage, onCopy, onForward, onShare }) => {
  if (!selectedMessage) return null;

  return (
    <Modal
      visible={visible}
      transparent={true}
      animationType="fade"
      onRequestClose={onClose}
    >
      <TouchableOpacity
        style={styles.modalOverlay}
        activeOpacity={1}
        onPress={onClose}
      >
        <TouchableOpacity
          activeOpacity={1}
          style={[styles.modalContentContainer, { paddingBottom: 20 }]}
        >
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle} numberOfLines={1}>Message Options</Text>
            <TouchableOpacity onPress={onClose}>
              <X size={22} color="#111B21" />
            </TouchableOpacity>
          </View>

          {/* Preview of message being acted upon */}
          <View style={{
            backgroundColor: '#F0F2F5',
            padding: 12,
            borderRadius: 10,
            marginVertical: 12,
            borderLeftWidth: 4,
            borderLeftColor: '#00A884'
          }}>
            <Text style={{ fontSize: 13, color: '#667781', fontStyle: 'italic' }} numberOfLines={3}>
              "{selectedMessage.text || (selectedMessage.type === 'image' ? 'Photo' : selectedMessage.type === 'document' ? 'Document' : 'Audio Message')}"
            </Text>
          </View>

          <View style={{ gap: 8 }}>
            {selectedMessage.text ? (
              <TouchableOpacity
                style={actionBtnStyle}
                onPress={() => {
                  onCopy(selectedMessage);
                  onClose();
                }}
              >
                <Copy size={20} color="#128C7E" style={{ marginRight: 14 }} />
                <Text style={actionTextStyle}>Copy Text</Text>
              </TouchableOpacity>
            ) : null}

            <TouchableOpacity
              style={actionBtnStyle}
              onPress={() => {
                onClose();
                onForward(selectedMessage);
              }}
            >
              <CornerUpRight size={20} color="#128C7E" style={{ marginRight: 14 }} />
              <Text style={actionTextStyle}>Forward Message</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={actionBtnStyle}
              onPress={() => {
                onShare(selectedMessage);
                onClose();
              }}
            >
              <Share2 size={20} color="#128C7E" style={{ marginRight: 14 }} />
              <Text style={actionTextStyle}>Share...</Text>
            </TouchableOpacity>
          </View>
        </TouchableOpacity>
      </TouchableOpacity>
    </Modal>
  );
};

const actionBtnStyle = {
  flexDirection: 'row',
  alignItems: 'center',
  paddingVertical: 14,
  paddingHorizontal: 16,
  borderRadius: 12,
  backgroundColor: '#F7F8FA'
};

const actionTextStyle = {
  fontSize: 16,
  fontWeight: '600',
  color: '#111B21'
};
