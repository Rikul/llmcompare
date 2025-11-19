"""
LLM Service for handling API calls to various providers
"""

import os
import logging
import requests
from datetime import datetime
from typing import Dict, Any

from openai import (
    OpenAIError,
    APIError,
    APIConnectionError,
    RateLimitError,
    APITimeoutError,
)

from .base import LLMProvider
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .google_provider import GoogleProvider
from .xai_provider import xAIProvider

logger = logging.getLogger(__name__)


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

    def get_available_models(self) -> Dict[str, Any]:
        """Get all available models from configured providers"""
        available_models = {}
        for provider_name in self.providers.keys():
            api_key_env = f"{provider_name.upper()}_API_KEY"
            if provider_name == 'Google':
                api_key_env = "GEMINI_API_KEY"
            elif provider_name == 'xAI':
                api_key_env = "XAI_API_KEY"

            api_key = os.getenv(api_key_env)
            if api_key:
                try:
                    provider = self.get_provider(provider_name, api_key)
                    models = provider.get_models()
                    available_models.update(models)
                except Exception as e:
                    logger.error(f"Error fetching models for {provider_name}: {e}")
        return available_models

    def get_available_providers(self) -> Dict[str, Any]:
        """Get all available providers from configured providers"""
        available_providers = []
        for provider_name in self.providers.keys():
            api_key_env = f"{provider_name.upper()}_API_KEY"
            if provider_name == 'Google':
                api_key_env = "GEMINI_API_KEY"
            elif provider_name == 'xAI':
                api_key_env = "XAI_API_KEY"

            api_key = os.getenv(api_key_env)
            if api_key:
                available_providers.append(provider_name)
        return available_providers

    def get_available_models_by_provider(self, provider_name: str) -> Dict[str, Any]:
        """Get all available models from a specific configured provider"""
        available_models = {}
        api_key_env = f"{provider_name.upper()}_API_KEY"
        if provider_name == 'Google':
            api_key_env = "GEMINI_API_KEY"
        elif provider_name == 'xAI':
            api_key_env = "XAI_API_KEY"

        api_key = os.getenv(api_key_env)
        if api_key:
            try:
                provider = self.get_provider(provider_name, api_key)
                models = provider.get_models()
                available_models.update(models)
            except Exception as e:
                logger.error(f"Error fetching models for {provider_name}: {e}")
        return available_models

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

        except (OpenAIError, APIError, APIConnectionError, RateLimitError, APITimeoutError) as e:
            error_msg = f"OpenAI API Error: {str(e)}"
            logger.error(f"OpenAI Error for {model_id}: {error_msg}")
            return self._error_response(model_info, error_msg, 'openai_api_error')

        except Exception as e:
            if 'Google' in model_info['provider']:
                error_msg = f"Google API Error: {str(e)}"
                logger.error(f"Google API Error for {model_id}: {error_msg}")
                return self._error_response(model_info, error_msg, 'google_api_error')

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
