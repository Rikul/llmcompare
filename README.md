# LLM Model Comparison Tool

A modern Flask web application for comparing responses from multiple Large Language Models (LLMs) side by side.

## Features

- **Multiple Model Support**: Compare responses from various LLM providers:
  - OpenAI (GPT-3.5 Turbo, GPT-4)
  - Anthropic (Claude 3 Opus, Claude 3 Sonnet)
  - Google (Gemini Pro)

- **Clean Architecture**: Modular design with separate provider classes
- **Modern UI**: Clean, responsive interface built with TailwindCSS
- **Interactive Tabs**: View each model's response in separate tabs
- **Real-time Comparison**: Send the same prompt to multiple models simultaneously
- **Copy to Clipboard**: Easily copy responses with one click
- **Error Handling**: Graceful error handling with informative messages
- **API Key Management**: Clear error page when API keys are not configured

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

## Project Structure

```
llm-comparison-app/
├── app.py                    # Main Flask application with provider classes
├── templates/
│   ├── index.html           # Main application interface
│   ├── no_api_keys.html     # Error page when no API keys configured
│   └── response.html        # Response component template
├── static/
│   └── css/
│       └── custom.css       # Additional styling
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
├── .env.example            # Example environment file
└── README.md               # This file
```

## Architecture

The refactored code includes:

- **Provider Classes**: Separate classes for each LLM provider (OpenAI, Anthropic, Google)
- **Service Layer**: `LLMService` class handles API calls with proper error handling
- **API Key Validation**: Automatic detection and UI adaptation based on configured keys
- **Template Separation**: Separate templates for different UI states
- **Type Hints**: Better code maintainability with type annotations
- **Logging**: Comprehensive logging for debugging

## API Endpoints

- `GET /` - Main application page (or error page if no API keys)
- `GET /api/models` - Get available models
- `POST /api/compare` - Compare models with a prompt
- `GET /health` - Health check endpoint

## Adding New Models

To add a new model, update the `AVAILABLE_MODELS` dictionary in `app.py`:

```python
'model-id': {
    'name': 'Display Name',
    'endpoint': 'https://api.example.com/endpoint',
    'api_key_env': 'API_KEY_ENV_VAR',
    'provider': 'ProviderName'
}
```

Then create a new provider class if needed:

```python
class NewProvider(LLMProvider):
    def call_api(self, model_id: str, prompt: str, endpoint: str) -> Dict[str, Any]:
        # Implement API call logic
        pass
```

## Error Handling

The application handles various error scenarios:
- No API keys configured (shows helpful setup page)
- Missing specific API keys (disables those models)
- API request failures
- Timeout errors
- Invalid responses

All errors are logged and user-friendly messages are displayed.

## Getting API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/settings/keys
- **Google AI**: https://makersuite.google.com/app/apikey

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: TailwindCSS, Vanilla JavaScript
- **Fonts**: Inter (Google Fonts)
- **Styling**: Modern gradient design with hover effects

## License

MIT License - feel free to use this for your own projects!