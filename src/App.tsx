import { useState } from 'react';
import entriesDataRaw from './data/entries.json';
import pageOverlaysRaw from './data/page_overlays.json';
import { VocabEntry, PageOverlayData, PageOverlayItem } from './types';
import { Header } from './components/Header';
import { PdfPageView } from './components/PdfPageView';
import { VocabInfoPanel } from './components/VocabInfoPanel';
import { AllVocabModal } from './components/AllVocabModal';
import { HelpModal } from './components/HelpModal';
import { playAudio, stopAllAudio } from './utils/audioPlayer';

const entriesData = entriesDataRaw as Record<string, VocabEntry>;
const pageOverlays = pageOverlaysRaw as Record<string, PageOverlayData>;

export function App() {
  // Default to Topic 1: Bài 3: C c
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [selectedEntryId, setSelectedEntryId] = useState<string | null>('ca_nuoc');
  const [selectedOverlayId, setSelectedOverlayId] = useState<string | null>('ov_t1_ca_nuoc');
  const [isAllVocabOpen, setIsAllVocabOpen] = useState(false);
  const [isHelpOpen, setIsHelpOpen] = useState(false);

  const totalPages = 5;
  const currentPageData: PageOverlayData = pageOverlays[currentPage.toString()] || {
    pageNumber: currentPage,
    image: `/pages/topic_${currentPage}.png`,
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
      // Strictly single audio playback: plays English pronunciation, stopping all others
      const audioUrl = entriesData[item.entryId].audioEn;
      if (audioUrl) {
        playAudio(audioUrl);
      } else {
        stopAllAudio();
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
    // Strictly single audio playback: plays English pronunciation, stopping all others
    const audioUrl = entriesData[entryId]?.audioEn;
    if (audioUrl) {
      playAudio(audioUrl);
    } else {
      stopAllAudio();
    }
  };

  const handlePageChange = (newPage: number) => {
    // Stop any ongoing audio when changing page
    stopAllAudio();

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
        currentLessonIndex={currentPage - 1}
        totalLessons={5}
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

          {/* RIGHT COLUMN: TOP VOCAB CARD + BOTTOM SUGGESTED WORDS */}
          <div className="lg:col-span-5 xl:col-span-5 lg:sticky lg:top-20">
            <VocabInfoPanel
              currentEntry={currentEntry}
              pageVocabEntries={pageVocabEntries}
              allEntries={entriesData}
              currentPage={currentPage}
              onSelectWord={handleSelectWordFromRight}
              onNavigatePage={handlePageChange}
            />
          </div>
        </div>
      </main>

      {/* Modals */}
      <AllVocabModal
        entries={entriesData}
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
      <footer className="mt-8 py-6 border-t border-slate-200/80 bg-white/90 backdrop-blur-xs text-center text-xs text-slate-600 px-4">
        <div className="max-w-4xl mx-auto space-y-1.5">
          <h2 className="text-sm sm:text-base font-extrabold text-slate-800 tracking-tight">
            VIỆT NGỮ MỞ LỐI – ANH NGỮ VƯƠN XA
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 font-medium">
            Học liệu điện tử song ngữ Việt – Anh trong dạy học Tiếng Việt lớp 1
          </p>
          <div className="pt-2.5 border-t border-slate-100 text-[11px] text-slate-500 space-y-1">
            <p>
              Tài liệu nguồn: Sách giáo khoa Tiếng Việt 1 - Bộ Kết nối tri thức với cuộc sống (NXB Giáo dục Việt Nam).
            </p>
            <p>
              Học liệu điện tử tương tác đa phương tiện hỗ trợ học sinh học chữ, phát âm chuẩn và mở rộng vốn từ song ngữ theo ngữ cảnh bài học.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
