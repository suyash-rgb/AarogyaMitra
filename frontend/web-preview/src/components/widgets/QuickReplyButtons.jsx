import React from 'react';
import { ChevronRight } from 'lucide-react';

export default function QuickReplyButtons({ buttons, onSelect }) {
  if (!buttons || !buttons.length) return null;

  return (
    <div className="flex flex-wrap gap-2 mt-3 pt-2 border-t border-gray-200/20">
      {buttons.map((btnText, idx) => (
        <button
          key={idx}
          onClick={() => onSelect(btnText)}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-[#00a884] dark:text-[#00a884] bg-[#00a884]/10 hover:bg-[#00a884]/20 border border-[#00a884]/40 rounded-full transition-all duration-150 active:scale-95 shadow-sm"
        >
          <span>{btnText}</span>
          <ChevronRight className="w-3.5 h-3.5" />
        </button>
      ))}
    </div>
  );
}
