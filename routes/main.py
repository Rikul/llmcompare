from flask import Blueprint, render_template
import os
from llmprovider import LLMService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
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

    # Get all available models from the service
    llm_service = LLMService()
    models = llm_service.get_available_models()
    
    return render_template('index.html', models=models, api_keys_status=api_keys_status)


@main_bp.route('/results')
def results():
    """Render the results page"""
    return render_template('results.html')
