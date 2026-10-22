import React, { useState } from 'react';
import { VocabEntry } from '../types';
import { X, Search, Volume2, ArrowRight, BookMarked, Bookmark, BookmarkCheck, Trash2 } from 'lucide-react';

interface AllVocabModalProps {
  entries: Record<string, VocabEntry>;
  savedWordIds: string[];
  onToggleSave: (entryId: string) => void;
  isOpen: boolean;
  onClose: () => void;
  onSelectWord: (entryId: string) => void;
}

export const AllVocabModal: React.FC<AllVocabModalProps> = ({
  entries,
  savedWordIds,
  onToggleSave,
  isOpen,
  onClose,
  onSelectWord,
}) => {
  // Tab: 'saved' (ONLY SAVED WORDS - default!) or 'all'
  const [activeTab, setActiveTab] = useState<'saved' | 'all'>('saved');
  const [searchTerm, setSearchTerm] = useState('');

  if (!isOpen) return null;

  const allList = Object.values(entries);
  const savedList = allList.filter((item) => savedWordIds.includes(item.id));

  const currentDisplayList = activeTab === 'saved' ? savedList : allList;

  const filteredList = currentDisplayList.filter((item) => {
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
    const audio = new Audio(audioSrc);
    audio.play().catch(() => {});
  };

  return (
    <div
      className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
    >
      <div
        className="relative w-full max-w-3xl max-h-[85vh] flex flex-col bg-white rounded-3xl shadow-2xl border-4 border-amber-300 overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-4 sm:p-5 bg-gradient-to-r from-amber-50 via-rose-50 to-amber-50 border-b border-amber-200 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-rose-500 text-white rounded-2xl shadow-sm">
              <BookMarked className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl sm:text-2xl font-black text-slate-800 font-heading">
                Sổ Tay Từ Vựng Của Bé
              </h2>
              <p className="text-xs text-slate-500 font-medium">
                Chỉ lưu và ôn tập các từ vựng bé đã tích lưu khi học bài
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            type="button"
            className="p-2 text-slate-400 hover:text-rose-600 bg-white hover:bg-rose-50 rounded-full transition-colors"
            title="Đóng (Esc)"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Switcher & Search Bar */}
        <div className="p-3 sm:p-4 bg-slate-50 border-b border-slate-200 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          {/* Tabs */}
          <div className="flex items-center gap-1.5 bg-slate-200/80 p-1 rounded-2xl">
            <button
              type="button"
              onClick={() => setActiveTab('saved')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl font-bold text-xs transition-all ${
                activeTab === 'saved'
                  ? 'bg-rose-500 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <BookmarkCheck className="w-3.5 h-3.5" />
              <span>Đã lưu ({savedList.length})</span>
            </button>

            <button
              type="button"
              onClick={() => setActiveTab('all')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl font-bold text-xs transition-all ${
                activeTab === 'all'
                  ? 'bg-indigo-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <span>Tất cả từ ({allList.length})</span>
            </button>
          </div>

          {/* Search Bar */}
          <div className="relative flex-1 max-w-xs">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Tìm từ trong sổ tay..."
              className="w-full pl-9 pr-3 py-1.5 bg-white border border-slate-200 rounded-xl text-xs font-semibold text-slate-800 focus:outline-none focus:border-rose-400"
            />
          </div>
        </div>

        {/* Words Grid */}
        <div className="p-4 sm:p-5 overflow-y-auto flex-1 grid grid-cols-1 sm:grid-cols-2 gap-3 scrollbar-thin">
          {filteredList.map((entry) => {
            const isSaved = savedWordIds.includes(entry.id);

            return (
              <div
                key={entry.id}
                onClick={() => {
                  onClose();
                  onSelectWord(entry.id);
                }}
                className="group p-3 bg-gradient-to-br from-white to-amber-50/40 hover:to-rose-50 rounded-2xl border-2 border-slate-200 hover:border-rose-300 shadow-xs hover:shadow-md transition-all cursor-pointer flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <h3 className="text-lg font-black text-indigo-700 font-heading group-hover:text-rose-700 transition-colors">
                        {entry.wordVi}
                      </h3>
                      <div className="text-xs text-sky-800 font-bold mt-0.5">
                        {entry.meaningsEn[0]?.meaning}
                        {entry.ipa && (
                          <span className="ml-1 text-slate-400 font-mono text-[11px]">
                            {entry.ipa}
                          </span>
                        )}
                      </div>
                    </div>

                    <div className="flex items-center gap-1">
                      <button
                        type="button"
                        onClick={(e) => playQuickAudio(e, entry.audioEn)}
                        className="p-1.5 text-sky-600 hover:text-sky-700 bg-sky-50 hover:bg-sky-100 rounded-xl transition-colors cursor-pointer"
                        title="Nghe phát âm tiếng Anh"
                      >
                        <Volume2 className="w-3.5 h-3.5" />
                      </button>

                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          onToggleSave(entry.id);
                        }}
                        className={`p-1.5 rounded-xl transition-colors ${
                          isSaved
                            ? 'text-rose-500 hover:text-rose-700 bg-rose-50 hover:bg-rose-100'
                            : 'text-slate-300 hover:text-rose-500 hover:bg-slate-100'
                        }`}
                        title={isSaved ? 'Xóa khỏi sổ tay' : 'Lưu vào sổ tay'}
                      >
                        {isSaved ? (
                          <Trash2 className="w-3.5 h-3.5" />
                        ) : (
                          <Bookmark className="w-3.5 h-3.5" />
                        )}
                      </button>
                    </div>
                  </div>

                  <p className="text-xs text-slate-600 mt-1.5 line-clamp-2 leading-relaxed">
                    {entry.meaningVi}
                  </p>
                </div>

                <div className="flex items-center justify-between mt-2.5 pt-2 border-t border-slate-100 text-[11px] text-slate-400">
                  <span className="capitalize">{entry.partOfSpeech}</span>
                  <span className="flex items-center gap-1 text-indigo-600 font-bold group-hover:underline">
                    <span>Đến bài đọc</span>
                    <ArrowRight className="w-3 h-3" />
                  </span>
                </div>
              </div>
            );
          })}

          {filteredList.length === 0 && (
            <div className="col-span-full py-12 text-center text-slate-400 font-medium space-y-2">
              {activeTab === 'saved' ? (
                <>
                  <Bookmark className="w-10 h-10 text-amber-300 mx-auto" />
                  <p className="text-base font-bold text-slate-700">
                    Sổ tay của bé chưa có từ vựng nào!
                  </p>
                  <p className="text-xs text-slate-400 max-w-sm mx-auto">
                    Khi đọc sách, bé hãy bấm vào nút 🔖 "Lưu từ này" ở khung bên phải để lưu các từ mình yêu thích vào đây nhé.
                  </p>
                  <button
                    type="button"
                    onClick={() => setActiveTab('all')}
                    className="mt-2 px-4 py-1.5 bg-indigo-50 text-indigo-700 hover:bg-indigo-100 font-bold text-xs rounded-xl"
                  >
                    Xem tất cả từ vựng trong sách
                  </button>
                </>
              ) : (
                <p>Không tìm thấy từ vựng nào khớp với từ khóa "{searchTerm}".</p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
