from typing import List
from pydantic import BaseModel

from app.agents.base import BaseAgent

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
        subject_name: str, 
        subject_description: str, 
        user_goals: str, 
        current_level: str
    ) -> PlannerOutput:
        
        user_prompt = f"""
        Please generate a curriculum for:
        Subject: {subject_name}
        Description: {subject_description}
        User Goals: {user_goals}
        User's Current Level: {current_level}
        """
        
        return await self.generate_structured(
            task_type="curriculum",
            user_prompt=user_prompt,
            response_model=PlannerOutput,
            temperature=0.7 # A bit of creativity for curriculum planning
        )

planner_agent = PlannerAgent()
