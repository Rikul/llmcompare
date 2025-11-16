"""
Google Gemini API Provider implementation
"""

from typing import Dict, Any
import google.generativeai as genai

from .base import LLMProvider


class GoogleProvider(LLMProvider):
    """Google Gemini API implementation"""

    def __init__(self, api_key: str, available_models: Dict[str, Any] = None):
        super().__init__(api_key, available_models)

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
        """Get available Google models from API, with config as fallback"""
        # Try API call first if we have a real API key
        if self.api_key != "dummy_key":
            try:
                genai.configure(api_key=self.api_key)
                models = genai.list_models()
                
                # Filter for models that support generateContent
                return {
                    model.name.replace('models/', ''): {
                        "name": model.display_name if hasattr(model, 'display_name') else model.name.replace('models/', ''),
                        "provider": "Google",
                        "endpoint": f"https://generativelanguage.googleapis.com/v1beta/{model.name}:generateContent",
                        "api_key_env": "GEMINI_API_KEY"
                    }
                    for model in models
                    if 'generateContent' in getattr(model, 'supported_generation_methods', [])
                }
            except Exception as e:
                # Handle API errors gracefully - fall through to config fallback
                print(f"Error fetching Google models from API: {e}")
        
        # Fallback to config models if available
        if self.available_models:
            google_models = {
                model_id: model_info
                for model_id, model_info in self.available_models.items()
                if model_info.get('provider') == 'Google'
            }
            if google_models:
                return google_models
        
        # No models available
        return {}
