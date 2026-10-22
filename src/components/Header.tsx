import React from 'react';
import { BookOpen, HelpCircle } from 'lucide-react';

interface HeaderProps {
  currentLessonIndex: number;
  totalLessons: number;
  onOpenAllVocab: () => void;
  onOpenHelp: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  currentLessonIndex,
  totalLessons,
  onOpenAllVocab,
  onOpenHelp,
}) => {
  const progressPercent = Math.round(((currentLessonIndex + 1) / totalLessons) * 100);

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-xs transition-all">
      <div className="max-w-7xl mx-auto px-3 sm:px-6 py-2.5 sm:py-3">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-3">
          {/* Logo & Main Title Section */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-gradient-to-br from-indigo-600 to-blue-700 flex items-center justify-center shadow-sm shrink-0">
              <BookOpen className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
            </div>
            <h1 className="text-base sm:text-lg md:text-xl font-black text-slate-900 tracking-tight leading-snug">
              VIỆT NGỮ MỞ LỐI – ANH NGỮ VƯƠN XA
            </h1>
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
              className="px-3.5 py-1.5 sm:py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs sm:text-sm rounded-xl shadow-xs hover:shadow-sm transition-all active:scale-95 cursor-pointer"
              title="Tra cứu từ vựng bài học"
            >
              Sổ tay từ vựng
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

