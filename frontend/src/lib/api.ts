import axios from 'axios';

// Ensure this matches your FastAPI backend port
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface StartSessionRequest {
  user_id: string;
  subject_name: string;
  subject_description?: string;
  user_goals?: string;
  current_level?: string;
}

export interface Topic {
  name: string;
  description: string;
  difficulty_level: number;
  order_index: number;
  prerequisites: string[];
  content_type: string;
  learning_objectives: string[];
  estimated_minutes: number;
}

export interface Question {
  question_id: string;
  question_text: string;
  question_type: string;
  options?: string[];
}

export interface StartSessionResponse {
  session_id: string;
  curriculum: Topic[];
  current_topic: string;
  teaching_materials: string;
  assessment_questions: Question[];
}

export interface SubmitAnswersRequest {
  session_id: string;
  user_id: string;
  answers: Record<string, string>;
}

export interface GradingResult {
  question_id: string;
  is_correct: boolean;
  score: number;
  feedback: string;
  correct_answer: string;
}

export interface SubmitAnswersResponse {
  grading_results: GradingResult[];
  analysis_summary: string;
  next_action: string;
  next_topic?: string;
  next_teaching_materials?: string;
  next_assessment_questions?: Question[];
}

// API functions
export const learningApi = {
  startSession: async (data: StartSessionRequest): Promise<StartSessionResponse> => {
    const response = await api.post<StartSessionResponse>('/learning/start', data);
    return response.data;
  },
  
  submitAnswers: async (data: SubmitAnswersRequest): Promise<SubmitAnswersResponse> => {
    const response = await api.post<SubmitAnswersResponse>('/learning/submit_answers', data);
    return response.data;
  }
};

export const progressApi = {
  getMastery: async (userId: string) => {
    const response = await api.get(`/progress/mastery/${userId}`);
    return response.data;
  },
  
  getRetentionWarnings: async (userId: string) => {
    const response = await api.get(`/progress/retention/${userId}`);
    return response.data;
  }
};
