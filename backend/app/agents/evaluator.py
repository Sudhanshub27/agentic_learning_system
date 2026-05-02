from typing import List, Optional
from pydantic import BaseModel

from app.agents.base import BaseAgent

# --- Schemas ---

class QuestionSchema(BaseModel):
    question_id: str
    question_type: str  # mcq, short_answer, coding
    question_text: str
    options: Optional[List[str]] = None
    expected_answer: str
    rubric: str

class EvaluatorGenerateOutput(BaseModel):
    questions: List[QuestionSchema]

class EvaluatorGradeOutput(BaseModel):
    is_correct: bool
    score: float
    feedback: str


class EvaluatorAgent(BaseAgent):
    """
    Generates questions and grades user answers.
    Uses two different prompts depending on the task.
    """
    def __init__(self):
        # We use a dummy filename here, we override it in the methods
        super().__init__(role_name="Evaluator", prompt_filename="evaluator_generate.md")
        self.generate_prompt = self._load_prompt("evaluator_generate.md")
        self.grade_prompt = self._load_prompt("evaluator_grade.md")
        
    async def generate_assessment(
        self, 
        topic_name: str, 
        difficulty_level: int, 
        content_type: str
    ) -> EvaluatorGenerateOutput:
        
        self.prompt_template = self.generate_prompt
        
        user_prompt = f"""
        Generate an assessment for:
        Topic: {topic_name}
        Difficulty: {difficulty_level}/10
        Content Type: {content_type}
        """
        
        return await self.generate_structured(
            task_type="grading", # Fast model is usually fine for generating MCQs
            user_prompt=user_prompt,
            response_model=EvaluatorGenerateOutput,
            temperature=0.4
        )

    async def grade_answer(
        self, 
        question: QuestionSchema, 
        user_answer: str
    ) -> EvaluatorGradeOutput:
        
        self.prompt_template = self.grade_prompt
        
        user_prompt = f"""
        Question: {question.question_text}
        Question Type: {question.question_type}
        Expected Answer: {question.expected_answer}
        Rubric: {question.rubric}
        
        User's Answer: {user_answer}
        """
        
        return await self.generate_structured(
            task_type="grading", # Groq is perfect here (ultra-fast)
            user_prompt=user_prompt,
            response_model=EvaluatorGradeOutput,
            temperature=0.1 # We want deterministic grading
        )

evaluator_agent = EvaluatorAgent()
