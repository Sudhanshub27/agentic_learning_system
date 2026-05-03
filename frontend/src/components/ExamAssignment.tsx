"use client";

import React, { useState } from 'react';
import { AlertTriangle, Plus } from 'lucide-react';

interface ExamItem {
  title: string;
  overdueDays?: number;
  description: string;
  subject: string;
  tags: string[];
  type: 'Assignment' | 'Exam' | 'Review';
}

const demoItems: ExamItem[] = [
  { title: 'Data Structures Practice', overdueDays: 3, description: 'Implement linked lists and binary trees', subject: 'Python', tags: ['Upcoming', 'Midterm'], type: 'Assignment' },
  { title: 'Quantum Basics Quiz', overdueDays: 7, description: 'Test on superposition and entanglement', subject: 'Physics', tags: ['Upcoming', 'Quiz'], type: 'Exam' },
  { title: 'Calculus Review', description: 'Review derivatives and integrals', subject: 'Mathematics', tags: ['Upcoming', 'Midterm'], type: 'Review' },
];

const typeColors: Record<string, string> = {
  Assignment: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  Exam: 'bg-rose-500/20 text-rose-400 border-rose-500/30',
  Review: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30',
};

const tagColors: Record<string, string> = {
  Upcoming: 'bg-amber-500/20 text-amber-400',
  Midterm: 'bg-blue-500/20 text-blue-400',
  Quiz: 'bg-green-500/20 text-green-400',
};

export default function ExamAssignment() {
  const [filter, setFilter] = useState<'Upcoming' | 'All'>('Upcoming');

  const grouped = {
    Assignment: demoItems.filter(i => i.type === 'Assignment'),
    Exam: demoItems.filter(i => i.type === 'Exam'),
    Review: demoItems.filter(i => i.type === 'Review'),
  };

  return (
    <div className="card">
      <h2 className="text-lg font-bold mb-4">Exam & Assignment</h2>

      {/* Filters */}
      <div className="flex items-center gap-3 mb-5">
        {(['Upcoming', 'All'] as const).map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`text-sm font-medium px-3 py-1 rounded-lg transition-colors ${
              filter === f ? 'bg-[var(--bg-elevated)] text-white' : 'text-[var(--text-muted)] hover:text-[var(--text-secondary)]'
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Grouped Sections */}
      {Object.entries(grouped).map(([type, items]) => (
        <div key={type} className="mb-6">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-xs text-[var(--text-muted)]">▼</span>
            <span className={`badge border ${typeColors[type]}`}>{type}</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {items.map((item, idx) => (
              <div key={idx} className="card-elevated rounded-xl p-4 hover:border-[var(--border-muted)] transition-colors cursor-pointer">
                <h4 className="font-semibold text-sm mb-1" style={{ color: type === 'Assignment' ? '#a855f7' : type === 'Exam' ? '#f43f5e' : '#06b6d4' }}>
                  {item.title}
                </h4>
                {item.overdueDays && (
                  <div className="flex items-center gap-1 text-[12px] text-amber-400 mb-1">
                    <AlertTriangle className="w-3 h-3" /> Overdue by {item.overdueDays} days
                  </div>
                )}
                <p className="text-[12px] text-[var(--text-muted)] mb-2">{item.description}</p>
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-[11px] text-[var(--text-muted)]">📚 {item.subject}</span>
                  {item.tags.map(tag => (
                    <span key={tag} className={`badge text-[10px] ${tagColors[tag] || 'bg-zinc-700 text-zinc-300'}`}>{tag}</span>
                  ))}
                </div>
              </div>
            ))}

            {/* + new page */}
            <div className="border border-dashed border-[var(--border-muted)] rounded-xl flex items-center justify-center py-8 cursor-pointer hover:border-[var(--text-muted)] transition-colors">
              <span className="text-sm text-[var(--text-muted)] flex items-center gap-1"><Plus className="w-4 h-4" /> new page</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
