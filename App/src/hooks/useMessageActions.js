import { useState } from 'react';
import { Share } from 'react-native';
import * as Clipboard from 'expo-clipboard';

export function useMessageActions({ chat, setMessages, onForwardToOtherChat }) {
  const [toastText, setToastText] = useState('');
  const [actionModalVisible, setActionModalVisible] = useState(false);
  const [selectedActionMsg, setSelectedActionMsg] = useState(null);
  const [forwardModalVisible, setForwardModalVisible] = useState(false);
  const [msgToForward, setMsgToForward] = useState(null);

  const showToast = (text) => {
    setToastText(text);
    setTimeout(() => {
      setToastText('');
    }, 2500);
  };

  const handleLongPressMessage = (msg) => {
    setSelectedActionMsg(msg);
    setActionModalVisible(true);
  };

  const handleCopyMessage = async (msg) => {
    if (msg.text) {
      await Clipboard.setStringAsync(msg.text);
      showToast('Copied to clipboard');
    }
  };

  const handleShareMessage = async (msg) => {
    if (msg.text) {
      try {
        await Share.share({ message: msg.text });
      } catch (err) {
        console.error("Share error:", err);
      }
    }
  };

  const handleOpenForwardModal = (msg) => {
    setMsgToForward(msg);
    setForwardModalVisible(true);
  };

  const handleForwardToChat = (targetChat) => {
    setForwardModalVisible(false);
    if (!msgToForward) return;

    if (targetChat.id === chat.id) {
      const fwdMsg = {
        id: Date.now().toString(),
        text: msgToForward.text,
        sender: 'me',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        isForwarded: true
      };
      setMessages(prev => [...prev, fwdMsg]);
      showToast(`Forwarded to ${targetChat.name}`);
    } else if (onForwardToOtherChat) {
      onForwardToOtherChat(targetChat.id, msgToForward);
      showToast(`Forwarded to ${targetChat.name}`);
    }
    setMsgToForward(null);
  };

  return {
    toastText,
    showToast,
    actionModalVisible,
    setActionModalVisible,
    selectedActionMsg,
    handleLongPressMessage,
    handleCopyMessage,
    handleShareMessage,
    forwardModalVisible,
    setForwardModalVisible,
    msgToForward,
    handleOpenForwardModal,
    handleForwardToChat
  };
}
