import React, { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';

export default function MessageList({
  messages,
  onQuickReplySelect,
  onBookDoctor,
  onViewSchemeDetails,
  onContextMenu
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-3 relative z-10 scrollbar-thin scrollbar-thumb-gray-700">
      {/* Date Header Badge */}
      <div className="flex justify-center my-3 select-none">
        <span className="bg-[#182229] text-gray-400 text-[11px] font-semibold px-3 py-1 rounded-md shadow uppercase tracking-wider border border-gray-700">
          TODAY
        </span>
      </div>

      {messages.map((msg) => (
        <MessageBubble
          key={msg.id}
          msg={msg}
          onQuickReplySelect={onQuickReplySelect}
          onBookDoctor={onBookDoctor}
          onViewSchemeDetails={onViewSchemeDetails}
          onContextMenu={onContextMenu}
        />
      ))}

      <div ref={bottomRef} />
    </div>
  );
}
