import React from 'react';
import { CheckCircle2, Calendar, Clock, UserCheck, Shield, PhoneCall } from 'lucide-react';

export default function BookingTicket({ bookingData }) {
  if (!bookingData) return null;

  const { doctor, ticketNo, date, time, abhaToken } = bookingData;

  return (
    <div className="my-2 max-w-sm bg-gradient-to-br from-[#00382B] to-[#0b141a] text-white rounded-xl p-4 border border-[#00a884]/40 shadow-xl relative overflow-hidden">
      {/* Background watermark badge */}
      <div className="absolute -right-4 -bottom-4 opacity-10 text-white pointer-events-none">
        <Shield className="w-32 h-32" />
      </div>

      <div className="flex items-center justify-between border-b border-[#00a884]/30 pb-2 mb-3">
        <div className="flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 text-[#00a884]" />
          <span className="font-bold text-sm tracking-wide text-white">APPOINTMENT CONFIRMED</span>
        </div>
        <span className="text-[10px] bg-[#00a884] text-white px-2 py-0.5 rounded font-bold uppercase tracking-wider">
          FREE GOVT OP
        </span>
      </div>

      <div className="flex items-center gap-3 mb-3">
        <img
          src={doctor.avatar}
          alt={doctor.name}
          className="w-12 h-12 rounded-full object-cover border-2 border-[#00a884]"
        />
        <div>
          <h4 className="font-bold text-sm text-white">{doctor.name}</h4>
          <p className="text-xs text-[#00a884] font-medium">{doctor.specialty}</p>
          <p className="text-[11px] text-gray-300">{doctor.hospital}</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-2 bg-[#111b21]/70 p-2.5 rounded-lg border border-[#00a884]/20 text-xs mb-3">
        <div>
          <span className="text-[10px] text-gray-400 block uppercase font-semibold">Date & Time</span>
          <span className="font-medium text-white flex items-center gap-1 mt-0.5">
            <Calendar className="w-3 h-3 text-[#00a884]" />
            {date || 'Today'}, {time || doctor.availableTime}
          </span>
        </div>
        <div>
          <span className="text-[10px] text-gray-400 block uppercase font-semibold">ABHA Health ID</span>
          <span className="font-mono text-[#00a884] font-bold text-[11px] block mt-0.5">
            {abhaToken || 'ABHA-9182-4412-0091'}
          </span>
        </div>
      </div>

      <div className="flex items-center justify-between text-[11px] text-gray-300">
        <span className="flex items-center gap-1">
          <UserCheck className="w-3.5 h-3.5 text-[#00a884]" />
          Status: <strong className="text-emerald-400">Confirmed</strong>
        </span>
        <button
          onClick={() => alert(`Initiating video tele-consult with ${doctor.name}...`)}
          className="flex items-center gap-1 text-[#00a884] hover:underline font-semibold"
        >
          <PhoneCall className="w-3 h-3" />
          Join Room
        </button>
      </div>
    </div>
  );
}
