import React, { useState } from 'react';
import { ArrowLeft, Moon, MapPin, Globe, Bot, ChevronRight, MessageSquare } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

export default function SettingsDrawer({
  isOpen,
  onClose,
  onOpenThemeModal,
  onOpenStateModal,
  onOpenLanguageModal,
  onSelectChat,
  currentState,
  currentLanguageObj
}) {
  const [view, setView] = useState('main'); // 'main' | 'chats'
  const { theme } = useTheme();

  if (!isOpen) return null;

  const handleBack = () => {
    if (view === 'chats') {
      setView('main');
    } else {
      onClose();
    }
  };

  const getThemeLabel = (t) => {
    if (t === 'dark') return 'Dark';
    if (t === 'light') return 'Light';
    return 'System default';
  };

  return (
    <div className="absolute inset-0 z-30 bg-white dark:bg-[#111b21] flex flex-col h-full animate-fadeIn select-none border-r border-gray-200 dark:border-[#222d34]">
      {/* Header */}
      <div className="bg-gray-100 dark:bg-[#202c33] text-gray-800 dark:text-gray-100 px-4 py-4 flex items-center gap-4 border-b border-gray-200 dark:border-gray-700">
        <button
          onClick={handleBack}
          className="p-1 hover:bg-gray-200 dark:hover:bg-[#2a3942] rounded-full text-gray-600 dark:text-gray-300 transition-all"
          title="Back"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <h2 className="text-base font-semibold">
          {view === 'main' ? 'Settings' : 'Chats'}
        </h2>
      </div>

      {/* Content View */}
      <div className="flex-1 overflow-y-auto divide-y divide-gray-100 dark:divide-[#222d34]/60">
        {view === 'main' ? (
          <>
            {/* User Profile Card */}
            <div className="p-4 flex items-center gap-4 bg-gray-50 dark:bg-[#111b21]">
              <img
                src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80"
                alt="Leo (You)"
                className="w-16 h-16 rounded-full object-cover border-2 border-[#00a884]"
              />
              <div>
                <h3 className="font-semibold text-base text-gray-900 dark:text-gray-100">Leo (You)</h3>
                <p className="text-xs text-gray-500 dark:text-gray-400">Available • Healthcare Active</p>
              </div>
            </div>

            {/* Menu Options */}
            <div className="py-2">
              <button
                onClick={() => setView('chats')}
                className="w-full flex items-center justify-between px-5 py-3.5 hover:bg-gray-100 dark:hover:bg-[#202c33] transition-all text-left group"
              >
                <div className="flex items-center gap-4">
                  <MessageSquare className="w-5 h-5 text-gray-500 dark:text-gray-400 group-hover:text-[#00a884]" />
                  <div>
                    <div className="text-sm font-medium text-gray-800 dark:text-gray-200">Chats</div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">Theme, wallpaper, chat history</div>
                  </div>
                </div>
                <ChevronRight className="w-4 h-4 text-gray-400" />
              </button>

              <button
                onClick={() => {
                  onOpenStateModal();
                }}
                className="w-full flex items-center justify-between px-5 py-3.5 hover:bg-gray-100 dark:hover:bg-[#202c33] transition-all text-left group"
              >
                <div className="flex items-center gap-4">
                  <MapPin className="w-5 h-5 text-gray-500 dark:text-gray-400 group-hover:text-[#00a884]" />
                  <div>
                    <div className="text-sm font-medium text-gray-800 dark:text-gray-200">State / Region</div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">{currentState}</div>
                  </div>
                </div>
                <ChevronRight className="w-4 h-4 text-gray-400" />
              </button>

              <button
                onClick={() => {
                  onOpenLanguageModal();
                }}
                className="w-full flex items-center justify-between px-5 py-3.5 hover:bg-gray-100 dark:hover:bg-[#202c33] transition-all text-left group"
              >
                <div className="flex items-center gap-4">
                  <Globe className="w-5 h-5 text-gray-500 dark:text-gray-400 group-hover:text-[#00a884]" />
                  <div>
                    <div className="text-sm font-medium text-gray-800 dark:text-gray-200">App Language</div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">{currentLanguageObj?.name || 'English'}</div>
                  </div>
                </div>
                <ChevronRight className="w-4 h-4 text-gray-400" />
              </button>

              <button
                onClick={() => {
                  onSelectChat('ai-bot');
                  onClose();
                }}
                className="w-full flex items-center justify-between px-5 py-3.5 hover:bg-gray-100 dark:hover:bg-[#202c33] transition-all text-left group border-t border-gray-100 dark:border-[#222d34]"
              >
                <div className="flex items-center gap-4">
                  <Bot className="w-5 h-5 text-[#00a884]" />
                  <div>
                    <div className="text-sm font-medium text-[#00a884]">AarogyaMitra Assistant</div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">Open primary medical consultation</div>
                  </div>
                </div>
                <ChevronRight className="w-4 h-4 text-gray-400" />
              </button>
            </div>
          </>
        ) : (
          /* Chats Settings View */
          <div className="py-2">
            <button
              onClick={onOpenThemeModal}
              className="w-full flex items-center justify-between px-5 py-3.5 hover:bg-gray-100 dark:hover:bg-[#202c33] transition-all text-left group"
            >
              <div className="flex items-center gap-4">
                <Moon className="w-5 h-5 text-gray-500 dark:text-gray-400 group-hover:text-[#00a884]" />
                <div>
                  <div className="text-sm font-medium text-gray-800 dark:text-gray-200">Theme</div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">{getThemeLabel(theme)}</div>
                </div>
              </div>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
