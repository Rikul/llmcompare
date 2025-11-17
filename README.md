# LLM Model Comparison Tool

## Features

- **Multiple Model Support**: Compare responses from various LLM providers:
  - OpenAI (GPT-3.5 Turbo, GPT-4)
  - Anthropic (Claude 3 Opus, Claude 3 Sonnet)
  - Google (Gemini Pro)

## Requirements

- Python 3.7 or higher
- At least one configured API key (OpenAI, Anthropic, or Google)

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys** (required):

   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

   You need at least one API key configured to use the application.

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### With API Keys Configured

1. Select the models you want to compare (only models with configured API keys are selectable)
2. Enter your prompt in the text area
3. Click "Compare Models" to see responses
4. Switch between tabs to view different model responses
5. Use the "Copy" button to copy any response to clipboard

### Without API Keys

If no API keys are configured, you'll see a helpful error page with:
- Current API key status
- Step-by-step configuration instructions
- Direct links to get API keys from each provider

## Model Discovery

The application automatically discovers available models from each provider using their SDK APIs:

- **OpenAI**: Fetches models via `client.models.list()` and filters for GPT/o3 models
- **Anthropic**: Fetches models via `client.models.list()` 
- **Google**: Fetches models via `genai.list_models()` and filters for models supporting content generation
- **xAI**: Fetches models via `client.models.list_language_models()`

Models defined in `config.py` serve as a fallback when SDK calls fail or API keys are invalid. This ensures:
- Users automatically see new models as providers release them
- Service remains available even if provider APIs are temporarily unavailable
- Curated model lists can be maintained in config when needed

## Adding New Models

The application will automatically discover new models from configured providers. However, you can also manually add models to `config.py` as a fallback or to add models from new providers:

```python
'model-id': {
    'name': 'Display Name',
    'endpoint': 'https://api.example.com/endpoint',
    'api_key_env': 'API_KEY_ENV_VAR',
    'provider': 'ProviderName'
}
```

To add a completely new provider, create a provider class:

```python
class NewProvider(LLMProvider):
    def call_api(self, model_id: str, prompt: str, endpoint: str) -> Dict[str, Any]:
        # Implement API call logic
        pass
    
    def get_models(self) -> Dict[str, Any]:
        # Implement model listing via SDK
        # Fall back to config on errors
        pass
```

## Getting API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/settings/keys
- **Google AI**: https://makersuite.google.com/app/apikey
- **xAI**: https://x.ai/api

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: TailwindCSS, Vanilla JavaScript
- **Fonts**: Inter (Google Fonts)
- **Styling**: Modern gradient design with hover effects
