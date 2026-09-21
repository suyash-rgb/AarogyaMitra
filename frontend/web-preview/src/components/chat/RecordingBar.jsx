import React, { useState, useEffect, useRef } from 'react';
import { Trash2, Pause, Play, Send } from 'lucide-react';
import { formatAudioDuration } from '../../utils/audio';

export default function RecordingBar({ onCancel, onSendAudio }) {
  const [duration, setDuration] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);

  useEffect(() => {
    // Start recording audio via Browser MediaRecorder API if available
    async function startMediaRecorder() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;

        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data);
          }
        };

        mediaRecorder.start();
      } catch (err) {
        console.warn('Microphone access unavailable or denied:', err);
      }
    }

    startMediaRecorder();

    // Timer interval
    timerRef.current = setInterval(() => {
      setDuration((prev) => prev + 1);
    }, 1000);

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop();
      }
    };
  }, []);

  const handlePauseResume = () => {
    if (!mediaRecorderRef.current) return;
    if (isPaused) {
      mediaRecorderRef.current.resume();
      timerRef.current = setInterval(() => setDuration((prev) => prev + 1), 1000);
      setIsPaused(false);
    } else {
      mediaRecorderRef.current.pause();
      if (timerRef.current) clearInterval(timerRef.current);
      setIsPaused(true);
    }
  };

  const handleFinish = () => {
    if (timerRef.current) clearInterval(timerRef.current);

    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        const audioUrl = URL.createObjectURL(audioBlob);
        onSendAudio(audioUrl, duration);
      };
      mediaRecorderRef.current.stop();
    } else {
      // Fallback synthetic audio duration
      onSendAudio(null, duration || 3);
    }
  };

  return (
    <div className="bg-[#202c33] px-4 py-2.5 flex items-center justify-between gap-4 border-t border-gray-700 animate-fadeIn">
      {/* Trash / Cancel */}
      <button
        onClick={onCancel}
        title="Discard recording"
        className="p-2 text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded-full transition-all"
      >
        <Trash2 className="w-5 h-5" />
      </button>

      {/* Recording Duration Timer */}
      <div className="flex items-center gap-2">
        <span className="w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse" />
        <span className="text-sm font-mono font-bold text-gray-100">
          {formatAudioDuration(duration)}
        </span>
      </div>

      {/* Animated Audio Waveform Bars */}
      <div className="flex-1 flex items-center justify-center gap-1 h-6 px-4 overflow-hidden">
        {[40, 75, 25, 90, 50, 80, 30, 95, 60, 45, 85, 35, 70, 90, 40, 65, 80].map((h, i) => (
          <span
            key={i}
            style={{ height: isPaused ? '20%' : `${h}%` }}
            className="w-1 bg-[#00a884] rounded-full transition-all duration-300 animate-pulse"
          />
        ))}
      </div>

      {/* Pause / Resume */}
      <button
        onClick={handlePauseResume}
        title={isPaused ? 'Resume recording' : 'Pause recording'}
        className="p-2 text-gray-300 hover:text-white hover:bg-[#2a3942] rounded-full transition-all"
      >
        {isPaused ? <Play className="w-5 h-5" /> : <Pause className="w-5 h-5" />}
      </button>

      {/* Green Send Audio */}
      <button
        onClick={handleFinish}
        title="Send voice note"
        className="p-2.5 bg-[#00a884] hover:bg-[#008f6f] text-white rounded-full shadow-lg transition-all active:scale-95"
      >
        <Send className="w-5 h-5" />
      </button>
    </div>
  );
}
