import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator
} from 'react-native';
import { useStyles } from '../constants/styles';
import { useTheme } from '../context/ThemeContext';
import { ChatHeader } from '../components/chat/ChatHeader';
import { ChatInputBar } from '../components/chat/ChatInputBar';
import { ChatMessageBubble } from '../components/chat/ChatMessageBubble';
import { LanguagePickerModal } from '../components/chat/LanguagePickerModal';
import { StatePickerModal } from '../components/chat/StatePickerModal';
import { MessageActionModal } from '../components/chat/MessageActionModal';
import { ForwardModal } from '../components/chat/ForwardModal';
import { Toast } from '../components/chat/Toast';

import { useMessageActions } from '../hooks/useMessageActions';
import { useMediaPicker } from '../hooks/useMediaPicker';
import { useBotLogic } from '../hooks/useBotLogic';

export default function ChatScreen({ chat, allChats = [], goBack, openProfile, onUpdateMessages, onForwardToOtherChat, initialLanguage = 'en' }) {
  const [messages, setMessages] = useState(chat.messages || []);
  const [inputText, setInputText] = useState('');
  const scrollViewRef = useRef(null);

  const styles = useStyles();
  const { colors } = useTheme();

  const {
    toastText,
    actionModalVisible,
    setActionModalVisible,
    selectedActionMsg,
    handleLongPressMessage,
    handleCopyMessage,
    handleShareMessage,
    forwardModalVisible,
    setForwardModalVisible,
    handleOpenForwardModal,
    handleForwardToChat
  } = useMessageActions({ chat, setMessages, onForwardToOtherChat });

  const {
    isRecording,
    setIsRecording,
    handleAttachment,
    handleCamera,
    sendMediaMessage
  } = useMediaPicker({ setMessages });

  const {
    isTyping,
    currentLanguage,
    langModalVisible,
    setLangModalVisible,
    stateModalVisible,
    setStateModalVisible,
    userState,
    availableStates,
    simulateBotResponse,
    handleBookDoctor,
    handleSelectLanguage,
    handleQuickReplyButtonPress,
    handleStateSelect
  } = useBotLogic({ chat, messages, setMessages, initialLanguage });

  useEffect(() => {
    if (onUpdateMessages) {
      onUpdateMessages(messages);
    }
  }, [messages]);

  const handleSendMessage = () => {
    if (inputText.trim() === '') return;

    const userText = inputText.trim();
    const newMsg = {
      id: Date.now().toString(),
      text: userText,
      sender: 'me',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, newMsg]);
    setInputText('');

    if (chat.isOfficial) {
      simulateBotResponse(userText);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.keyboardView}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ChatHeader chat={chat} goBack={goBack} openProfile={openProfile} />

      <View style={styles.chatAreaWrapper}>
        <View style={styles.chatBackground} />
        <ScrollView
          ref={scrollViewRef}
          style={styles.messageArea}
          contentContainerStyle={styles.messageAreaContent}
          onContentSizeChange={() => scrollViewRef.current?.scrollToEnd({ animated: true })}
        >
          {messages.map((msg) => (
            <ChatMessageBubble
              key={msg.id}
              msg={msg}
              isMe={msg.sender === 'me'}
              onButtonPress={handleQuickReplyButtonPress}
              onBookDoctor={handleBookDoctor}
              onLongPressMessage={handleLongPressMessage}
            />
          ))}

          {isTyping && (
            <View style={[styles.msgRow, styles.msgRowLeft]}>
              <View style={[styles.bubble, styles.bubbleOther, styles.typingBubble]}>
                <ActivityIndicator size="small" color={colors.accent} />
                <Text style={styles.typingText}>typing...</Text>
              </View>
            </View>
          )}
        </ScrollView>
      </View>

      <ChatInputBar
        isRecording={isRecording}
        setIsRecording={setIsRecording}
        inputText={inputText}
        setInputText={setInputText}
        handleSendMessage={handleSendMessage}
        handleAttachment={handleAttachment}
        handleCamera={handleCamera}
        onRecordSend={(uri) => {
          sendMediaMessage({ type: 'audio', uri });
          setIsRecording(false);
        }}
      />

      <LanguagePickerModal
        visible={langModalVisible}
        onClose={() => setLangModalVisible(false)}
        currentLanguage={currentLanguage}
        onSelectLanguage={handleSelectLanguage}
      />

      <StatePickerModal
        visible={stateModalVisible}
        onClose={() => setStateModalVisible(false)}
        availableStates={availableStates}
        userState={userState}
        onSelectState={handleStateSelect}
      />

      <MessageActionModal
        visible={actionModalVisible}
        onClose={() => setActionModalVisible(false)}
        selectedMessage={selectedActionMsg}
        onCopy={handleCopyMessage}
        onForward={handleOpenForwardModal}
        onShare={handleShareMessage}
      />

      <ForwardModal
        visible={forwardModalVisible}
        onClose={() => setForwardModalVisible(false)}
        chats={allChats}
        onForward={handleForwardToChat}
      />

      <Toast text={toastText} />
    </KeyboardAvoidingView>
  );
}
