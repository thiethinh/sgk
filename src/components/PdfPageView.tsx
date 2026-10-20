import React, { useRef, useState, useCallback, useEffect } from 'react';
import { PageOverlayData, PageOverlayItem } from '../types';
import { ChevronUp, ChevronDown } from 'lucide-react';

interface PdfPageViewProps {
  pageData: PageOverlayData;
  currentPage: number;
  totalPages: number;
  onPageChange: (newPage: number) => void;
  selectedEntryId: string | null;
  selectedOverlayId: string | null;
  onSelectOverlay: (item: PageOverlayItem) => void;
  onSelectLessonPage: (page: number) => void;
}

export const PdfPageView: React.FC<PdfPageViewProps> = ({
  pageData,
  currentPage,
  totalPages,
  onPageChange,
  selectedEntryId,
  selectedOverlayId,
  onSelectOverlay,
  onSelectLessonPage,
}) => {
  // Double-buffering state for book page-turn transition with zero white flash
  const [displayData, setDisplayData] = useState<PageOverlayData>(pageData);
  const [previousData, setPreviousData] = useState<PageOverlayData | null>(null);
  const [turnDirection, setTurnDirection] = useState<'next' | 'prev'>('next');
  const [isAnimating, setIsAnimating] = useState<boolean>(false);
  const transitionTimeoutRef = useRef<number | null>(null);

  // References to keep event listener values fresh
  const currentPageRef = useRef(currentPage);
  const totalPagesRef = useRef(totalPages);
  currentPageRef.current = currentPage;
  totalPagesRef.current = totalPages;

  // Wheel and Touch cooldown to eliminate jitter / rapid jumping
  const lastPageChangeTime = useRef<number>(0);
  const wheelDeltaAccumulator = useRef<number>(0);
  const touchStartY = useRef<number | null>(null);

  // Reference to the PDF viewer container element
  const viewerContainerRef = useRef<HTMLDivElement | null>(null);

  const hasPrev = currentPage > 1;
  const hasNext = currentPage < totalPages;

  // Preload neighboring pages into browser cache for 0ms instant display without white flash
  useEffect(() => {
    const preloadPage = (p: number) => {
      if (p >= 1 && p <= totalPages) {
        const img = new Image();
        img.src = `/pages/page_${String(p).padStart(3, '0')}.jpg`;
      }
    };

    preloadPage(currentPage + 1);
    preloadPage(currentPage + 2);
    if (currentPage > 1) {
      preloadPage(currentPage - 1);
    }
    if (currentPage > 2) {
      preloadPage(currentPage - 2);
    }
  }, [currentPage, totalPages]);

  // When pageData changes, load and trigger smooth book page-turn animation
  useEffect(() => {
    if (pageData.pageNumber !== displayData.pageNumber) {
      const dir = pageData.pageNumber > displayData.pageNumber ? 'next' : 'prev';

      const triggerTransition = () => {
        if (transitionTimeoutRef.current) {
          clearTimeout(transitionTimeoutRef.current);
        }
        setTurnDirection(dir);
        setPreviousData(displayData);
        setDisplayData(pageData);
        setIsAnimating(true);

        transitionTimeoutRef.current = window.setTimeout(() => {
          setIsAnimating(false);
          setPreviousData(null);
        }, 300);
      };

      // Check if image is already cached
      const img = new Image();
      img.src = pageData.image;
      if (img.complete) {
        triggerTransition();
      } else {
        img.onload = triggerTransition;
        img.onerror = triggerTransition;
      }
    } else {
      setDisplayData(pageData);
    }

    return () => {
      if (transitionTimeoutRef.current) {
        clearTimeout(transitionTimeoutRef.current);
      }
    };
  }, [pageData, displayData.pageNumber]);

  // Clean, zero-flash page change with gentle cooldown
  const smoothChangePage = useCallback(
    (newPage: number) => {
      const now = Date.now();
      if (now - lastPageChangeTime.current < 320) return; // 320ms cooldown matching page-turn animation
      lastPageChangeTime.current = now;
      wheelDeltaAccumulator.current = 0;

      onPageChange(newPage);
    },
    [onPageChange]
  );

  // PREVENT OUTER FRAME SCROLLING WHEN CURSOR IS INSIDE THE PDF FRAME
  useEffect(() => {
    const el = viewerContainerRef.current;
    if (!el) return;

    const handleNativeWheel = (e: WheelEvent) => {
      // PREVENT DEFAULT: Lock the outer page / window from moving!
      e.preventDefault();
      e.stopPropagation();

      wheelDeltaAccumulator.current += e.deltaY;

      // Threshold of 60px ensures intentional scroll gesture
      if (wheelDeltaAccumulator.current > 60) {
        if (currentPageRef.current < totalPagesRef.current) {
          smoothChangePage(currentPageRef.current + 1);
        }
        wheelDeltaAccumulator.current = 0;
      } else if (wheelDeltaAccumulator.current < -60) {
        if (currentPageRef.current > 1) {
          smoothChangePage(currentPageRef.current - 1);
        }
        wheelDeltaAccumulator.current = 0;
      }
    };

    const handleNativeTouchMove = (e: TouchEvent) => {
      if (e.cancelable) {
        e.preventDefault();
      }
    };

    // Attach non-passive native listeners to allow e.preventDefault()
    el.addEventListener('wheel', handleNativeWheel, { passive: false });
    el.addEventListener('touchmove', handleNativeTouchMove, { passive: false });

    return () => {
      el.removeEventListener('wheel', handleNativeWheel);
      el.removeEventListener('touchmove', handleNativeTouchMove);
    };
  }, [smoothChangePage]);

  // Smooth Touch Swipe Vertical Support
  const handleTouchStart = (e: React.TouchEvent) => {
    touchStartY.current = e.touches[0].clientY;
  };

  const handleTouchEnd = (e: React.TouchEvent) => {
    if (touchStartY.current === null) return;
    const touchEndY = e.changedTouches[0].clientY;
    const diff = touchStartY.current - touchEndY;

    if (diff > 45 && hasNext) {
      smoothChangePage(currentPage + 1);
    } else if (diff < -45 && hasPrev) {
      smoothChangePage(currentPage - 1);
    }
    touchStartY.current = null;
  };

  return (
    <div className="flex flex-col gap-2.5">
      {/* Main PDF Container with viewerContainerRef to capture & lock wheel/swipe events */}
      <div
        ref={viewerContainerRef}
        style={{ overscrollBehavior: 'contain' }}
        className="flex flex-col bg-[#FDFBF7] rounded-3xl shadow-md border-3 border-amber-200 relative select-none"
      >
        {/* Top Control Toolbar */}
        <div className="p-2 sm:p-2.5 bg-gradient-to-r from-amber-100/95 via-orange-50 to-amber-100/95 border-b-2 border-amber-200 flex flex-wrap items-center justify-between gap-2 z-10 shrink-0 rounded-t-[21px]">
          {/* Navigation Buttons: Up / Down matching vertical scroll */}
          <div className="flex items-center gap-1 sm:gap-1.5">
            <button
              type="button"
              disabled={!hasPrev}
              onClick={() => hasPrev && smoothChangePage(currentPage - 1)}
              className={`flex items-center p-1.5 sm:px-2 sm:py-1.5 rounded-xl font-bold transition-all ${
                hasPrev
                  ? 'bg-amber-200 hover:bg-amber-300 text-amber-900 active:scale-95 cursor-pointer shadow-xs border border-amber-300'
                  : 'bg-slate-100 text-slate-300 cursor-not-allowed border border-slate-200'
              }`}
              title="Lên trang trước (hoặc cuộn chuột lên)"
            >
              <ChevronUp className="w-4 h-4" />
            </button>

            {/* Page dropdown */}
            <div className="flex items-center gap-1.5 bg-white px-2.5 py-1 rounded-xl border border-amber-300 shadow-inner">
              <span className="text-[11px] font-bold text-slate-500 uppercase">Trang</span>
              <select
                value={currentPage}
                onChange={(e) => smoothChangePage(Number(e.target.value))}
                className="font-extrabold text-xs sm:text-sm text-indigo-700 bg-transparent focus:outline-none cursor-pointer"
              >
                {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
                  <option key={p} value={p}>
                    {p} / {totalPages}
                  </option>
                ))}
              </select>
            </div>

            <button
              type="button"
              disabled={!hasNext}
              onClick={() => hasNext && smoothChangePage(currentPage + 1)}
              className={`flex items-center p-1.5 sm:px-2 sm:py-1.5 rounded-xl font-bold transition-all ${
                hasNext
                  ? 'bg-amber-200 hover:bg-amber-300 text-amber-900 active:scale-95 cursor-pointer shadow-xs border border-amber-300'
                  : 'bg-slate-100 text-slate-300 cursor-not-allowed border border-slate-200'
              }`}
              title="Xuống trang sau (hoặc cuộn chuột xuống)"
            >
              <ChevronDown className="w-4 h-4" />
            </button>
          </div>

          {/* Jump to Lesson Dropdown */}
          <div className="flex items-center gap-1.5">
            <select
              onChange={(e) => onSelectLessonPage(Number(e.target.value))}
              className="text-[11px] font-bold text-slate-700 bg-white border border-amber-300 rounded-xl px-2 py-1 shadow-xs focus:outline-none cursor-pointer max-w-[130px] sm:max-w-none"
              defaultValue=""
            >
              <option value="" disabled>Chọn bài học...</option>
              <option value="9">Đồ dùng học tập (Trang 9)</option>
              <option value="15">Bài 1: A a (Trang 15)</option>
              <option value="17">Bài 2: B b (Trang 17)</option>
              <option value="19">Bài 3: C c (Trang 19)</option>
              <option value="21">Bài 4: E e, Ê ê (Trang 21)</option>
              <option value="23">Bài 5: Ôn tập 1 (Trang 23)</option>
              <option value="25">Bài 6: O o (Trang 25)</option>
              <option value="27">Bài 7: Ô ô, Ơ ơ (Trang 27)</option>
              <option value="29">Bài 8: D d, Đ đ (Trang 29)</option>
              <option value="31">Bài 9: Dấu hỏi, nặng (Trang 31)</option>
              <option value="33">Bài 10: Ôn tập 2 (Trang 33)</option>
              <option value="35">Bài 11: I i, K k (Trang 35)</option>
              <option value="37">Bài 12: H h, L l (Trang 37)</option>
              <option value="39">Bài 13: U u, Ư ư (Trang 39)</option>
              <option value="41">Bài 14: Ch, Kh (Trang 41)</option>
              <option value="43">Bài 15: Ôn tập 3 (Trang 43)</option>
              <option value="45">Bài 16: M m, N n (Trang 45)</option>
              <option value="47">Bài 17: G g, Gi gi (Trang 47)</option>
              <option value="49">Bài 18: Gh, Nh (Trang 49)</option>
              <option value="51">Bài 19: Ng, Ngh (Trang 51)</option>
              <option value="53">Bài 20: Ôn tập 4 (Trang 53)</option>
              <option value="55">Bài 21: R r, S s (Trang 55)</option>
            </select>
          </div>
        </div>

        {/* Clean PDF Display Area - Gentle eye-friendly warm paper tone, zero white flash */}
        <div
          onTouchStart={handleTouchStart}
          onTouchEnd={handleTouchEnd}
          className="bg-amber-50/40 p-2 sm:p-3 flex items-start justify-center min-h-[480px] relative rounded-b-[21px]"
        >
          {/* CUTE STICKY NOTE OVERLAPPING THE LEFT BORDER - SCALED DOWN 15% */}
          <div className="hidden sm:flex flex-col w-[128px] bg-gradient-to-br from-amber-100 via-amber-50 to-amber-200/95 border-2 border-amber-300/90 rounded-2xl p-2 shadow-lg shadow-amber-300/40 -rotate-3 hover:rotate-0 transition-transform duration-200 absolute -left-3 sm:-left-4.5 top-6 sm:top-8 z-30 select-none cursor-default">
            {/* Cute Pin */}
            <div className="text-center -mt-4 mb-0.5">
              <span className="text-xl drop-shadow-sm filter">📌</span>
            </div>
            
            <div className="text-center font-black text-amber-950 text-[10.5px] tracking-tight mb-1.5">
              Hướng dẫn bé!
            </div>

            <div className="space-y-1.5 text-[9.5px] font-bold text-amber-900 leading-snug">
              <div className="bg-white/90 p-1.5 rounded-xl border border-amber-200/70 shadow-2xs flex items-center gap-1.5">
                <span className="text-xs shrink-0">👆</span>
                <span>Chạm từ có viền để nghe đọc</span>
              </div>
              
              <div className="bg-white/90 p-1.5 rounded-xl border border-amber-200/70 shadow-2xs flex items-center gap-1.5">
                <span className="text-xs shrink-0">🖱️</span>
                <span>Cuộn chuột để lật trang sách</span>
              </div>
            </div>
          </div>

          {/* Main Book Frame - Fixed standard 55% size */}
          <div
            className="relative shadow-lg rounded-2xl overflow-hidden bg-[#FAF7F2] border border-amber-200/90 shrink-0"
            style={{
              width: '55%',
              maxWidth: '520px',
            }}
          >
            {/* BACKGROUND BUFFER LAYER (Previous page during turn - stays 100% visible so NO white flash ever happens) */}
            {isAnimating && previousData && (
              <div className="absolute inset-0 z-0 pointer-events-none select-none">
                <img
                  src={previousData.image}
                  alt="Trang trước"
                  className="w-full h-auto block"
                />
              </div>
            )}

            {/* ACTIVE FOREGROUND LAYER (Current / Incoming page) */}
            <div
              className={`relative z-10 w-full ${
                isAnimating
                  ? turnDirection === 'next'
                    ? 'animate-page-turn-next'
                    : 'animate-page-turn-prev'
                  : ''
              }`}
            >
              <img
                src={displayData.image}
                alt={`Trang PDF ${currentPage}`}
                className="w-full h-auto block pointer-events-none select-none"
                loading="eager"
              />

              {/* Overlaid Interactive Word DIVs on active page */}
              {displayData.overlays.map((item) => {
                const isSelected =
                  item.id === selectedOverlayId ||
                  (item.entryId && item.entryId === selectedEntryId);

                return (
                  <div
                    key={item.id}
                    onClick={(e) => {
                      e.stopPropagation();
                      onSelectOverlay(item);
                    }}
                    onPointerDown={(e) => {
                      e.stopPropagation();
                    }}
                    onTouchEnd={(e) => {
                      e.stopPropagation();
                      onSelectOverlay(item);
                    }}
                    style={{
                      left: `${item.left}%`,
                      top: `${item.top}%`,
                      width: `${item.width}%`,
                      height: `${item.height}%`,
                    }}
                    className={`absolute transition-all duration-150 cursor-pointer rounded-md touch-manipulation active:scale-95 ${
                      isSelected
                        ? 'border-3 border-indigo-600 bg-indigo-500/35 ring-4 ring-indigo-300/60 shadow-lg scale-105 z-20'
                        : 'border-2 border-amber-400/80 bg-amber-300/25 hover:bg-amber-400/50 hover:border-amber-600 hover:scale-105 z-10 shadow-xs'
                    }`}
                    title={`Nhấn để tra từ "${item.text}"`}
                  />
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
