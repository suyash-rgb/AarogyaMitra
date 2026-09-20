import React, { useState, useRef } from 'react';
import { Smile, Paperclip, Mic, Send, Image, FileText, X } from 'lucide-react';
import RecordingBar from './RecordingBar';

export default function InputBar({ onSendMessage, onSendMedia, onSendAudio }) {
  const [text, setText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [showAttachMenu, setShowAttachMenu] = useState(false);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const fileInputRef = useRef(null);
  const docInputRef = useRef(null);

  const emojis = ['👍', '❤️', '🙏', '😊', '🏥', '🩺', '💊', '🚑', '✅', '👋', '😷', '🔥'];

  const handleSend = () => {
    const trimmed = text.trim();
    if (!trimmed) return;
    onSendMessage(trimmed);
    setText('');
    setShowEmojiPicker(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileChange = (e, type) => {
    const file = e.target.files[0];
    if (!file) return;

    const url = URL.createObjectURL(file);
    onSendMedia({
      type,
      name: file.name,
      url,
      size: `${(file.size / 1024).toFixed(1)} KB`
    });
    setShowAttachMenu(false);
  };

  if (isRecording) {
    return (
      <RecordingBar
        onCancel={() => setIsRecording(false)}
        onSendAudio={(audioUrl, duration) => {
          setIsRecording(false);
          onSendAudio(audioUrl, duration);
        }}
      />
    );
  }

  return (
    <div className="relative bg-[#202c33] px-4 py-2.5 flex items-center gap-3 border-t border-gray-700">
      {/* Attachment Popover Menu */}
      {showAttachMenu && (
        <div className="absolute bottom-14 left-10 z-30 bg-[#233138] border border-gray-700 rounded-2xl shadow-2xl p-2 flex flex-col gap-2 animate-fadeIn">
          <button
            onClick={() => fileInputRef.current?.click()}
            className="flex items-center gap-3 px-4 py-2.5 hover:bg-[#182229] text-gray-200 rounded-xl text-xs font-semibold transition-all"
          >
            <div className="w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center text-white">
              <Image className="w-4 h-4" />
            </div>
            <span>Photos & Videos</span>
          </button>
          <button
            onClick={() => docInputRef.current?.click()}
            className="flex items-center gap-3 px-4 py-2.5 hover:bg-[#182229] text-gray-200 rounded-xl text-xs font-semibold transition-all"
          >
            <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white">
              <FileText className="w-4 h-4" />
            </div>
            <span>Document / Medical Record</span>
          </button>
        </div>
      )}

      {/* Hidden File Inputs */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={(e) => handleFileChange(e, 'image')}
        className="hidden"
      />
      <input
        ref={docInputRef}
        type="file"
        accept=".pdf,.doc,.docx,.png,.jpg"
        onChange={(e) => handleFileChange(e, 'document')}
        className="hidden"
      />

      {/* Emoji Picker Popover */}
      {showEmojiPicker && (
        <div className="absolute bottom-14 left-2 z-30 bg-[#233138] border border-gray-700 rounded-2xl shadow-2xl p-3 grid grid-cols-6 gap-2 animate-fadeIn">
          {emojis.map((emoji, idx) => (
            <button
              key={idx}
              onClick={() => setText((prev) => prev + emoji)}
              className="text-xl p-1.5 hover:bg-[#182229] rounded-lg transition-all"
            >
              {emoji}
            </button>
          ))}
        </div>
      )}

      {/* Action Buttons Left */}
      <div className="flex items-center gap-1.5 text-gray-400">
        <button
          onClick={() => {
            setShowEmojiPicker((prev) => !prev);
            setShowAttachMenu(false);
          }}
          className="p-1.5 hover:text-gray-200 hover:bg-[#2a3942] rounded-full transition-all"
        >
          <Smile className="w-6 h-6" />
        </button>

        <button
          onClick={() => {
            setShowAttachMenu((prev) => !prev);
            setShowEmojiPicker(false);
          }}
          className="p-1.5 hover:text-gray-200 hover:bg-[#2a3942] rounded-full transition-all"
        >
          <Paperclip className="w-6 h-6 rotate-45" />
        </button>
      </div>

      {/* Center Input Field */}
      <div className="flex-1 bg-[#2a3942] rounded-lg px-4 py-2 flex items-center border border-transparent focus-within:border-[#00a884] transition-all">
        <input
          type="text"
          placeholder="Type a message"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          className="w-full bg-transparent text-gray-100 text-sm focus:outline-none placeholder-gray-400"
        />
      </div>

      {/* Mic or Send Button */}
      {text.trim() ? (
        <button
          onClick={handleSend}
          title="Send message"
          className="p-2.5 bg-[#00a884] hover:bg-[#008f6f] text-white rounded-full shadow transition-all active:scale-95"
        >
          <Send className="w-5 h-5" />
        </button>
      ) : (
        <button
          onClick={() => setIsRecording(true)}
          title="Record voice note"
          className="p-2.5 text-gray-400 hover:text-gray-100 hover:bg-[#2a3942] rounded-full transition-all"
        >
          <Mic className="w-6 h-6 text-[#00a884]" />
        </button>
      )}
    </div>
  );
}
