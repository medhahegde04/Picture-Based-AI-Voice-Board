import React from 'react';
import { motion } from 'framer-motion';

export default function Favorites({ onBack }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="p-6 bg-slate-900 text-white min-h-[300px] rounded-lg shadow"
    >
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Favorites</h2>
        <button
          onClick={onBack}
          className="text-sm text-slate-300 hover:text-white transition-colors"
        >
          Back
        </button>
      </div>
      <div className="h-56 flex items-center justify-center text-slate-400 border border-slate-700 rounded-lg">
        No favourites yet — add items to see them here.
      </div>
    </motion.div>
  );
}
