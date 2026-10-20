import { useState, useEffect } from 'react';
import entriesDataRaw from './data/entries.json';
import pageOverlaysRaw from './data/page_overlays.json';
import { VocabEntry, PageOverlayData, PageOverlayItem } from './types';
import { Header } from './components/Header';
import { PdfPageView } from './components/PdfPageView';
import { VocabInfoPanel } from './components/VocabInfoPanel';
import { AllVocabModal } from './components/AllVocabModal';
import { HelpModal } from './components/HelpModal';
import { Sparkles, Heart } from 'lucide-react';

const entriesData = entriesDataRaw as Record<string, VocabEntry>;
const pageOverlays = pageOverlaysRaw as Record<string, PageOverlayData>;

export function App() {
  // Default to page 15 (Lesson 1: A a)
  const [currentPage, setCurrentPage] = useState<number>(15);
  const [selectedEntryId, setSelectedEntryId] = useState<string | null>('ca_hat');
  const [selectedOverlayId, setSelectedOverlayId] = useState<string | null>('ov_p15_cahat');
  const [isAllVocabOpen, setIsAllVocabOpen] = useState(false);
  const [isHelpOpen, setIsHelpOpen] = useState(false);

  // Saved vocabulary notebook state with localStorage persistence
  const [savedWordIds, setSavedWordIds] = useState<string[]>(() => {
    try {
      const stored = localStorage.getItem('sgk1_saved_vocab_ids');
      if (stored) {
        return JSON.parse(stored);
      }
    } catch {
      // fallback
    }
    // Default sample saved words for a welcoming start
    return ['ca_hat', 'bup_be', 'con_bo'];
  });

  useEffect(() => {
    try {
      localStorage.setItem('sgk1_saved_vocab_ids', JSON.stringify(savedWordIds));
    } catch {
      // ignore
    }
  }, [savedWordIds]);

  const handleToggleSave = (entryId: string) => {
    setSavedWordIds((prev) =>
      prev.includes(entryId) ? prev.filter((id) => id !== entryId) : [...prev, entryId]
    );
  };

  const totalPages = 57;
  const currentPageData: PageOverlayData = pageOverlays[currentPage.toString()] || {
    pageNumber: currentPage,
    image: `/pages/page_${String(currentPage).padStart(3, '0')}.jpg`,
    overlays: [],
    vocabWordIds: []
  };

  // Find vocabulary entries present on this page
  const pageVocabEntries: VocabEntry[] = currentPageData.vocabWordIds
    .map((id) => entriesData[id])
    .filter((entry): entry is VocabEntry => Boolean(entry));

  // Only select entry if it actually belongs to the current page
  const currentEntry =
    selectedEntryId && currentPageData.vocabWordIds.includes(selectedEntryId)
      ? entriesData[selectedEntryId] || null
      : null;

  const handleSelectOverlay = (item: PageOverlayItem) => {
    setSelectedOverlayId(item.id);
    if (item.entryId && entriesData[item.entryId]) {
      setSelectedEntryId(item.entryId);
      // Immediate English pronunciation feedback on tapping word
      const audioUrl = entriesData[item.entryId].audioEn;
      if (audioUrl) {
        try {
          const audio = new Audio(audioUrl);
          audio.play().catch(() => {});
        } catch (e) {
          // ignore audio play errors in unsupported environments
        }
      }
    }
  };

  const handleSelectWordFromRight = (entryId: string) => {
    setSelectedEntryId(entryId);
    // Find matching overlay on current page to highlight
    const match = currentPageData.overlays.find((ov) => ov.entryId === entryId);
    if (match) {
      setSelectedOverlayId(match.id);
    } else {
      setSelectedOverlayId(null);
    }
    // Immediate English pronunciation feedback when selecting from English word list
    const audioUrl = entriesData[entryId]?.audioEn;
    if (audioUrl) {
      try {
        const audio = new Audio(audioUrl);
        audio.play().catch(() => {});
      } catch (e) {
        // ignore audio play errors
      }
    }
  };

  const handlePageChange = (newPage: number) => {
    const validPage = Math.max(1, Math.min(totalPages, newPage));
    setCurrentPage(validPage);
    setSelectedOverlayId(null);

    // Auto-select first vocabulary word of the new page if available
    const newPageData = pageOverlays[validPage.toString()];
    if (newPageData && newPageData.vocabWordIds && newPageData.vocabWordIds.length > 0) {
      const firstId = newPageData.vocabWordIds[0];
      setSelectedEntryId(firstId);
      const firstOverlay = newPageData.overlays.find((ov) => ov.entryId === firstId);
      if (firstOverlay) {
        setSelectedOverlayId(firstOverlay.id);
      }
    } else {
      // Clear selection on pages without vocabulary (e.g. title/cover/intro pages)
      setSelectedEntryId(null);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-amber-50/70 via-sky-50/50 to-pink-50/60 text-slate-800">
      {/* Top Header */}
      <Header
        currentLessonIndex={Math.max(0, Math.floor((currentPage - 14) / 2))}
        totalLessons={21}
        savedCount={savedWordIds.length}
        onOpenAllVocab={() => setIsAllVocabOpen(true)}
        onOpenHelp={() => setIsHelpOpen(true)}
      />

      {/* Main Dual-Pane Layout */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-2 sm:px-6 py-3 sm:py-5">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6 items-start">
          {/* LEFT COLUMN: PDF PAGE VIEW WITH COMPACT SCALING & VERTICAL SWIPE */}
          <div className="lg:col-span-7 xl:col-span-7">
            <PdfPageView
              pageData={currentPageData}
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={handlePageChange}
              selectedEntryId={selectedEntryId}
              selectedOverlayId={selectedOverlayId}
              onSelectOverlay={handleSelectOverlay}
              onSelectLessonPage={handlePageChange}
            />
          </div>

          {/* RIGHT COLUMN: TOP VOCAB CARD (WITH SAVE) + BOTTOM SUGGESTED WORDS */}
          <div className="lg:col-span-5 xl:col-span-5 lg:sticky lg:top-20">
            <VocabInfoPanel
              currentEntry={currentEntry}
              pageVocabEntries={pageVocabEntries}
              allEntries={entriesData}
              currentPage={currentPage}
              savedWordIds={savedWordIds}
              onToggleSave={handleToggleSave}
              onSelectWord={handleSelectWordFromRight}
              onNavigatePage={handlePageChange}
            />
          </div>
        </div>
      </main>

      {/* Modals */}
      <AllVocabModal
        entries={entriesData}
        savedWordIds={savedWordIds}
        onToggleSave={handleToggleSave}
        isOpen={isAllVocabOpen}
        onClose={() => setIsAllVocabOpen(false)}
        onSelectWord={(entryId) => {
          setSelectedEntryId(entryId);
          const entry = entriesData[entryId];
          if (entry && entry.sourcePages && entry.sourcePages.length > 0) {
            handlePageChange(entry.sourcePages[0]);
          }
        }}
      />

      <HelpModal
        isOpen={isHelpOpen}
        onClose={() => setIsHelpOpen(false)}
      />

      {/* Footer */}
      <footer className="mt-4 py-4 border-t border-amber-200 bg-white/80 backdrop-blur-xs text-center text-xs text-slate-500 space-y-1 px-4">
        <div className="flex items-center justify-center gap-1 font-bold text-slate-600">
          <span>Sản phẩm tập đọc tương tác Tiếng Việt Lớp 1</span>
          <Heart className="w-3.5 h-3.5 text-rose-500 fill-rose-500 inline" />
          <span>kèm từ điển song ngữ ngữ cảnh và sổ tay từ vựng của bé</span>
        </div>
        <p>
          Tài liệu nguồn: Sách giáo khoa Tiếng Việt 1 - Tập Một (Bộ Kết nối tri thức với cuộc sống, NXB Giáo dục Việt Nam).
        </p>
        <p className="flex items-center justify-center gap-1 text-[11px] text-slate-400">
          <Sparkles className="w-3 h-3 text-amber-500" />
          Lọc sạch 100% vần, tên riêng và tiêu đề rác — chỉ lưu trữ từ vựng có ý nghĩa học tập.
        </p>
      </footer>
    </div>
  );
}

export default App;
