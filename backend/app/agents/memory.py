from app.agents.base import BaseAgent
from app.services.memory_service import memory_service

class MemoryAgent(BaseAgent):
    """
    Summarizes session data for long-term memory retrieval (ChromaDB).
    This doesn't use a structured JSON output, it returns a dense markdown summary.
    """
    def __init__(self):
        super().__init__(role_name="Memory", prompt_filename="memory.md")
        self.prompt_template = """
        You are the Memory Agent. 
        Your task is to summarize a learning session so that it can be stored in a Vector Database (ChromaDB) for long-term retrieval.
        Extract the key concepts learned, specific struggles the user faced, and major breakthroughs.
        Keep it dense and factual.
        """
        
    async def summarize_session(
        self, 
        user_id: str,
        subject: str,
        topics_covered: list[str],
        overall_performance: str,
        key_weaknesses: list[str]
    ) -> str:
        
        user_prompt = f"""
        Subject: {subject}
        Topics Covered: {', '.join(topics_covered)}
        Performance Summary: {overall_performance}
        Key Weaknesses: {', '.join(key_weaknesses)}
        
        Please provide a dense summary of this session for vector storage.
        """
        
        summary = await self.generate_text(
            task_type="curriculum", 
            user_prompt=user_prompt,
            temperature=0.3 
        )
        
        # Store in ChromaDB
        await memory_service.store_session(
            user_id=user_id,
            subject=subject,
            summary=summary
        )
        
        return summary

memory_agent = MemoryAgent()
