"""
LLM Provider classes for various AI model APIs

This module contains the base LLMProvider class and implementations
for OpenAI, Anthropic, Google Gemini, and xAI APIs.
"""

import requests
import os
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class LLMProvider:
    """Base class for LLM providers"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def call_api(self, model_id: str, prompt: str, endpoint: str, system_prompt: str = None) -> Dict[str, Any]:
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """OpenAI API implementation"""

    def call_api(self, model_id: str, prompt: str, endpoint: str, system_prompt: str = None) -> Dict[str, Any]:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        # Support both the legacy chat.completions endpoint and the new
        # responses endpoint which is required for the latest OpenAI models
        if endpoint.rstrip('/').endswith('responses'):
            input_messages = []
            if system_prompt:
                input_messages.append({
                    'role': 'system',
                    'content': [{'type': 'text', 'text': system_prompt}]
                })
            input_messages.append({
                'role': 'user',
                'content': [{'type': 'text', 'text': prompt}]
            })

            data = {
                'model': model_id,
                'input': input_messages,
                'temperature': 0.7,
                'max_output_tokens': 1000
            }
        else:
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

        if endpoint.rstrip('/').endswith('responses'):
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

        return {
            'content': response_data['choices'][0]['message']['content'],
            'usage': response_data.get('usage', {})
        }


class AnthropicProvider(LLMProvider):
    """Anthropic API implementation"""

    def call_api(self, model_id: str, prompt: str, endpoint: str, system_prompt: str = None) -> Dict[str, Any]:
        headers = {
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json'
        }
        data = {
            'model': model_id,
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'text',
                            'text': prompt
                        }
                    ]
                }
            ],
            'max_tokens': 1000
        }

        if system_prompt:
            data['system'] = system_prompt

        response = requests.post(endpoint, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        response_data = response.json()
        return {
            'content': response_data['content'][0]['text'],
            'usage': response_data.get('usage', {})
        }


class GoogleProvider(LLMProvider):
    """Google Gemini API implementation"""

    def call_api(self, model_id: str, prompt: str, endpoint: str, system_prompt: str = None) -> Dict[str, Any]:
        headers = {
            'Content-Type': 'application/json'
        }

        # Google Gemini handles system prompt differently
        # We prepend it to the user prompt if provided
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        data = {
            'contents': [{
                'role': 'user',
                'parts': [{'text': full_prompt}]
            }],
            'generationConfig': {
                'temperature': 0.7,
                'maxOutputTokens': 1000
            }
        }

        url = f"{endpoint}?key={self.api_key}"
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        response_data = response.json()
        return {
            'content': response_data['candidates'][0]['content']['parts'][0]['text'],
            'usage': {}  # Google doesn't return usage in the same format
        }


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


class LLMService:
    """Service class to handle LLM API calls"""

    def __init__(self):
        self.providers = {
            'OpenAI': OpenAIProvider,
            'Anthropic': AnthropicProvider,
            'Google': GoogleProvider,
            'xAI': xAIProvider
        }

    def get_provider(self, provider_name: str, api_key: str) -> LLMProvider:
        """Get the appropriate provider instance"""
        provider_class = self.providers.get(provider_name)
        if not provider_class:
            raise ValueError(f"Unknown provider: {provider_name}")
        return provider_class(api_key)

    def call_model(self, model_id: str, prompt: str, model_info: Dict[str, Any], system_prompt: str = None) -> Dict[str, Any]:
        """Call a specific model with error handling"""
        api_key = os.getenv(model_info['api_key_env'])

        if not api_key:
            return {
                'model_name': model_info['name'],
                'provider': model_info['provider'],
                'response': f"API key not set. Please set {model_info['api_key_env']} in your .env file.",
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error_type': 'missing_api_key'
            }

        try:
            provider = self.get_provider(model_info['provider'], api_key)
            result = provider.call_api(model_id, prompt, model_info['endpoint'], system_prompt)

            return {
                'model_name': model_info['name'],
                'provider': model_info['provider'],
                'response': result['content'],
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'usage': result.get('usage', {})
            }

        except requests.exceptions.HTTPError as e:
            error_msg = f"API Error: {e.response.status_code} - {e.response.text[:200]}"
            logger.error(f"HTTP Error for {model_id}: {error_msg}")
            return self._error_response(model_info, error_msg, 'api_error')

        except requests.exceptions.Timeout:
            error_msg = "Request timed out. Please try again."
            logger.error(f"Timeout for {model_id}")
            return self._error_response(model_info, error_msg, 'timeout')

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"Error for {model_id}: {error_msg}")
            return self._error_response(model_info, error_msg, 'unknown_error')

    def _error_response(self, model_info: Dict[str, Any], error_msg: str, error_type: str) -> Dict[str, Any]:
        """Create a standardized error response"""
        return {
            'model_name': model_info['name'],
            'provider': model_info['provider'],
            'response': error_msg,
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error_type': error_type
        }
