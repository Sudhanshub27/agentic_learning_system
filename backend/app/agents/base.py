import os
import json
import logging
from typing import Type, TypeVar, Any, Dict

from pydantic import BaseModel

from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

class BaseAgent:
    """
    Base class for all AI agents in the Agentic Learning System.
    Handles prompt loading, system/user message construction,
    LLM invocation via the multi-provider LLMService, and Pydantic parsing.
    """
    
    def __init__(self, role_name: str, prompt_filename: str):
        self.role_name = role_name
        self.prompt_template = self._load_prompt(prompt_filename)
        
    def _load_prompt(self, filename: str) -> str:
        """Loads a markdown prompt template from the prompts directory."""
        prompt_path = os.path.join(
            os.path.dirname(__file__), "..", "prompts", filename
        )
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"Prompt file {filename} not found at {prompt_path}")
            return "You are an AI assistant."
            
    async def generate_structured(
        self, 
        task_type: str, 
        user_prompt: str, 
        response_model: Type[T],
        temperature: float = 0.7
    ) -> T:
        """
        Calls the LLM service and strictly parses the output into a Pydantic model.
        """
        logger.info(f"[{self.role_name}] Generating structured response for: {task_type}")
        
        response_text = await llm_service.generate(
            task_type=task_type,
            system_prompt=self.prompt_template,
            prompt=user_prompt,
            temperature=temperature,
            json_mode=True
        )
        
        return self._parse_json(response_text, response_model)

    async def generate_text(
        self, 
        task_type: str, 
        user_prompt: str, 
        temperature: float = 0.7
    ) -> str:
        """
        Calls the LLM service and returns plain markdown/text.
        """
        logger.info(f"[{self.role_name}] Generating text response for: {task_type}")
        return await llm_service.generate(
            task_type=task_type,
            system_prompt=self.prompt_template,
            prompt=user_prompt,
            temperature=temperature
        )
        
    def _parse_json(self, response_text: str, model: Type[T]) -> T:
        """
        Extracts JSON from markdown code blocks or general text and parses it into a Pydantic model.
        """
        cleaned_text = response_text.strip()
        
        # 1. Try to find the JSON block if it's embedded in text
        start_idx = -1
        end_idx = -1
        
        # Look for the start of an object or array
        for i, char in enumerate(cleaned_text):
            if char in ['{', '[']:
                start_idx = i
                break
        
        # Look for the end of an object or array
        for i, char in enumerate(reversed(cleaned_text)):
            if char in ['}', ']']:
                end_idx = len(cleaned_text) - i
                break
                
        if start_idx != -1 and end_idx != -1:
            json_candidate = cleaned_text[start_idx:end_idx]
        else:
            json_candidate = cleaned_text

        try:
            data = json.loads(json_candidate)
            return model(**data)
        except json.JSONDecodeError as e:
            logger.error(f"[{self.role_name}] Failed to parse JSON: {e}\nCandidate: {json_candidate}\nRaw: {response_text}")
            raise ValueError("Agent failed to output valid JSON.") from e
        except Exception as e:
            logger.error(f"[{self.role_name}] Failed to validate against Pydantic schema: {e}\nCandidate: {json_candidate}\nRaw: {response_text}")
            raise ValueError("Agent output did not match expected schema.") from e
