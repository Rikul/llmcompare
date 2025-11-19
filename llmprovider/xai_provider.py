

from typing import Dict, Any
from xai_sdk import Client
from xai_sdk.chat import system, user

from .base import LLMProvider


class xAIProvider(LLMProvider):
    """xAI (Grok) API implementation"""

    def __init__(self, api_key: str):
        super().__init__(api_key)

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
        # Define xAI (Grok) models directly
        xai_models = {
            'grok-4': {
                'name': 'Grok 4',
                'endpoint': 'https://api.x.ai/v1/chat/completions',
                'api_key_env': 'XAI_API_KEY',
                'provider': 'xAI'
            },
            'grok-3': {
                'name': 'Grok 3',
                'endpoint': 'https://api.x.ai/v1/chat/completions',
                'api_key_env': 'XAI_API_KEY',
                'provider': 'xAI'
            },
            'grok-3-mini': {
                'name': 'Grok 3 Mini',
                'endpoint': 'https://api.x.ai/v1/chat/completions',
                'api_key_env': 'XAI_API_KEY',
                'provider': 'xAI'
            }
        }
        return xai_models
