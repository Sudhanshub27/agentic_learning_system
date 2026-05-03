"use client";

import React from 'react';
import {
  BookOpen, GraduationCap, ClipboardList, CheckSquare,
  FileText, LayoutDashboard, History, Brain, BarChart3,
  Plus, BrainCircuit
} from 'lucide-react';

interface SidebarProps {
  activeView: string;
  onNavigate: (view: string) => void;
  onNewSession: () => void;
  yearProgress: number;
  monthProgress: number;
  weekProgress: number;
}

export default function Sidebar({ activeView, onNavigate, onNewSession, yearProgress, monthProgress, weekProgress }: SidebarProps) {
  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="flex items-center gap-2 px-2 mb-2">
        <div className="bg-amber-500 p-1.5 rounded-lg">
          <BrainCircuit className="w-5 h-5 text-black" />
        </div>
        <span className="text-base font-bold tracking-tight">Agentic Learning</span>
      </div>

      {/* Quick Actions */}
      <div>
        <h3 className="sidebar-section-title">Quick Action</h3>
        <div className="space-y-1">
          <button onClick={onNewSession} className="sidebar-btn">
            <Plus className="w-4 h-4 text-amber-500" /> <span>New Course</span>
          </button>
          <button className="sidebar-btn">
            <GraduationCap className="w-4 h-4 text-cyan-400" /> <span>New Exam</span>
          </button>
          <button className="sidebar-btn">
            <ClipboardList className="w-4 h-4 text-purple-400" /> <span>New Assignment</span>
          </button>
          <button className="sidebar-btn">
            <CheckSquare className="w-4 h-4 text-green-400" /> <span>New Task</span>
          </button>
          <button className="sidebar-btn">
            <FileText className="w-4 h-4 text-rose-400" /> <span>New Note</span>
          </button>
        </div>
      </div>

      {/* Navigation */}
      <div>
        <h3 className="sidebar-section-title">Navigation</h3>
        <div className="space-y-1">
          {[
            { id: 'dashboard', icon: LayoutDashboard, label: 'Dashboard' },
            { id: 'sessions', icon: History, label: 'Sessions' },
            { id: 'progress', icon: BarChart3, label: 'Progress' },
            { id: 'memory', icon: Brain, label: 'Memory Bank' },
            { id: 'notes', icon: FileText, label: 'Notes' },
          ].map(item => (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={`sidebar-btn ${activeView === item.id ? 'active' : ''}`}
            >
              <item.icon className="w-4 h-4" /> <span>{item.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Status */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h3 className="sidebar-section-title mb-0">Status</h3>
          <span className="text-[11px] text-[var(--text-muted)]">
            {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
        <div className="space-y-3">
          {[
            { label: 'YEAR', pct: yearProgress, color: 'bg-amber-500' },
            { label: 'MONTH', pct: monthProgress, color: 'bg-cyan-500' },
            { label: 'WEEK', pct: weekProgress, color: 'bg-purple-500' },
          ].map(bar => (
            <div key={bar.label}>
              <div className="flex items-center justify-between mb-1">
                <span className="text-[11px] font-semibold text-[var(--text-muted)] tracking-wider">{bar.label}</span>
                <span className="text-[11px] font-bold text-[var(--text-secondary)]">{bar.pct}%</span>
              </div>
              <div className="progress-track">
                <div className={`progress-fill ${bar.color}`} style={{ width: `${bar.pct}%` }}></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </aside>
  );
}
