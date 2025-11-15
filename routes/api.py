from flask import Blueprint, request, jsonify
from datetime import datetime
import os
from llmprovider import LLMService
from config import AVAILABLE_MODELS

api_bp = Blueprint('api', __name__)

llm_service = LLMService()

@api_bp.route('/api/models', methods=['GET'])
def get_models():
    """Get available models"""
    return jsonify(AVAILABLE_MODELS)


@api_bp.route('/api/compare', methods=['POST'])
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


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_available': len(AVAILABLE_MODELS)
    })
