

API_KEYS = {
    'OPENAI_API_KEY': 'your-openai-api-key',
    'ANTHROPIC_API_KEY': 'your-anthropic-api-key',
    'GOOGLE_API_KEY': 'your-google-api-key',
    'XAI_API_KEY': 'your-xai-api-key'
}

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

