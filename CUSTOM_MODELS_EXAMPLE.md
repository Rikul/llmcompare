# Adding Custom Models - Example

This file shows how to add your own custom models to the LLM Comparison Tool.

## Example: Adding Mistral AI Models

To add Mistral AI models, update the `AVAILABLE_MODELS`:

```python
AVAILABLE_MODELS = {
    # ... existing models ...
    
    'mistral-tiny': {
        'name': 'Mistral Tiny',
        'endpoint': 'https://api.mistral.ai/v1/chat/completions',
        'api_key_env': 'MISTRAL_API_KEY',
        'provider': 'Mistral'
    },
    'mistral-small': {
        'name': 'Mistral Small',
        'endpoint': 'https://api.mistral.ai/v1/chat/completions',
        'api_key_env': 'MISTRAL_API_KEY',
        'provider': 'Mistral'
    },
    'mistral-medium': {
        'name': 'Mistral Medium',
        'endpoint': 'https://api.mistral.ai/v1/chat/completions',
        'api_key_env': 'MISTRAL_API_KEY',
        'provider': 'Mistral'
    }
}
```

## Example: Adding Local/Self-Hosted Models

For local models using Ollama:

```python
'llama2-local': {
    'name': 'Llama 2 (Local)',
    'endpoint': 'http://localhost:11434/api/generate',
    'api_key_env': None,  # No API key needed for local
    'provider': 'Ollama'
}
```

## Example: Adding Hugging Face Models

```python
'falcon-7b': {
    'name': 'Falcon 7B',
    'endpoint': 'https://api-inference.huggingface.co/models/tiiuae/falcon-7b',
    'api_key_env': 'HUGGINGFACE_API_KEY',
    'provider': 'Hugging Face'
}
```

## Implementing the API Call Logic

After adding the model configuration, implement the API call logic in the `compare_models` function:

```python
elif model_info['provider'] == 'Mistral':
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': model_id,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.7
    }
    response = requests.post(model_info['endpoint'], headers=headers, json=data)
    response_data = response.json()
    
    responses[model_id] = {
        'model_name': model_info['name'],
        'provider': model_info['provider'],
        'response': response_data['choices'][0]['message']['content'],
        'timestamp': datetime.now().isoformat(),
        'status': 'success'
    }
```

## Don't Forget!

1. Add the new API key to your `.env` file:
   ```
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

2. The UI will automatically show the new models in the selection grid!

3. Test with a simple prompt first to ensure the integration works correctly.