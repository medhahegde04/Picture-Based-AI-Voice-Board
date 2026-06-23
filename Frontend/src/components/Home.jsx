import React from 'react';
import MenuIcon from './icons/MenuIcon';
import CameraIcon from './icons/CameraIcon';
import DefaultImage from './icons/DefaultImage';
import { motion, AnimatePresence } from 'framer-motion';

export default function Home({
  user,
  onLogout,
  onOpenCamera,
  capturedImage,
  detectionResult, 
  navigate,
  menuOpen,
  setMenuOpen,
}) {
  const menuItems = ['school', 'home', 'general', 'hobbies', 'grocery store'];

  return (
    <div className="relative min-h-screen bg-slate-900 flex flex-col text-white">
      {/* Header */}
      <header className="flex items-center justify-between p-4 bg-slate-800 shadow-md">
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="p-2 rounded-md hover:bg-slate-700 transition-colors"
        >
          <MenuIcon />
        </button>
        <div className="text-center">
          <div className="text-sm text-slate-300">Welcome</div>
          <div className="font-semibold">{user?.name || user?.username || 'User'}</div>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={onOpenCamera}
            className="p-2 rounded-md hover:bg-slate-700 transition-colors"
          >
            <CameraIcon />
          </button>
          <button
            className="text-xs px-3 py-1 bg-slate-700 border border-slate-600 rounded hover:bg-slate-600 transition-colors"
            onClick={onLogout}
          >
            Logout
          </button>
        </div>
      </header>

      {/* Side Menu */}
      <AnimatePresence>
        {menuOpen && (
          <motion.div
            initial={{ x: -300, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -300, opacity: 0 }}
            className="absolute z-30 top-0 left-0 h-full w-full bg-black/60"
            onClick={() => setMenuOpen(false)}
          >
            <motion.div
              initial={{ x: -260 }}
              animate={{ x: 0 }}
              exit={{ x: -260 }}
              className="bg-slate-800 w-64 h-full p-4 shadow-lg"
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className="font-semibold text-lg mb-4">Choose your envt</h3>
              <nav className="space-y-2">
                {menuItems.map((t) => (
                  <button
                    key={t}
                    onClick={() => navigate(t)}
                    className="w-full text-left p-2 rounded hover:bg-slate-700 capitalize transition-colors"
                  >
                  {t}
                  </button>
                ))}
              </nav>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Content: Displaying the captured/detected image and results */}
      <main className="flex-1 p-4">
        <h1 className="text-2xl font-semibold">Hi {user?.name || user?.username}!</h1>
        
        {/* Detection Result Display */}
        <div className="mt-4 p-3 bg-slate-700 rounded-lg shadow-md border-l-4 border-sky-400">
            <p className="text-sm font-light text-slate-300">
              {detectionResult.object ? 'Detected Object:' : 'System Status:'}
            </p>
            <p className="text-lg font-bold text-sky-400">
              {detectionResult.object || 'Real-Time Server Connected'}
            </p>
            <p className="text-md mt-1 italic">
              {detectionResult.phrase}
            </p>
            {detectionResult.confidence && (
                <p className="text-xs mt-1 text-slate-400">
                    Confidence: {detectionResult.confidence}%
                </p>
            )}
        </div>

        <div className="mt-6">
          <div className="w-full h-56 rounded-lg border border-slate-600 overflow-hidden flex items-center justify-center bg-slate-800 shadow-inner">
            {capturedImage ? (
              <img
                src={capturedImage}
                alt="captured"
                className="object-cover w-full h-full"
              />
            ) : (
              <DefaultImage />
            )}
          </div>
          <div className="mt-3 text-sm text-slate-300">
            Image above is the last captured photo or a default placeholder.
          </div>
        </div>
      </main>

      {/* Footer Navigation */}
      <nav className="border-t bg-slate-800 p-3 flex items-center justify-between shadow-inner">
        <button
          onClick={() => navigate('home')}
          className="flex-1 py-2 font-semibold hover:text-sky-400 transition-colors"
        >
          Home
        </button>
        <button
          onClick={() => navigate('fav')}
          className="flex-1 py-2 hover:text-sky-400 transition-colors"
        >
          Fav
        </button>
        <button
          onClick={() => navigate('profile')}
          className="flex-1 py-2 hover:text-sky-400 transition-colors"
        >
          Profile
        </button>
      </nav>

    </div>
  );
}