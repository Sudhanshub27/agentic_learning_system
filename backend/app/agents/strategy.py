from typing import List
from pydantic import BaseModel

from app.agents.base import BaseAgent

class StrategyConfig(BaseModel):
    focus_areas: List[str]
    difficulty_adjustment: str

class StrategyOutput(BaseModel):
    action: str  # advance, reteach, review_prerequisite
    reasoning: str
    strategy_config: StrategyConfig

class StrategyAgent(BaseAgent):
    """
    Decides the next transition in the state machine (advance, reteach, review).
    """
    def __init__(self):
        super().__init__(role_name="Strategy", prompt_filename="strategy.md")
        
    async def determine_next_step(
        self, 
        topic_name: str, 
        analysis_summary: str, 
        new_mastery_score: float, 
        detected_weaknesses: List[dict],
        attempts: int
    ) -> StrategyOutput:
        
        weaknesses_str = str(detected_weaknesses) if detected_weaknesses else "None"
        
        user_prompt = f"""
        Topic: {topic_name}
        New Mastery Score: {new_mastery_score:.2f}
        Attempts on this topic: {attempts}
        
        Analysis Summary: {analysis_summary}
        Detected Weaknesses: {weaknesses_str}
        """
        
        return await self.generate_structured(
            task_type="curriculum", 
            user_prompt=user_prompt,
            response_model=StrategyOutput,
            temperature=0.2 
        )

strategy_agent = StrategyAgent()
