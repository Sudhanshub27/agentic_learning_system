from typing import List
from pydantic import BaseModel

from app.agents.base import BaseAgent
from app.services.memory_service import memory_service
from app.services.ml_service import ml_service

class TopicSchema(BaseModel):
    name: str
    description: str
    difficulty_level: int
    order_index: int
    prerequisites: List[str]
    content_type: str
    learning_objectives: List[str]
    estimated_minutes: int

class PlannerOutput(BaseModel):
    topics: List[TopicSchema]

class PlannerAgent(BaseAgent):
    """
    Generates structured learning curriculums for any subject domain.
    """
    def __init__(self):
        super().__init__(role_name="Planner", prompt_filename="planner.md")
        
    async def generate_curriculum(
        self, 
        user_id: str,
        subject_name: str, 
        subject_description: str, 
        user_goals: str, 
        current_level: str
    ) -> PlannerOutput:
        
        # 1. Retrieve historical context for this user and subject (Phase 5)
        historical_context = await memory_service.recall_history(
            user_id=user_id,
            query=f"Curriculum and progression for {subject_name}",
            n_results=2
        )
        
        # 2. Check for spaced repetition (Phase 6)
        # In a real system, we would fetch the user's past topics from the DB here
        # and calculate `days_since_last_review`. We simulate this for the prompt logic.
        topics_needing_review = []
        # Simulate predicting a topic that needs review
        # retention_prob = ml_service.predict_retention(mastery=0.8, attempts=2, days=14, difficulty=7)
        # if ml_service.needs_review(retention_prob):
        #     topics_needing_review.append("Previously Learned Topic Example")
        review_str = ", ".join(topics_needing_review) if topics_needing_review else "None right now."
        
        user_prompt = f"""
        Please generate a curriculum for:
        Subject: {subject_name}
        Description: {subject_description}
        User Goals: {user_goals}
        User's Current Level: {current_level}
        
        Historical Context (Past Sessions):
        {historical_context}
        
        Spaced Repetition Flag:
        The ML model predicts the user is forgetting these topics: {review_str}
        If there are topics listed above, you MUST include a brief Refresher topic at the very beginning of the curriculum.
        
        Use the historical context to avoid repeating topics the user has already mastered, 
        unless they need a brief refresher.
        """
        
        return await self.generate_structured(
            task_type="curriculum",
            user_prompt=user_prompt,
            response_model=PlannerOutput,
            temperature=0.7 # A bit of creativity for curriculum planning
        )

planner_agent = PlannerAgent()
