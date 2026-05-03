"use client";

import React from 'react';
import { BookOpen, Plus, Flame, Clock } from 'lucide-react';

interface Course {
  name: string;
  level: string;
  progress: number;
  emoji: string;
}

interface CoursesGridProps {
  courses: Course[];
  onStartNew: () => void;
  onSelectCourse: (name: string) => void;
}

const levelColors: Record<string, string> = {
  beginner: 'bg-green-500/20 text-green-400',
  intermediate: 'bg-amber-500/20 text-amber-400',
  advanced: 'bg-rose-500/20 text-rose-400',
  medium: 'bg-amber-500/20 text-amber-400',
  hard: 'bg-rose-500/20 text-rose-400',
};

const cardGradients = [
  'course-card-green', 'course-card-cyan', 'course-card-purple',
  'course-card-amber', 'course-card-rose', 'course-card-blue',
];

export default function CoursesGrid({ courses, onStartNew, onSelectCourse }: CoursesGridProps) {
  return (
    <div className="card">
      <h2 className="text-lg font-bold mb-4 text-amber-400 flex items-center gap-2">
        <BookOpen className="w-5 h-5" /> Courses
      </h2>
      <div className="flex gap-4 overflow-x-auto pb-2">
        {courses.map((course, idx) => (
          <div
            key={course.name}
            onClick={() => onSelectCourse(course.name)}
            className="min-w-[180px] max-w-[200px] cursor-pointer group"
          >
            {/* Icon Area */}
            <div className={`${cardGradients[idx % cardGradients.length]} rounded-xl p-6 flex items-center justify-center mb-3 group-hover:scale-[1.03] transition-transform`}>
              <span className="text-4xl">{course.emoji}</span>
            </div>
            {/* Info */}
            <h3 className="font-semibold text-sm mb-1 truncate">{course.name}</h3>
            <span className={`badge ${levelColors[course.level.toLowerCase()] || levelColors['medium']}`}>
              {course.level}
            </span>
            {/* Progress */}
            <div className="flex items-center gap-2 mt-2">
              <div className="progress-track">
                <div className="progress-fill bg-amber-500" style={{ width: `${course.progress}%` }}></div>
              </div>
              <span className="text-[11px] text-[var(--text-muted)] font-bold">{course.progress}%</span>
            </div>
          </div>
        ))}

        {/* + New Course */}
        <div
          onClick={onStartNew}
          className="min-w-[180px] max-w-[200px] border-2 border-dashed border-[var(--border-muted)] rounded-xl flex flex-col items-center justify-center cursor-pointer hover:border-amber-500/50 transition-colors py-10"
        >
          <Plus className="w-8 h-8 text-[var(--text-muted)] mb-2" />
          <span className="text-sm text-[var(--text-muted)]">New Course</span>
        </div>
      </div>
    </div>
  );
}
