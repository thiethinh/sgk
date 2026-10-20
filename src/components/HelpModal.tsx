import React from 'react';
import { X, Sparkles, Volume2, MousePointerClick, Heart } from 'lucide-react';

interface HelpModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const HelpModal: React.FC<HelpModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
    >
      <div
        className="relative w-full max-w-lg bg-gradient-to-b from-white to-amber-50 rounded-3xl shadow-2xl border-4 border-amber-300 p-6 md:p-8 overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          type="button"
          className="absolute top-4 right-4 p-2 text-slate-400 hover:text-rose-600 bg-white hover:bg-rose-50 rounded-full transition-colors"
        >
          <X className="w-6 h-6" />
        </button>

        <div className="flex items-center gap-2 mb-4">
          <div className="p-2 bg-amber-400 text-slate-900 rounded-2xl shadow-sm">
            <Sparkles className="w-5 h-5" />
          </div>
          <h2 className="text-2xl font-black text-slate-800 font-heading">
            Hướng Dẫn Cho Bé & Phụ Huynh
          </h2>
        </div>

        <div className="space-y-4 text-slate-700 text-sm md:text-base">
          <div className="flex items-start gap-3 bg-white p-3.5 rounded-2xl border border-amber-200">
            <div className="p-2 bg-amber-100 text-amber-700 rounded-xl shrink-0 mt-0.5">
              <MousePointerClick className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-bold text-slate-900 mb-0.5">1. Chạm vào từ có màu nổi bật</h4>
              <p className="text-slate-600 text-xs sm:text-sm">
                Khi đọc câu, bé hãy nhấn vào các từ vựng có viền vàng cam để mở cửa sổ tra cứu nghĩa và phiên âm.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 bg-white p-3.5 rounded-2xl border border-amber-200">
            <div className="p-2 bg-emerald-100 text-emerald-700 rounded-xl shrink-0 mt-0.5">
              <Volume2 className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-bold text-slate-900 mb-0.5">2. Lắng nghe giọng đọc mẫu</h4>
              <p className="text-slate-600 text-xs sm:text-sm">
                Bé bấm nút màu xanh lá để nghe cô giáo phát âm tiếng Việt, hoặc nút màu xanh biển để nghe phát âm tiếng Anh giọng Mỹ.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 bg-white p-3.5 rounded-2xl border border-amber-200">
            <div className="p-2 bg-sky-100 text-sky-700 rounded-xl shrink-0 mt-0.5">
              <Heart className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-bold text-slate-900 mb-0.5">3. Tiến bộ mỗi ngày</h4>
              <p className="text-slate-600 text-xs sm:text-sm">
                Sử dụng các nút "Bài trước", "Bài tiếp theo" để khám phá trọn vẹn 21 bài học đầu đời của bộ sách Kết nối tri thức.
              </p>
            </div>
          </div>
        </div>

        <button
          type="button"
          onClick={onClose}
          className="w-full mt-6 py-3 bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-500 hover:to-amber-600 text-slate-900 font-extrabold text-base rounded-2xl shadow-md transition-all active:scale-98 cursor-pointer"
        >
          Bé đã hiểu, bắt đầu đọc thôi!
        </button>
      </div>
    </div>
  );
};
