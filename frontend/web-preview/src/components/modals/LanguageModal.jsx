import React from 'react';
import { X, Globe, Check } from 'lucide-react';
import { INDIC_LANGUAGES } from '../../data/mockData';

export default function LanguageModal({ currentLanguage, onSelect, onClose }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
      <div className="bg-white dark:bg-[#111b21] w-full max-w-md rounded-2xl shadow-2xl overflow-hidden border border-gray-200 dark:border-[#222d34]">
        <div className="bg-[#202c33] text-white p-4 flex items-center justify-between border-b border-gray-700">
          <div className="flex items-center gap-2">
            <Globe className="w-5 h-5 text-[#00a884]" />
            <h3 className="font-bold text-base">Select Indic Language</h3>
          </div>
          <button onClick={onClose} className="p-1 hover:bg-[#2a3942] rounded-full text-gray-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-4 grid grid-cols-2 gap-2.5 max-h-[60vh] overflow-y-auto">
          {INDIC_LANGUAGES.map((lang) => {
            const isSelected = currentLanguage === lang.code;
            return (
              <button
                key={lang.code}
                onClick={() => {
                  onSelect(lang);
                  onClose();
                }}
                className={`flex items-center justify-between p-3 rounded-xl border text-left transition-all ${
                  isSelected
                    ? 'border-[#00a884] bg-[#00a884]/15 text-[#00a884] font-bold shadow-sm'
                    : 'border-gray-200 dark:border-[#222d34] bg-gray-50 dark:bg-[#202c33] text-gray-800 dark:text-gray-200 hover:bg-[#2a3942]/30'
                }`}
              >
                <div>
                  <div className="text-sm font-semibold">{lang.native}</div>
                  <div className="text-xs text-gray-400 font-normal">{lang.name}</div>
                </div>
                {isSelected && <Check className="w-4 h-4 text-[#00a884]" />}
              </button>
            );
          })}
        </div>

        <div className="bg-[#202c33] p-3 text-center border-t border-gray-700 text-xs text-gray-400">
          Language choices dynamically re-translate bot clinical responses
        </div>
      </div>
    </div>
  );
}
