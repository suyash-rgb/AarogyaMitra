import React from 'react';
import { View, Text, TouchableOpacity, Modal } from 'react-native';
import { Copy, CornerUpRight, Share2, X } from 'lucide-react-native';
import { useStyles } from '../../constants/styles';
import { useTheme } from '../../context/ThemeContext';

export const MessageActionModal = ({ visible, onClose, selectedMessage, onCopy, onForward, onShare }) => {
  const styles = useStyles();
  const { colors } = useTheme();

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
              <X size={22} color={colors.text} />
            </TouchableOpacity>
          </View>

          {/* Preview of message being acted upon */}
          <View style={{
            backgroundColor: colors.doctorBg,
            padding: 12,
            borderRadius: 10,
            marginVertical: 12,
            borderLeftWidth: 4,
            borderLeftColor: colors.accent
          }}>
            <Text style={{ fontSize: 13, color: colors.textSecondary, fontStyle: 'italic' }} numberOfLines={3}>
              "{selectedMessage.text || (selectedMessage.type === 'image' ? 'Photo' : selectedMessage.type === 'document' ? 'Document' : 'Audio Message')}"
            </Text>
          </View>

            <View style={{ gap: 8 }}>
            {selectedMessage.text ? (
              <TouchableOpacity
                style={[actionBtnStyle, { backgroundColor: colors.doctorBg }]}
                onPress={() => {
                  onCopy(selectedMessage);
                  onClose();
                }}
              >
                <Copy size={20} color={colors.accent} style={{ marginRight: 14 }} />
                <Text style={[actionTextStyle, { color: colors.text }]}>Copy Text</Text>
              </TouchableOpacity>
            ) : null}

            <TouchableOpacity
              style={[actionBtnStyle, { backgroundColor: colors.doctorBg }]}
              onPress={() => {
                onClose();
                onForward(selectedMessage);
              }}
            >
              <CornerUpRight size={20} color={colors.accent} style={{ marginRight: 14 }} />
              <Text style={[actionTextStyle, { color: colors.text }]}>Forward Message</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[actionBtnStyle, { backgroundColor: colors.doctorBg }]}
              onPress={() => {
                onShare(selectedMessage);
                onClose();
              }}
            >
              <Share2 size={20} color={colors.accent} style={{ marginRight: 14 }} />
              <Text style={[actionTextStyle, { color: colors.text }]}>Share...</Text>
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
};

const actionTextStyle = {
  fontSize: 16,
  fontWeight: '600',
};
