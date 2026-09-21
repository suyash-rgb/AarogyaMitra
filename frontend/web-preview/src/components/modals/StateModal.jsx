import React, { useState } from 'react';
import { X, MapPin, Search, Check } from 'lucide-react';
import { INDIAN_STATES } from '../../data/mockData';

export default function StateModal({ currentState, onSelect, onClose }) {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredStates = INDIAN_STATES.filter((st) =>
    st.toLowerCase().includes(searchTerm.toLowerCase().trim())
  );

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
      <div className="bg-white dark:bg-[#111b21] w-full max-w-md rounded-2xl shadow-2xl overflow-hidden border border-gray-200 dark:border-[#222d34] flex flex-col max-h-[80vh]">
        <div className="bg-[#202c33] text-white p-4 flex items-center justify-between border-b border-gray-700">
          <div className="flex items-center gap-2">
            <MapPin className="w-5 h-5 text-[#00a884]" />
            <h3 className="font-bold text-base">Select Your State / UT</h3>
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
              placeholder="Search 36 States & UTs..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-[#202c33] text-white text-sm pl-9 pr-4 py-2 rounded-lg border border-gray-700 focus:outline-none focus:border-[#00a884]"
            />
          </div>
        </div>

        <div className="p-3 overflow-y-auto flex-1 divide-y divide-gray-100 dark:divide-gray-800">
          {filteredStates.map((st) => {
            const isSelected = currentState === st;
            return (
              <button
                key={st}
                onClick={() => {
                  onSelect(st);
                  onClose();
                }}
                className={`w-full flex items-center justify-between py-2.5 px-3 text-left rounded-lg transition-all ${
                  isSelected
                    ? 'bg-[#00a884]/15 text-[#00a884] font-bold'
                    : 'text-gray-800 dark:text-gray-200 hover:bg-[#202c33]'
                }`}
              >
                <span className="text-sm">{st}</span>
                {isSelected && <Check className="w-4 h-4 text-[#00a884]" />}
              </button>
            );
          })}
        </div>

        <div className="bg-[#202c33] p-3 text-center border-t border-gray-700 text-xs text-gray-400">
          State selection filter tailors government health schemes
        </div>
      </div>
    </div>
  );
}
