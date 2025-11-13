"""
Configuration file for LLM Model Comparison Tool

This module contains model configurations for all supported LLM providers.
"""

# Model configurations - Updated for 2025
AVAILABLE_MODELS = {
    # OpenAI Models
    'gpt-4o': {
        'name': 'GPT-4o',
        'endpoint': 'https://api.openai.com/v1/chat/completions',
        'api_key_env': 'OPENAI_API_KEY',
        'provider': 'OpenAI'
    },
    'gpt-4-turbo': {
        'name': 'GPT-4 Turbo',
        'endpoint': 'https://api.openai.com/v1/chat/completions',
        'api_key_env': 'OPENAI_API_KEY',
        'provider': 'OpenAI'
    },
    'gpt-3.5-turbo': {
        'name': 'GPT-3.5 Turbo',
        'endpoint': 'https://api.openai.com/v1/chat/completions',
        'api_key_env': 'OPENAI_API_KEY',
        'provider': 'OpenAI'
    },
    'o3-mini-2025-01-31': {
        'name': 'o3-mini',
        'endpoint': 'https://api.openai.com/v1/chat/completions',
        'api_key_env': 'OPENAI_API_KEY',
        'provider': 'OpenAI'
    },
    # Anthropic Claude Models
    'claude-sonnet-4-5-20250929': {
        'name': 'Claude Sonnet 4.5',
        'endpoint': 'https://api.anthropic.com/v1/messages',
        'api_key_env': 'ANTHROPIC_API_KEY',
        'provider': 'Anthropic'
    },
    'claude-opus-4-1-20250805': {
        'name': 'Claude Opus 4.1',
        'endpoint': 'https://api.anthropic.com/v1/messages',
        'api_key_env': 'ANTHROPIC_API_KEY',
        'provider': 'Anthropic'
    },
    'claude-haiku-4-5-20251001': {
        'name': 'Claude Haiku 4.5',
        'endpoint': 'https://api.anthropic.com/v1/messages',
        'api_key_env': 'ANTHROPIC_API_KEY',
        'provider': 'Anthropic'
    },
    'claude-3-7-sonnet-20250219': {
        'name': 'Claude 3.7 Sonnet',
        'endpoint': 'https://api.anthropic.com/v1/messages',
        'api_key_env': 'ANTHROPIC_API_KEY',
        'provider': 'Anthropic'
    },
    # Google Gemini Models
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
    'gemini-2.0-flash-exp': {
        'name': 'Gemini 2.0 Flash',
        'endpoint': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent',
        'api_key_env': 'GEMINI_API_KEY',
        'provider': 'Google'
    },
    # xAI Grok Models
    'grok-4-0709': {
        'name': 'Grok 4',
        'endpoint': 'https://api.x.ai/v1/chat/completions',
        'api_key_env': 'XAI_API_KEY',
        'provider': 'xAI'
    },
    'grok-3-beta': {
        'name': 'Grok 3',
        'endpoint': 'https://api.x.ai/v1/chat/completions',
        'api_key_env': 'XAI_API_KEY',
        'provider': 'xAI'
    },
    'grok-3-mini': {
        'name': 'Grok 3 Mini',
        'endpoint': 'https://api.x.ai/v1/chat/completions',
        'api_key_env': 'XAI_API_KEY',
        'provider': 'xAI'
    }
}
