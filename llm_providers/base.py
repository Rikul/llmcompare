"""
LLM Provider base class
"""
from typing import Dict, Any

class LLMProvider:
    """Base class for LLM providers"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def call_api(self, model_id: str, prompt: str, endpoint: str, system_prompt: str = None) -> Dict[str, Any]:
        raise NotImplementedError
