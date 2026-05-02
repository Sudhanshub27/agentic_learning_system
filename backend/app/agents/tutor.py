from typing import List

from app.agents.base import BaseAgent
from app.services.memory_service import memory_service

class TutorAgent(BaseAgent):
    """
    Generates teaching materials adapted to the user's current knowledge state.
    """
    def __init__(self):
        super().__init__(role_name="Tutor", prompt_filename="tutor.md")
        
    async def teach_topic(
        self, 
        user_id: str,
        topic_name: str, 
        subject_domain: str, 
        user_level: str, 
        mastery_score: float,
        known_weaknesses: List[str],
        content_type: str
    ) -> str:
        
        weaknesses_str = ", ".join(known_weaknesses) if known_weaknesses else "None"
        
        # Retrieve historical context for this user and topic
        historical_context = await memory_service.recall_history(
            user_id=user_id,
            query=f"Struggles and breakthroughs when learning {topic_name} in {subject_domain}",
            n_results=1
        )
        
        user_prompt = f"""
        Please teach the following topic:
        Topic: {topic_name}
        Domain: {subject_domain}
        Content Type: {content_type}
        
        User Profile:
        Level: {user_level}
        Current Mastery Score: {mastery_score:.2f}/1.0
        Known Weaknesses to Address: {weaknesses_str}
        
        Historical Context (Past Sessions):
        {historical_context}
        
        Use the historical context to tailor your explanation. If they struggled with a specific concept before, 
        try a new analogy or approach.
        """
        
        # We don't need structured JSON for the tutor, just rich markdown text
        return await self.generate_text(
            task_type="curriculum", # Gemini is best for teaching
            user_prompt=user_prompt,
            temperature=0.6 
        )

tutor_agent = TutorAgent()
