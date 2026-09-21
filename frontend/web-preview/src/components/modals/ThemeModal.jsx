import React, { useState } from 'react';
import { useTheme } from '../../context/ThemeContext';

export default function ThemeModal({ onClose }) {
  const { theme, setTheme } = useTheme();
  const [selectedTheme, setSelectedTheme] = useState(theme);

  const handleSave = () => {
    setTheme(selectedTheme);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fadeIn">
      <div className="bg-white dark:bg-[#222e35] text-gray-900 dark:text-gray-100 w-full max-w-sm rounded-lg shadow-2xl overflow-hidden border border-gray-200 dark:border-gray-700">
        <div className="p-6">
          <h3 className="text-lg font-medium mb-4 text-gray-900 dark:text-[#e9edef]">Theme</h3>

          <div className="space-y-4">
            <label className="flex items-center gap-3 cursor-pointer group">
              <input
                type="radio"
                name="theme"
                value="system"
                checked={selectedTheme === 'system'}
                onChange={() => setSelectedTheme('system')}
                className="w-4 h-4 accent-[#00a884] focus:ring-[#00a884]"
              />
              <span className="text-sm font-normal text-gray-700 dark:text-[#d1d7db] group-hover:text-gray-900 dark:group-hover:text-white">
                System default
              </span>
            </label>

            <label className="flex items-center gap-3 cursor-pointer group">
              <input
                type="radio"
                name="theme"
                value="light"
                checked={selectedTheme === 'light'}
                onChange={() => setSelectedTheme('light')}
                className="w-4 h-4 accent-[#00a884] focus:ring-[#00a884]"
              />
              <span className="text-sm font-normal text-gray-700 dark:text-[#d1d7db] group-hover:text-gray-900 dark:group-hover:text-white">
                Light
              </span>
            </label>

            <label className="flex items-center gap-3 cursor-pointer group">
              <input
                type="radio"
                name="theme"
                value="dark"
                checked={selectedTheme === 'dark'}
                onChange={() => setSelectedTheme('dark')}
                className="w-4 h-4 accent-[#00a884] focus:ring-[#00a884]"
              />
              <span className="text-sm font-normal text-gray-700 dark:text-[#d1d7db] group-hover:text-gray-900 dark:group-hover:text-white">
                Dark
              </span>
            </label>
          </div>
        </div>

        <div className="px-6 py-4 bg-gray-50 dark:bg-[#111b21] flex justify-end gap-3 border-t border-gray-200 dark:border-[#222d34]">
          <button
            onClick={onClose}
            className="px-4 py-1.5 text-xs font-medium text-[#00a884] hover:bg-[#00a884]/10 rounded-full transition-all"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="px-5 py-1.5 text-xs font-medium bg-[#00a884] text-white hover:bg-[#008f70] rounded-full transition-all shadow-sm"
          >
            OK
          </button>
        </div>
      </div>
    </div>
  );
}
