import React from 'react';
import { Star, Video, Calendar, ShieldCheck } from 'lucide-react';

export default function DoctorCarousel({ doctors, onBook }) {
  if (!doctors || !doctors.length) return null;

  return (
    <div className="mt-3 mb-1">
      <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-gray-600">
        {doctors.map((doc) => (
          <div
            key={doc.id}
            className="flex-shrink-0 w-[240px] bg-white dark:bg-[#111b21] border border-gray-200 dark:border-[#222d34] rounded-xl p-3 shadow-md hover:shadow-lg transition-all"
          >
            <div className="flex items-center gap-3 mb-2.5">
              <img
                src={doc.avatar}
                alt={doc.name}
                className="w-12 h-12 rounded-full object-cover border-2 border-[#00a884]"
              />
              <div className="overflow-hidden">
                <h4 className="text-sm font-semibold text-gray-900 dark:text-gray-100 truncate flex items-center gap-1">
                  {doc.name}
                  <ShieldCheck className="w-3.5 h-3.5 text-[#00a884] flex-shrink-0" />
                </h4>
                <p className="text-[11px] text-[#00a884] font-medium truncate">{doc.specialty}</p>
                <p className="text-[10px] text-gray-500 dark:text-gray-400">{doc.experience}</p>
              </div>
            </div>

            <div className="flex items-center justify-between text-xs mb-2 bg-gray-50 dark:bg-[#202c33] p-1.5 rounded-md">
              <span className="flex items-center text-amber-500 font-semibold gap-1 text-[11px]">
                <Star className="w-3 h-3 fill-amber-500" />
                {doc.rating} ({doc.reviews})
              </span>
              <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-100 dark:bg-emerald-950 px-1.5 py-0.5 rounded">
                {doc.fees}
              </span>
            </div>

            <div className="text-[11px] text-gray-600 dark:text-gray-300 mb-2.5 flex items-center gap-1">
              <Calendar className="w-3.5 h-3.5 text-gray-400" />
              <span>{doc.availableTime}</span>
            </div>

            <button
              onClick={() => onBook(doc)}
              className="w-full flex items-center justify-center gap-1.5 bg-[#00a884] hover:bg-[#008f6f] text-white py-1.5 px-3 rounded-lg text-xs font-semibold shadow transition-all active:scale-95"
            >
              <Video className="w-3.5 h-3.5" />
              <span>Book Free Call</span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
