"use client";

import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  ArrowLeft, ArrowRight, CheckCircle2, XCircle,
  Trophy, Loader2, ChevronRight
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

  const handleAnswerChange = (qid: string, val: string) => {
    setAnswers(prev => ({ ...prev, [qid]: val }));
  };

  const submitQuiz = async () => {
    setLoading(true);
    try {
      const results = await learningApi.submitAnswers({
        session_id: sessionData.session_id,
        user_id: "demo_user_1",
        answers,
      });
      setQuizResults(results);
      setStep('RESULTS');
    } catch (err) {
      console.error("Submit failed:", err);
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
          <div className="flex justify-center mt-8">
            <button disabled={loading || Object.keys(answers).length < sessionData.assessment_questions.length} onClick={submitQuiz}
              className="bg-white text-black hover:bg-zinc-200 disabled:opacity-40 disabled:cursor-not-allowed px-10 py-3.5 rounded-xl font-bold transition-all flex items-center gap-2"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Submit Assessment"}
            </button>
          </div>
        </div>
      )}

      {step === 'RESULTS' && quizResults && (
        <div>
          <div className="text-center mb-8">
            <Trophy className="w-12 h-12 text-amber-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold mb-2">Results</h2>
            <p className="text-[var(--text-muted)] max-w-lg mx-auto">{quizResults.analysis_summary}</p>
          </div>
          <div className="space-y-3">
            {quizResults.grading_results.map((res, idx) => (
              <div key={idx} className={`card flex items-start gap-4 ${res.is_correct ? 'border-green-500/20' : 'border-rose-500/20'}`}>
                {res.is_correct ? <CheckCircle2 className="w-5 h-5 text-green-500 mt-0.5 shrink-0" /> : <XCircle className="w-5 h-5 text-rose-500 mt-0.5 shrink-0" />}
                <div>
                  <h4 className="font-semibold text-sm mb-1">{res.is_correct ? "Correct" : "Needs Review"}</h4>
                  <p className="text-sm text-[var(--text-muted)]">{res.feedback}</p>
                  {!res.is_correct && (
                    <div className="mt-2 p-3 bg-[var(--bg-elevated)] rounded-lg border border-[var(--border-subtle)]">
                      <span className="text-[11px] text-[var(--text-muted)] uppercase font-bold block mb-1">Answer</span>
                      <span className="text-green-400 text-sm">{res.correct_answer}</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
          <div className="card mt-6 text-center">
            <p className="text-amber-400 font-medium mb-4 text-lg">"{quizResults.next_action}"</p>
            <button onClick={moveToNext} className="bg-amber-500 hover:bg-amber-400 text-black font-semibold px-8 py-3 rounded-xl transition-colors">
              {quizResults.next_topic ? `Next: ${quizResults.next_topic}` : "Continue"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
