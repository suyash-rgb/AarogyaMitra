import React from 'react';
import { Phone, Search, MoreVertical, BadgeCheck, Lock, Shield, Stethoscope, ArrowLeft } from 'lucide-react';
import MessageList from './MessageList';
import InputBar from './InputBar';

export default function ChatArea({
  activeChat,
  onSendMessage,
  onSendMedia,
  onSendAudio,
  onQuickReplySelect,
  onBookDoctor,
  onViewSchemeDetails,
  onOpenProfile,
  onContextMenu,
  onBackToSidebar
}) {
  if (!activeChat) {
    // Default Unselected Welcome Screen
    return (
      <div className="hidden md:flex flex-1 flex-col items-center justify-center bg-gray-50 dark:bg-[#111b21] text-gray-700 dark:text-gray-300 p-8 border-l border-gray-200 dark:border-[#222d34] relative select-none">
        <div className="max-w-md text-center space-y-4">
          <div className="w-24 h-24 rounded-full bg-white dark:bg-[#202c33] border-2 border-[#00a884] flex items-center justify-center mx-auto shadow-2xl animate-pulse">
            <Stethoscope className="w-12 h-12 text-[#00a884]" />
          </div>

          <h1 className="text-2xl font-light text-gray-900 dark:text-gray-100 tracking-wide">WhatsApp Web for AarogyaMitra</h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
            Send and receive medical guidance, locate nearby primary health centers, and explore government schemes seamlessly.
          </p>

          <div className="pt-8 flex items-center justify-center gap-2 text-xs text-gray-500">
            <Lock className="w-3.5 h-3.5 text-[#00a884]" />
            <span>End-to-end encrypted healthcare assistant</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col h-full bg-[#efeae2] dark:bg-[#0b141a] relative overflow-hidden">
      {/* WhatsApp Background Wallpaper Pattern */}
      <div
        className="absolute inset-0 pointer-events-none bg-repeat opacity-[var(--chat-pattern-opacity,0.1)]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 30L15 15M30 30l15 15M30 30l-15 15M30 30l15-15' stroke='%2523000000' stroke-width='1.5' fill='none'/%3E%3C/svg%3E")`
        }}
      />

      {/* Active Chat Header */}
      <div className="bg-gray-100 dark:bg-[#202c33] px-4 py-2.5 flex items-center justify-between border-b border-gray-200 dark:border-gray-700 z-20 shadow-xs">
        <div className="flex items-center gap-3 cursor-pointer" onClick={onOpenProfile}>
          {/* Mobile Back Button */}
          <button
            onClick={(e) => {
              e.stopPropagation();
              onBackToSidebar();
            }}
            className="md:hidden p-1 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>

          <div className="relative">
            <img
              src={activeChat.avatar}
              alt={activeChat.name}
              className="w-10 h-10 rounded-full object-cover border border-[#00a884]"
            />
            {activeChat.isOfficial && (
              <span className="absolute -bottom-0.5 -right-0.5 bg-[#00a884] rounded-full p-0.5 border border-white dark:border-[#202c33]">
                <BadgeCheck className="w-3 h-3 text-white" />
              </span>
            )}
          </div>

          <div>
            <h3 className="font-semibold text-sm text-gray-900 dark:text-gray-100 flex items-center gap-1">
              <span>{activeChat.name}</span>
              {activeChat.verifiedBadge && <BadgeCheck className="w-4 h-4 text-[#00a884]" />}
            </h3>
            <p className="text-[11px] text-gray-500 dark:text-gray-400">
              {activeChat.onlineStatus || 'click here for contact info'}
            </p>
          </div>
        </div>

        {/* Action Header Icons */}
        <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400">
          <button
            onClick={() => onSendMessage('104')}
            title="Call 104 Helpline"
            className="p-2 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-200 dark:hover:bg-[#2a3942] rounded-full transition-all"
          >
            <Phone className="w-5 h-5 text-[#00a884]" />
          </button>
          <button
            title="Search in conversation"
            className="p-2 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-200 dark:hover:bg-[#2a3942] rounded-full transition-all"
          >
            <Search className="w-5 h-5" />
          </button>
          <button
            onClick={onOpenProfile}
            title="Menu"
            className="p-2 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-200 dark:hover:bg-[#2a3942] rounded-full transition-all"
          >
            <MoreVertical className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Message Viewport Stream */}
      <MessageList
        messages={activeChat.messages || []}
        onQuickReplySelect={onQuickReplySelect}
        onBookDoctor={onBookDoctor}
        onViewSchemeDetails={onViewSchemeDetails}
        onContextMenu={onContextMenu}
      />

      {/* Input Bar */}
      <InputBar
        onSendMessage={onSendMessage}
        onSendMedia={onSendMedia}
        onSendAudio={onSendAudio}
      />
    </div>
  );
}
