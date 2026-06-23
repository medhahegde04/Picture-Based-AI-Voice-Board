import React, { useState } from 'react';
import { motion } from 'framer-motion';

export default function Signup({ onSignup, onLogin }) {
  const [username, setUsername] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  function handleSignup() {
    if (!username || !name || !email || !password) return alert('Please fill all fields');
    onSignup({ username, name, email, password });
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-6 bg-slate-800 rounded-lg shadow-md min-h-[80vh] text-white"
    >
      <h2 className="text-2xl font-semibold text-white">Create account</h2>
      <p className="text-sm text-slate-300 mt-1">Sign up to start using the app</p>

      <div className="mt-6 space-y-4">
        <label className="block">
          <span className="text-sm text-slate-300">Username</span>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="mt-1 block w-full rounded border border-slate-600 p-3 bg-slate-700 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
            placeholder="username"
          />
        </label>

        <label className="block">
          <span className="text-sm text-slate-300">Name</span>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="mt-1 block w-full rounded border border-slate-600 p-3 bg-slate-700 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
            placeholder="Your full name"
          />
        </label>

        <label className="block">
          <span className="text-sm text-slate-300">Email</span>
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 block w-full rounded border border-slate-600 p-3 bg-slate-700 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
            placeholder="you@example.com"
          />
        </label>

        <label className="block">
          <span className="text-sm text-slate-300">Password</span>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 block w-full rounded border border-slate-600 p-3 bg-slate-700 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
            placeholder="Choose a password"
          />
        </label>

        <button
          onClick={handleSignup}
          className="w-full bg-gradient-to-r from-sky-500 to-indigo-500 text-white py-3 rounded-lg shadow hover:from-sky-600 hover:to-indigo-600 transition-colors"
        >
          Sign up
        </button>

        <button
          onClick={onLogin}
          className="w-full border border-slate-600 py-3 rounded-lg text-white hover:bg-slate-700 transition-colors"
        >
          Back to login
        </button>
      </div>
    </motion.div>
  );
}
