"use client";

import React, { useState, useEffect } from 'react';
import { 
  Loader2, ArrowRight, BookOpen, Target, Sparkles, X, Trash2, User,
  History, BarChart3, Brain, FileText, GraduationCap, ClipboardList, 
  CheckSquare, Plus, AlertCircle
} from 'lucide-react';
import Sidebar from '@/components/Sidebar';
import CoursesGrid from '@/components/CoursesGrid';
import DailyHabits, { DEFAULT_HABITS, HabitData } from '@/components/DailyHabits';
import ExamAssignment from '@/components/ExamAssignment';
import LessonView from '@/components/LessonView';
import { learningApi, StartSessionResponse } from '@/lib/api';

type View = 'dashboard' | 'lesson' | 'profile' | 'sessions' | 'progress' | 'memory' | 'notes';

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
  const [habits, setHabits] = useState<HabitData[]>([]);
  const [activeCourse, setActiveCourse] = useState<CourseEntry | null>(null);

  // New Session Modal state
  const [showModal, setShowModal] = useState(false);
  const [subject, setSubject] = useState('');
  const [goals, setGoals] = useState('');
  const [level, setLevel] = useState('Beginner');
  const [loading, setLoading] = useState(false);

  const { yearPct, monthPct, weekPct } = getTimeProgress();

  // Load data from localStorage
  useEffect(() => {
    const savedCourses = localStorage.getItem('als_courses');
    if (savedCourses) setCourses(JSON.parse(savedCourses));

    const savedHabits = localStorage.getItem('als_habits');
    if (savedHabits) setHabits(JSON.parse(savedHabits));
    else setHabits(DEFAULT_HABITS);
  }, []);

  // Save data to localStorage
  useEffect(() => {
    if (courses.length > 0) localStorage.setItem('als_courses', JSON.stringify(courses));
    if (habits.length > 0) localStorage.setItem('als_habits', JSON.stringify(habits));
  }, [courses, habits]);

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

  const handleToggleHabit = (habitName: string, date: string) => {
    setHabits(prev => prev.map(h => {
      if (h.name === habitName) {
        const completed = h.completedDates.includes(date)
          ? h.completedDates.filter(d => d !== date)
          : [...h.completedDates, date];
        return { ...h, completedDates: completed };
      }
      return h;
    }));
  };

  const clearData = () => {
    if (confirm("Are you sure you want to clear all local data? This cannot be undone.")) {
      localStorage.removeItem('als_courses');
      localStorage.removeItem('als_habits');
      setCourses([]);
      setHabits(DEFAULT_HABITS);
      setActiveCourse(null);
      setView('dashboard');
      setActiveNav('dashboard');
    }
  };

  const renderPlaceholderView = (title: string, icon: React.ReactNode, description: string) => (
    <div className="max-w-[800px] mx-auto space-y-8 animate-fade-in-up mt-12 text-center">
      <div className="inline-flex items-center justify-center p-6 bg-amber-500/10 rounded-3xl mb-4 border border-amber-500/20">
        {icon}
      </div>
      <h1 className="text-4xl font-bold">{title}</h1>
      <p className="text-[var(--text-muted)] text-lg max-w-xl mx-auto">{description}</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
        <div className="card-elevated p-8 text-left">
          <h3 className="font-bold text-lg mb-2">Upcoming Feature</h3>
          <p className="text-sm text-[var(--text-muted)]">This view is currently being optimized for your custom learning profile. Stay tuned!</p>
        </div>
        <div className="card-elevated p-8 text-left">
          <h3 className="font-bold text-lg mb-2">Data Integration</h3>
          <p className="text-sm text-[var(--text-muted)]">Once active, this will sync with your AI agents to provide deep insights into your learning journey.</p>
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex min-h-screen">
      <Sidebar
        activeView={activeNav}
        onNavigate={(v) => { 
          setActiveNav(v); 
          if (v === 'profile') setView('profile');
          else if (v === 'sessions') setView('sessions');
          else if (v === 'progress') setView('progress');
          else if (v === 'memory') setView('memory');
          else if (v === 'notes') setView('notes');
          else setView('dashboard'); 
        }}
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
            <DailyHabits habits={habits} onToggleHabit={handleToggleHabit} />
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

        {view === 'sessions' && renderPlaceholderView(
          "Learning Sessions", 
          <History className="w-12 h-12 text-amber-500" />,
          "Review your past AI-guided learning sessions, curriculum changes, and historical progress."
        )}

        {view === 'progress' && renderPlaceholderView(
          "Mastery Progress", 
          <BarChart3 className="w-12 h-12 text-cyan-400" />,
          "Visual breakdown of your mastery levels across all subjects, powered by our evaluation agents."
        )}

        {view === 'memory' && renderPlaceholderView(
          "Memory Bank", 
          <Brain className="w-12 h-12 text-purple-400" />,
          "Access your RAG-powered knowledge base. See what the system has learned about your learning style."
        )}

        {view === 'notes' && renderPlaceholderView(
          "Smart Notes", 
          <FileText className="w-12 h-12 text-rose-400" />,
          "AI-summarized notes from your lessons, organized by topic and difficulty level."
        )}

        {view === 'profile' && (
          <div className="max-w-[800px] mx-auto space-y-8 animate-fade-in-up">
            <div className="flex items-center gap-4 mb-8">
              <div className="w-16 h-16 rounded-2xl bg-amber-500 flex items-center justify-center">
                <User className="w-8 h-8 text-black" />
              </div>
              <div>
                <h1 className="text-3xl font-bold">User Profile</h1>
                <p className="text-[var(--text-muted)] text-sm">Manage your local storage and persistence settings.</p>
              </div>
            </div>

            <div className="card">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Trash2 className="w-5 h-5 text-rose-500" /> Danger Zone
              </h2>
              <p className="text-sm text-[var(--text-secondary)] mb-6">
                Currently, your data is stored locally in your browser's <strong>localStorage</strong>. 
                Use this button if you want to reset everything and start from scratch.
              </p>
              <button 
                onClick={clearData}
                className="bg-rose-500/10 hover:bg-rose-500/20 text-rose-500 border border-rose-500/30 px-6 py-3 rounded-xl font-bold transition-all flex items-center gap-2"
              >
                <Trash2 className="w-4 h-4" /> Clear All Local Data
              </button>
            </div>

            <div className="card">
              <h2 className="text-xl font-bold mb-4">Local Statistics</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="card-elevated">
                  <span className="text-[var(--text-muted)] text-xs uppercase font-bold">Total Courses</span>
                  <div className="text-2xl font-bold mt-1">{courses.length}</div>
                </div>
                <div className="card-elevated">
                  <span className="text-[var(--text-muted)] text-xs uppercase font-bold">Habits Tracked</span>
                  <div className="text-2xl font-bold mt-1">{habits.length}</div>
                </div>
              </div>
            </div>
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
