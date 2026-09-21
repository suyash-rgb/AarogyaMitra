import React, { useState } from 'react';
import { CircleDashed, Users, MessageSquarePlus, MoreVertical, Search, Bot, MapPin, Globe, Sparkles } from 'lucide-react';
import ChatListItem from './ChatListItem';

export default function Sidebar({
  chats,
  activeChatId,
  onSelectChat,
  onOpenNewChat,
  onOpenStateModal,
  onOpenLanguageModal,
  currentState,
  currentLanguageObj
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeTab, setActiveTab] = useState('All');
  const [showMenu, setShowMenu] = useState(false);

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
    <aside className="w-full md:w-[32%] lg:w-[30%] min-w-[320px] max-w-[450px] bg-[#111b21] flex flex-col h-full border-r border-[#222d34] select-none">
      {/* Sidebar Top Header */}
      <div className="bg-[#202c33] px-4 py-3 flex items-center justify-between border-b border-gray-700">
        <div className="flex items-center gap-3">
          <img
            src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80"
            alt="Leo (You)"
            className="w-10 h-10 rounded-full object-cover border-2 border-[#00a884] cursor-pointer"
            title="Leo (You)"
          />
          <div>
            <h3 className="font-semibold text-sm text-gray-100 leading-tight">Leo (You)</h3>
            <span className="text-[10px] text-[#00a884] font-medium flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-[#00a884] animate-ping" />
              Online • Healthcare Active
            </span>
          </div>
        </div>

        {/* Action Header Icons */}
        <div className="flex items-center gap-2 text-gray-400">
          <button
            onClick={() => onSelectChat('meta-ai')}
            title="Ask Meta AI"
            className="p-2 hover:text-[#00a884] hover:bg-[#2a3942] rounded-full transition-all"
          >
            <Sparkles className="w-5 h-5 text-blue-400" />
          </button>
          <button
            title="Status / Updates"
            className="p-2 hover:text-gray-100 hover:bg-[#2a3942] rounded-full transition-all"
          >
            <CircleDashed className="w-5 h-5" />
          </button>
          <button
            title="Communities"
            className="p-2 hover:text-gray-100 hover:bg-[#2a3942] rounded-full transition-all"
          >
            <Users className="w-5 h-5" />
          </button>
          <button
            onClick={onOpenNewChat}
            title="New Chat"
            className="p-2 hover:text-gray-100 hover:bg-[#2a3942] rounded-full transition-all"
          >
            <MessageSquarePlus className="w-5 h-5 text-[#00a884]" />
          </button>
          
          {/* 3 Dots Menu */}
          <div className="relative">
            <button
              onClick={() => setShowMenu((prev) => !prev)}
              title="Menu"
              className="p-2 hover:text-gray-100 hover:bg-[#2a3942] rounded-full transition-all"
            >
              <MoreVertical className="w-5 h-5" />
            </button>

            {showMenu && (
              <div className="absolute right-0 top-10 z-30 w-52 bg-[#233138] border border-gray-700 rounded-xl shadow-2xl py-1 text-xs text-gray-200">
                <button
                  onClick={() => {
                    onOpenStateModal();
                    setShowMenu(false);
                  }}
                  className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-[#182229] transition-all text-left"
                >
                  <MapPin className="w-4 h-4 text-[#00a884]" />
                  <span>State: {currentState}</span>
                </button>
                <button
                  onClick={() => {
                    onOpenLanguageModal();
                    setShowMenu(false);
                  }}
                  className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-[#182229] transition-all text-left"
                >
                  <Globe className="w-4 h-4 text-[#00a884]" />
                  <span>Language: {currentLanguageObj?.name || 'English'}</span>
                </button>
                <button
                  onClick={() => {
                    onSelectChat('ai-bot');
                    setShowMenu(false);
                  }}
                  className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-[#182229] transition-all text-left border-t border-gray-700 font-semibold text-[#00a884]"
                >
                  <Bot className="w-4 h-4" />
                  <span>AarogyaMitra Bot</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* State & Language Quick Badges Bar */}
      <div className="bg-[#111b21] px-3 py-2 flex items-center justify-between border-b border-[#222d34] text-xs">
        <button
          onClick={onOpenStateModal}
          className="flex items-center gap-1.5 bg-[#202c33] hover:bg-[#2a3942] text-gray-200 px-3 py-1 rounded-full border border-gray-700 transition-all font-medium"
        >
          <MapPin className="w-3.5 h-3.5 text-[#00a884]" />
          <span className="truncate max-w-[120px]">{currentState}</span>
        </button>

        <button
          onClick={onOpenLanguageModal}
          className="flex items-center gap-1.5 bg-[#202c33] hover:bg-[#2a3942] text-gray-200 px-3 py-1 rounded-full border border-gray-700 transition-all font-medium"
        >
          <Globe className="w-3.5 h-3.5 text-[#00a884]" />
          <span>{currentLanguageObj?.native || 'English'}</span>
        </button>
      </div>

      {/* Search Input Bar */}
      <div className="p-2.5 bg-[#111b21]">
        <div className="relative">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search or start new chat"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-[#202c33] text-gray-100 text-sm pl-9 pr-4 py-1.5 rounded-lg border border-transparent focus:outline-none focus:border-[#00a884] placeholder-gray-400"
          />
        </div>
      </div>

      {/* Quick Filter Tabs */}
      <div className="flex gap-2 px-3 pb-2 border-b border-[#222d34] text-xs">
        {filterTabs.map((tab) => {
          const isActive = activeTab === tab;
          return (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-3 py-1 rounded-full font-semibold transition-all ${
                isActive
                  ? 'bg-[#00a884]/20 text-[#00a884] border border-[#00a884]/40'
                  : 'bg-[#202c33] text-gray-400 hover:text-gray-200 hover:bg-[#2a3942]'
              }`}
            >
              {tab}
            </button>
          );
        })}
      </div>

      {/* Chat List */}
      <div className="flex-1 overflow-y-auto divide-y divide-[#222d34]/40 scrollbar-thin scrollbar-thumb-gray-700">
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
