import React, { useState, useEffect } from 'react';
import Sidebar from '../sidebar/Sidebar';
import ChatArea from '../chat/ChatArea';
import SchemeDetailModal from '../modals/SchemeDetailModal';
import LanguageModal from '../modals/LanguageModal';
import StateModal from '../modals/StateModal';
import ContextMenu from '../modals/ContextMenu';
import ForwardModal from '../modals/ForwardModal';
import NewChatModal from '../modals/NewChatModal';
import ThemeModal from '../modals/ThemeModal';
import ProfileDrawer from '../drawers/ProfileDrawer';
import { INITIAL_CHATS, INDIC_LANGUAGES } from '../../data/mockData';
import { getSavedChats, saveChats, getUserState, setUserState as saveUserState, getCurrentLanguage, setCurrentLanguage as saveLanguage } from '../../utils/storage';
import { classifyQuery } from '../../services/api';
import { playNotificationSound } from '../../utils/audio';

import { getTranslation } from '../../data/translations';

export default function WhatsAppLayout() {
  const [chats, setChats] = useState(() => getSavedChats() || INITIAL_CHATS);
  const [activeChatId, setActiveChatId] = useState('ai-bot');
  const [userState, setUserState] = useState(() => getUserState());
  const [currentLang, setCurrentLang] = useState(() => getCurrentLanguage());

  // Modal / Drawer States
  const [selectedScheme, setSelectedScheme] = useState(null);
  const [showLangModal, setShowLangModal] = useState(false);
  const [showStateModal, setShowStateModal] = useState(false);
  const [showNewChatModal, setShowNewChatModal] = useState(false);
  const [showThemeModal, setShowThemeModal] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [contextMenuConfig, setContextMenuConfig] = useState(null); // { x, y, message }
  const [forwardMessage, setForwardMessage] = useState(null);

  useEffect(() => {
    saveChats(chats);
  }, [chats]);

  const activeChat = chats.find((c) => c.id === activeChatId) || null;
  const currentLangObj = INDIC_LANGUAGES.find((l) => l.code === currentLang) || INDIC_LANGUAGES[0];

  // Post User Message and trigger Bot Assistant logic
  const handleSendMessage = async (text, customPayload = {}) => {
    if (!activeChatId) return;

    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const userMsgId = 'msg_' + Date.now();

    const userMsg = {
      id: userMsgId,
      sender: 'user',
      text,
      timestamp: timeStr,
      ...customPayload
    };

    // Update state with user message
    setChats((prevChats) =>
      prevChats.map((c) => {
        if (c.id === activeChatId) {
          return {
            ...c,
            lastMessageTime: timeStr,
            messages: [...c.messages, userMsg]
          };
        }
        return c;
      })
    );

    // If chat is with official bot (Aarogya Mitra or Meta AI), process AI response
    if (activeChatId === 'ai-bot' || activeChatId === 'meta-ai') {
      setTimeout(async () => {
        let botResponse = null;

        if (activeChatId === 'meta-ai') {
          botResponse = {
            intent: 'META_AI',
            message: `🤖 **Meta AI Response**:\n\nRegarding *"${text}"*, I am here to provide quick general answers. For specialized government health schemes or PHC locations, switch to **Aarogya Mitra**.`
          };
        } else {
          botResponse = await classifyQuery(text);
        }

        const botMsgTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const botMsg = {
          id: 'bot_' + Date.now(),
          sender: 'bot',
          text: botResponse.message || botResponse.text,
          timestamp: botMsgTime,
          quickReplies: botResponse.quickReplies,
          schemes: botResponse.schemes,
          facilities: botResponse.facilities,
          doctors: botResponse.doctors,
          openModal: botResponse.openModal
        };

        if (botResponse.actionUrl) {
          window.open(botResponse.actionUrl, '_blank');
        }

        if (botResponse.openModal === 'language') {
          setShowLangModal(true);
        }

        playNotificationSound();

        setChats((prevChats) =>
          prevChats.map((c) => {
            if (c.id === activeChatId) {
              return {
                ...c,
                lastMessageTime: botMsgTime,
                messages: [...c.messages, botMsg]
              };
            }
            return c;
          })
        );
      }, 500);
    }
  };

  const handleSendMedia = (mediaObj) => {
    handleSendMessage(`Sent attachment: ${mediaObj.name}`, { media: mediaObj });
  };

  const handleSendAudio = (audioUrl, duration) => {
    handleSendMessage('', { audioUrl, audioDuration: duration });
  };

  // Quick Reply Button Click
  const handleQuickReplySelect = (btnText) => {
    handleSendMessage(btnText);
  };

  // Doctor Booking Trigger
  const handleBookDoctor = (doc) => {
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const abhaToken = 'ABHA-' + Math.floor(1000 + Math.random() * 9000) + '-' + Math.floor(1000 + Math.random() * 9000);

    const bookingMsg = {
      id: 'ticket_' + Date.now(),
      sender: 'bot',
      text: `✅ **Tele-consultation Call Confirmed with ${doc.name}**!\n\nYour ABHA appointment reference has been generated below:`,
      timestamp: timeStr,
      bookingData: {
        doctor: doc,
        ticketNo: 'TICK-' + Date.now().toString().slice(-6),
        date: 'Today',
        time: doc.availableTime,
        abhaToken
      }
    };

    playNotificationSound();

    setChats((prevChats) =>
      prevChats.map((c) => {
        if (c.id === activeChatId) {
          return {
            ...c,
            lastMessageTime: timeStr,
            messages: [...c.messages, bookingMsg]
          };
        }
        return c;
      })
    );
  };

  // Language Selection
  const handleSelectLanguage = (langObj) => {
    setCurrentLang(langObj.code);
    saveLanguage(langObj.code);
    const confirmMsg = getTranslation(langObj.code, 'confirmLang');
    handleSendMessage(confirmMsg || `Selected language: ${langObj.name} (${langObj.native})`);
  };

  // State Selection
  const handleSelectState = (stName) => {
    setUserState(stName);
    saveUserState(stName);
    handleSendMessage(`Selected state: ${stName}`);
  };

  // Context Menu Handling
  const handleContextMenu = (e, msg) => {
    setContextMenuConfig({
      x: Math.min(e.clientX, window.innerWidth - 200),
      y: Math.min(e.clientY, window.innerHeight - 150),
      message: msg
    });
  };

  const handleCopyText = (msg) => {
    if (msg.text) {
      navigator.clipboard.writeText(msg.text);
    }
  };

  const handleForwardConfirm = (targetChatIds, msg) => {
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    setChats((prev) =>
      prev.map((c) => {
        if (targetChatIds.includes(c.id)) {
          const fwdMsg = {
            ...msg,
            id: 'fwd_' + Date.now() + '_' + Math.random().toString(36).substring(2, 6),
            isForwarded: true,
            sender: 'user',
            timestamp: timeStr
          };
          return {
            ...c,
            lastMessageTime: timeStr,
            messages: [...c.messages, fwdMsg]
          };
        }
        return c;
      })
    );
  };

  return (
    <div className="w-screen h-screen overflow-hidden bg-gray-200 dark:bg-[#0c1317] flex justify-center items-center font-sans">
      <div className="w-full h-full max-w-[1600px] flex shadow-2xl overflow-hidden relative">
        {/* Left Sidebar */}
        <Sidebar
          chats={chats}
          activeChatId={activeChatId}
          onSelectChat={(id) => {
            setActiveChatId(id);
            // Mark chat unread count as zero
            setChats((prev) =>
              prev.map((c) => (c.id === id ? { ...c, unreadCount: 0 } : c))
            );
          }}
          onOpenNewChat={() => setShowNewChatModal(true)}
          onOpenStateModal={() => setShowStateModal(true)}
          onOpenLanguageModal={() => setShowLangModal(true)}
          onOpenThemeModal={() => setShowThemeModal(true)}
          currentState={userState}
          currentLanguageObj={currentLangObj}
        />

        {/* Right Chat Window */}
        <ChatArea
          activeChat={activeChat}
          onSendMessage={handleSendMessage}
          onSendMedia={handleSendMedia}
          onSendAudio={handleSendAudio}
          onQuickReplySelect={handleQuickReplySelect}
          onBookDoctor={handleBookDoctor}
          onViewSchemeDetails={(scheme) => setSelectedScheme(scheme)}
          onOpenProfile={() => setIsProfileOpen(true)}
          onContextMenu={handleContextMenu}
          onBackToSidebar={() => setActiveChatId(null)}
        />

        {/* Drawers & Modals */}
        <ProfileDrawer
          contact={activeChat}
          isOpen={isProfileOpen}
          onClose={() => setIsProfileOpen(false)}
        />

        {selectedScheme && (
          <SchemeDetailModal
            scheme={selectedScheme}
            onClose={() => setSelectedScheme(null)}
          />
        )}

        {showLangModal && (
          <LanguageModal
            currentLanguage={currentLang}
            onSelect={handleSelectLanguage}
            onClose={() => setShowLangModal(false)}
          />
        )}

        {showStateModal && (
          <StateModal
            currentState={userState}
            onSelect={handleSelectState}
            onClose={() => setShowStateModal(false)}
          />
        )}

        {showNewChatModal && (
          <NewChatModal
            contacts={chats}
            onSelectContact={(id) => setActiveChatId(id)}
            onClose={() => setShowNewChatModal(false)}
          />
        )}

        {showThemeModal && (
          <ThemeModal
            onClose={() => setShowThemeModal(false)}
          />
        )}

        {contextMenuConfig && (
          <ContextMenu
            x={contextMenuConfig.x}
            y={contextMenuConfig.y}
            message={contextMenuConfig.message}
            onClose={() => setContextMenuConfig(null)}
            onCopy={handleCopyText}
            onForward={(msg) => setForwardMessage(msg)}
            onShare={(msg) => {
              if (navigator.share && msg.text) {
                navigator.share({ text: msg.text });
              } else if (msg.text) {
                navigator.clipboard.writeText(msg.text);
              }
            }}
          />
        )}

        {forwardMessage && (
          <ForwardModal
            chats={chats}
            messageToForward={forwardMessage}
            onConfirmForward={handleForwardConfirm}
            onClose={() => setForwardMessage(null)}
          />
        )}
      </div>
    </div>
  );
}
