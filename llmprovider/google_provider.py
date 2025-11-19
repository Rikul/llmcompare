
from typing import Dict, Any
import google.generativeai as genai

from .base import LLMProvider


class GoogleProvider(LLMProvider):
    """Google Gemini API implementation"""

    def __init__(self, api_key: str):
        super().__init__(api_key)

    def call_api(self, model_id: str, prompt: str, endpoint: str, system_prompt: str = None) -> Dict[str, Any]:
        genai.configure(api_key=self.api_key)

        # Google Gemini handles system prompt differently
        # We prepend it to the user prompt if provided
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        model = genai.GenerativeModel(model_id)
        response = model.generate_content(full_prompt)

        return {
            'content': response.text,
            'usage': {}  # Google doesn't return usage in the same format
        }

    def get_models(self) -> Dict[str, Any]:
        """Get available Google models"""
        # Define Google Gemini models directly
        google_models = {
            'gemini-2.5-pro': {
                'name': 'Gemini 2.5 Pro',
                'endpoint': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent',
                'api_key_env': 'GEMINI_API_KEY',
                'provider': 'Google'
            },
            'gemini-2.5-flash': {
                'name': 'Gemini 2.5 Flash',
                'endpoint': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent',
                'api_key_env': 'GEMINI_API_KEY',
                'provider': 'Google'
            },
            'gemini-3-pro-preview': {
                'name': 'Gemini 3 Pro (Preview)',
                'endpoint': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent',
                'api_key_env': 'GEMINI_API_KEY',
                'provider': 'Google'
            }
        }
        return google_models
