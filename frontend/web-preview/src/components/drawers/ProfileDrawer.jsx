import React, { useState } from 'react';
import { X, BadgeCheck, Phone, Globe, Shield, Lock, Languages, Ban, AlertTriangle, ChevronRight, ExternalLink } from 'lucide-react';

export default function ProfileDrawer({ contact, onClose, isOpen }) {
  const [chatLocked, setChatLocked] = useState(false);
  const [autoTranslate, setAutoTranslate] = useState(true);
  const [fullImgOpen, setFullImgOpen] = useState(false);

  if (!contact || !isOpen) return null;

  return (
    <>
      <div
        className="fixed inset-0 z-40 bg-black/40 backdrop-blur-[1px] transition-opacity"
        onClick={onClose}
      />
      <aside
        className={`fixed top-0 right-0 z-50 h-full w-full max-w-sm bg-[#111b21] text-gray-100 border-l border-[#222d34] shadow-2xl transition-transform duration-300 transform flex flex-col ${
          isOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        {/* Drawer Header */}
        <div className="bg-[#202c33] p-4 flex items-center gap-4 border-b border-gray-700">
          <button onClick={onClose} className="p-1 hover:bg-[#2a3942] rounded-full text-gray-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
          <h3 className="font-semibold text-base">Contact info</h3>
        </div>

        {/* Drawer Body */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Avatar & Title */}
          <div className="flex flex-col items-center bg-[#111b21] p-4 rounded-xl border border-[#222d34]">
            <img
              src={contact.avatar}
              alt={contact.name}
              onClick={() => setFullImgOpen(true)}
              className="w-32 h-32 rounded-full object-cover border-4 border-[#00a884] cursor-pointer hover:opacity-90 transition-opacity shadow-lg"
            />
            <h2 className="text-lg font-bold mt-3 flex items-center gap-1.5">
              <span>{contact.name}</span>
              {contact.verifiedBadge && <BadgeCheck className="w-5 h-5 text-[#00a884]" />}
            </h2>
            <p className="text-xs text-[#00a884] font-medium mt-0.5">{contact.phone || '+91 22 2275 0353'}</p>
            {contact.category && (
              <span className="mt-2 text-[11px] bg-[#202c33] text-gray-300 px-3 py-1 rounded-full font-medium border border-gray-700 text-center">
                {contact.category}
              </span>
            )}
          </div>

          {/* About / Website */}
          <div className="bg-[#202c33] p-4 rounded-xl space-y-3 border border-gray-700">
            <div>
              <span className="text-xs text-gray-400 font-semibold uppercase block">About</span>
              <p className="text-sm text-gray-200 mt-1">
                {contact.onlineStatus || 'Official Govt Healthcare Assistant'}
              </p>
            </div>
            {contact.website && (
              <div className="pt-2 border-t border-gray-700">
                <span className="text-xs text-gray-400 font-semibold uppercase block">Official Website</span>
                <a
                  href={contact.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-[#00a884] hover:underline flex items-center gap-1 font-semibold mt-1"
                >
                  <Globe className="w-3.5 h-3.5" />
                  <span>{contact.website}</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            )}
          </div>

          {/* Privacy & Settings Toggles */}
          <div className="bg-[#202c33] rounded-xl overflow-hidden border border-gray-700 divide-y divide-gray-700">
            <div className="p-3.5 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Lock className="w-4 h-4 text-[#00a884]" />
                <div>
                  <div className="text-xs font-semibold text-gray-100">Chat Lock</div>
                  <div className="text-[10px] text-gray-400">Lock and hide this chat on this device</div>
                </div>
              </div>
              <input
                type="checkbox"
                checked={chatLocked}
                onChange={(e) => setChatLocked(e.target.checked)}
                className="accent-[#00a884] w-4 h-4 cursor-pointer"
              />
            </div>

            <div className="p-3.5 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Languages className="w-4 h-4 text-[#00a884]" />
                <div>
                  <div className="text-xs font-semibold text-gray-100">Auto-Translate Messages</div>
                  <div className="text-[10px] text-gray-400">Translate incoming medical replies</div>
                </div>
              </div>
              <input
                type="checkbox"
                checked={autoTranslate}
                onChange={(e) => setAutoTranslate(e.target.checked)}
                className="accent-[#00a884] w-4 h-4 cursor-pointer"
              />
            </div>
          </div>

          {/* Block & Report */}
          <div className="bg-[#202c33] rounded-xl overflow-hidden border border-gray-700 divide-y divide-gray-700 text-xs">
            <button
              onClick={() => alert(`Blocked ${contact.name}`)}
              className="w-full flex items-center gap-3 p-3.5 text-red-400 hover:bg-red-500/10 transition-all font-semibold"
            >
              <Ban className="w-4 h-4" />
              <span>Block {contact.name}</span>
            </button>
            <button
              onClick={() => alert(`Reported ${contact.name}`)}
              className="w-full flex items-center gap-3 p-3.5 text-red-400 hover:bg-red-500/10 transition-all font-semibold"
            >
              <AlertTriangle className="w-4 h-4" />
              <span>Report contact</span>
            </button>
          </div>
        </div>
      </aside>

      {/* Full-screen Image Preview Modal */}
      {fullImgOpen && (
        <div
          className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4 cursor-pointer"
          onClick={() => setFullImgOpen(false)}
        >
          <div className="relative max-w-lg max-h-[80vh]">
            <img src={contact.avatar} alt={contact.name} className="max-w-full max-h-[80vh] rounded-2xl shadow-2xl object-contain" />
            <button
              onClick={() => setFullImgOpen(false)}
              className="absolute top-2 right-2 bg-black/60 text-white p-2 rounded-full"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>
      )}
    </>
  );
}
