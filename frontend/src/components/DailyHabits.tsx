"use client";

import React from 'react';
import { Flame, Dumbbell, BookOpen, Brain } from 'lucide-react';

interface Habit {
  name: string;
  icon: React.ReactNode;
  streak: number;
  cells: number[]; // 0=empty, 1=done, 2=missed
  color: string;
}

function generateHabitCells(): number[] {
  const cells: number[] = [];
  const today = new Date();
  for (let i = 34; i >= 0; i--) {
    const d = new Date(today);
    d.setDate(d.getDate() - i);
    if (i === 0) cells.push(0); // today not yet done
    else cells.push(Math.random() > 0.25 ? 1 : 2);
  }
  return cells;
}

const defaultHabits: Habit[] = [
  { name: 'Meditate', icon: <Flame className="w-4 h-4" />, streak: 8, cells: generateHabitCells(), color: '#f43f5e' },
  { name: 'Study', icon: <BookOpen className="w-4 h-4" />, streak: 12, cells: generateHabitCells(), color: '#22c55e' },
  { name: 'Exercise', icon: <Dumbbell className="w-4 h-4" />, streak: 5, cells: generateHabitCells(), color: '#3b82f6' },
  { name: 'Review Flashcards', icon: <Brain className="w-4 h-4" />, streak: 3, cells: generateHabitCells(), color: '#a855f7' },
];

export default function DailyHabits() {
  return (
    <div className="card">
      <h2 className="text-lg font-bold mb-4 text-amber-400 flex items-center gap-2">
        🔥 Daily Habits
      </h2>
      <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
        {defaultHabits.map(habit => (
          <div key={habit.name} className="card-elevated rounded-xl p-4">
            <div className="flex items-center gap-2 mb-3">
              <span style={{ color: habit.color }}>{habit.icon}</span>
              <span className="font-semibold text-sm">{habit.name}</span>
            </div>
            {/* Heat Map Grid */}
            <div className="habit-grid mb-3">
              {habit.cells.map((val, i) => (
                <div
                  key={i}
                  className="habit-cell"
                  style={{
                    backgroundColor: val === 1 ? habit.color : val === 2 ? 'rgba(255,255,255,0.04)' : 'rgba(255,255,255,0.08)',
                    opacity: val === 1 ? 0.85 : 1,
                  }}
                ></div>
              ))}
            </div>
            <div className="flex items-center justify-between text-[12px] text-[var(--text-muted)]">
              <span className="flex items-center gap-1">
                <Flame className="w-3 h-3" style={{ color: habit.color }} /> Pending
              </span>
              <span>{habit.streak} DAYS</span>
            </div>
            <div className="text-[11px] text-[var(--text-muted)] mt-1">Done</div>
          </div>
        ))}
      </div>
    </div>
  );
}
