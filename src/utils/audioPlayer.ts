/**
 * Global Audio Manager for SGK1 Reading Web App
 * Ensures strictly ONLY ONE audio (HTML5 Audio or Web Speech API) plays at any given moment.
 */

let currentAudio: HTMLAudioElement | null = null;
let currentOnStopCallback: (() => void) | null = null;

/**
 * Stops all currently playing sounds (both HTML5 Audio and SpeechSynthesis).
 * Invokes previous callbacks to reset UI states (e.g., playing buttons).
 */
export const stopAllAudio = (): void => {
  // 1. Stop any active HTML5 audio element
  if (currentAudio) {
    try {
      currentAudio.pause();
      currentAudio.currentTime = 0;
      currentAudio.onended = null;
      currentAudio.onerror = null;
    } catch {
      // ignore
    }
    currentAudio = null;
  }

  // 2. Stop any active Web Speech synthesis utterance
  if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
    try {
      window.speechSynthesis.cancel();
    } catch {
      // ignore
    }
  }

  // 3. Notify previous callback so UI resets immediately
  if (currentOnStopCallback) {
    const cb = currentOnStopCallback;
    currentOnStopCallback = null;
    try {
      cb();
    } catch {
      // ignore
    }
  }
};

/**
 * Plays an audio file strictly ensuring any previously playing sound is stopped first.
 */
export const playAudio = (
  audioUrl: string,
  options?: {
    onStart?: () => void;
    onEnded?: () => void;
    onError?: () => void;
  }
): HTMLAudioElement => {
  // Strictly terminate any sound currently playing across the app
  stopAllAudio();

  const audio = new Audio(audioUrl);
  currentAudio = audio;

  const handleFinish = () => {
    if (currentAudio === audio) {
      currentAudio = null;
      currentOnStopCallback = null;
    }
    options?.onEnded?.();
  };

  currentOnStopCallback = handleFinish;

  audio.onended = handleFinish;
  audio.onerror = () => {
    if (currentAudio === audio) {
      currentAudio = null;
      currentOnStopCallback = null;
    }
    options?.onError?.();
  };

  try {
    options?.onStart?.();
    const playPromise = audio.play();
    if (playPromise !== undefined) {
      playPromise.catch(() => {
        if (currentAudio === audio) {
          currentAudio = null;
          currentOnStopCallback = null;
        }
        options?.onError?.();
      });
    }
  } catch {
    if (currentAudio === audio) {
      currentAudio = null;
      currentOnStopCallback = null;
    }
    options?.onError?.();
  }

  return audio;
};

/**
 * Speaks text using Web Speech API strictly ensuring all sounds are stopped first.
 */
export const playSpeech = (
  text: string,
  lang: 'vi-VN' | 'en-US' = 'vi-VN',
  options?: {
    onStart?: () => void;
    onEnded?: () => void;
    onError?: () => void;
  }
): void => {
  stopAllAudio();

  if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
    options?.onError?.();
    return;
  }

  try {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;

    const handleFinish = () => {
      currentOnStopCallback = null;
      options?.onEnded?.();
    };

    currentOnStopCallback = handleFinish;

    utterance.onstart = () => {
      options?.onStart?.();
    };

    utterance.onend = handleFinish;
    utterance.onerror = () => {
      currentOnStopCallback = null;
      options?.onError?.();
    };

    window.speechSynthesis.speak(utterance);
  } catch {
    currentOnStopCallback = null;
    options?.onError?.();
  }
};
