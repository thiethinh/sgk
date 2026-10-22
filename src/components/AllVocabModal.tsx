import React, { useState, useEffect } from 'react';
import { VocabEntry } from '../types';
import { playAudio, stopAllAudio } from '../utils/audioPlayer';

interface AllVocabModalProps {
  entries: Record<string, VocabEntry>;
  isOpen: boolean;
  onClose: () => void;
  onSelectWord: (entryId: string) => void;
}

export const AllVocabModal: React.FC<AllVocabModalProps> = ({
  entries,
  isOpen,
  onClose,
  onSelectWord,
}) => {
  const [searchTerm, setSearchTerm] = useState('');

  // Stop audio on unmount or close
  useEffect(() => {
    return () => {
      stopAllAudio();
    };
  }, []);

  if (!isOpen) return null;

  const allList = Object.values(entries);

  const filteredList = allList.filter((item) => {
    const term = searchTerm.toLowerCase().trim();
    if (!term) return true;
    return (
      item.wordVi.toLowerCase().includes(term) ||
      item.meaningVi.toLowerCase().includes(term) ||
      item.meaningsEn.some((en) => en.meaning.toLowerCase().includes(term))
    );
  });

  const playQuickAudio = (e: React.MouseEvent, audioSrc: string) => {
    e.stopPropagation();
    playAudio(audioSrc);
  };

  const handleClose = () => {
    stopAllAudio();
    onClose();
  };

  return (
    <div
      className="fixed inset-0 z-[60] flex items-center justify-center p-3 sm:p-4 bg-slate-900/50 backdrop-blur-xs animate-fade-in"
      onClick={handleClose}
      role="dialog"
      aria-modal="true"
    >
      <div
        className="relative w-full max-w-3xl max-h-[85vh] flex flex-col bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header - Chỉ dùng chữ, không dùng icon */}
        <div className="px-5 py-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <div>
            <h2 className="text-lg sm:text-xl font-bold text-slate-900 tracking-tight">
              Sổ Tay Từ Vựng
            </h2>
            <p className="text-xs text-slate-500 font-medium">
              Tra cứu và nghe phát âm toàn bộ từ vựng, câu hội thoại trong các bài học
            </p>
          </div>
          <button
            onClick={handleClose}
            type="button"
            className="px-3 py-1.5 text-xs font-semibold text-slate-600 hover:text-slate-900 bg-slate-200/70 hover:bg-slate-300 rounded-lg transition-colors cursor-pointer"
            title="Đóng (Esc)"
          >
            Đóng
          </button>
        </div>

        {/* Search Bar & Counter - Chỉ dùng ô nhập chữ, không dùng icon */}
        <div className="px-5 py-3 bg-white border-b border-slate-100 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <div className="relative flex-1 max-w-sm">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Tìm kiếm từ tiếng Việt, tiếng Anh..."
              className="w-full px-3 py-1.5 bg-slate-50 hover:bg-white focus:bg-white border border-slate-200 focus:border-indigo-500 rounded-lg text-xs font-medium text-slate-800 placeholder-slate-400 transition-colors focus:outline-none"
            />
          </div>

          <div className="text-xs font-semibold text-slate-500 shrink-0">
            Tổng số: <span className="font-bold text-slate-800">{filteredList.length}</span> / {allList.length} từ
          </div>
        </div>

        {/* Words Grid - Chỉ hiển thị nội dung chữ, không dùng icon */}
        <div className="p-4 sm:p-5 overflow-y-auto flex-1 grid grid-cols-1 sm:grid-cols-2 gap-3 scrollbar-thin bg-slate-50/50">
          {filteredList.map((entry) => (
            <div
              key={entry.id}
              onClick={() => {
                handleClose();
                onSelectWord(entry.id);
              }}
              className="group p-3.5 bg-white rounded-xl border border-slate-200 hover:border-indigo-300 hover:shadow-xs transition-all cursor-pointer flex flex-col justify-between gap-2.5"
            >
              <div>
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="text-base font-bold text-slate-900 group-hover:text-indigo-600 transition-colors">
                      {entry.wordVi}
                    </h3>
                    <div className="text-xs text-slate-700 font-medium mt-0.5">
                      <span>{entry.meaningsEn[0]?.meaning}</span>
                      {entry.ipa && (
                        <span className="ml-1.5 text-slate-400 font-mono text-[11px]">
                          {entry.ipa}
                        </span>
                      )}
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={(e) => playQuickAudio(e, entry.audioEn)}
                    className="px-2.5 py-1 text-xs font-semibold text-indigo-700 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 rounded-lg border border-indigo-200 transition-colors cursor-pointer shrink-0"
                    title="Nghe phát âm tiếng Anh"
                  >
                    Nghe
                  </button>
                </div>

                <p className="text-xs text-slate-600 mt-2 line-clamp-2 leading-relaxed">
                  {entry.meaningVi}
                </p>
              </div>

              <div className="flex items-center justify-between pt-2 border-t border-slate-100 text-[11px] text-slate-400">
                <span className="capitalize">{entry.partOfSpeech}</span>
                <span className="text-indigo-600 font-semibold group-hover:underline text-xs">
                  Xem vị trí bài học
                </span>
              </div>
            </div>
          ))}

          {filteredList.length === 0 && (
            <div className="col-span-full py-12 text-center text-slate-400 font-medium">
              Không tìm thấy từ vựng nào khớp với từ khóa "{searchTerm}".
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
