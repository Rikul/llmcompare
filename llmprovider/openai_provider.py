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

    def __init__(self, api_key: str, available_models: Dict[str, Any] = None):
        super().__init__(api_key, available_models)
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
        """Get available models from OpenAI API, with config as fallback"""
        # Try API call first if we have a real API key
        if self.api_key != "dummy_key":
            try:
                response = self.client.models.list()
                models = response.data
                # Filter for GPT models and format the output
                # Map models that require the 'responses' endpoint
                responses_models = {"gpt-4o", "o3-mini"}
                return {
                    model.id: {
                        "name": model.id,
                        "provider": "OpenAI",
                        "endpoint": "responses" if model.id in responses_models else "chat/completions",
                        "api_key_env": "OPENAI_API_KEY"
                    }
                    for model in models
                    if model.id.startswith("gpt") or model.id.startswith("o3-")
                }
            except (OpenAIError, APIError, APIConnectionError, RateLimitError, APITimeoutError) as e:
                # Handle API errors gracefully - fall through to config fallback
                print(f"Error fetching OpenAI models from API: {e}")
        
        # Fallback to config models if available
        if self.available_models:
            openai_models = {
                model_id: model_info
                for model_id, model_info in self.available_models.items()
                if model_info.get('provider') == 'OpenAI'
            }
            if openai_models:
                return openai_models
        
        # Last resort: return minimal hardcoded models
        return {
            "gpt-3.5-turbo": {
                "name": "gpt-3.5-turbo",
                "provider": "OpenAI",
                "endpoint": "chat/completions",
                "api_key_env": "OPENAI_API_KEY"
            },
            "gpt-4": {
                "name": "gpt-4",
                "provider": "OpenAI",
                "endpoint": "chat/completions",
                "api_key_env": "OPENAI_API_KEY"
            },
        }
