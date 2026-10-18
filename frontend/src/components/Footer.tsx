import React from 'react';
import { Sparkles, Heart } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 py-8 text-xs text-slate-500 dark:text-slate-400 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <div className="w-5 h-5 rounded-md bg-brand-600 flex items-center justify-center text-white">
            <Sparkles className="w-3 h-3" />
          </div>
          <span className="font-semibold text-slate-700 dark:text-slate-300">InterviewAce AI</span>
          <span>— Empowers Indian engineering graduates to crack technical and HR rounds with confidence.</span>
        </div>
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1">
            Engineered with <Heart className="w-3.5 h-3.5 text-rose-500 fill-rose-500 inline" /> for Indian campus placements
          </span>
          <span>•</span>
          <span className="font-mono text-[11px] text-slate-400">Groq Powered</span>
        </div>
      </div>
    </footer>
  );
};
