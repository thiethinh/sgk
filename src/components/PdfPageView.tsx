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
        img.src = `/pages/topic_${p}.png`;
      }
    };

    preloadPage(currentPage + 1);
    preloadPage(currentPage + 2);
    if (currentPage > 1) {
      preloadPage(currentPage - 1);
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
    <div className="flex flex-col gap-2.5 relative">
      {/* CUTE STICKY NOTE: COMPLETELY OUTSIDE THE SGK PANEL AT TOP-LEFT */}
      <div className="hidden xl:flex flex-col w-[128px] bg-gradient-to-br from-amber-100 via-amber-50 to-amber-200/95 border-2 border-amber-300/90 rounded-2xl p-2 shadow-lg shadow-amber-300/40 -rotate-3 hover:rotate-0 transition-transform duration-200 absolute -left-[140px] top-2 z-10 select-none cursor-default">
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
            <span>Chạm từ hoặc ảnh để nghe đọc</span>
          </div>
          
          <div className="bg-white/90 p-1.5 rounded-xl border border-amber-200/70 shadow-2xs flex items-center gap-1.5">
            <span className="text-xs shrink-0">💬</span>
            <span>Chạm tranh nghe hội thoại</span>
          </div>

          <div className="bg-white/90 p-1.5 rounded-xl border border-amber-200/70 shadow-2xs flex items-center gap-1.5">
            <span className="text-xs shrink-0">🖱️</span>
            <span>Cuộn chuột đổi bài học</span>
          </div>
        </div>
      </div>

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
              value={currentPage}
              onChange={(e) => onSelectLessonPage(Number(e.target.value))}
              className="text-[11px] font-bold text-slate-700 bg-white border border-amber-300 rounded-xl px-2 py-1 shadow-xs focus:outline-none cursor-pointer max-w-[170px] sm:max-w-none"
            >
              <option value="1">Bài 3: C c (Trang 18 - 19)</option>
              <option value="2">Bài 6: O o (Trang 24 - 25)</option>
              <option value="3">Bài 10: Ôn tập - Đàn kiến (Trang 32 - 33)</option>
              <option value="4">Bài 16: M m, N n (Trang 44 - 45)</option>
              <option value="5">Bài 28: Y y (Trang 68 - 69)</option>
            </select>
          </div>
        </div>

        {/* Clean PDF Display Area - Gentle eye-friendly warm paper tone, zero white flash */}
        <div
          onTouchStart={handleTouchStart}
          onTouchEnd={handleTouchEnd}
          className="bg-amber-50/40 p-2 sm:p-3 flex items-start justify-center min-h-[480px] relative rounded-b-[21px]"
        >

          {/* Main Book Frame */}
          <div
            className="relative shadow-lg rounded-2xl overflow-hidden bg-[#FAF7F2] border border-amber-200/90 shrink-0 w-full"
            style={{
              maxWidth: '740px',
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

                const isDialogueOrStory =
                  item.entryId?.includes('thoai') ||
                  item.entryId?.includes('tranh') ||
                  item.entryId?.includes('kien');

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
                        ? 'border-3 border-indigo-600 bg-indigo-500/35 ring-4 ring-indigo-300/60 shadow-lg scale-[1.02] z-20'
                        : isDialogueOrStory
                        ? 'border-2 border-emerald-500/80 bg-emerald-400/20 hover:bg-emerald-400/40 hover:border-emerald-600 hover:scale-[1.02] z-10 shadow-xs'
                        : 'border-2 border-amber-400/80 bg-amber-300/25 hover:bg-amber-400/50 hover:border-amber-600 hover:scale-105 z-10 shadow-xs'
                    }`}
                    title={
                      isDialogueOrStory
                        ? `Nhấn để nghe hội thoại "${item.text}"`
                        : `Nhấn để tra từ "${item.text}"`
                    }
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
