import React, { useEffect, useRef } from 'react';
import { Copy, Forward, Share2, Trash2 } from 'lucide-react';

export default function ContextMenu({ x, y, message, onClose, onCopy, onForward, onShare }) {
  const menuRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        onClose();
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [onClose]);

  if (!message) return null;

  return (
    <div
      ref={menuRef}
      style={{ top: `${y}px`, left: `${x}px` }}
      className="fixed z-50 w-48 bg-[#233138] text-gray-200 rounded-lg shadow-2xl py-1 border border-gray-700 animate-fadeIn text-xs"
    >
      <button
        onClick={() => {
          onCopy(message);
          onClose();
        }}
        className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-[#182229] transition-all text-left"
      >
        <Copy className="w-4 h-4 text-gray-400" />
        <span>Copy message text</span>
      </button>

      <button
        onClick={() => {
          onForward(message);
          onClose();
        }}
        className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-[#182229] transition-all text-left"
      >
        <Forward className="w-4 h-4 text-gray-400" />
        <span>Forward message</span>
      </button>

      <button
        onClick={() => {
          onShare(message);
          onClose();
        }}
        className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-[#182229] transition-all text-left"
      >
        <Share2 className="w-4 h-4 text-gray-400" />
        <span>Share message</span>
      </button>
    </div>
  );
}
