import React from 'react';
import { X, BookOpen, Volume2, MousePointerClick, BookmarkCheck } from 'lucide-react';

interface HelpModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const HelpModal: React.FC<HelpModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
    >
      <div
        className="relative w-full max-w-lg bg-gradient-to-b from-white to-amber-50 rounded-3xl shadow-2xl border-2 border-amber-300 p-6 md:p-8 overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          type="button"
          className="absolute top-4 right-4 p-2 text-slate-400 hover:text-slate-700 bg-white hover:bg-slate-100 rounded-full transition-colors cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2.5 mb-5">
          <div className="p-2 bg-indigo-600 text-white rounded-xl shadow-xs">
            <BookOpen className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-xl font-black text-slate-800">
              Hướng Dẫn Sử Dụng Học Liệu
            </h2>
            <p className="text-xs text-slate-500">
              Dành cho giáo viên, phụ huynh và học sinh lớp 1
            </p>
          </div>
        </div>

        <div className="space-y-3.5 text-slate-700 text-sm">
          <div className="flex items-start gap-3 bg-white p-3.5 rounded-2xl border border-amber-200 shadow-xs">
            <div className="p-2 bg-amber-100 text-amber-800 rounded-xl shrink-0 mt-0.5">
              <MousePointerClick className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-bold text-slate-900 mb-0.5">1. Chạm vào từ hoặc tranh trên trang sách</h4>
              <p className="text-slate-600 text-xs sm:text-sm">
                Khi đọc trang sách, chạm vào bất kỳ từ vựng hoặc hình minh họa có khung tương tác để xem nghĩa, phiên âm và nghe giọng đọc.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 bg-white p-3.5 rounded-2xl border border-amber-200 shadow-xs">
            <div className="p-2 bg-emerald-100 text-emerald-800 rounded-xl shrink-0 mt-0.5">
              <Volume2 className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-bold text-slate-900 mb-0.5">2. Luyện nghe phát âm chuẩn song ngữ Việt – Anh</h4>
              <p className="text-slate-600 text-xs sm:text-sm">
                Bấm nút loa Tiếng Việt để nghe phát âm mẫu, hoặc bấm nút loa Tiếng Anh để nghe phát âm bản ngữ theo ngữ cảnh tự nhiên.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 bg-white p-3.5 rounded-2xl border border-amber-200 shadow-xs">
            <div className="p-2 bg-blue-100 text-blue-800 rounded-xl shrink-0 mt-0.5">
              <BookmarkCheck className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-bold text-slate-900 mb-0.5">3. Lưu từ vào sổ tay và chuyển bài học</h4>
              <p className="text-slate-600 text-xs sm:text-sm">
                Sử dụng nút "Lưu vào sổ tay" để ôn tập từ vựng yêu thích, hoặc dùng thanh chuyển bài để di chuyển nhanh giữa các chủ đề SGK.
              </p>
            </div>
          </div>
        </div>

        <button
          type="button"
          onClick={onClose}
          className="w-full mt-6 py-2.5 bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 text-white font-bold text-sm rounded-xl shadow-sm transition-all active:scale-98 cursor-pointer"
        >
          Đã hiểu, bắt đầu khám phá
        </button>
      </div>
    </div>
  );
};
