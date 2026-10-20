import React from 'react';
import { Lesson } from '../types';
import { ChevronLeft, ChevronRight, List } from 'lucide-react';

interface LessonNavigatorProps {
  lessons: Lesson[];
  currentIndex: number;
  onSelectLesson: (index: number) => void;
}

export const LessonNavigator: React.FC<LessonNavigatorProps> = ({
  lessons,
  currentIndex,
  onSelectLesson,
}) => {
  const currentLesson = lessons[currentIndex];
  const hasPrev = currentIndex > 0;
  const hasNext = currentIndex < lessons.length - 1;

  return (
    <div className="w-full bg-white/70 backdrop-blur-sm rounded-3xl p-4 shadow-sm border-2 border-amber-200/80 mb-6">
      <div className="flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Navigation Buttons */}
        <div className="flex items-center gap-3 w-full md:w-auto justify-between">
          <button
            type="button"
            disabled={!hasPrev}
            onClick={() => hasPrev && onSelectLesson(currentIndex - 1)}
            className={`flex items-center gap-1.5 px-4 py-2.5 rounded-2xl font-black text-sm transition-all shadow-sm ${
              hasPrev
                ? 'bg-amber-100 hover:bg-amber-200 text-amber-900 hover:scale-105 active:scale-95 cursor-pointer'
                : 'bg-slate-100 text-slate-300 cursor-not-allowed'
            }`}
          >
            <ChevronLeft className="w-5 h-5" />
            <span>Bài trước</span>
          </button>

          {/* Current Lesson Badge */}
          <div className="text-center px-2">
            <span className="text-xs font-bold uppercase tracking-wider text-amber-700 bg-amber-100/90 px-3 py-1 rounded-full border border-amber-200">
              Trang {currentLesson.pageBook}
            </span>
            <div className="text-lg md:text-xl font-extrabold text-slate-800 font-heading mt-0.5">
              {currentLesson.title}
            </div>
          </div>

          <button
            type="button"
            disabled={!hasNext}
            onClick={() => hasNext && onSelectLesson(currentIndex + 1)}
            className={`flex items-center gap-1.5 px-4 py-2.5 rounded-2xl font-black text-sm transition-all shadow-sm ${
              hasNext
                ? 'bg-gradient-to-r from-emerald-400 to-teal-500 hover:from-emerald-500 hover:to-teal-600 text-white hover:scale-105 active:scale-95 cursor-pointer'
                : 'bg-slate-100 text-slate-300 cursor-not-allowed'
            }`}
          >
            <span>Bài tiếp theo</span>
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>

        {/* Quick Lesson Selector Chips */}
        <div className="w-full md:w-auto flex items-center gap-1.5 overflow-x-auto pb-1 max-w-full md:max-w-md scrollbar-thin">
          <span className="text-xs font-bold text-slate-400 flex items-center gap-1 pr-1 shrink-0">
            <List className="w-3.5 h-3.5" />
            Chọn bài:
          </span>
          {lessons.map((les, idx) => {
            const isSelected = idx === currentIndex;
            return (
              <button
                key={les.id}
                type="button"
                onClick={() => onSelectLesson(idx)}
                className={`shrink-0 w-8 h-8 rounded-xl font-black text-xs transition-all ${
                  isSelected
                    ? 'bg-indigo-600 text-white shadow-md scale-110'
                    : 'bg-slate-100 hover:bg-amber-100 text-slate-700 hover:text-amber-900'
                }`}
                title={`${les.title}: ${les.letters}`}
              >
                {les.lessonNumber}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
