import React, { useState } from 'react';
import { MessageSquarePlus, MoreVertical, Search, Bot, Globe, Sparkles, Settings as SettingsIcon } from 'lucide-react';
import ChatListItem from './ChatListItem';
import SettingsDrawer from '../drawers/SettingsDrawer';

export default function Sidebar({
  chats,
  activeChatId,
  onSelectChat,
  onOpenNewChat,
  onOpenStateModal,
  onOpenLanguageModal,
  onOpenThemeModal,
  currentState,
  currentLanguageObj
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeTab, setActiveTab] = useState('All');
  const [showMenu, setShowMenu] = useState(false);
  const [showSettingsDrawer, setShowSettingsDrawer] = useState(false);

  const filterTabs = ['All', 'Unread', 'Favorites', 'Groups'];

  const filteredChats = chats.filter((c) => {
    const matchesSearch = c.name.toLowerCase().includes(searchTerm.toLowerCase().trim());
    if (!matchesSearch) return false;

    if (activeTab === 'Unread') return c.unreadCount > 0;
    if (activeTab === 'Favorites') return c.isOfficial;
    if (activeTab === 'Groups') return c.name.includes('Group') || c.name.includes('Family');
    return true;
  });

  return (
    <aside className="w-full md:w-[32%] lg:w-[30%] min-w-[320px] max-w-[450px] bg-white dark:bg-[#111b21] flex flex-col h-full border-r border-gray-200 dark:border-[#222d34] select-none relative">
      {/* Settings Drawer Overlay */}
      <SettingsDrawer
        isOpen={showSettingsDrawer}
        onClose={() => setShowSettingsDrawer(false)}
        onOpenThemeModal={onOpenThemeModal}
        onOpenStateModal={onOpenStateModal}
        onOpenLanguageModal={onOpenLanguageModal}
        onSelectChat={onSelectChat}
        currentState={currentState}
        currentLanguageObj={currentLanguageObj}
      />

      {/* Sidebar Top Header */}
      <div className="bg-gray-100 dark:bg-[#202c33] px-4 py-3 flex items-center justify-between border-b border-gray-200 dark:border-gray-700">
        <div
          className="flex items-center gap-3 cursor-pointer"
          onClick={() => setShowSettingsDrawer(true)}
          title="Open Settings"
        >
          <img
            src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80"
            alt="Leo (You)"
            className="w-10 h-10 rounded-full object-cover border-2 border-[#00a884]"
          />
          <div>
            <h3 className="font-semibold text-sm text-gray-800 dark:text-gray-100 leading-tight">Leo (You)</h3>
            <span className="text-[10px] text-[#00a884] font-medium flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-[#00a884] animate-ping" />
              Online
            </span>
          </div>
        </div>

        {/* Action Header Icons */}
        <div className="flex items-center gap-1 text-gray-500 dark:text-gray-400">
          <button
            onClick={() => onSelectChat('meta-ai')}
            title="Ask Meta AI"
            className="p-2 hover:text-[#00a884] hover:bg-gray-200 dark:hover:bg-[#2a3942] rounded-full transition-all"
          >
            <Sparkles className="w-5 h-5 text-blue-500" />
          </button>

          <button
            onClick={onOpenNewChat}
            title="New Chat"
            className="p-2 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-200 dark:hover:bg-[#2a3942] rounded-full transition-all"
          >
            <MessageSquarePlus className="w-5 h-5 text-[#00a884]" />
          </button>

          {/* 3 Dots Menu */}
          <div className="relative">
            <button
              onClick={() => setShowMenu((prev) => !prev)}
              title="Menu"
              className="p-2 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-200 dark:hover:bg-[#2a3942] rounded-full transition-all"
            >
              <MoreVertical className="w-5 h-5" />
            </button>

            {showMenu && (
              <div className="absolute right-0 top-10 z-30 w-52 bg-white dark:bg-[#233138] border border-gray-200 dark:border-gray-700 rounded-xl shadow-2xl py-1 text-xs text-gray-800 dark:text-gray-200">
                <button
                  onClick={() => {
                    setShowSettingsDrawer(true);
                    setShowMenu(false);
                  }}
                  className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-gray-100 dark:hover:bg-[#182229] transition-all text-left font-medium"
                >
                  <SettingsIcon className="w-4 h-4 text-[#00a884]" />
                  <span>Settings</span>
                </button>

                <button
                  onClick={() => {
                    onOpenLanguageModal();
                    setShowMenu(false);
                  }}
                  className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-gray-100 dark:hover:bg-[#182229] transition-all text-left"
                >
                  <Globe className="w-4 h-4 text-[#00a884]" />
                  <span>Language: {currentLanguageObj?.name || 'English'}</span>
                </button>
                <button
                  onClick={() => {
                    onSelectChat('ai-bot');
                    setShowMenu(false);
                  }}
                  className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-gray-100 dark:hover:bg-[#182229] transition-all text-left border-t border-gray-100 dark:border-gray-700 font-semibold text-[#00a884]"
                >
                  <Bot className="w-4 h-4" />
                  <span>AarogyaMitra Bot</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Language Quick Badge Bar */}
      <div className="bg-gray-50 dark:bg-[#111b21] px-3 py-2 flex items-center justify-end border-b border-gray-200 dark:border-[#222d34] text-xs">

        <button
          onClick={onOpenLanguageModal}
          className="flex items-center gap-1.5 bg-white dark:bg-[#202c33] hover:bg-gray-200 dark:hover:bg-[#2a3942] text-gray-700 dark:text-gray-200 px-3 py-1 rounded-full border border-gray-200 dark:border-gray-700 transition-all font-medium shadow-xs"
        >
          <Globe className="w-3.5 h-3.5 text-[#00a884]" />
          <span>{currentLanguageObj?.native || 'English'}</span>
        </button>
      </div>

      {/* Search Input Bar */}
      <div className="p-2.5 bg-white dark:bg-[#111b21]">
        <div className="relative">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search or start new chat"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-gray-100 dark:bg-[#202c33] text-gray-900 dark:text-gray-100 text-sm pl-9 pr-4 py-1.5 rounded-lg border border-transparent focus:outline-none focus:border-[#00a884] placeholder-gray-500 dark:placeholder-gray-400"
          />
        </div>
      </div>

      {/* Quick Filter Tabs */}
      <div className="flex gap-2 px-3 pb-2 border-b border-gray-200 dark:border-[#222d34] text-xs">
        {filterTabs.map((tab) => {
          const isActive = activeTab === tab;
          return (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-3 py-1 rounded-full font-semibold transition-all ${isActive
                  ? 'bg-[#00a884]/20 text-[#00a884] border border-[#00a884]/40'
                  : 'bg-gray-100 dark:bg-[#202c33] text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-200 dark:hover:bg-[#2a3942]'
                }`}
            >
              {tab}
            </button>
          );
        })}
      </div>

      {/* Chat List */}
      <div className="flex-1 overflow-y-auto divide-y divide-gray-100 dark:divide-[#222d34]/40 scrollbar-thin scrollbar-thumb-gray-400 dark:scrollbar-thumb-gray-700">
        {filteredChats.map((c) => (
          <ChatListItem
            key={c.id}
            chat={c}
            isActive={c.id === activeChatId}
            onClick={() => onSelectChat(c.id)}
          />
        ))}

        {filteredChats.length === 0 && (
          <div className="p-8 text-center text-xs text-gray-500">
            No chats found matching search
          </div>
        )}
      </div>
    </aside>
  );
}
