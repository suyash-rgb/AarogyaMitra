import React from 'react';
import { BadgeCheck, Volume2, Image, FileText, CheckCheck } from 'lucide-react';

export default function ChatListItem({ chat, isActive, onClick }) {
  const lastMsg = chat.messages && chat.messages.length ? chat.messages[chat.messages.length - 1] : null;

  const renderSnippet = () => {
    if (!lastMsg) return 'No messages yet';
    if (lastMsg.audioUrl) {
      return (
        <span className="flex items-center gap-1 text-[#00a884]">
          <Volume2 className="w-3.5 h-3.5" /> 🎵 Audio message
        </span>
      );
    }
    if (lastMsg.media) {
      return (
        <span className="flex items-center gap-1 text-gray-300">
          {lastMsg.media.type === 'image' ? <Image className="w-3.5 h-3.5" /> : <FileText className="w-3.5 h-3.5" />}
          {lastMsg.media.name || 'Attachment'}
        </span>
      );
    }
    return lastMsg.text;
  };

  return (
    <div
      onClick={onClick}
      className={`flex items-center gap-3 p-3 cursor-pointer transition-all duration-150 border-b border-[#222d34]/60 ${
        isActive
          ? 'bg-[#2a3942]'
          : 'hover:bg-[#202c33]'
      }`}
    >
      <div className="relative flex-shrink-0">
        <img
          src={chat.avatar}
          alt={chat.name}
          className="w-12 h-12 rounded-full object-cover border border-[#00a884]/30"
        />
        {chat.isOfficial && (
          <span className="absolute -bottom-0.5 -right-0.5 bg-[#00a884] rounded-full p-0.5 border border-[#111b21]">
            <BadgeCheck className="w-3 h-3 text-white" />
          </span>
        )}
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between mb-0.5">
          <h4 className="text-sm font-semibold text-gray-100 truncate flex items-center gap-1">
            <span>{chat.name}</span>
            {chat.verifiedBadge && <BadgeCheck className="w-4 h-4 text-[#00a884] flex-shrink-0" />}
          </h4>
          <span className="text-[11px] text-gray-400 flex-shrink-0">
            {lastMsg?.timestamp || chat.lastMessageTime || ''}
          </span>
        </div>

        <div className="flex items-center justify-between gap-1 text-xs text-gray-400">
          <div className="truncate flex items-center gap-1 flex-1">
            {lastMsg?.sender === 'user' && (
              <CheckCheck className="w-3.5 h-3.5 text-[#53bdeb] flex-shrink-0" />
            )}
            <div className="truncate">{renderSnippet()}</div>
          </div>

          {chat.unreadCount > 0 && (
            <span className="w-5 h-5 rounded-full bg-[#00a884] text-white text-[10px] font-bold flex items-center justify-center flex-shrink-0">
              {chat.unreadCount}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
