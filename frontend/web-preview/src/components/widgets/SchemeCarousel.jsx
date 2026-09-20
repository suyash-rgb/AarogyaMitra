import React from 'react';
import { Award, FileText, ChevronRight, CheckCircle2 } from 'lucide-react';

export default function SchemeCarousel({ schemes, onViewDetails }) {
  if (!schemes || !schemes.length) return null;

  return (
    <div className="mt-3 mb-1">
      <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-gray-600">
        {schemes.map((scm) => (
          <div
            key={scm.id}
            className="flex-shrink-0 w-[260px] bg-white dark:bg-[#111b21] border border-gray-200 dark:border-[#222d34] rounded-xl p-3.5 shadow-md hover:shadow-lg transition-all flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between gap-1 mb-2">
                <span className={`text-[9px] font-bold px-2 py-0.5 rounded tracking-wide uppercase ${
                  scm.level.includes('CENTRAL')
                    ? 'bg-blue-100 text-blue-700 dark:bg-blue-950 dark:text-blue-300'
                    : 'bg-amber-100 text-amber-700 dark:bg-amber-950 dark:text-amber-300'
                }`}>
                  {scm.level}
                </span>
                <Award className="w-4 h-4 text-[#00a884]" />
              </div>

              <h4 className="text-xs font-bold text-gray-900 dark:text-gray-100 line-clamp-2 mb-1">
                {scm.title}
              </h4>
              <p className="text-[10px] text-gray-500 dark:text-gray-400 font-medium mb-2 line-clamp-1">
                {scm.department}
              </p>
              <p className="text-[11px] text-gray-600 dark:text-gray-300 line-clamp-2 mb-3">
                {scm.description}
              </p>
            </div>

            <button
              onClick={() => onViewDetails(scm)}
              className="w-full flex items-center justify-center gap-1.5 bg-[#202c33] hover:bg-[#2a3942] text-[#00a884] dark:text-[#00a884] py-1.5 px-3 rounded-lg text-xs font-semibold border border-[#00a884]/30 transition-all active:scale-95"
            >
              <FileText className="w-3.5 h-3.5" />
              <span>View Full Scheme Details</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
