import React, { useState } from 'react';
import { X, Send, BadgeCheck, Search } from 'lucide-react';

export default function ForwardModal({ chats, messageToForward, onConfirmForward, onClose }) {
  const [selectedChatIds, setSelectedChatIds] = useState([]);
  const [search, setSearch] = useState('');

  if (!messageToForward) return null;

  const toggleSelect = (id) => {
    setSelectedChatIds((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    );
  };

  const handleForward = () => {
    if (!selectedChatIds.length) return;
    onConfirmForward(selectedChatIds, messageToForward);
    onClose();
  };

  const filteredChats = chats.filter((c) =>
    c.name.toLowerCase().includes(search.toLowerCase().trim())
  );

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
      <div className="bg-[#111b21] w-full max-w-md rounded-2xl shadow-2xl overflow-hidden border border-[#222d34] flex flex-col max-h-[80vh]">
        <div className="bg-[#202c33] text-white p-4 flex items-center justify-between border-b border-gray-700">
          <h3 className="font-bold text-base">Forward Message To...</h3>
          <button onClick={onClose} className="p-1 hover:bg-[#2a3942] rounded-full text-gray-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-3 bg-[#111b21] border-b border-gray-800">
          <div className="relative">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search contacts..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-[#202c33] text-white text-sm pl-9 pr-4 py-2 rounded-lg border border-gray-700 focus:outline-none focus:border-[#00a884]"
            />
          </div>
        </div>

        <div className="p-2 overflow-y-auto flex-1 divide-y divide-gray-800">
          {filteredChats.map((c) => {
            const isSelected = selectedChatIds.includes(c.id);
            return (
              <div
                key={c.id}
                onClick={() => toggleSelect(c.id)}
                className={`flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-all ${
                  isSelected ? 'bg-[#00a884]/20 border border-[#00a884]' : 'hover:bg-[#202c33]'
                }`}
              >
                <img src={c.avatar} alt={c.name} className="w-10 h-10 rounded-full object-cover" />
                <div className="flex-1">
                  <div className="flex items-center gap-1 font-semibold text-sm text-gray-100">
                    <span>{c.name}</span>
                    {c.verifiedBadge && <BadgeCheck className="w-4 h-4 text-[#00a884]" />}
                  </div>
                  <span className="text-xs text-gray-400">{c.onlineStatus || 'Contact'}</span>
                </div>
                <input
                  type="checkbox"
                  checked={isSelected}
                  onChange={() => {}}
                  className="accent-[#00a884] w-4 h-4"
                />
              </div>
            );
          })}
        </div>

        <div className="bg-[#202c33] p-4 flex justify-between items-center border-t border-gray-700">
          <span className="text-xs text-gray-400">
            {selectedChatIds.length} contact{selectedChatIds.length === 1 ? '' : 's'} selected
          </span>
          <button
            disabled={!selectedChatIds.length}
            onClick={handleForward}
            className="flex items-center gap-2 bg-[#00a884] disabled:opacity-40 hover:bg-[#008f6f] text-white px-4 py-2 rounded-lg text-xs font-bold transition-all"
          >
            <Send className="w-4 h-4" />
            <span>Forward Now</span>
          </button>
        </div>
      </div>
    </div>
  );
}
