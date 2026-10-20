import React, { useEffect, useState, useRef } from 'react';
import { VocabEntry } from '../types';
import { Volume2, X, BookOpen, Globe2, Sparkles, CheckCircle2 } from 'lucide-react';

interface VocabModalProps {
  entry: VocabEntry | null;
  onClose: () => void;
}

export const VocabModal: React.FC<VocabModalProps> = ({ entry, onClose }) => {
  const [playingVi, setPlayingVi] = useState(false);
  const [playingEn, setPlayingEn] = useState(false);
  const audioViRef = useRef<HTMLAudioElement | null>(null);
  const audioEnRef = useRef<HTMLAudioElement | null>(null);

  // Close on Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!entry) return null;

  const playVietnamese = () => {
    if (playingVi) return;
    setPlayingVi(true);

    if (entry.audioVi) {
      if (!audioViRef.current) {
        audioViRef.current = new Audio(entry.audioVi);
      } else {
        audioViRef.current.src = entry.audioVi;
      }

      audioViRef.current.onended = () => setPlayingVi(false);
      audioViRef.current.onerror = () => {
        // Fallback to SpeechSynthesis
        if ('speechSynthesis' in window) {
          const utterance = new SpeechSynthesisUtterance(entry.wordVi);
          utterance.lang = 'vi-VN';
          utterance.onend = () => setPlayingVi(false);
          utterance.onerror = () => setPlayingVi(false);
          window.speechSynthesis.speak(utterance);
        } else {
          setPlayingVi(false);
        }
      };

      audioViRef.current.play().catch(() => {
        // Fallback
        if ('speechSynthesis' in window) {
          const utterance = new SpeechSynthesisUtterance(entry.wordVi);
          utterance.lang = 'vi-VN';
          utterance.onend = () => setPlayingVi(false);
          utterance.onerror = () => setPlayingVi(false);
          window.speechSynthesis.speak(utterance);
        } else {
          setPlayingVi(false);
        }
      });
    }
  };

  const playEnglish = () => {
    if (playingEn) return;
    setPlayingEn(true);

    if (entry.audioEn) {
      if (!audioEnRef.current) {
        audioEnRef.current = new Audio(entry.audioEn);
      } else {
        audioEnRef.current.src = entry.audioEn;
      }

      audioEnRef.current.onended = () => setPlayingEn(false);
      audioEnRef.current.onerror = () => {
        // Fallback to SpeechSynthesis
        if ('speechSynthesis' in window) {
          const primaryEn = entry.meaningsEn[0]?.meaning.split(' (')[0] || '';
          const utterance = new SpeechSynthesisUtterance(primaryEn);
          utterance.lang = 'en-US';
          utterance.onend = () => setPlayingEn(false);
          utterance.onerror = () => setPlayingEn(false);
          window.speechSynthesis.speak(utterance);
        } else {
          setPlayingEn(false);
        }
      };

      audioEnRef.current.play().catch(() => {
        if ('speechSynthesis' in window) {
          const primaryEn = entry.meaningsEn[0]?.meaning.split(' (')[0] || '';
          const utterance = new SpeechSynthesisUtterance(primaryEn);
          utterance.lang = 'en-US';
          utterance.onend = () => setPlayingEn(false);
          utterance.onerror = () => setPlayingEn(false);
          window.speechSynthesis.speak(utterance);
        } else {
          setPlayingEn(false);
        }
      });
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
    >
      <div
        className="relative w-full max-w-lg bg-gradient-to-b from-white to-amber-50 rounded-3xl shadow-2xl border-4 border-amber-300 p-6 md:p-8 transform transition-all animate-scale-up"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          type="button"
          className="absolute top-4 right-4 p-2 text-slate-400 hover:text-rose-600 bg-slate-100 hover:bg-rose-100 rounded-full transition-colors"
          title="Đóng (Phím Esc)"
          aria-label="Đóng popup"
        >
          <X className="w-6 h-6" />
        </button>

        {/* Header Tag */}
        <div className="flex items-center gap-2 mb-3">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-200 text-amber-900 font-bold text-xs uppercase tracking-wider rounded-full">
            <Sparkles className="w-3.5 h-3.5 text-amber-700" />
            Từ vựng lớp 1
          </span>
          <span className="text-xs text-slate-500 font-semibold">
            {entry.partOfSpeech}
          </span>
        </div>

        {/* Vietnamese Word & Audio */}
        <div className="flex items-center justify-between gap-4 pb-4 border-b-2 border-amber-200/60 mb-5">
          <div>
            <h2 className="text-3xl md:text-4xl font-extrabold text-indigo-700 tracking-tight font-heading">
              {entry.wordVi}
            </h2>
          </div>
          <button
            type="button"
            onClick={playVietnamese}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-2xl font-bold text-base transition-all shadow-md ${
              playingVi
                ? 'bg-emerald-500 text-white animate-pulse'
                : 'bg-emerald-100 hover:bg-emerald-200 text-emerald-800 hover:scale-105 active:scale-95'
            }`}
            title="Nghe phát âm tiếng Việt chuẩn"
          >
            <Volume2 className={`w-5 h-5 ${playingVi ? 'animate-bounce' : ''}`} />
            <span>{playingVi ? 'Đang đọc...' : 'Nghe Tiếng Việt'}</span>
          </button>
        </div>

        {/* Vietnamese Meaning for Grade 1 */}
        <div className="mb-6 bg-amber-100/70 p-4 rounded-2xl border border-amber-200">
          <div className="flex items-center gap-2 text-amber-900 font-bold text-sm mb-1.5">
            <BookOpen className="w-4 h-4 text-amber-700" />
            <span>Giải thích cho bé:</span>
          </div>
          <p className="text-slate-800 text-base md:text-lg leading-relaxed font-medium">
            {entry.meaningVi}
          </p>
        </div>

        {/* English Section */}
        <div className="bg-sky-50 p-4 md:p-5 rounded-2xl border border-sky-200 mb-6">
          <div className="flex items-center justify-between gap-2 mb-3">
            <div className="flex items-center gap-2 text-sky-900 font-bold text-sm">
              <Globe2 className="w-4 h-4 text-sky-700" />
              <span>Tiếng Anh tương ứng (ngữ cảnh):</span>
            </div>
            <button
              type="button"
              onClick={playEnglish}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl font-bold text-sm transition-all shadow-sm ${
                playingEn
                  ? 'bg-sky-600 text-white animate-pulse'
                  : 'bg-sky-200 hover:bg-sky-300 text-sky-900 hover:scale-105'
              }`}
              title="Nghe phát âm tiếng Anh chuẩn"
            >
              <Volume2 className="w-4 h-4" />
              <span>{playingEn ? 'Đang phát...' : 'Nghe English'}</span>
            </button>
          </div>

          <div className="space-y-2">
            {entry.meaningsEn.map((item, idx) => (
              <div key={idx} className="flex flex-wrap items-baseline gap-2 bg-white/80 px-3 py-2 rounded-xl">
                <span className="text-xl font-extrabold text-sky-800">
                  {item.meaning}
                </span>
                {item.ipa && (
                  <span className="text-sm font-mono text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md">
                    {item.ipa}
                  </span>
                )}
                <span className="text-xs text-sky-600 italic">
                  ({item.partOfSpeech})
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Footer info & Done button */}
        <div className="flex items-center justify-between pt-2">
          <div className="flex items-center gap-1 text-xs text-emerald-700 font-medium">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>Đã kiểm định sách giáo khoa lớp 1</span>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="px-6 py-2.5 bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-500 hover:to-amber-600 text-slate-900 font-extrabold text-base rounded-2xl shadow-md hover:shadow-lg transition-all active:scale-95 cursor-pointer"
          >
            Đã hiểu rồi!
          </button>
        </div>
      </div>
    </div>
  );
};
