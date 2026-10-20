import React from 'react';
import { Lesson } from '../types';
import { InteractiveSentence } from './InteractiveSentence';
import { Eye, BookOpen, MessageSquare, Sparkles, HelpCircle } from 'lucide-react';

interface LessonViewProps {
  lesson: Lesson;
  onSelectWord: (entryId: string) => void;
}

export const LessonView: React.FC<LessonViewProps> = ({ lesson, onSelectWord }) => {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Textbook Lesson Illustration Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-white shadow-md border-3 border-amber-200">
        <div className="h-44 sm:h-64 md:h-80 w-full overflow-hidden bg-amber-50 relative flex items-center justify-center">
          <img
            src={lesson.bannerImage}
            alt={`Tranh minh họa ${lesson.title}`}
            className="w-full h-full object-cover object-top hover:scale-102 transition-transform duration-500"
            onError={(e) => {
              // fallback if image fails to load
              e.currentTarget.style.display = 'none';
            }}
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent flex items-end p-4 sm:p-6">
            <div className="text-white drop-shadow-md">
              <span className="text-xs font-bold uppercase tracking-widest text-amber-300 bg-black/40 px-3 py-1 rounded-full backdrop-blur-sm">
                Sách Tiếng Việt 1 - Trang {lesson.pageBook}
              </span>
              <h2 className="text-2xl sm:text-3xl md:text-4xl font-extrabold font-heading mt-1 text-white">
                {lesson.title}
              </h2>
            </div>
          </div>
        </div>
      </div>

      {/* Main Reading Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Section 1: Nhận biết */}
        <div className="bg-gradient-to-br from-amber-50 to-orange-50/50 p-6 rounded-3xl border-2 border-amber-200 shadow-sm relative overflow-hidden">
          <div className="flex items-center justify-between mb-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-amber-200/80 text-amber-900 rounded-full font-black text-sm">
              <Eye className="w-4 h-4 text-amber-700" />
              <span>1. Nhận biết</span>
            </div>
            <span className="text-xs text-amber-700/80 font-bold flex items-center gap-1">
              <Sparkles className="w-3.5 h-3.5 text-amber-500" />
              Chạm vào từ để học
            </span>
          </div>

          <div className="bg-white/90 p-4 sm:p-5 rounded-2xl border border-amber-200 shadow-inner">
            <InteractiveSentence
              tokens={lesson.nhanBiet.tokens}
              onSelectWord={onSelectWord}
            />
          </div>

          <p className="text-xs text-slate-500 font-medium mt-3 italic">
            * Quan sát tranh trên và đọc câu nhận biết mở đầu bài học.
          </p>
        </div>

        {/* Section 2: Đọc từ ngữ */}
        <div className="bg-gradient-to-br from-emerald-50 to-teal-50/50 p-6 rounded-3xl border-2 border-emerald-200 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-emerald-200/80 text-emerald-900 rounded-full font-black text-sm">
              <BookOpen className="w-4 h-4 text-emerald-700" />
              <span>2. Từ ngữ trọng tâm</span>
            </div>
            <span className="text-xs text-emerald-700 font-bold">
              {lesson.docTuNgu.length} từ vựng
            </span>
          </div>

          <div className="flex flex-wrap gap-2.5">
            {lesson.docTuNgu.map((w, idx) => {
              if (w.entryId) {
                return (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => onSelectWord(w.entryId!)}
                    className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-emerald-100 border-2 border-emerald-300 hover:border-emerald-400 text-emerald-900 font-extrabold text-base md:text-lg rounded-2xl shadow-sm hover:shadow transition-all transform hover:-translate-y-0.5 cursor-pointer active:scale-95"
                  >
                    <span>{w.word}</span>
                    <Sparkles className="w-3.5 h-3.5 text-emerald-500" />
                  </button>
                );
              }
              return (
                <span
                  key={idx}
                  className="px-4 py-2 bg-white/70 text-slate-700 font-bold text-base md:text-lg rounded-2xl border border-slate-200"
                >
                  {w.word}
                </span>
              );
            })}
          </div>

          <p className="text-xs text-slate-500 font-medium mt-4 italic">
            * Bấm vào từng thẻ từ để nghe phát âm tiếng Việt và tiếng Anh.
          </p>
        </div>
      </div>

      {/* Section 3: Tập đọc câu ứng dụng */}
      <div className="bg-gradient-to-br from-sky-50 to-indigo-50/50 p-6 rounded-3xl border-2 border-sky-200 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-sky-200/80 text-sky-900 rounded-full font-black text-sm">
            <BookOpen className="w-4 h-4 text-sky-700" />
            <span>3. Tập đọc câu</span>
          </div>
          <span className="text-xs text-sky-700 font-bold">
            Luyện đọc trôi chảy
          </span>
        </div>

        <div className="bg-white/95 p-5 sm:p-6 rounded-2xl border border-sky-200 shadow-inner">
          <InteractiveSentence
            tokens={lesson.tapDoc.tokens}
            onSelectWord={onSelectWord}
          />
        </div>
      </div>

      {/* Section 4: Story (if exists) or Talking/Speaking Practice */}
      {lesson.story ? (
        <div className="bg-gradient-to-br from-purple-50 to-pink-50/50 p-6 rounded-3xl border-2 border-purple-200 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-purple-200/80 text-purple-900 rounded-full font-black text-sm">
              <MessageSquare className="w-4 h-4 text-purple-700" />
              <span>4. Kể chuyện theo tranh: {lesson.story.title}</span>
            </div>
          </div>

          <div className="bg-white/90 p-5 rounded-2xl border border-purple-200 space-y-3">
            <p className="text-slate-700 font-bold text-base">
              Gợi ý câu hỏi để bé quan sát và kể lại câu chuyện:
            </p>
            <ol className="space-y-2 list-decimal list-inside text-slate-800 font-medium text-sm sm:text-base">
              {lesson.story.questions.map((q, idx) => (
                <li key={idx} className="leading-relaxed bg-purple-50/60 p-2.5 rounded-xl border border-purple-100">
                  <span className="font-semibold text-purple-900">{q}</span>
                </li>
              ))}
            </ol>
          </div>
        </div>
      ) : (
        <div className="bg-gradient-to-br from-amber-50/60 to-rose-50/60 p-6 rounded-3xl border-2 border-rose-200/80 shadow-sm">
          <div className="flex items-center gap-2 mb-3">
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-rose-200/80 text-rose-900 rounded-full font-black text-sm">
              <MessageSquare className="w-4 h-4 text-rose-700" />
              <span>4. Luyện nói mở rộng</span>
            </div>
          </div>
          <div className="bg-white/90 p-4 rounded-2xl border border-rose-200">
            <p className="text-slate-800 text-base md:text-lg font-bold">
              Chủ đề thảo luận: <span className="text-rose-700 font-extrabold">{lesson.luyenNoi}</span>
            </p>
            <p className="text-xs text-slate-500 mt-1">
              Thầy cô và phụ huynh hãy cùng bé trao đổi những câu nói hay theo chủ đề trên nhé!
            </p>
          </div>
        </div>
      )}

      {/* Helpful Hint banner */}
      <div className="bg-amber-100/60 border border-amber-300/80 rounded-2xl p-4 flex items-center gap-3 text-amber-900 text-sm font-semibold">
        <HelpCircle className="w-5 h-5 text-amber-600 shrink-0" />
        <span>
          Mẹo cho bé: Bấm vào bất kỳ từ vựng nào có viền cam để mở bảng tra cứu từ điển song ngữ và nghe giọng đọc chuẩn của cô giáo nhé!
        </span>
      </div>
    </div>
  );
};
