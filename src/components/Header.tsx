import React from 'react';
import { BookOpen, HelpCircle } from 'lucide-react';

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
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-amber-200/80 shadow-xs transition-all">
      <div className="max-w-7xl mx-auto px-3 sm:px-6 py-2.5 sm:py-3">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-3">
          {/* Logo & Main Title Section */}
          <div className="flex items-start sm:items-center gap-3">
            <div className="w-11 h-11 sm:w-12 sm:h-12 rounded-xl bg-gradient-to-br from-indigo-600 to-blue-700 flex items-center justify-center shadow-sm shrink-0">
              <BookOpen className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2 mb-0.5">
                <span className="px-2 py-0.5 bg-indigo-50 text-indigo-700 text-[11px] font-bold rounded border border-indigo-200">
                  Tiếng Việt 1 — Bộ Kết nối tri thức
                </span>
              </div>
              <h1 className="text-base sm:text-lg md:text-xl font-black text-slate-900 tracking-tight leading-snug">
                VIỆT NGỮ MỞ LỐI – ANH NGỮ VƯƠN XA
              </h1>
              <p className="text-xs text-slate-600 font-medium leading-normal">
                Học liệu điện tử song ngữ Việt – Anh trong dạy học Tiếng Việt lớp 1
              </p>
            </div>
          </div>

          {/* Right Action Buttons */}
          <div className="flex items-center gap-2 sm:gap-3 justify-between lg:justify-end shrink-0 pt-1 lg:pt-0 border-t lg:border-t-0 border-slate-100">
            {/* Progress Badge */}
            <div className="flex flex-col items-start sm:items-end min-w-[120px]">
              <span className="text-xs font-semibold text-slate-600">
                Bài học: <span className="font-bold text-indigo-600">{currentLessonIndex + 1}/{totalLessons}</span>
              </span>
              <div className="w-28 sm:w-32 h-2 bg-slate-100 rounded-full overflow-hidden mt-1 border border-slate-200">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 to-emerald-500 rounded-full transition-all duration-300"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
            </div>

            {/* Dictionary / Notebook button */}
            <button
              type="button"
              onClick={onOpenAllVocab}
              className="flex items-center gap-1.5 px-3 py-1.5 sm:px-3.5 sm:py-2 bg-gradient-to-r from-rose-500 to-pink-600 hover:from-rose-600 hover:to-pink-700 text-white font-bold text-xs sm:text-sm rounded-xl shadow-xs hover:shadow transition-all active:scale-95 cursor-pointer"
              title="Mở sổ tay từ vựng bé đã lưu"
            >
              <span>Sổ tay từ vựng</span>
              {savedCount > 0 && (
                <span className="ml-0.5 px-1.5 py-0.2 bg-white/25 text-white rounded-md text-[11px] font-black">
                  {savedCount}
                </span>
              )}
            </button>

            {/* Help button */}
            <button
              type="button"
              onClick={onOpenHelp}
              className="flex items-center gap-1 px-2.5 py-1.5 sm:py-2 text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors cursor-pointer text-xs font-semibold"
              title="Hướng dẫn sử dụng"
            >
              <HelpCircle className="w-4 h-4" />
              <span className="hidden sm:inline">Hướng dẫn</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

