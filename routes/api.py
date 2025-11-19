from flask import Blueprint, request, jsonify
from datetime import datetime
import os
from llmprovider import LLMService

api_bp = Blueprint('api', __name__)

llm_service = LLMService()

@api_bp.route('/api/models', methods=['GET'])
def get_models():
    """Get all available models from all providers"""
    models = llm_service.get_available_models()
    return jsonify(models)


@api_bp.route('/api/available_models', methods=['GET'])
def get_available_models():
    """Get available models from providers with API keys"""
    models = llm_service.get_available_models()
    return jsonify(models)


@api_bp.route('/api/providers', methods=['GET'])
def get_providers():
    """Get available providers with API keys"""
    providers = llm_service.get_available_providers()
    return jsonify(providers)


@api_bp.route('/api/models/<provider>', methods=['GET'])
def get_models_by_provider(provider):
    """Get available models from a specific provider with API keys"""
    models = llm_service.get_available_models_by_provider(provider)
    return jsonify(models)


@api_bp.route('/api/get_model_response', methods=['POST'])
def get_model_response():
    """Compare a single model"""
    data = request.json
    system_prompt = data.get('system_prompt', '').strip()
    prompt = data.get('prompt', '').strip()
    model_id = data.get('model_id')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    if not model_id:
        return jsonify({'error': 'A model must be selected'}), 400

    # Check if any API keys are configured
    api_keys_configured = any([
        os.getenv('OPENAI_API_KEY'),
        os.getenv('ANTHROPIC_API_KEY'),
        os.getenv('GEMINI_API_KEY'),
        os.getenv('XAI_API_KEY')
    ])

    if not api_keys_configured:
        return jsonify({'error': 'No API keys configured. Please add API keys to use this service.'}), 503

    # Get all available models to validate and get model info
    all_models = llm_service.get_available_models()
    
    if model_id not in all_models:
        return jsonify({'error': 'Invalid model selected.'}), 400

    model_info = all_models[model_id]

    # Real API call with system prompt
    response = llm_service.call_model(model_id, prompt, model_info, system_prompt if system_prompt else None)

    return jsonify(response)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    all_models = llm_service.get_available_models()
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_available': len(all_models)
    })
