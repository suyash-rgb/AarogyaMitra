import React, { useState } from 'react';
import { X, Search, UserPlus, BadgeCheck, MessageSquare } from 'lucide-react';

export default function NewChatModal({ contacts, onSelectContact, onClose }) {
  const [search, setSearch] = useState('');

  const filtered = contacts.filter((c) =>
    c.name.toLowerCase().includes(search.toLowerCase().trim())
  );

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
      <div className="bg-[#111b21] w-full max-w-md rounded-2xl shadow-2xl overflow-hidden border border-[#222d34] flex flex-col max-h-[80vh]">
        <div className="bg-[#202c33] text-white p-4 flex items-center justify-between border-b border-gray-700">
          <div className="flex items-center gap-2">
            <MessageSquare className="w-5 h-5 text-[#00a884]" />
            <h3 className="font-bold text-base">New Chat</h3>
          </div>
          <button onClick={onClose} className="p-1 hover:bg-[#2a3942] rounded-full text-gray-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-3 bg-[#111b21] border-b border-gray-800">
          <div className="relative">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search contacts or enter number..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-[#202c33] text-white text-sm pl-9 pr-4 py-2 rounded-lg border border-gray-700 focus:outline-none focus:border-[#00a884]"
            />
          </div>
        </div>

        <div className="p-2 overflow-y-auto flex-1 divide-y divide-gray-800">
          {filtered.map((c) => (
            <div
              key={c.id}
              onClick={() => {
                onSelectContact(c.id);
                onClose();
              }}
              className="flex items-center gap-3 p-3 rounded-xl cursor-pointer hover:bg-[#202c33] transition-all"
            >
              <img src={c.avatar} alt={c.name} className="w-10 h-10 rounded-full object-cover" />
              <div className="flex-1">
                <div className="flex items-center gap-1 font-semibold text-sm text-gray-100">
                  <span>{c.name}</span>
                  {c.verifiedBadge && <BadgeCheck className="w-4 h-4 text-[#00a884]" />}
                </div>
                <span className="text-xs text-gray-400">{c.phone || 'Contact'}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
