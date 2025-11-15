"""
xAI (Grok) API implementation - OpenAI-compatible API
"""
from typing import Dict, Any
import requests

from .base import LLMProvider


class xAIProvider(LLMProvider):
    """xAI (Grok) API implementation - OpenAI-compatible API"""

    def call_api(self, model_id: str, prompt: str, endpoint: str, system_prompt: str = None) -> Dict[str, Any]:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})

        data = {
            'model': model_id,
            'messages': messages,
            'temperature': 0.7,
            'max_tokens': 1000
        }

        response = requests.post(endpoint, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        response_data = response.json()
        return {
            'content': response_data['choices'][0]['message']['content'],
            'usage': response_data.get('usage', {})
        }
