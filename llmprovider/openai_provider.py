"""
OpenAI API Provider implementation
"""

from typing import Dict, Any
from openai import (
    OpenAI,
    OpenAIError,
    APIError,
    APIConnectionError,
    RateLimitError,
    APITimeoutError,
)

from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI API implementation"""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = OpenAI(api_key=api_key)

    def call_api(self, model_id: str, prompt: str, endpoint: str, system_prompt: str = None) -> Dict[str, Any]:
        # Support both the legacy chat.completions endpoint and the new
        # responses endpoint which is required for the latest OpenAI models
        if endpoint.rstrip('/').endswith('responses'):
            input_messages = []
            if system_prompt:
                input_messages.append({
                    'role': 'system',
                    'content': [{'type': 'input_text', 'text': system_prompt}]
                })
            input_messages.append({
                'role': 'user',
                'content': [{'type': 'input_text', 'text': prompt}]
            })

            response = self.client.responses.create(
                model=model_id,
                input=input_messages,
                temperature=0.7,
                max_output_tokens=1000,
            )

            response_data = response.model_dump()

            # Responses endpoint returns data under the `output` key
            output = response_data.get('output', [])
            if not output:
                raise ValueError('No output returned from OpenAI responses API')
            content_parts = output[0].get('content', [])
            if not content_parts:
                raise ValueError('OpenAI responses output missing content')
            text = ''.join(
                part.get('text', '')
                for part in content_parts
                if part.get('type') in {'output_text', 'text'}
            )
            if not text:
                text = content_parts[0].get('text', '')
            return {
                'content': text,
                'usage': response_data.get('usage', {})
            }

        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})

        response = self.client.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )

        response_data = response.model_dump()

        return {
            'content': response_data['choices'][0]['message']['content'],
            'usage': response_data.get('usage', {})
        }

    def get_models(self) -> Dict[str, Any]:
        """Get available models from OpenAI"""
        # Define OpenAI models directly
        openai_models = {
            'gpt-4o': {
                'name': 'GPT-4o',
                'endpoint': 'https://api.openai.com/v1/chat/completions',
                'api_key_env': 'OPENAI_API_KEY',
                'provider': 'OpenAI'
            },
            'gpt-4o-mini': {
                'name': 'GPT-4o Mini',
                'endpoint': 'https://api.openai.com/v1/chat/completions',
                'api_key_env': 'OPENAI_API_KEY',
                'provider': 'OpenAI'
            },
            'gpt-4-turbo': {
                'name': 'GPT-4 Turbo',
                'endpoint': 'https://api.openai.com/v1/chat/completions',
                'api_key_env': 'OPENAI_API_KEY',
                'provider': 'OpenAI'
            },
            'gpt-3.5-turbo': {
                'name': 'GPT-3.5 Turbo',
                'endpoint': 'https://api.openai.com/v1/chat/completions',
                'api_key_env': 'OPENAI_API_KEY',
                'provider': 'OpenAI'
            },
            'o1': {
                'name': 'o1',
                'endpoint': 'https://api.openai.com/v1/chat/completions',
                'api_key_env': 'OPENAI_API_KEY',
                'provider': 'OpenAI'
            },
            'o1-mini': {
                'name': 'o1 Mini',
                'endpoint': 'https://api.openai.com/v1/chat/completions',
                'api_key_env': 'OPENAI_API_KEY',
                'provider': 'OpenAI'
            }
        }
        return openai_models