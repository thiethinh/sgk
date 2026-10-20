import React from 'react';
import { BookOpen, Sparkles, BookMarked, HelpCircle } from 'lucide-react';

interface HeaderProps {
  currentLessonIndex: number;
  totalLessons: number;
  savedCount?: number;
  onOpenAllVocab: () => void;
  onOpenHelp: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  currentLessonIndex,
  totalLessons,
  savedCount = 0,
  onOpenAllVocab,
  onOpenHelp,
}) => {
  const progressPercent = Math.round(((currentLessonIndex + 1) / totalLessons) * 100);

  return (
    <header className="sticky top-0 z-30 bg-white/90 backdrop-blur-md border-b-2 border-amber-200 shadow-sm transition-all">
      <div className="max-w-6xl mx-auto px-4 py-3 sm:px-6">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
          {/* Logo & Title */}
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-amber-400 to-rose-400 flex items-center justify-center shadow-md transform hover:rotate-6 transition-transform">
              <BookOpen className="w-7 h-7 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl sm:text-2xl font-black text-slate-800 tracking-tight font-heading">
                  Bé Tập Đọc Lớp 1
                </h1>
                <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-amber-100 text-amber-800 text-xs font-extrabold rounded-full border border-amber-300">
                  <Sparkles className="w-3 h-3 text-amber-600" />
                  SGK Tập 1
                </span>
              </div>
              <p className="text-xs text-slate-500 font-medium">
                Kết nối tri thức với cuộc sống & Từ điển Anh - Việt phát âm chuẩn
              </p>
            </div>
          </div>

          {/* Right Action Buttons */}
          <div className="flex items-center gap-2 sm:gap-3 w-full sm:w-auto justify-between sm:justify-end">
            {/* Progress Badge */}
            <div className="hidden md:flex flex-col items-end min-w-[130px]">
              <span className="text-xs font-bold text-indigo-700">
                Tiến độ: Bài {currentLessonIndex + 1}/{totalLessons} ({progressPercent}%)
              </span>
              <div className="w-32 h-2.5 bg-slate-100 rounded-full overflow-hidden mt-1 border border-slate-200">
                <div
                  className="h-full bg-gradient-to-r from-amber-400 to-emerald-400 rounded-full transition-all duration-300"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
            </div>

            {/* Dictionary / Notebook button */}
            <button
              type="button"
              onClick={onOpenAllVocab}
              className="flex items-center gap-1.5 px-3 py-1.5 sm:px-3.5 sm:py-2 bg-gradient-to-r from-rose-500 to-pink-600 hover:from-rose-600 hover:to-pink-700 text-white font-bold text-xs sm:text-sm rounded-2xl shadow-sm hover:shadow transition-all active:scale-95 cursor-pointer"
              title="Mở sổ tay từ vựng bé đã lưu"
            >
              <BookMarked className="w-4 h-4" />
              <span>Sổ tay của bé</span>
              {savedCount > 0 && (
                <span className="ml-1 px-2 py-0.5 bg-white/25 text-white rounded-full text-xs font-black">
                  {savedCount}
                </span>
              )}
            </button>

            {/* Help button */}
            <button
              type="button"
              onClick={onOpenHelp}
              className="p-2 text-slate-500 hover:text-slate-800 bg-slate-100 hover:bg-slate-200 rounded-2xl transition-colors cursor-pointer"
              title="Hướng dẫn sử dụng"
            >
              <HelpCircle className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};
