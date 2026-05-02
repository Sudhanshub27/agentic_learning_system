"use client";

import { useState } from 'react';
import { learningApi, StartSessionResponse } from '@/lib/api';
import { BookOpen, BrainCircuit, Sparkles, Target, ArrowRight, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function Dashboard() {
  const [subject, setSubject] = useState("");
  const [goals, setGoals] = useState("");
  const [level, setLevel] = useState("Beginner");
  
  const [loading, setLoading] = useState(false);
  const [sessionData, setSessionData] = useState<StartSessionResponse | null>(null);

  const startSession = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await learningApi.startSession({
        user_id: "demo_user_1",
        subject_name: subject,
        user_goals: goals,
        current_level: level
      });
      setSessionData(data);
    } catch (error) {
      console.error("Failed to start session:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen relative overflow-hidden flex flex-col items-center justify-center p-6">
      {/* Animated Background Blobs */}
      <div className="absolute top-0 -left-4 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-2xl opacity-20 animate-blob"></div>
      <div className="absolute top-0 -right-4 w-72 h-72 bg-indigo-500 rounded-full mix-blend-multiply filter blur-2xl opacity-20 animate-blob animation-delay-2000"></div>
      <div className="absolute -bottom-8 left-20 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-2xl opacity-20 animate-blob animation-delay-4000"></div>

      <div className="relative z-10 w-full max-w-4xl">
        {!sessionData ? (
          <div className="glass-panel p-8 md:p-12 rounded-3xl shadow-2xl border border-white/10">
            <div className="text-center mb-10">
              <div className="inline-flex items-center justify-center p-3 bg-indigo-500/10 rounded-2xl mb-4 border border-indigo-500/20">
                <BrainCircuit className="w-8 h-8 text-indigo-400" />
              </div>
              <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-white to-indigo-200">
                Agentic Learning System
              </h1>
              <p className="text-slate-400 text-lg max-w-2xl mx-auto">
                Enter any subject and our autonomous AI agents will generate a personalized curriculum and teach it to you interactively.
              </p>
            </div>

            <form onSubmit={startSession} className="space-y-6 max-w-xl mx-auto">
              <div>
                <label className="flex items-center text-sm font-medium text-slate-300 mb-2">
                  <BookOpen className="w-4 h-4 mr-2" /> What do you want to learn?
                </label>
                <input
                  type="text"
                  required
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  placeholder="e.g. Quantum Physics, Spanish, Python..."
                  className="w-full bg-slate-900/50 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                />
              </div>

              <div>
                <label className="flex items-center text-sm font-medium text-slate-300 mb-2">
                  <Target className="w-4 h-4 mr-2" /> What are your goals?
                </label>
                <input
                  type="text"
                  required
                  value={goals}
                  onChange={(e) => setGoals(e.target.value)}
                  placeholder="e.g. Pass an exam, build a project..."
                  className="w-full bg-slate-900/50 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                />
              </div>

              <div>
                <label className="flex items-center text-sm font-medium text-slate-300 mb-2">
                  <Sparkles className="w-4 h-4 mr-2" /> Current Experience Level
                </label>
                <select
                  value={level}
                  onChange={(e) => setLevel(e.target.value)}
                  className="w-full bg-slate-900/50 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all appearance-none"
                >
                  <option value="Absolute Beginner">Absolute Beginner</option>
                  <option value="Beginner">Beginner</option>
                  <option value="Intermediate">Intermediate</option>
                  <option value="Advanced">Advanced</option>
                </select>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full relative group overflow-hidden rounded-xl p-[1px]"
              >
                <span className="absolute inset-0 bg-gradient-to-r from-indigo-500 via-purple-500 to-indigo-500 rounded-xl opacity-70 group-hover:opacity-100 transition-opacity duration-300"></span>
                <div className="relative bg-slate-950 px-8 py-4 rounded-xl flex items-center justify-center transition-all duration-300 group-hover:bg-opacity-0">
                  {loading ? (
                    <Loader2 className="w-5 h-5 animate-spin text-white" />
                  ) : (
                    <>
                      <span className="text-white font-semibold mr-2">Start Learning Journey</span>
                      <ArrowRight className="w-5 h-5 text-white group-hover:translate-x-1 transition-transform" />
                    </>
                  )}
                </div>
              </button>
            </form>
          </div>
        ) : (
          <div className="glass-panel p-8 rounded-3xl shadow-2xl border border-white/10">
            <h2 className="text-2xl font-bold text-white mb-6">Your Curriculum Prepared!</h2>
            <div className="space-y-4">
              {sessionData.curriculum.map((topic, idx) => (
                <div key={idx} className="p-4 bg-slate-800/50 rounded-xl border border-slate-700">
                  <div className="flex items-center">
                    <span className="bg-indigo-500 text-white text-xs font-bold px-2 py-1 rounded-md mr-3">
                      Module {topic.order_index}
                    </span>
                    <h3 className="text-lg font-semibold text-white">{topic.name}</h3>
                  </div>
                  <p className="text-slate-400 mt-2 text-sm">{topic.description}</p>
                </div>
              ))}
            </div>
            
            <div className="mt-8 pt-8 border-t border-slate-700">
              <h3 className="text-xl font-bold text-indigo-300 mb-4">First Lesson: {sessionData.current_topic}</h3>
              <div className="prose prose-invert max-w-none bg-slate-900/50 p-6 rounded-xl border border-slate-700 overflow-y-auto max-h-96">
                {/* In a real app we would render markdown here using react-markdown */}
                <pre className="whitespace-pre-wrap font-sans text-slate-300">{sessionData.teaching_materials}</pre>
              </div>
            </div>
            
            {/* The rest of the interactive quiz UI would go here */}
          </div>
        )}
      </div>
    </main>
  );
}
