from app.agents.base import BaseAgent

class MemoryAgent(BaseAgent):
    """
    Summarizes session data for long-term memory retrieval (ChromaDB).
    This doesn't use a structured JSON output, it returns a dense markdown summary.
    """
    def __init__(self):
        # We don't have a specific file for memory yet, so we just pass a string inline
        # or load a simple prompt. We'll bypass the file loader for this simple one.
        super().__init__(role_name="Memory", prompt_filename="memory.md")
        self.prompt_template = """
        You are the Memory Agent. 
        Your task is to summarize a learning session so that it can be stored in a Vector Database (ChromaDB) for long-term retrieval.
        Extract the key concepts learned, specific struggles the user faced, and major breakthroughs.
        Keep it dense and factual.
        """
        
    async def summarize_session(
        self, 
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
        
        return await self.generate_text(
            task_type="curriculum", 
            user_prompt=user_prompt,
            temperature=0.3 
        )

memory_agent = MemoryAgent()
