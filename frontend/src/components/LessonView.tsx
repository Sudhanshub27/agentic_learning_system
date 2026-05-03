"use client";

import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  ArrowLeft, ArrowRight, CheckCircle2, XCircle,
  Trophy, Loader2, ChevronRight, AlertCircle
} from 'lucide-react';
import { learningApi, StartSessionResponse, SubmitAnswersResponse, Question } from '@/lib/api';

type LessonStep = 'CURRICULUM' | 'LESSON' | 'QUIZ' | 'RESULTS';

interface LessonViewProps {
  sessionData: StartSessionResponse;
  onBack: () => void;
  onSessionUpdate: (data: StartSessionResponse) => void;
}

// Make all links open in new tab
const LinkRenderer = ({ href, children, ...props }: any) => (
  <a href={href} target="_blank" rel="noopener noreferrer" {...props}>{children}</a>
);

export default function LessonView({ sessionData, onBack, onSessionUpdate }: LessonViewProps) {
  const [step, setStep] = useState<LessonStep>('CURRICULUM');
  const [loading, setLoading] = useState(false);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [quizResults, setQuizResults] = useState<SubmitAnswersResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnswerChange = (qid: string, val: string) => {
    setAnswers(prev => ({ ...prev, [qid]: val }));
    setError(null);
  };

  const submitQuiz = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log("[LessonView] Submitting answers:", answers);
      const results = await learningApi.submitAnswers({
        session_id: sessionData.session_id,
        user_id: "demo_user_1",
        answers,
      });
      console.log("[LessonView] Received results:", results);
      
      if (!results || !results.grading_results) {
        throw new Error("Invalid response from server");
      }

      setQuizResults(results);
      setStep('RESULTS');
    } catch (err) {
      console.error("[LessonView] Submit failed:", err);
      setError("Failed to submit assessment. Please check your internet connection or backend server.");
    } finally {
      setLoading(false);
    }
  };

  const moveToNext = () => {
    if (!quizResults) return;
    onSessionUpdate({
      ...sessionData,
      current_topic: quizResults.next_topic || sessionData.current_topic,
      teaching_materials: quizResults.next_teaching_materials || "",
      assessment_questions: quizResults.next_assessment_questions || [],
    });
    setAnswers({});
    setQuizResults(null);
    setStep('LESSON');
  };

  const missingAnswersCount = sessionData.assessment_questions.length - Object.keys(answers).length;

  return (
    <div className="animate-fade-in-up">
      {/* Breadcrumb */}
      <button onClick={onBack} className="flex items-center gap-2 text-sm text-[var(--text-muted)] hover:text-[var(--text-primary)] mb-6 transition-colors">
        <ArrowLeft className="w-4 h-4" /> Back to Dashboard
      </button>

      {step === 'CURRICULUM' && (
        <div>
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold">Your Learning Path</h1>
            <button onClick={() => setStep('LESSON')} className="flex items-center gap-2 bg-amber-500 hover:bg-amber-400 text-black font-semibold px-5 py-2.5 rounded-xl transition-colors text-sm">
              Start First Lesson <ChevronRight className="w-4 h-4" />
            </button>
          </div>
          <div className="space-y-3">
            {sessionData.curriculum.map((topic, idx) => (
              <div key={idx} className="card flex items-start gap-4 hover:border-[var(--border-muted)] transition-colors">
                <div className="w-10 h-10 rounded-xl bg-[var(--bg-elevated)] flex items-center justify-center text-amber-400 font-bold text-sm shrink-0">
                  {idx + 1}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold">{topic.name}</h3>
                    <span className="text-xs text-[var(--text-muted)] bg-[var(--bg-elevated)] px-2 py-1 rounded">{topic.estimated_minutes} min</span>
                  </div>
                  <p className="text-sm text-[var(--text-muted)] mt-1 line-clamp-2">{topic.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {step === 'LESSON' && (
        <div>
          <div className="flex items-center gap-3 mb-2">
            <span className="text-xs text-amber-400 font-bold uppercase tracking-widest">Now Studying</span>
            <div className="h-px flex-1 bg-[var(--border-subtle)]"></div>
          </div>
          <div className="card mt-4">
            <h1 className="text-2xl font-bold mb-8">{sessionData.current_topic}</h1>
            <div className="prose prose-invert max-w-none">
              <ReactMarkdown remarkPlugins={[remarkGfm]} components={{ a: LinkRenderer }}>
                {sessionData.teaching_materials}
              </ReactMarkdown>
            </div>
            <div className="mt-10 pt-8 border-t border-[var(--border-subtle)] flex justify-end">
              <button onClick={() => setStep('QUIZ')} className="flex items-center gap-2 bg-amber-500 hover:bg-amber-400 text-black font-semibold px-6 py-3 rounded-xl transition-colors">
                Take Quiz <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}

      {step === 'QUIZ' && (
        <div>
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold mb-1">Knowledge Check</h2>
            <p className="text-[var(--text-muted)]">Test your understanding of {sessionData.current_topic}</p>
          </div>
          
          {error && (
            <div className="mb-6 p-4 bg-rose-500/10 border border-rose-500/20 rounded-xl flex items-center gap-3 text-rose-500">
              <AlertCircle className="w-5 h-5 shrink-0" />
              <p className="text-sm font-medium">{error}</p>
            </div>
          )}

          <div className="space-y-4">
            {sessionData.assessment_questions.map((q, idx) => (
              <div key={q.question_id} className="card">
                <div className="flex gap-3 mb-4">
                  <span className="bg-amber-500/15 text-amber-400 text-xs font-bold px-2.5 py-1 rounded h-fit">Q{idx + 1}</span>
                  <h3 className="font-semibold">{q.question_text}</h3>
                </div>
                {q.options ? (
                  <div className="space-y-2 ml-10">
                    {q.options.map(opt => (
                      <button key={opt} onClick={() => handleAnswerChange(q.question_id, opt)}
                        className={`w-full text-left p-3.5 rounded-xl border text-sm transition-all ${
                          answers[q.question_id] === opt
                            ? 'bg-amber-500/10 border-amber-500/50 text-white'
                            : 'bg-[var(--bg-elevated)] border-[var(--border-subtle)] text-[var(--text-secondary)] hover:border-[var(--border-muted)]'
                        }`}
                      >{opt}</button>
                    ))}
                  </div>
                ) : (
                  <textarea value={answers[q.question_id] || ""} onChange={e => handleAnswerChange(q.question_id, e.target.value)}
                    placeholder="Type your answer..."
                    className="w-full bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-xl px-4 py-3 text-white ml-10 max-w-[calc(100%-2.5rem)] min-h-[100px] focus:outline-none focus:border-amber-500/50 text-sm"
                  />
                )}
              </div>
            ))}
          </div>

          <div className="flex flex-col items-center mt-8">
            <button 
              disabled={loading || missingAnswersCount > 0} 
              onClick={submitQuiz}
              className="bg-white text-black hover:bg-zinc-200 disabled:opacity-40 disabled:cursor-not-allowed px-10 py-3.5 rounded-xl font-bold transition-all flex items-center gap-2 shadow-xl shadow-white/5"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Submit Assessment"}
            </button>
            {missingAnswersCount > 0 && !loading && (
              <p className="mt-3 text-[var(--text-muted)] text-xs font-medium">
                Please answer {missingAnswersCount} more question{missingAnswersCount > 1 ? 's' : ''} to submit.
              </p>
            )}
          </div>
        </div>
      )}

      {step === 'RESULTS' && quizResults && (
        <div className="space-y-6">
          <div className="text-center mb-8">
            <Trophy className="w-12 h-12 text-amber-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold mb-2">Results</h2>
            <p className="text-[var(--text-muted)] max-w-lg mx-auto">{quizResults.analysis_summary}</p>
          </div>

          <div className="space-y-3">
            {quizResults.grading_results.map((res, idx) => (
              <div key={idx} className={`card flex items-start gap-4 ${res.is_correct ? 'border-green-500/20' : 'border-rose-500/20'}`}>
                {res.is_correct ? (
                  <div className="bg-green-500/10 p-1.5 rounded-lg shrink-0">
                    <CheckCircle2 className="w-5 h-5 text-green-500" />
                  </div>
                ) : (
                  <div className="bg-rose-500/10 p-1.5 rounded-lg shrink-0">
                    <XCircle className="w-5 h-5 text-rose-500" />
                  </div>
                )}
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <h4 className="font-bold text-sm">{res.is_correct ? "Mastered" : "Needs Review"}</h4>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider ${res.is_correct ? 'bg-green-500/20 text-green-400' : 'bg-rose-500/20 text-rose-400'}`}>
                      Score: {res.score}%
                    </span>
                  </div>
                  <p className="text-sm text-[var(--text-secondary)] mb-3">{res.feedback}</p>
                  
                  {/* ALWAYS SHOW CORRECT ANSWER IF WRONG */}
                  {!res.is_correct && (
                    <div className="p-3 bg-[var(--bg-elevated)] rounded-xl border border-[var(--border-subtle)]">
                      <span className="text-[10px] text-[var(--text-muted)] uppercase font-bold block mb-1.5">Correct Explanation / Answer</span>
                      <div className="text-green-400 text-sm font-medium leading-relaxed">
                        {res.correct_answer}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>

          <div className="card mt-8 text-center bg-gradient-to-br from-[var(--bg-card)] to-[var(--bg-elevated)] border-amber-500/20">
            <h3 className="text-sm font-bold text-amber-500 uppercase tracking-widest mb-2">Next Step</h3>
            <p className="text-white font-medium mb-6 text-lg leading-relaxed">"{quizResults.next_action}"</p>
            
            <button 
              onClick={moveToNext} 
              className="group bg-amber-500 hover:bg-amber-400 text-black font-bold px-10 py-4 rounded-xl transition-all shadow-xl shadow-amber-500/20 flex items-center gap-2 mx-auto"
            >
              {quizResults.next_topic ? `Continue: ${quizResults.next_topic}` : "Continue Learning"}
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
