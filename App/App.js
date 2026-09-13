import { setupGlobalLogging } from './src/utils/logger';
setupGlobalLogging();

import { StatusBar } from 'expo-status-bar';
import React, { useState, useEffect } from 'react';
import { View } from 'react-native';
import { SafeAreaView, SafeAreaProvider } from 'react-native-safe-area-context';
import { initialChats } from './src/constants/mockData';
import { styles } from './src/constants/styles';
import ProfileScreen from './src/screens/ProfileScreen';
import ChatScreen from './src/screens/ChatScreen';
import ChatListScreen from './src/screens/ChatListScreen';
import { getUserPersona } from './src/utils/userSession';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState('chatList');
  const [activeChat, setActiveChat] = useState(null);
  const [chats, setChats] = useState(initialChats);
  const [userPersona, setUserPersona] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const persona = await getUserPersona();
        setUserPersona(persona);
        if (persona.presetChats && persona.presetChats.length > 0) {
          setChats(persona.presetChats);
        }
      } catch (err) {
        console.error('Failed to load user persona:', err);
      }
    })();
  }, []);

  const handleSelectChat = (chat) => {
    // Clear unread count when opening the chat
    setChats(prevChats => prevChats.map(c => c.id === chat.id ? { ...c, unreadCount: 0 } : c));
    setActiveChat(chat);
    setCurrentScreen('chat');
  };

  const updateChatMessages = (chatId, updatedMessages) => {
    setChats(prevChats => prevChats.map(c => c.id === chatId ? { ...c, messages: updatedMessages } : c));
  };

  const renderScreen = () => {
    if (currentScreen === 'chatList') {
      return (
        <ChatListScreen 
          chats={chats} 
          onSelectChat={handleSelectChat} 
        />
      );
    }
    
    if (currentScreen === 'chat') {
      const currentChat = chats.find(c => c.id === activeChat?.id) || activeChat;
      return (
        <ChatScreen 
          key={activeChat.id} // forces remount for fresh chat state
          chat={currentChat} 
          goBack={() => setCurrentScreen('chatList')}
          openProfile={() => setCurrentScreen('profile')}
          onUpdateMessages={(updatedMessages) => updateChatMessages(activeChat.id, updatedMessages)}
        />
      );
    }

    if (currentScreen === 'profile') {
      const currentChat = chats.find(c => c.id === activeChat?.id) || activeChat;
      return (
        <ProfileScreen
          activeChat={currentChat}
          goBack={() => setCurrentScreen('chat')}
        />
      );
    }
  };

  return (
    <SafeAreaProvider>
      <SafeAreaView style={styles.container}>
        <StatusBar style="light" backgroundColor="#054c44" />
        {renderScreen()}
      </SafeAreaView>
    </SafeAreaProvider>
  );
}
