import React from 'react';
import { MapPin, Navigation, Phone, ShieldCheck } from 'lucide-react';

export default function FacilityCarousel({ facilities }) {
  if (!facilities || !facilities.length) return null;

  return (
    <div className="mt-3 mb-1">
      <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-gray-600">
        {facilities.map((fac) => (
          <div
            key={fac.id}
            className="flex-shrink-0 w-[260px] bg-white dark:bg-[#111b21] border border-gray-200 dark:border-[#222d34] rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-all"
          >
            <div className="relative h-28 w-full">
              <img
                src={fac.image}
                alt={fac.name}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
              <span className="absolute top-2 left-2 text-[9px] font-extrabold bg-red-600 text-white px-2 py-0.5 rounded shadow tracking-wider uppercase">
                {fac.statusBadge}
              </span>
              <span className="absolute bottom-1.5 left-2 text-[11px] font-semibold text-white flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5 text-[#00a884]" />
                {fac.distanceKm}
              </span>
            </div>

            <div className="p-3">
              <h4 className="text-xs font-bold text-gray-900 dark:text-gray-100 line-clamp-1 mb-0.5" title={fac.name}>
                {fac.name}
              </h4>
              <p className="text-[10px] text-[#00a884] font-medium mb-1.5">{fac.tier}</p>
              
              <div className="flex flex-wrap gap-1 mb-2.5">
                {fac.services.map((srv, idx) => (
                  <span
                    key={idx}
                    className="text-[9px] bg-gray-100 dark:bg-[#202c33] text-gray-700 dark:text-gray-300 px-1.5 py-0.5 rounded font-medium"
                  >
                    {srv}
                  </span>
                ))}
              </div>

              <div className="flex items-center justify-between gap-2 pt-2 border-t border-gray-100 dark:border-[#222d34]">
                <a
                  href={`https://www.google.com/maps/search/?api=1&query=${fac.lat},${fac.lon}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 flex items-center justify-center gap-1.5 bg-[#00a884] hover:bg-[#008f6f] text-white py-1.5 rounded-lg text-xs font-semibold transition-all active:scale-95"
                >
                  <Navigation className="w-3.5 h-3.5" />
                  <span>Navigate in Maps</span>
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
