import { setupGlobalLogging } from './src/utils/logger';
setupGlobalLogging();

import { StatusBar } from 'expo-status-bar';
import React, { useState, useEffect } from 'react';
import { View } from 'react-native';
import { SafeAreaView, SafeAreaProvider } from 'react-native-safe-area-context';
import { initialChats } from './src/constants/mockData';
import { useStyles } from './src/constants/styles';
import { ThemeProvider, useTheme } from './src/context/ThemeContext';
import ProfileScreen from './src/screens/ProfileScreen';
import ChatScreen from './src/screens/ChatScreen';
import ChatListScreen from './src/screens/ChatListScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import ChatsSettingsScreen from './src/screens/ChatsSettingsScreen';
import { getUserPersona } from './src/utils/userSession';

export default function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}

function AppContent() {
  const styles = useStyles();
  const { activeTheme } = useTheme();

  const [currentScreen, setCurrentScreen] = useState('chatList');
  const [activeChat, setActiveChat] = useState(null);
  const [chats, setChats] = useState(initialChats);
  const [userPersona, setUserPersona] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const persona = await getUserPersona();
        setUserPersona(persona);
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

  const handleForwardToOtherChat = (targetChatId, message) => {
    const fwdMsg = {
      id: Date.now().toString(),
      text: message.text,
      sender: 'me',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      isForwarded: true
    };
    setChats(prevChats => prevChats.map(c => {
      if (c.id === targetChatId) {
        return {
          ...c,
          messages: [...c.messages, fwdMsg]
        };
      }
      return c;
    }));
  };

  const renderScreen = () => {
    if (currentScreen === 'chatList') {
      return (
        <ChatListScreen 
          chats={chats} 
          onSelectChat={handleSelectChat} 
          openSettings={() => setCurrentScreen('settings')}
        />
      );
    }
    
    if (currentScreen === 'chat') {
      const currentChat = chats.find(c => c.id === activeChat?.id) || activeChat;
      return (
        <ChatScreen 
          key={activeChat.id} // forces remount for fresh chat state
          chat={currentChat} 
          allChats={chats}
          goBack={() => setCurrentScreen('chatList')}
          openProfile={() => setCurrentScreen('profile')}
          onUpdateMessages={(updatedMessages) => updateChatMessages(activeChat.id, updatedMessages)}
          onForwardToOtherChat={handleForwardToOtherChat}
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

    if (currentScreen === 'settings') {
      return (
        <SettingsScreen
          userPersona={userPersona}
          goBack={() => setCurrentScreen('chatList')}
          openChatsSettings={() => setCurrentScreen('chatsSettings')}
        />
      );
    }

    if (currentScreen === 'chatsSettings') {
      return (
        <ChatsSettingsScreen
          goBack={() => setCurrentScreen('settings')}
        />
      );
    }
  };

  return (
    <SafeAreaProvider>
      <SafeAreaView style={styles.container}>
        <StatusBar style={activeTheme === 'dark' ? "light" : "dark"} backgroundColor={activeTheme === 'dark' ? "#111B21" : "#054c44"} />
        {renderScreen()}
      </SafeAreaView>
    </SafeAreaProvider>
  );
}
