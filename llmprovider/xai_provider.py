"""
xAI (Grok) API Provider implementation
"""

from typing import Dict, Any
from xai_sdk import Client
from xai_sdk.chat import system, user

from .base import LLMProvider


class xAIProvider(LLMProvider):
    """xAI (Grok) API implementation"""

    def __init__(self, api_key: str, available_models: Dict[str, Any] = None):
        super().__init__(api_key, available_models)

    def call_api(self, model_id: str, prompt: str, endpoint: str, system_prompt: str = None) -> Dict[str, Any]:
        client = Client(api_key=self.api_key)

        messages = []
        if system_prompt:
            messages.append(system(system_prompt))

        chat = client.chat.create(
            model=model_id,
            messages=messages
        )
        chat.append(user(prompt))
        response = chat.sample()

        return {
            'content': response.content,
            'usage': {}
        }

    def get_models(self) -> Dict[str, Any]:
        """Get available xAI models"""

        if self.available_models:
            xai_models = {
                model_id: model_info
                for model_id, model_info in self.available_models.items()
                if model_info.get('provider') == 'xAI'
            }
            if xai_models:
                return xai_models
        
        # No models available
        return {}
