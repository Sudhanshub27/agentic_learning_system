"use client";

import React from 'react';
import { Flame, Dumbbell, BookOpen, Brain, Check } from 'lucide-react';

export interface HabitData {
  name: string;
  color: string;
  icon: string; // emoji-style key
  completedDates: string[]; // ISO date strings "2026-05-03"
}

export const DEFAULT_HABITS: HabitData[] = [
  { name: 'Meditate', color: '#f43f5e', icon: 'flame', completedDates: [] },
  { name: 'Study', color: '#22c55e', icon: 'book', completedDates: [] },
  { name: 'Exercise', color: '#3b82f6', icon: 'dumbbell', completedDates: [] },
  { name: 'Review Flashcards', color: '#a855f7', icon: 'brain', completedDates: [] },
];

const ICON_MAP: Record<string, React.ReactNode> = {
  flame: <Flame className="w-4 h-4" />,
  book: <BookOpen className="w-4 h-4" />,
  dumbbell: <Dumbbell className="w-4 h-4" />,
  brain: <Brain className="w-4 h-4" />,
};

function getToday(): string {
  return new Date().toISOString().split('T')[0];
}

function getLast35Days(): string[] {
  const days: string[] = [];
  const today = new Date();
  for (let i = 34; i >= 0; i--) {
    const d = new Date(today);
    d.setDate(d.getDate() - i);
    days.push(d.toISOString().split('T')[0]);
  }
  return days;
}

function getStreak(completedDates: string[]): number {
  const set = new Set(completedDates);
  let streak = 0;
  const today = new Date();
  for (let i = 0; i < 365; i++) {
    const d = new Date(today);
    d.setDate(d.getDate() - i);
    const key = d.toISOString().split('T')[0];
    if (set.has(key)) streak++;
    else break;
  }
  return streak;
}

interface DailyHabitsProps {
  habits: HabitData[];
  onToggleHabit: (habitName: string, date: string) => void;
}

export default function DailyHabits({ habits, onToggleHabit }: DailyHabitsProps) {
  const days = getLast35Days();
  const today = getToday();

  return (
    <div className="card">
      <h2 className="text-lg font-bold mb-4 text-amber-400 flex items-center gap-2">
        🔥 Daily Habits
      </h2>
      <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
        {habits.map(habit => {
          const streak = getStreak(habit.completedDates);
          const completedSet = new Set(habit.completedDates);
          const doneToday = completedSet.has(today);

          return (
            <div key={habit.name} className="card-elevated rounded-xl p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span style={{ color: habit.color }}>{ICON_MAP[habit.icon]}</span>
                  <span className="font-semibold text-sm">{habit.name}</span>
                </div>
                {/* Today toggle */}
                <button
                  onClick={() => onToggleHabit(habit.name, today)}
                  className={`w-7 h-7 rounded-lg flex items-center justify-center transition-all text-xs font-bold ${
                    doneToday
                      ? 'text-black'
                      : 'border border-[var(--border-muted)] text-[var(--text-muted)] hover:border-[var(--text-secondary)]'
                  }`}
                  style={doneToday ? { backgroundColor: habit.color } : {}}
                  title={doneToday ? 'Completed today! Click to undo.' : 'Mark as done today'}
                >
                  {doneToday ? <Check className="w-4 h-4" /> : ''}
                </button>
              </div>
              {/* Heat Map Grid */}
              <div className="habit-grid mb-3">
                {days.map(day => {
                  const done = completedSet.has(day);
                  return (
                    <div
                      key={day}
                      className="habit-cell"
                      title={`${day}${done ? ' ✓' : ''}`}
                      style={{
                        backgroundColor: done ? habit.color : 'rgba(255,255,255,0.04)',
                        opacity: done ? 0.85 : 1,
                      }}
                    ></div>
                  );
                })}
              </div>
              <div className="flex items-center justify-between text-[12px] text-[var(--text-muted)]">
                <span className="flex items-center gap-1">
                  <Flame className="w-3 h-3" style={{ color: habit.color }} />
                  {doneToday ? 'Done' : 'Pending'}
                </span>
                <span className="font-bold">{streak} day streak</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
