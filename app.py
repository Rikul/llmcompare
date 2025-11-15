from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import Dict, List, Any
import logging
from llm_service import LLMService
from config import AVAILABLE_MODELS

# Load environment variables
load_dotenv()

# Configure logging
#logging.basicConfig(level=logging.INFO)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Logs to file
        logging.StreamHandler()  # Also logs to console
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize the service
llm_service = LLMService()


@app.route('/')
def index():
    """Render the main page"""
    # Check if any API keys are configured
    api_keys_status = {
        'OpenAI': bool(os.getenv('OPENAI_API_KEY')),
        'Anthropic': bool(os.getenv('ANTHROPIC_API_KEY')),
        'Google': bool(os.getenv('GEMINI_API_KEY')),
        'xAI': bool(os.getenv('XAI_API_KEY'))
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
        os.getenv('GEMINI_API_KEY'),
        os.getenv('XAI_API_KEY')
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
        'Google': bool(os.getenv('GEMINI_API_KEY')),
        'xAI': bool(os.getenv('XAI_API_KEY'))
    }
    
    print("\nAPI Key Status:")
    for provider, has_key in api_keys_status.items():
        status = "✓ Configured" if has_key else "✗ Not configured"
        print(f"  {provider}: {status}")
    
    if not any(api_keys_status.values()):
        print("\n⚠️  No API keys configured. create a .env file with your API keys.")
        exit(1)

    print("\nStarting Flask server...")
    print("Access the app at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
