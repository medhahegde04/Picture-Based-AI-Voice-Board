import React, { useState } from 'react';
import { motion } from 'framer-motion';

export default function Login({ onLogin, onSignup }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-6 bg-slate-800 rounded-lg shadow-md text-white"
    >
      <h2 className="text-2xl font-semibold">Welcome back</h2>
      <p className="text-sm text-slate-300 mt-1">Login to continue to your AI app</p>

      <div className="mt-6 space-y-4">
        <label className="block">
          <span className="text-sm text-slate-300">Username</span>
          <input
            value={username}
            onChange={e => setUsername(e.target.value)}
            className="mt-1 block w-full rounded-lg border border-slate-600 p-3 bg-slate-700 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
            placeholder="your username"
          />
        </label>

        <label className="block">
          <span className="text-sm text-slate-300">Password</span>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            className="mt-1 block w-full rounded-lg border border-slate-600 p-3 bg-slate-700 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
            placeholder="••••••"
          />
        </label>

        <button
          onClick={() => onLogin({ username, password })}
          className="w-full bg-gradient-to-r from-sky-500 to-indigo-500 text-white py-3 rounded-lg shadow hover:from-sky-600 hover:to-indigo-600 transition-colors"
        >
          Login
        </button>

        <div className="text-center text-sm text-slate-400">or</div>

        <button
          onClick={onSignup}
          className="w-full border border-slate-600 py-3 rounded-lg text-white hover:bg-slate-700 transition-colors"
        >
          Create account
        </button>
      </div>
    </motion.div>
  );
}
