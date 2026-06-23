import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

export default function Profile({ user, onUpdate, onBack, onLogout }) {
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({ username: '', name: '', email: '', password: '' });

  useEffect(() => {
    if (user)
      setForm({
        username: user.username || '',
        name: user.name || '',
        email: user.email || '',
        password: user.password || '',
      });
  }, [user]);

  function save() {
    onUpdate(form);
    setEditing(false);
    alert('Profile updated');
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="p-6 bg-slate-800 rounded-lg shadow-md text-white min-h-[80vh]"
    >
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Profile</h2>
        <div className="space-x-2">
          <button onClick={onBack} className="text-sm text-slate-300 hover:text-white">
            Back
          </button>
          <button onClick={onLogout} className="text-sm text-red-400 hover:text-red-500">
            Logout
          </button>
        </div>
      </div>

      {!editing ? (
        <div className="space-y-3">
          <div>
            <strong>Username:</strong> {form.username}
          </div>
          <div>
            <strong>Name:</strong> {form.name}
          </div>
          <div>
            <strong>Email:</strong> {form.email}
          </div>
          <div>
            <strong>Password:</strong> {'•'.repeat(8)}
          </div>
          <button
            onClick={() => setEditing(true)}
            className="mt-4 w-full bg-gradient-to-r from-sky-500 to-indigo-500 text-white py-2 rounded hover:from-sky-600 hover:to-indigo-600 transition-colors"
          >
            Edit profile
          </button>
        </div>
      ) : (
        <div className="space-y-3">
          <label className="block">
            <span className="text-sm text-slate-300">Username</span>
            <input
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
              className="mt-1 block w-full rounded border border-slate-600 p-2 bg-slate-700 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
            />
          </label>
          <label className="block">
            <span className="text-sm text-slate-300">Name</span>
            <input
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              className="mt-1 block w-full rounded border border-slate-600 p-2 bg-slate-700 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
            />
          </label>
          <label className="block">
            <span className="text-sm text-slate-300">Email</span>
            <input
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="mt-1 block w-full rounded border border-slate-600 p-2 bg-slate-700 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
            />
          </label>
          <label className="block">
            <span className="text-sm text-slate-300">Password</span>
            <input
              type="password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              className="mt-1 block w-full rounded border border-slate-600 p-2 bg-slate-700 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
            />
          </label>
          <div className="flex gap-2">
            <button
              onClick={save}
              className="flex-1 bg-sky-600 text-white py-2 rounded hover:bg-sky-700 transition-colors"
            >
              Save
            </button>
            <button
              onClick={() => setEditing(false)}
              className="flex-1 border border-slate-600 py-2 rounded hover:bg-slate-700 transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </motion.div>
  );
}
