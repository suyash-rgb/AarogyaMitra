import React, { useState, useRef } from 'react';
import { CheckCheck, Play, Pause, FileText, Image, Forward, Volume2 } from 'lucide-react';
import FormattedMarkdownText from './FormattedMarkdownText';
import QuickReplyButtons from '../widgets/QuickReplyButtons';
import DoctorCarousel from '../widgets/DoctorCarousel';
import BookingTicket from '../widgets/BookingTicket';
import FacilityCarousel from '../widgets/FacilityCarousel';
import SchemeCarousel from '../widgets/SchemeCarousel';
import { formatAudioDuration } from '../../utils/audio';

export default function MessageBubble({
  msg,
  onQuickReplySelect,
  onBookDoctor,
  onViewSchemeDetails,
  onContextMenu
}) {
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [audioProgress, setAudioProgress] = useState(0);
  const audioRef = useRef(null);

  const isUser = msg.sender === 'user';

  const handleAudioPlayPause = () => {
    if (!audioRef.current) return;
    if (isPlayingAudio) {
      audioRef.current.pause();
      setIsPlayingAudio(false);
    } else {
      audioRef.current.play();
      setIsPlayingAudio(true);
    }
  };

  const handleTimeUpdate = () => {
    if (!audioRef.current) return;
    const current = audioRef.current.currentTime;
    const total = audioRef.current.duration || msg.audioDuration || 1;
    setAudioProgress((current / total) * 100);
  };

  const handleAudioEnded = () => {
    setIsPlayingAudio(false);
    setAudioProgress(0);
  };

  return (
    <div
      onContextMenu={(e) => {
        e.preventDefault();
        onContextMenu(e, msg);
      }}
      className={`flex flex-col my-1 relative group animate-fadeIn ${
        isUser ? 'items-end' : 'items-start'
      }`}
    >
      {/* Bubble Container */}
      <div
        className={`max-w-[85%] md:max-w-[70%] rounded-xl p-3 shadow-md relative border ${
          isUser
            ? 'bg-[#005c4b] text-gray-100 border-[#005c4b] rounded-tr-none'
            : 'bg-[#202c33] text-gray-100 border-[#222d34] rounded-tl-none'
        }`}
      >
        {/* Forwarded Tag */}
        {msg.isForwarded && (
          <div className="flex items-center gap-1 text-[10px] text-gray-400 italic mb-1">
            <Forward className="w-3 h-3 text-[#00a884]" />
            <span>Forwarded</span>
          </div>
        )}

        {/* Audio Message Bubble */}
        {msg.audioUrl ? (
          <div className="flex items-center gap-3 py-1 px-1 min-w-[220px]">
            <audio
              ref={audioRef}
              src={msg.audioUrl}
              onTimeUpdate={handleTimeUpdate}
              onEnded={handleAudioEnded}
              className="hidden"
            />
            <button
              onClick={handleAudioPlayPause}
              className="w-10 h-10 rounded-full bg-[#00a884] text-white flex items-center justify-center shadow hover:opacity-90 transition-all flex-shrink-0"
            >
              {isPlayingAudio ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5 ml-0.5" />}
            </button>
            <div className="flex-1 space-y-1">
              {/* Waveform Bar Graphic */}
              <div className="flex items-center gap-0.5 h-4">
                {[50, 80, 40, 95, 30, 70, 85, 45, 60, 90, 35, 75, 50, 90, 40].map((h, idx) => {
                  const barProgress = (idx / 15) * 100;
                  const isFilled = barProgress <= audioProgress;
                  return (
                    <span
                      key={idx}
                      style={{ height: `${h}%` }}
                      className={`w-1 rounded-full transition-colors ${
                        isFilled ? 'bg-[#00a884]' : 'bg-gray-600'
                      }`}
                    />
                  );
                })}
              </div>
              <div className="flex justify-between text-[10px] text-gray-400 font-mono">
                <span>{formatAudioDuration(msg.audioDuration || 3)}</span>
                <span className="flex items-center gap-0.5">
                  <Volume2 className="w-3 h-3 text-[#00a884]" /> Voice note
                </span>
              </div>
            </div>
          </div>
        ) : null}

        {/* Media Attachments (Photo / Doc) */}
        {msg.media && (
          <div className="mb-2 rounded-lg overflow-hidden border border-gray-700">
            {msg.media.type === 'image' ? (
              <img src={msg.media.url} alt={msg.media.name} className="max-h-60 w-full object-cover rounded" />
            ) : (
              <div className="flex items-center gap-3 p-3 bg-[#111b21] rounded">
                <FileText className="w-8 h-8 text-[#00a884]" />
                <div className="overflow-hidden">
                  <p className="text-xs font-semibold text-gray-200 truncate">{msg.media.name}</p>
                  <p className="text-[10px] text-gray-400">{msg.media.size || 'Document'}</p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Text Body */}
        {msg.text && <FormattedMarkdownText text={msg.text} />}

        {/* Embedded Specialized Healthcare Widgets */}
        {msg.schemes && (
          <SchemeCarousel schemes={msg.schemes} onViewDetails={onViewSchemeDetails} />
        )}

        {msg.facilities && (
          <FacilityCarousel facilities={msg.facilities} />
        )}

        {msg.doctors && (
          <DoctorCarousel doctors={msg.doctors} onBook={onBookDoctor} />
        )}

        {msg.bookingData && (
          <BookingTicket bookingData={msg.bookingData} />
        )}

        {/* Quick Action Reply Buttons */}
        {msg.quickReplies && (
          <QuickReplyButtons buttons={msg.quickReplies} onSelect={onQuickReplySelect} />
        )}

        {/* Timestamp & Read Status Footer */}
        <div className="flex items-center justify-end gap-1 text-[10px] text-gray-400 mt-1 select-none">
          <span>{msg.timestamp || '11:45 AM'}</span>
          {isUser && <CheckCheck className="w-3.5 h-3.5 text-[#53bdeb]" />}
        </div>
      </div>
    </div>
  );
}
