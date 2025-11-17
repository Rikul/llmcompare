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
   GEMINI_API_KEY=your_google_api_key
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
