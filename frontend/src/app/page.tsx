"use client";

import React, { useState } from 'react';
import { Loader2, ArrowRight, BookOpen, Target, Sparkles, X } from 'lucide-react';
import Sidebar from '@/components/Sidebar';
import CoursesGrid from '@/components/CoursesGrid';
import DailyHabits from '@/components/DailyHabits';
import ExamAssignment from '@/components/ExamAssignment';
import LessonView from '@/components/LessonView';
import { learningApi, StartSessionResponse } from '@/lib/api';

type View = 'dashboard' | 'lesson' | 'new-session';

interface CourseEntry {
  name: string;
  level: string;
  progress: number;
  emoji: string;
  sessionData?: StartSessionResponse;
}

const EMOJIS = ['🧬', '⚗️', '📐', '💰', '⚛️', '🐍', '🎨', '🌍', '🔬', '📊'];

function getTimeProgress() {
  const now = new Date();
  const startOfYear = new Date(now.getFullYear(), 0, 1);
  const endOfYear = new Date(now.getFullYear() + 1, 0, 1);
  const yearPct = Math.round(((now.getTime() - startOfYear.getTime()) / (endOfYear.getTime() - startOfYear.getTime())) * 100);

  const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
  const endOfMonth = new Date(now.getFullYear(), now.getMonth() + 1, 1);
  const monthPct = Math.round(((now.getTime() - startOfMonth.getTime()) / (endOfMonth.getTime() - startOfMonth.getTime())) * 100);

  const day = now.getDay() || 7;
  const weekPct = Math.round((day / 7) * 100);

  return { yearPct, monthPct, weekPct };
}

export default function Dashboard() {
  const [view, setView] = useState<View>('dashboard');
  const [activeNav, setActiveNav] = useState('dashboard');
  const [courses, setCourses] = useState<CourseEntry[]>([]);
  const [activeCourse, setActiveCourse] = useState<CourseEntry | null>(null);

  // New Session Modal state
  const [showModal, setShowModal] = useState(false);
  const [subject, setSubject] = useState('');
  const [goals, setGoals] = useState('');
  const [level, setLevel] = useState('Beginner');
  const [loading, setLoading] = useState(false);

  const { yearPct, monthPct, weekPct } = getTimeProgress();

  const openNewSession = () => {
    setShowModal(true);
  };

  const startSession = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await learningApi.startSession({
        user_id: "demo_user_1",
        subject_name: subject,
        user_goals: goals,
        current_level: level,
      });
      const newCourse: CourseEntry = {
        name: subject,
        level,
        progress: 0,
        emoji: EMOJIS[courses.length % EMOJIS.length],
        sessionData: data,
      };
      setCourses(prev => [...prev, newCourse]);
      setActiveCourse(newCourse);
      setShowModal(false);
      setSubject('');
      setGoals('');
      setView('lesson');
    } catch (err) {
      console.error("Failed to start:", err);
      alert("Failed to start session. Check that the backend is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const selectCourse = (name: string) => {
    const c = courses.find(c => c.name === name);
    if (c?.sessionData) {
      setActiveCourse(c);
      setView('lesson');
    }
  };

  const handleSessionUpdate = (data: StartSessionResponse) => {
    if (!activeCourse) return;
    const updated = { ...activeCourse, sessionData: data, progress: Math.min(activeCourse.progress + 20, 100) };
    setActiveCourse(updated);
    setCourses(prev => prev.map(c => c.name === updated.name ? updated : c));
  };

  return (
    <div className="flex min-h-screen">
      <Sidebar
        activeView={activeNav}
        onNavigate={(v) => { setActiveNav(v); setView('dashboard'); }}
        onNewSession={openNewSession}
        yearProgress={yearPct}
        monthProgress={monthPct}
        weekProgress={weekPct}
      />

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-6 lg:p-8">
        {view === 'dashboard' && (
          <div className="max-w-[1200px] mx-auto space-y-6">
            <CoursesGrid courses={courses} onStartNew={openNewSession} onSelectCourse={selectCourse} />
            <DailyHabits />
            <ExamAssignment />
          </div>
        )}

        {view === 'lesson' && activeCourse?.sessionData && (
          <div className="max-w-[900px] mx-auto">
            <LessonView
              sessionData={activeCourse.sessionData}
              onBack={() => setView('dashboard')}
              onSessionUpdate={handleSessionUpdate}
            />
          </div>
        )}
      </main>

      {/* ── New Session Modal ── */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
          <div className="bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-2xl w-full max-w-lg p-8 relative animate-fade-in-up">
            <button onClick={() => setShowModal(false)} className="absolute top-4 right-4 text-[var(--text-muted)] hover:text-white transition-colors">
              <X className="w-5 h-5" />
            </button>
            <h2 className="text-xl font-bold mb-6">Start a New Course</h2>
            <form onSubmit={startSession} className="space-y-5">
              <div>
                <label className="flex items-center text-sm font-medium text-[var(--text-secondary)] mb-2">
                  <BookOpen className="w-4 h-4 mr-2 text-amber-400" /> Subject
                </label>
                <input type="text" required value={subject} onChange={e => setSubject(e.target.value)}
                  placeholder="e.g. Quantum Computing, Python, Economics..."
                  className="w-full bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-xl px-4 py-3 text-white placeholder-[var(--text-muted)] focus:outline-none focus:border-amber-500/50 text-sm"
                />
              </div>
              <div>
                <label className="flex items-center text-sm font-medium text-[var(--text-secondary)] mb-2">
                  <Target className="w-4 h-4 mr-2 text-amber-400" /> Goals
                </label>
                <input type="text" value={goals} onChange={e => setGoals(e.target.value)}
                  placeholder="e.g. Pass an exam, build a project..."
                  className="w-full bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-xl px-4 py-3 text-white placeholder-[var(--text-muted)] focus:outline-none focus:border-amber-500/50 text-sm"
                />
              </div>
              <div>
                <label className="flex items-center text-sm font-medium text-[var(--text-secondary)] mb-2">
                  <Sparkles className="w-4 h-4 mr-2 text-amber-400" /> Level
                </label>
                <select value={level} onChange={e => setLevel(e.target.value)}
                  className="w-full bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-amber-500/50 text-sm appearance-none cursor-pointer"
                >
                  <option>Absolute Beginner</option>
                  <option>Beginner</option>
                  <option>Intermediate</option>
                  <option>Advanced</option>
                </select>
              </div>
              <button type="submit" disabled={loading}
                className="w-full bg-amber-500 hover:bg-amber-400 disabled:opacity-50 text-black font-semibold py-3 rounded-xl flex items-center justify-center gap-2 transition-colors"
              >
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <><span>Generate Journey</span><ArrowRight className="w-4 h-4" /></>}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
