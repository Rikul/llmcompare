from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import Dict, List, Any
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Model configurations
AVAILABLE_MODELS = {
    'gpt-3.5-turbo': {
        'name': 'GPT-3.5 Turbo',
        'endpoint': 'https://api.openai.com/v1/chat/completions',
        'api_key_env': 'OPENAI_API_KEY',
        'provider': 'OpenAI'
    },
    'gpt-4': {
        'name': 'GPT-4',
        'endpoint': 'https://api.openai.com/v1/chat/completions',
        'api_key_env': 'OPENAI_API_KEY',
        'provider': 'OpenAI'
    },
    'claude-3-opus': {
        'name': 'Claude 3 Opus',
        'endpoint': 'https://api.anthropic.com/v1/messages',
        'api_key_env': 'ANTHROPIC_API_KEY',
        'provider': 'Anthropic'
    },
    'claude-3-sonnet': {
        'name': 'Claude 3 Sonnet',
        'endpoint': 'https://api.anthropic.com/v1/messages',
        'api_key_env': 'ANTHROPIC_API_KEY',
        'provider': 'Anthropic'
    },
    'gemini-pro': {
        'name': 'Gemini Pro',
        'endpoint': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
        'api_key_env': 'GOOGLE_API_KEY',
        'provider': 'Google'
    }
}


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
            'messages': [{'role': 'user', 'content': prompt}],
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
            'contents': [{'parts': [{'text': full_prompt}]}],
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


class LLMService:
    """Service class to handle LLM API calls"""
    
    def __init__(self):
        self.providers = {
            'OpenAI': OpenAIProvider,
            'Anthropic': AnthropicProvider,
            'Google': GoogleProvider
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


# Initialize the service
llm_service = LLMService()


@app.route('/')
def index():
    """Render the main page"""
    # Check if any API keys are configured
    api_keys_status = {
        'OpenAI': bool(os.getenv('OPENAI_API_KEY')),
        'Anthropic': bool(os.getenv('ANTHROPIC_API_KEY')),
        'Google': bool(os.getenv('GOOGLE_API_KEY'))
    }

    if not any(api_keys_status.values()):
        # No API keys configured, show error template
        return render_template('no_api_keys.html', api_keys_status=api_keys_status)

    return render_template('index.html', models=AVAILABLE_MODELS, api_keys_status=api_keys_status)


@app.route('/results')
def results():
    """Render the results page"""
    return render_template('results.html')


@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available models"""
    return jsonify(AVAILABLE_MODELS)


@app.route('/api/compare', methods=['POST'])
def compare_models():
    """Compare responses from multiple models"""
    data = request.json
    system_prompt = data.get('system_prompt', '').strip()
    prompt = data.get('prompt', '').strip()
    selected_models = data.get('models', [])

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    if not selected_models:
        return jsonify({'error': 'At least one model must be selected'}), 400

    # Check if any API keys are configured
    api_keys_configured = any([
        os.getenv('OPENAI_API_KEY'),
        os.getenv('ANTHROPIC_API_KEY'),
        os.getenv('GOOGLE_API_KEY')
    ])

    if not api_keys_configured:
        return jsonify({'error': 'No API keys configured. Please add API keys to use this service.'}), 503

    responses = {}

    for model_id in selected_models:
        if model_id not in AVAILABLE_MODELS:
            continue

        model_info = AVAILABLE_MODELS[model_id]

        # Real API call with system prompt
        responses[model_id] = llm_service.call_model(model_id, prompt, model_info, system_prompt if system_prompt else None)

    return jsonify(responses)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_available': len(AVAILABLE_MODELS)
    })


if __name__ == '__main__':
    # Check for API keys and provide helpful message
    print("\n" + "="*60)
    print("LLM Model Comparison Tool")
    print("="*60)
    
    api_keys_status = {
        'OpenAI': bool(os.getenv('OPENAI_API_KEY')),
        'Anthropic': bool(os.getenv('ANTHROPIC_API_KEY')),
        'Google': bool(os.getenv('GOOGLE_API_KEY'))
    }
    
    print("\nAPI Key Status:")
    for provider, has_key in api_keys_status.items():
        status = "✓ Configured" if has_key else "✗ Not configured"
        print(f"  {provider}: {status}")
    
    if not any(api_keys_status.values()):
        print("\n⚠️  No API keys configured. The app will run in mock mode.")
        print("   To use real APIs, create a .env file with your API keys.")
    
    print("\nStarting Flask server...")
    print("Access the app at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
