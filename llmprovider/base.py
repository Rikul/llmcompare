"""
Base LLM Provider class
"""

from typing import Dict, Any


class LLMProvider:
    """Base class for LLM providers"""

    def __init__(self, api_key: str, available_models: Dict[str, Any] = None):
        self.api_key = api_key
        self.available_models = available_models or {}

    def call_api(self, model_id: str, prompt: str, endpoint: str, system_prompt: str = None) -> Dict[str, Any]:
        raise NotImplementedError

    def get_models(self) -> Dict[str, Any]:
        """Get available models from the provider"""
        raise NotImplementedError
