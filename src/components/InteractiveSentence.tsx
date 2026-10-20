import React from 'react';
import { InteractiveToken } from '../types';
import { Sparkles } from 'lucide-react';

interface InteractiveSentenceProps {
  tokens: InteractiveToken[];
  onSelectWord: (entryId: string) => void;
  className?: string;
}

export const InteractiveSentence: React.FC<InteractiveSentenceProps> = ({
  tokens,
  onSelectWord,
  className = ''
}) => {
  return (
    <div className={`flex flex-wrap items-center leading-relaxed tracking-wide ${className}`}>
      {tokens.map((token, index) => {
        if (token.type === 'space') {
          return <span key={index} className="inline-block w-2">&nbsp;</span>;
        }

        if (token.type === 'punct') {
          return (
            <span key={index} className="inline-block font-semibold text-slate-700">
              {token.text}
            </span>
          );
        }

        // Word token
        if (token.entryId) {
          return (
            <button
              key={index}
              type="button"
              onClick={() => onSelectWord(token.entryId!)}
              className="inline-flex items-center gap-1 px-3 py-1 my-1 mx-0.5 font-bold text-indigo-900 bg-amber-100 hover:bg-amber-200 active:bg-amber-300 border-2 border-amber-300 hover:border-amber-400 rounded-2xl shadow-sm hover:shadow transition-all duration-150 transform hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-indigo-400 cursor-pointer text-lg md:text-xl group"
              title={`Nhấn để tra từ "${token.text}" và nghe phát âm`}
              aria-label={`Từ ${token.text}, bấm để xem nghĩa và nghe phát âm`}
            >
              <span>{token.text}</span>
              <Sparkles className="w-3.5 h-3.5 text-amber-500 opacity-70 group-hover:opacity-100 transition-opacity" />
            </button>
          );
        }

        // Normal non-clickable word
        return (
          <span key={index} className="inline-block px-0.5 text-slate-800 font-medium text-lg md:text-xl">
            {token.text}
          </span>
        );
      })}
    </div>
  );
};
