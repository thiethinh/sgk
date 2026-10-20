export interface EnglishMeaning {
  meaning: string;
  ipa: string;
  partOfSpeech: string;
}

export interface VocabEntry {
  id: string;
  wordVi: string;
  meaningVi: string;
  meaningsEn: EnglishMeaning[];
  ipa: string;
  partOfSpeech: string;
  audioVi: string;
  audioEn: string;
  sourcePages: number[];
  reviewStatus?: 'verified' | 'unverified';
}

export interface InteractiveToken {
  type: 'word' | 'punct' | 'space';
  text: string;
  entryId?: string;
}

export interface LessonSection {
  sentence: string;
  tokens: InteractiveToken[];
}

export interface WordTag {
  word: string;
  entryId?: string;
}

export interface StorySection {
  title: string;
  questions: string[];
}

export interface Lesson {
  id: string;
  lessonNumber: number;
  title: string;
  letters: string;
  pagePdf: number;
  pageBook: number;
  bannerImage: string;
  nhanBiet: LessonSection;
  docTuNgu: WordTag[];
  tapDoc: LessonSection;
  luyenNoi: string;
  story?: StorySection;
}

export interface BookData {
  title: string;
  subtitle: string;
  publisher: string;
  totalLessons: number;
  lessons: Lesson[];
}

export interface PageOverlayItem {
  id: string;
  text: string;
  entryId?: string;
  left: number; // percentage
  top: number; // percentage
  width: number; // percentage
  height: number; // percentage
  isKeyVocab?: boolean;
}

export interface PageOverlayData {
  pageNumber: number;
  image: string;
  overlays: PageOverlayItem[];
  vocabWordIds: string[];
}
