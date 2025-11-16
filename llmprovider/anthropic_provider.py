"""
Anthropic API Provider implementation
"""

from typing import Dict, Any
from anthropic import Anthropic

from .base import LLMProvider


class AnthropicProvider(LLMProvider):
    """Anthropic API implementation"""
    
    def call_api(self, model_id: str, prompt: str, endpoint: str, system_prompt: str = None) -> Dict[str, Any]:
     
        client = Anthropic(
            api_key = self.api_key,  # This is the default and can be omitted
        )

        message = client.messages.create(
            max_tokens=1024,
            system=system_prompt if system_prompt else "",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model_id,
        )

         # Extract text content from the response
        content_text = ""
        if message.content:
            for block in message.content:
                if hasattr(block, 'text'):
                    content_text += block.text
        
        return {
            'content': content_text,
            'usage': {
                'prompt_tokens': message.usage.input_tokens if hasattr(message, 'usage') else 0,
                'completion_tokens': message.usage.output_tokens if hasattr(message, 'usage') else 0,
                'total_tokens': (message.usage.input_tokens + message.usage.output_tokens) if hasattr(message, 'usage') else 0
            }
        }

    def get_models(self) -> Dict[str, Any]:
        """Anthropic API does not support fetching models"""
        return {}
