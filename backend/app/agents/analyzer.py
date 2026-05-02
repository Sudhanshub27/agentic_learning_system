from typing import List, Dict, Any
from pydantic import BaseModel

from app.agents.base import BaseAgent

class WeaknessSchema(BaseModel):
    weakness_type: str
    description: str

class AnalyzerOutput(BaseModel):
    new_mastery_score: float
    detected_weaknesses: List[WeaknessSchema]
    analysis_summary: str

class AnalyzerAgent(BaseAgent):
    """
    Analyzes test results to detect weaknesses and update mastery scores.
    """
    def __init__(self):
        super().__init__(role_name="Analyzer", prompt_filename="analyzer.md")
        
    async def analyze_results(
        self, 
        topic_name: str, 
        current_mastery_score: float, 
        test_results: List[Dict[str, Any]]
    ) -> AnalyzerOutput:
        
        # Format the test results into a readable string for the prompt
        results_str = ""
        for i, res in enumerate(test_results):
            results_str += f"Q{i+1}: Score: {res.get('score', 0.0)}\n"
            results_str += f"Feedback: {res.get('feedback', '')}\n\n"
            
        user_prompt = f"""
        Topic: {topic_name}
        Current Mastery Score: {current_mastery_score:.2f}
        
        Test Results:
        {results_str}
        """
        
        return await self.generate_structured(
            task_type="curriculum", # Gemini is good at analysis/reasoning
            user_prompt=user_prompt,
            response_model=AnalyzerOutput,
            temperature=0.3 # Low temperature for consistent analysis
        )

analyzer_agent = AnalyzerAgent()
