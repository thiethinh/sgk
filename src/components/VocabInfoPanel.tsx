import React, { useState, useRef } from 'react';
import { VocabEntry } from '../types';
import { Volume2, BookOpen, Globe2, Bookmark, BookmarkCheck, ArrowRight } from 'lucide-react';

interface VocabInfoPanelProps {
  currentEntry: VocabEntry | null;
  pageVocabEntries: VocabEntry[];
  allEntries: Record<string, VocabEntry>;
  currentPage: number;
  savedWordIds: string[];
  onToggleSave: (entryId: string) => void;
  onSelectWord: (entryId: string) => void;
  onNavigatePage?: (page: number) => void;
}

export const VocabInfoPanel: React.FC<VocabInfoPanelProps> = ({
  currentEntry,
  pageVocabEntries,
  allEntries: _allEntries,
  currentPage,
  savedWordIds,
  onToggleSave,
  onSelectWord,
  onNavigatePage,
}) => {
  const [playingVi, setPlayingVi] = useState(false);
  const [playingEn, setPlayingEn] = useState(false);
  const audioViRef = useRef<HTMLAudioElement | null>(null);
  const audioEnRef = useRef<HTMLAudioElement | null>(null);

  // Active entry must strictly be from current page's vocabulary list
  const activeEntry =
    (currentEntry && pageVocabEntries.some((e) => e.id === currentEntry.id)
      ? currentEntry
      : pageVocabEntries[0]) || null;
  const isSaved = activeEntry ? savedWordIds.includes(activeEntry.id) : false;

  const playVietnamese = () => {
    if (!activeEntry || playingVi) return;
    setPlayingVi(true);

    if (activeEntry.audioVi) {
      if (!audioViRef.current) {
        audioViRef.current = new Audio(activeEntry.audioVi);
      } else {
        audioViRef.current.src = activeEntry.audioVi;
      }

      audioViRef.current.onended = () => setPlayingVi(false);
      audioViRef.current.onerror = () => {
        if ('speechSynthesis' in window) {
          const u = new SpeechSynthesisUtterance(activeEntry.wordVi);
          u.lang = 'vi-VN';
          u.onend = () => setPlayingVi(false);
          u.onerror = () => setPlayingVi(false);
          window.speechSynthesis.speak(u);
        } else {
          setPlayingVi(false);
        }
      };

      audioViRef.current.play().catch(() => {
        if ('speechSynthesis' in window) {
          const u = new SpeechSynthesisUtterance(activeEntry.wordVi);
          u.lang = 'vi-VN';
          u.onend = () => setPlayingVi(false);
          u.onerror = () => setPlayingVi(false);
          window.speechSynthesis.speak(u);
        } else {
          setPlayingVi(false);
        }
      });
    }
  };

  const playEnglish = () => {
    if (!activeEntry || playingEn) return;
    setPlayingEn(true);

    if (activeEntry.audioEn) {
      if (!audioEnRef.current) {
        audioEnRef.current = new Audio(activeEntry.audioEn);
      } else {
        audioEnRef.current.src = activeEntry.audioEn;
      }

      audioEnRef.current.onended = () => setPlayingEn(false);
      audioEnRef.current.onerror = () => {
        if ('speechSynthesis' in window) {
          const primaryEn = activeEntry.meaningsEn[0]?.meaning.split(' (')[0] || '';
          const u = new SpeechSynthesisUtterance(primaryEn);
          u.lang = 'en-US';
          u.onend = () => setPlayingEn(false);
          u.onerror = () => setPlayingEn(false);
          window.speechSynthesis.speak(u);
        } else {
          setPlayingEn(false);
        }
      };

      audioEnRef.current.play().catch(() => {
        if ('speechSynthesis' in window) {
          const primaryEn = activeEntry.meaningsEn[0]?.meaning.split(' (')[0] || '';
          const u = new SpeechSynthesisUtterance(primaryEn);
          u.lang = 'en-US';
          u.onend = () => setPlayingEn(false);
          u.onerror = () => setPlayingEn(false);
          window.speechSynthesis.speak(u);
        } else {
          setPlayingEn(false);
        }
      });
    }
  };

  const playQuickAudio = (e: React.MouseEvent, audioSrc: string) => {
    e.stopPropagation();
    const a = new Audio(audioSrc);
    a.play().catch(() => {});
  };

  return (
    <div className="flex flex-col gap-4 h-full">
      {/* 1. KHUNG THÔNG TIN TỪ NẰM TRÊN CÙNG (TOP VOCAB CARD) */}
      <div className="bg-gradient-to-b from-white via-amber-50/70 to-white rounded-3xl shadow-lg border-3 border-amber-300 p-4 sm:p-5 transition-all duration-200">
        <div className="flex items-center justify-between gap-2 mb-2">
          <span className="inline-flex items-center px-3 py-1 bg-amber-200 text-amber-900 font-extrabold text-xs uppercase tracking-wider rounded-full shadow-xs">
            Từ Vựng Đang Xem
          </span>

          {activeEntry && (
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded-lg border border-slate-200">
                {activeEntry.partOfSpeech}
              </span>

              {/* Bookmark Save Button */}
              <button
                type="button"
                onClick={() => onToggleSave(activeEntry.id)}
                className={`flex items-center gap-1 px-2.5 py-1 rounded-xl text-xs font-black transition-all shadow-xs cursor-pointer ${
                  isSaved
                    ? 'bg-rose-500 text-white hover:bg-rose-600'
                    : 'bg-white hover:bg-rose-50 text-slate-600 hover:text-rose-600 border border-slate-200'
                }`}
                title={isSaved ? 'Đã lưu vào Sổ tay từ vựng (Nhấn để bỏ lưu)' : 'Bấm để lưu vào Sổ tay từ vựng'}
              >
                {isSaved ? (
                  <>
                    <BookmarkCheck className="w-3.5 h-3.5 fill-current" />
                    <span>Đã lưu</span>
                  </>
                ) : (
                  <>
                    <Bookmark className="w-3.5 h-3.5" />
                    <span>Lưu từ này</span>
                  </>
                )}
              </button>
            </div>
          )}
        </div>

        {activeEntry ? (
          <div>
            {/* Vietnamese Word and Audio Buttons */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2.5 pb-2.5 border-b-2 border-amber-200/70 mb-3">
              <div>
                <h2 className="text-2xl sm:text-3xl font-black text-indigo-700 font-heading tracking-tight">
                  {activeEntry.wordVi}
                </h2>
              </div>

              {/* Audio Action Buttons */}
              <div className="flex items-center gap-1.5">
                <button
                  type="button"
                  onClick={playVietnamese}
                  className={`flex items-center gap-1 px-3 py-1.5 rounded-xl font-black text-xs transition-all shadow-xs ${
                    playingVi
                      ? 'bg-emerald-500 text-white animate-pulse'
                      : 'bg-emerald-100 hover:bg-emerald-200 text-emerald-900 hover:scale-105 active:scale-95 cursor-pointer'
                  }`}
                  title="Nghe phát âm tiếng Việt chuẩn"
                >
                  <Volume2 className={`w-3.5 h-3.5 ${playingVi ? 'animate-bounce' : ''}`} />
                  <span>{playingVi ? 'Đang đọc...' : 'Tiếng Việt'}</span>
                </button>

                <button
                  type="button"
                  onClick={playEnglish}
                  className={`flex items-center gap-1 px-3 py-1.5 rounded-xl font-black text-xs transition-all shadow-xs ${
                    playingEn
                      ? 'bg-sky-500 text-white animate-pulse'
                      : 'bg-sky-100 hover:bg-sky-200 text-sky-900 hover:scale-105 active:scale-95 cursor-pointer'
                  }`}
                  title="Nghe phát âm tiếng Anh giọng bản ngữ"
                >
                  <Volume2 className={`w-3.5 h-3.5 ${playingEn ? 'animate-bounce' : ''}`} />
                  <span>{playingEn ? 'Đang đọc...' : 'English'}</span>
                </button>
              </div>
            </div>

            {/* Vietnamese Meaning for Grade 1 */}
            <div className="mb-3 bg-amber-100/80 p-2.5 rounded-2xl border border-amber-200">
              <div className="flex items-center gap-1.5 text-amber-900 font-bold text-xs mb-0.5">
                <BookOpen className="w-3.5 h-3.5 text-amber-700" />
                <span>Nghĩa tiếng Việt:</span>
              </div>
              <p className="text-slate-800 text-sm sm:text-base font-semibold leading-relaxed">
                {activeEntry.meaningVi}
              </p>
            </div>

            {/* Contextual English Translation + IPA */}
            <div className="bg-sky-50/90 p-2.5 rounded-2xl border border-sky-200">
              <div className="flex items-center gap-1.5 text-sky-900 font-bold text-xs mb-1.5">
                <Globe2 className="w-3.5 h-3.5 text-sky-700" />
                <span>Nghĩa tiếng Anh theo ngữ cảnh:</span>
              </div>
              <div className="space-y-1">
                {activeEntry.meaningsEn.map((item, idx) => (
                  <div
                    key={idx}
                    className="flex flex-wrap items-baseline gap-2 bg-white px-2.5 py-1 rounded-xl border border-sky-100 shadow-2xs"
                  >
                    <span className="text-base font-black text-sky-800">
                      {item.meaning}
                    </span>
                    {item.ipa && (
                      <span className="text-xs font-mono text-slate-500 bg-slate-100 px-1.5 py-0.2 rounded-md">
                        {item.ipa}
                      </span>
                    )}
                    <span className="text-[11px] text-sky-600 italic">
                      ({item.partOfSpeech})
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="py-6 px-3 text-center text-slate-500 space-y-2.5">
            <div className="w-12 h-12 bg-amber-100 text-amber-700 rounded-2xl flex items-center justify-center mx-auto shadow-inner">
              <BookOpen className="w-6 h-6" />
            </div>
            <div>
              <p className="font-extrabold text-sm text-slate-800">
                {pageVocabEntries.length === 0
                  ? 'Trang không có từ vựng bài học'
                  : 'Chạm vào từ có viền cam trên trang sách bên trái!'}
              </p>
              <p className="text-xs text-slate-400 mt-1 max-w-xs mx-auto">
                {pageVocabEntries.length === 0
                  ? 'Trang này là phần bìa sách, hướng dẫn hoặc mục lục. Bé hãy chuyển sang các trang bài học để cùng khám phá từ mới nhé!'
                  : 'Khung thông tin từ điển và giọng đọc sẽ hiển thị tại đây.'}
              </p>
            </div>
            {pageVocabEntries.length === 0 && onNavigatePage && (
              <button
                type="button"
                onClick={() => onNavigatePage(1)}
                className="inline-flex items-center gap-1.5 px-3.5 py-2 bg-gradient-to-r from-amber-400 to-orange-400 hover:from-amber-500 hover:to-orange-500 text-slate-900 font-extrabold text-xs rounded-xl shadow-xs hover:scale-105 active:scale-95 cursor-pointer transition-all"
              >
                <span>Đến Bài 1 (Bài 3: C c)</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        )}
      </div>

      {/* 2. GỢI Ý CÁC TỪ MỞ SẴN Ở BÊN DƯỚI (SUGGESTED WORDS LIST) */}
      <div className="bg-white rounded-3xl shadow-md border-3 border-amber-200 p-4 flex-1 flex flex-col">
        <div className="flex items-center justify-between gap-2 mb-2.5">
          <div>
            <h3 className="text-sm font-black text-slate-800 font-heading">
              Gợi Ý Từ Vựng & Hội Thoại (Bài {currentPage})
            </h3>
            <p className="text-[10px] text-slate-400">
              Nhấn vào từ hoặc tranh để xem thông tin & vị trí trên sách
            </p>
          </div>

          <span className="text-xs font-black text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-full border border-emerald-300">
            {pageVocabEntries.length} từ
          </span>
        </div>

        {/* Cards Container */}
        <div className="flex-1 overflow-y-auto space-y-2 max-h-[300px] pr-1 scrollbar-thin">
          {pageVocabEntries.length > 0 ? (
            pageVocabEntries.map((entry) => {
              const isSelected = activeEntry?.id === entry.id;
              const isWordSaved = savedWordIds.includes(entry.id);

              return (
                <div
                  key={entry.id}
                  onClick={() => onSelectWord(entry.id)}
                  className={`p-2.5 rounded-2xl border-2 transition-all cursor-pointer flex items-center justify-between gap-2 ${
                    isSelected
                      ? 'bg-gradient-to-r from-amber-100 to-amber-50 border-amber-400 shadow-sm scale-101 ring-2 ring-amber-300/60'
                      : 'bg-slate-50 hover:bg-amber-50/70 border-slate-200 hover:border-amber-300'
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        onToggleSave(entry.id);
                      }}
                      className={`p-1 rounded-lg transition-colors ${
                        isWordSaved
                          ? 'text-rose-500 hover:text-rose-600 bg-rose-50'
                          : 'text-slate-300 hover:text-rose-500 hover:bg-slate-100'
                      }`}
                      title={isWordSaved ? 'Đã lưu (bấm để bỏ)' : 'Lưu vào sổ tay'}
                    >
                      <Bookmark className={`w-3.5 h-3.5 ${isWordSaved ? 'fill-current' : ''}`} />
                    </button>

                    <div>
                      <div className="flex items-center gap-1.5">
                        <span className="font-black text-sm text-indigo-900 font-heading">
                          {entry.wordVi}
                        </span>
                        <span className="text-xs font-bold text-sky-800">
                          • {entry.meaningsEn[0]?.meaning}
                        </span>
                      </div>
                      <span className="text-[11px] font-mono text-slate-400">
                        {entry.ipa}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-1">
                    <button
                      type="button"
                      onClick={(e) => playQuickAudio(e, entry.audioEn)}
                      className="p-1.5 text-sky-700 hover:text-sky-800 hover:bg-sky-100 bg-white rounded-lg border border-sky-200 shadow-2xs transition-colors cursor-pointer"
                      title="Nghe phát âm tiếng Anh"
                    >
                      <Volume2 className="w-3.5 h-3.5" />
                    </button>
                    <ArrowRight className="w-3.5 h-3.5 text-amber-500 opacity-60" />
                  </div>
                </div>
              );
            })
          ) : (
            <div className="py-6 text-center text-slate-400 text-xs">
              Trang này chưa có mục từ vựng nổi bật. Bé có thể chuyển sang trang bài học tiếp theo nhé!
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
